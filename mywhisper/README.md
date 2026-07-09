# MyWhisper Dictation

Small personal Windows dictation utility:

- Press `Ctrl+D` to start recording.
- Press `Ctrl+D` again to stop.
- Speech is transcribed locally with `faster-whisper`.
- Text is typed into the currently focused application using Windows `SendInput`.
- The clipboard is not used.
- A short beep indicates recording start and stop.

## Setup

Use a virtual environment. From the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -c "import faster_whisper"
python -c "import sounddevice"
python -c "import keyboard"
```

Install only packages that are missing:

```powershell
pip install -r .\mywhisper\requirements.txt
```

## First Model Download

By default the app disables model downloads during runtime. To allow a one-time download of the default `base.en` model into `mywhisper\models`, run:

```powershell
python .\mywhisper\dictate.py --allow-model-download
```

After the model is present locally, run without download permission:

```powershell
python .\mywhisper\dictate.py
```

Or use the Windows batch launcher:

```powershell
.\mywhisper\run.bat
```

For better accuracy, especially if `base.en` misses words, use:

```powershell
.\mywhisper\run-accurate.bat --allow-model-download
```

After the `small.en` model downloads once:

```powershell
.\mywhisper\run-accurate.bat
```

If you already have a local faster-whisper/CTranslate2 model folder, point to it:

```powershell
python .\mywhisper\dictate.py --model C:\path\to\local-model
```

## Usage

1. Start the script.
2. Click into Outlook, Word, Notepad, Excel, command prompt, or another typing target.
3. Press `Ctrl+D`.
4. Dictate.
5. Press `Ctrl+D` again.
6. Wait for the text to appear in the focused app.

## Useful Options

```powershell
python .\mywhisper\dictate.py --hotkey ctrl+alt+d
python .\mywhisper\dictate.py --model small.en --allow-model-download
python .\mywhisper\dictate.py --type-delay-ms 3
python .\mywhisper\dictate.py --language ""
python .\mywhisper\dictate.py --no-sound
python .\mywhisper\dictate.py --no-vad
python .\mywhisper\dictate.py --list-devices
python .\mywhisper\dictate.py --input-device 2
```

## Improving Recognition Quality

If the output becomes `...` or misses most of what you said, try these in order:

1. Use the more accurate launcher:

```powershell
.\mywhisper\run-accurate.bat --allow-model-download
```

2. Check that Windows is using the correct microphone:

```powershell
.\mywhisper\run.bat --list-devices
.\mywhisper\run.bat --input-device 2
```

3. Watch the audio level printed after each recording:

- `peak` below `0.025` or `rms` below `0.003` means the mic is too quiet.
- `peak` near `1.000` means the mic may be clipping.

4. Disable VAD if words are cut off:

```powershell
.\mywhisper\run.bat --no-vad
```

5. For Indian English or mixed-language speech, try auto language detection:

```powershell
.\mywhisper\run.bat --language ""
```

Notes:

- `Ctrl+D` has meanings in some apps. If it conflicts, use `--hotkey ctrl+alt+d`.
- Direct typing is slower than clipboard paste for long paragraphs, but it keeps your clipboard untouched.
- Punctuation-only results such as `...` are treated as no speech and will not be typed.
- Windows may block typed input into administrator apps unless this script also runs as administrator.
- The app uses local inference. No external API calls are made by the dictation flow.
