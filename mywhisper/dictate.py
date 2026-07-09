from __future__ import annotations

import argparse
import ctypes
import string
from ctypes import wintypes
import os
import tempfile
import threading
import time
import wave
from dataclasses import dataclass
from pathlib import Path

import numpy as np


KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_UNICODE = 0x0004
INPUT_KEYBOARD = 1
ULONG_PTR = getattr(wintypes, "ULONG_PTR", ctypes.c_size_t)


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUT_UNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


class INPUT(ctypes.Structure):
    _fields_ = [("type", wintypes.DWORD), ("u", INPUT_UNION)]


@dataclass(frozen=True)
class AppConfig:
    hotkey: str
    model: str
    language: str
    device: str
    compute_type: str
    input_device: int | str | None
    sample_rate: int
    type_delay_ms: int
    suppress_hotkey: bool
    vad_filter: bool
    allow_model_download: bool
    download_root: Path
    keep_recordings: bool
    sound: bool
    list_devices: bool


class UnicodeTyper:
    def __init__(self, delay_seconds: float) -> None:
        self.delay_seconds = delay_seconds
        self.user32 = ctypes.windll.user32
        self.user32.SendInput.argtypes = [wintypes.UINT, ctypes.POINTER(INPUT), ctypes.c_int]
        self.user32.SendInput.restype = wintypes.UINT

    def type_text(self, text: str) -> None:
        if not text:
            return

        data = text.replace("\n", "\r").encode("utf-16-le")
        for index in range(0, len(data), 2):
            scan_code = data[index] | (data[index + 1] << 8)
            self._send_unicode_key(scan_code, key_up=False)
            self._send_unicode_key(scan_code, key_up=True)
            if self.delay_seconds:
                time.sleep(self.delay_seconds)

    def _send_unicode_key(self, scan_code: int, key_up: bool) -> None:
        flags = KEYEVENTF_UNICODE | (KEYEVENTF_KEYUP if key_up else 0)
        keyboard_input = KEYBDINPUT(0, scan_code, flags, 0, 0)
        input_event = INPUT(INPUT_KEYBOARD, INPUT_UNION(ki=keyboard_input))
        sent = self.user32.SendInput(1, ctypes.byref(input_event), ctypes.sizeof(input_event))
        if sent != 1:
            raise ctypes.WinError()


class AudioRecorder:
    def __init__(self, sample_rate: int, input_device: int | str | None) -> None:
        try:
            import sounddevice as sd
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: sounddevice. Install dependencies from mywhisper/requirements.txt."
            ) from exc

        self._sd = sd
        self.sample_rate = sample_rate
        self.input_device = input_device
        self._frames: list[np.ndarray] = []
        self._stream = None
        self._lock = threading.Lock()

    def start(self) -> None:
        with self._lock:
            if self._stream is not None:
                return

            self._frames = []
            self._stream = self._sd.InputStream(
                samplerate=self.sample_rate,
                device=self.input_device,
                channels=1,
                dtype="float32",
                callback=self._callback,
            )
            self._stream.start()

    def stop(self) -> np.ndarray:
        with self._lock:
            if self._stream is None:
                return np.empty((0, 1), dtype=np.float32)

            self._stream.stop()
            self._stream.close()
            self._stream = None

            if not self._frames:
                return np.empty((0, 1), dtype=np.float32)

            return np.concatenate(self._frames, axis=0)

    def _callback(self, indata, frames, time_info, status) -> None:
        if status:
            print(f"Audio warning: {status}", flush=True)
        self._frames.append(indata.copy())

    @staticmethod
    def print_input_devices() -> None:
        try:
            import sounddevice as sd
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: sounddevice. Install dependencies from mywhisper/requirements.txt."
            ) from exc

        print("Input devices:", flush=True)
        for index, device in enumerate(sd.query_devices()):
            if device.get("max_input_channels", 0) > 0:
                default_marker = " *default*" if index == sd.default.device[0] else ""
                print(
                    f"  {index}: {device['name']} "
                    f"({device['max_input_channels']} ch, default {int(device['default_samplerate'])} Hz)"
                    f"{default_marker}",
                    flush=True,
                )


