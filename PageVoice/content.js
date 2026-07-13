(() => {
  // Guard: only inject the player once per page load
  if (document.getElementById('pagevoice-player')) return;

  // ── State ────────────────────────────────────────────────────────────────
  let sentences = [];
  let currentIndex = 0;
  let status = 'stopped'; // 'playing' | 'paused' | 'stopped'
  let speed = 1.0;

  // ── Sentence segmenter ───────────────────────────────────────────────────
  const segmenter = new Intl.Segmenter('en', { granularity: 'sentence' });

  // Pause durations in ms (scaled by speed so fast reading stays proportional)
  const PAUSE_SENTENCE  = 350;  // after a sentence-ending full stop
  const PAUSE_PARAGRAPH = 650;  // after a paragraph ends
  const PAUSE_HEADING   = 900;  // after a heading before body text

  // Each item: { text: string, pauseAfter: number }
  function extractSegments() {
    const docClone = document.cloneNode(true);
    const reader = new Readability(docClone);
    const article = reader.parse();

    // Build segments from structured DOM when available; fall back to plain text
    if (article && article.content) {
      const tmp = document.createElement('div');
      tmp.innerHTML = article.content;
      return domToSegments(tmp);
    }

    // Fallback: treat whole body as one paragraph
    const raw = (article ? article.textContent : document.body.innerText)
      .replace(/\s+/g, ' ').trim();
    return textToSegments(raw, PAUSE_SENTENCE);
  }

  // Walk DOM nodes, emit sentence-level segments with appropriate pauses
  function domToSegments(root) {
    const HEADING_TAGS = new Set(['H1','H2','H3','H4','H5','H6']);
    const BLOCK_TAGS   = new Set(['P','LI','TD','TH','BLOCKQUOTE','PRE','FIGCAPTION']);
    const segments = [];

    function visitNode(node) {
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      const tag = node.tagName;

      if (HEADING_TAGS.has(tag)) {
        const text = node.textContent.replace(/\s+/g, ' ').trim();
        if (text) segments.push({ text, pauseAfter: PAUSE_HEADING });
        return; // don't recurse into heading children
      }

      if (BLOCK_TAGS.has(tag)) {
        const text = node.textContent.replace(/\s+/g, ' ').trim();
        if (text) {
          const sents = textToSegments(text, PAUSE_SENTENCE);
          if (sents.length > 0) {
            // Upgrade the last sentence's pause to paragraph-level
            sents[sents.length - 1].pauseAfter = PAUSE_PARAGRAPH;
            segments.push(...sents);
          }
        }
        return; // don't recurse; we already grabbed the full text
      }

      // Recurse into containers (div, section, article, etc.)
      for (const child of node.children) visitNode(child);
    }

    visitNode(root);

    // If DOM walk yielded nothing (e.g. all inline elements), fall back
    if (segments.length === 0) {
      const raw = root.textContent.replace(/\s+/g, ' ').trim();
      return textToSegments(raw, PAUSE_SENTENCE);
    }

    return segments;
  }

  // Split a plain-text block into sentence segments
  function textToSegments(text, defaultPause) {
    return Array.from(segmenter.segment(text))
      .map(s => s.segment.trim())
      .filter(s => s.length > 0)
      .map(s => ({ text: s, pauseAfter: defaultPause }));
  }

  // ── Voice selection ──────────────────────────────────────────────────────
  // Preferred female voices in order — neural/natural ones first
  const PREFERRED_VOICES = [
    'Microsoft Ava Online (Natural) - English (United States)',
    'Microsoft Jenny Online (Natural) - English (United States)',
    'Microsoft Aria Online (Natural) - English (United States)',
    'Microsoft Sonia Online (Natural) - English (United Kingdom)',
    'Microsoft Libby Online (Natural) - English (United Kingdom)',
    'Google UK English Female',
    'Microsoft Zira - English (United States)',
    'Microsoft Hazel Desktop - English (Great Britain)',
    'Samantha',
    'Karen',
    'Moira',
  ];

  // Keywords that strongly indicate a male voice — used to filter them out
  const MALE_VOICE_NAMES = /\b(david|mark|richard|james|george|ryan|guy|daniel|fred|alex|tom|eric|paul|rishi|sean|oliver|thomas|liam|noah|ethan)\b/i;

  let selectedVoice = null;
  let availableFemaleVoices = [];

  function isFemaleVoice(v) {
    if (MALE_VOICE_NAMES.test(v.name)) return false;
    if (/male/i.test(v.name) && !/female/i.test(v.name)) return false;
    if (/female|woman|girl|zira|ava|jenny|aria|sonia|libby|hazel|samantha|karen|moira|victoria|allison|susan|helena|nora|tessa/i.test(v.name)) return true;
    // Neural/Online English voices not explicitly male are usually female
    if (v.lang.startsWith('en') && /online|natural|neural/i.test(v.name)) return true;
    return false;
  }

  function pickBestVoice(voices) {
    // 1. Try the preferred list in order
    for (const name of PREFERRED_VOICES) {
      const match = voices.find(v => v.name === name);
      if (match) return match;
    }
    // 2. Any detected female English voice
    const femaleEn = voices.find(v => v.lang.startsWith('en') && isFemaleVoice(v));
    if (femaleEn) return femaleEn;
    // 3. Any English voice as last resort
    return voices.find(v => v.lang.startsWith('en')) || voices[0] || null;
  }

  function buildVoiceDropdown(voices) {
    const select = document.getElementById('pv-voice-select');
    if (!select) return;
    select.innerHTML = '';
    availableFemaleVoices = voices.filter(v => v.lang.startsWith('en') && isFemaleVoice(v));

    // If none detected as female, show all English voices
    const list = availableFemaleVoices.length > 0
      ? availableFemaleVoices
      : voices.filter(v => v.lang.startsWith('en'));

    list.forEach((v, i) => {
      const opt = document.createElement('option');
      opt.value = i;
      opt.textContent = shortVoiceName(v);
      opt.title = v.name;
      if (selectedVoice && v.name === selectedVoice.name) opt.selected = true;
      select.appendChild(opt);
    });

    select.addEventListener('change', () => {
      selectedVoice = list[parseInt(select.value)];
      if (status === 'playing') {
        clearPauseTimer();
        window.speechSynthesis.cancel();
        speakFrom(currentIndex);
      }
    });
  }

  function shortVoiceName(v) {
    return v.name
      .replace(/^Microsoft\s+/i, '')
      .replace(/\s+Online\s*\(Natural\)/i, ' ✦')
      .replace(/\s+-\s+English.*/i, '')
      .trim();
  }

  function initVoices() {
    const voices = window.speechSynthesis.getVoices();
    if (voices.length === 0) return;
    selectedVoice = pickBestVoice(voices);
    buildVoiceDropdown(voices);
  }

  if (window.speechSynthesis.getVoices().length > 0) {
    initVoices();
  } else {
    window.speechSynthesis.addEventListener('voiceschanged', initVoices, { once: true });
  }

  // ── TTS engine ───────────────────────────────────────────────────────────
  let pauseTimer = null;

  function speakFrom(index) {
    if (index >= sentences.length) {
      stopReading();
      return;
    }
    currentIndex = index;
    updateProgress();

    const { text, pauseAfter } = sentences[index];
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate   = speed;
    utterance.pitch  = 1.1;   // above 1.0 keeps voice clearly feminine
    utterance.volume = 0.92;
    if (selectedVoice) utterance.voice = selectedVoice;
    utterance.onend = () => {
      if (status !== 'playing') return;
      const delay = pauseAfter / speed; // scale pause inversely with speed
      if (delay > 50) {
        pauseTimer = setTimeout(() => speakFrom(currentIndex + 1), delay);
      } else {
        speakFrom(currentIndex + 1);
      }
    };
    utterance.onerror = (e) => {
      if (e.error !== 'interrupted' && e.error !== 'canceled') {
        console.warn('[PageVoice] utterance error:', e.error);
      }
    };
    window.speechSynthesis.speak(utterance);
  }

  function clearPauseTimer() {
    if (pauseTimer !== null) {
      clearTimeout(pauseTimer);
      pauseTimer = null;
    }
  }

  function playReading() {
    if (status === 'paused') {
      status = 'playing';
      // If we paused mid-gap (timer was running), resume from next sentence
      if (pauseTimer === null) {
        window.speechSynthesis.resume();
      } else {
        clearPauseTimer();
        speakFrom(currentIndex + 1);
      }
      updateButtons();
      return;
    }
    // Fresh start: re-extract so navigation changes are picked up
    clearPauseTimer();
    window.speechSynthesis.cancel();
    sentences = extractSegments();
    currentIndex = 0;
    status = 'playing';
    updateButtons();
    speakFrom(0);
  }

  function pauseReading() {
    if (status !== 'playing') return;
    status = 'paused';
    // If speaking, pause the engine; if in a between-sentence gap, just stop the timer
    if (window.speechSynthesis.speaking) {
      window.speechSynthesis.pause();
    } else {
      clearPauseTimer();
    }
    updateButtons();
  }

  function stopReading() {
    clearPauseTimer();
    status = 'stopped';
    window.speechSynthesis.cancel();
    sentences = [];
    currentIndex = 0;
    updateButtons();
    updateProgress();
  }

  // ── Build UI ─────────────────────────────────────────────────────────────
  const player = document.createElement('div');
  player.id = 'pagevoice-player';
  player.innerHTML = `
    <button id="pv-play"  title="Play">&#9654;</button>
    <button id="pv-pause" title="Pause">&#9646;&#9646;</button>
    <button id="pv-stop"  title="Stop">&#9632;</button>
    <div id="pv-progress-track">
      <div id="pv-progress-fill"></div>
    </div>
    <select id="pv-speed" title="Speed">
      <option value="0.75">0.75x</option>
      <option value="1"    selected>1x</option>
      <option value="1.25">1.25x</option>
      <option value="1.5">1.5x</option>
      <option value="2">2x</option>
    </select>
    <select id="pv-voice-select" title="Voice"></select>
  `;
  document.body.appendChild(player);

  // Button references
  const btnPlay  = document.getElementById('pv-play');
  const btnPause = document.getElementById('pv-pause');
  const btnStop  = document.getElementById('pv-stop');
  const progressFill = document.getElementById('pv-progress-fill');
  const speedSelect  = document.getElementById('pv-speed');

  function updateButtons() {
    btnPlay.disabled  = (status === 'playing');
    btnPause.disabled = (status !== 'playing');
    btnStop.disabled  = (status === 'stopped');
  }

  function updateProgress() {
    const pct = sentences.length > 0
      ? Math.round((currentIndex / sentences.length) * 100)
      : 0;
    progressFill.style.width = pct + '%';
    progressFill.title = sentences.length > 0
      ? `Sentence ${currentIndex + 1} of ${sentences.length}`
      : '';
  }

  updateButtons();

  btnPlay.addEventListener('click',  playReading);
  btnPause.addEventListener('click', pauseReading);
  btnStop.addEventListener('click',  stopReading);

  speedSelect.addEventListener('change', () => {
    speed = parseFloat(speedSelect.value);
    if (status === 'playing') {
      clearPauseTimer();
      window.speechSynthesis.cancel();
      speakFrom(currentIndex);
    }
  });

  // ── Draggable pill ───────────────────────────────────────────────────────
  let dragging = false;
  let dragOffsetX = 0;
  let dragOffsetY = 0;

  player.addEventListener('mousedown', (e) => {
    // Don't drag when clicking buttons or select
    if (e.target !== player && e.target.id !== 'pv-progress-track') return;
    dragging = true;
    dragOffsetX = e.clientX - player.getBoundingClientRect().left;
    dragOffsetY = e.clientY - player.getBoundingClientRect().top;
    player.style.cursor = 'grabbing';
    e.preventDefault();
  });

  document.addEventListener('mousemove', (e) => {
    if (!dragging) return;
    const x = e.clientX - dragOffsetX;
    const y = e.clientY - dragOffsetY;
    // Keep within viewport
    const maxX = window.innerWidth  - player.offsetWidth;
    const maxY = window.innerHeight - player.offsetHeight;
    player.style.left   = Math.max(0, Math.min(x, maxX)) + 'px';
    player.style.top    = Math.max(0, Math.min(y, maxY)) + 'px';
    player.style.right  = 'auto';
    player.style.bottom = 'auto';
  });

  document.addEventListener('mouseup', () => {
    dragging = false;
    player.style.cursor = 'grab';
  });

  // Stop reading if the user navigates away (SPA frameworks fire this)
  window.addEventListener('beforeunload', () => {
    window.speechSynthesis.cancel();
  });
})();
