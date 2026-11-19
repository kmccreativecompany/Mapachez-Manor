# Read aloud

For players who would rather listen than read.

- **Select any words** (drag with a mouse, or press and hold on a phone). A green **🔊 Read this** bubble appears at the bottom of the screen. Tap it to hear the words.
- While it talks, the bubble turns red: **■ Stop**. One tap stops it.
- Story cards keep their **Read this aloud** button. It now turns into **Stop reading** while it talks.
- Closing a card, or switching away from the game, stops the voice.
- Works inside the Silver Key practice desk too.
- **Settings → Read selected text** turns the bubble off or on. The choice is remembered on this device (`mapachez_readaloud_v1`).

Costs nothing: it uses the browser's own built-in voice (Web Speech API). No account, no network, no paid service. If a browser has no voice, the bubble never shows and the setting says so.

Long text is read in short pieces, because some phones cut off long speech.

Tests: `tests/test_read_aloud.py` (the browser voice is replaced with a silent recorder).