class LocalWhisper:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._model = None

    def transcribe(self, wav_path: Path) -> str:
        model = self._get_model()
        segments, _info = model.transcribe(
            str(wav_path),
            language=self.config.language or None,
            vad_filter=self.config.vad_filter,
            beam_size=5,
            condition_on_previous_text=False,
        )
        text = " ".join(segment.text.strip() for segment in segments).strip()
        return normalize_text(text)

    def _get_model(self):
        if self._model is not None:
            return self._model

        try:
            from faster_whisper import WhisperModel
        except ModuleNotFoundError as exc:
            raise RuntimeError(
                "Missing dependency: faster-whisper. Install dependencies from mywhisper/requirements.txt."
            ) from exc

        self.config.download_root.mkdir(parents=True, exist_ok=True)
        print(f"Loading model '{self.config.model}'...", flush=True)
        self._model = WhisperModel(
            self.config.model,
            device=self.config.device,
            compute_type=self.config.compute_type,
            download_root=str(self.config.download_root),
            local_files_only=not self.config.allow_model_download,
        )
        return self._model


class StatusSound:
    def __init__(self, enabled: bool) -> None:
        self.enabled = enabled
        self._winsound = None
        if enabled:
            try:
                import winsound

                self._winsound = winsound
            except ModuleNotFoundError:
                self.enabled = False

    def start(self) -> None:
        self._beep(880, 90)

    def stop(self) -> None:
        self._beep(660, 90)

    def _beep(self, frequency: int, duration_ms: int) -> None:
        if not self.enabled or self._winsound is None:
            return
        threading.Thread(
            target=self._winsound.Beep,
            args=(frequency, duration_ms),
            daemon=True,
        ).start()


class DictationApp:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self.recorder = AudioRecorder(config.sample_rate, config.input_device)
        self.transcriber = LocalWhisper(config)
        self.typer = UnicodeTyper(config.type_delay_ms / 1000)
        self.sound = StatusSound(config.sound)
        self._is_recording = False
        self._is_busy = False
        self._lock = threading.Lock()

    def toggle(self) -> None:
        with self._lock:
            if self._is_busy:
                print("Still processing the previous dictation. Please wait.", flush=True)
                return

            if self._is_recording:
                self._is_recording = False
                self._is_busy = True
                self.sound.stop()
                audio = self.recorder.stop()
                print("Recording stopped. Transcribing...", flush=True)
                threading.Thread(target=self._transcribe_and_type, args=(audio,), daemon=True).start()
                return

            self.recorder.start()
            self._is_recording = True
            self.sound.start()
            print("Recording started. Press the hotkey again to stop.", flush=True)

    def _transcribe_and_type(self, audio: np.ndarray) -> None:
        wav_path = None
        try:
            if audio.size == 0:
                print("No audio captured.", flush=True)
                return

            print_audio_stats(audio, self.config.sample_rate)
            wav_path = write_temp_wav(audio, self.config.sample_rate)
            if self.config.keep_recordings:
                print(f"Recording saved at: {wav_path}", flush=True)

            text = self.transcriber.transcribe(wav_path)
            if not text:
                print("No speech detected.", flush=True)
                return

            print(f"Typing: {text}", flush=True)
            self.typer.type_text(text)
            print("Done.", flush=True)
        except Exception as exc:
            print(f"Dictation failed: {exc}", flush=True)
        finally:
            if wav_path and wav_path.exists() and not self.config.keep_recordings:
                wav_path.unlink(missing_ok=True)
            with self._lock:
                self._is_busy = False


def normalize_text(text: str) -> str:
    normalized = " ".join(text.split())
    punctuation = set(string.punctuation) | {" ", "\t", "\r", "\n", "...", "…"}
    if normalized and all(character in punctuation for character in normalized):
        return ""
    return normalized


def print_audio_stats(audio: np.ndarray, sample_rate: int) -> None:
    mono = np.squeeze(audio)
    if mono.size == 0:
        return

    duration = mono.size / sample_rate
    peak = float(np.max(np.abs(mono)))
    rms = float(np.sqrt(np.mean(np.square(mono))))
    print(f"Audio captured: {duration:.1f}s, peak={peak:.3f}, rms={rms:.3f}", flush=True)
    if peak < 0.025 or rms < 0.003:
        print("Audio looks very quiet. Move closer to the mic or raise microphone input volume.", flush=True)
    elif peak > 0.98:
        print("Audio may be clipping. Lower microphone input volume slightly.", flush=True)


