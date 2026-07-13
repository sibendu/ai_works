# PageVoice

A browser extension that reads the main content of any webpage aloud. Built for technical blogs and documentation — it extracts only the article body, skips navbars and sidebars, and pauses naturally at headings, paragraphs, and sentence boundaries.

---

## Installation

1. Open **Chrome** or **Edge** and go to:
   - Chrome: `chrome://extensions`
   - Edge: `edge://extensions`

2. Enable **Developer mode** using the toggle in the top-right corner.

3. Click **Load unpacked**.

4. Select the `PageVoice` folder:
   ```
   C:\Users\320090746\OneDrive - Philips\Art\2026\Claude_Projects\PageVoice
   ```

5. PageVoice is now installed. You will see it in your extensions list and toolbar.

---

## How to Use

Once installed, a small player pill appears at the **bottom-right corner of every page**:

```
┌─────────────────────────────────┐
│  ▶  ⏸  ■   ━━━●━━━━━━━━  1x  │
└─────────────────────────────────┘
```

### Controls

| Button | Action |
|--------|--------|
| **▶ Play** | Extracts the page's main content and starts reading from the beginning |
| **⏸ Pause** | Pauses reading at the current sentence |
| **■ Stop** | Stops reading and resets position |
| **Speed dropdown** | Change reading speed: 0.75x / 1x / 1.25x / 1.5x / 2x |

### Reading a new page or topic

When you click a new topic in the documentation index and the page content changes, simply press **▶ Play** again. It always re-extracts the current page content fresh, so it will start reading the new topic from the top.

### Moving the player

Click and drag the pill to any corner of the screen if it overlaps content you need to read.

---

## Reading Behaviour

PageVoice reads with structured pauses so it sounds natural:

- **Short pause** after every sentence (350 ms)
- **Medium pause** after every paragraph (650 ms)
- **Long pause** after every heading before the next section begins (900 ms)

Pauses scale automatically with your chosen speed — faster speed means proportionally shorter pauses.

---

## Updating the Extension

If the source files are changed:

1. Go to `chrome://extensions` or `edge://extensions`
2. Click the **↺ reload icon** on the PageVoice card
3. Hard-refresh any open tab with `Ctrl + Shift + R`

---

## Tested On

- MDN Web Docs
- React / Vue / Angular documentation
- dev.to articles
- Medium technical posts
- GitHub README pages