def write_temp_wav(audio: np.ndarray, sample_rate: int) -> Path:
    mono = np.squeeze(audio)
    clipped = np.clip(mono, -1.0, 1.0)
    pcm16 = (clipped * 32767).astype(np.int16)

    fd, raw_path = tempfile.mkstemp(prefix="dictation_", suffix=".wav")
    os.close(fd)
    path = Path(raw_path)

    with wave.open(str(path), "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(pcm16.tobytes())

    return path


def parse_args() -> AppConfig:
    parser = argparse.ArgumentParser(
        description="Offline push-to-dictate utility for Windows."
    )
    parser.add_argument("--hotkey", default="ctrl+d", help="Global hotkey, e.g. ctrl+d or ctrl+alt+d.")
    parser.add_argument("--model", default="base.en", help="faster-whisper model name or local model path.")
    parser.add_argument("--language", default="en", help="Speech language code. Use empty string for auto-detect.")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"], help="Inference device.")
    parser.add_argument("--compute-type", default="int8", help="faster-whisper compute type, e.g. int8 or float16.")
    parser.add_argument("--input-device", default=None, help="Microphone device index or name.")
    parser.add_argument("--list-devices", action="store_true", help="List available microphone devices and exit.")
    parser.add_argument("--sample-rate", type=int, default=16000, help="Microphone sample rate.")
    parser.add_argument("--type-delay-ms", type=int, default=1, help="Delay between typed characters.")
    parser.add_argument("--no-suppress", action="store_true", help="Do not suppress the hotkey in the focused app.")
    parser.add_argument("--no-vad", action="store_true", help="Disable voice activity detection. Try this if speech is cut off.")
    parser.add_argument(
        "--allow-model-download",
        action="store_true",
        help="Allow faster-whisper to download the selected model if it is not already local.",
    )
    parser.add_argument(
        "--download-root",
        default=str(Path(__file__).resolve().parent / "models"),
        help="Where faster-whisper stores downloaded model files.",
    )
    parser.add_argument("--keep-recordings", action="store_true", help="Keep temporary WAV files for debugging.")
    parser.add_argument("--no-sound", action="store_true", help="Disable start/stop beeps.")
    args = parser.parse_args()
    input_device = parse_input_device(args.input_device)

    return AppConfig(
        hotkey=args.hotkey,
        model=args.model,
        language=args.language,
        device=args.device,
        compute_type=args.compute_type,
        input_device=input_device,
        sample_rate=args.sample_rate,
        type_delay_ms=args.type_delay_ms,
        suppress_hotkey=not args.no_suppress,
        vad_filter=not args.no_vad,
        allow_model_download=args.allow_model_download,
        download_root=Path(args.download_root),
        keep_recordings=args.keep_recordings,
        sound=not args.no_sound,
        list_devices=args.list_devices,
    )


def parse_input_device(value: str | None) -> int | str | None:
    if value is None or value.strip() == "":
        return None
    stripped = value.strip()
    if stripped.isdigit():
        return int(stripped)
    return stripped


def main() -> None:
    if os.name != "nt":
        raise SystemExit("This dictation utility currently supports Windows only.")

    config = parse_args()
    if config.list_devices:
        AudioRecorder.print_input_devices()
        return

    try:
        import keyboard
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: keyboard. Install dependencies from mywhisper/requirements.txt."
        ) from exc

    app = DictationApp(config)

    print("Offline dictation app is running.", flush=True)
    print(f"Hotkey: {config.hotkey}", flush=True)
    print("Press Ctrl+C in this terminal to exit.", flush=True)
    print(
        "Model downloads are disabled."
        if not config.allow_model_download
        else "Model download is allowed for this run.",
        flush=True,
    )
    print(f"Voice activity detection: {'on' if config.vad_filter else 'off'}", flush=True)

    keyboard.add_hotkey(config.hotkey, app.toggle, suppress=config.suppress_hotkey)
    keyboard.wait()


if __name__ == "__main__":
    main()
