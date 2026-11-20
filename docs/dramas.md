# Manor dramas (DRAMAS v1)

Short, funny vertical videos about the manor promote the game. The game links to them; it never embeds them, so they cost nothing to run.

## Turn the button on

The title screen has a "🎬 Watch the manor dramas" button. It stays hidden until there is at least one link.

1. Post a video (YouTube Shorts first, then TikTok, Reels, RedNote and the rest).
2. Open `index.html`, search for `const MANOR_DRAMAS=[`.
3. Add one line per video, newest first:

```js
const MANOR_DRAMAS=[
  {title:'The Stapler Mystery',url:'https://youtube.com/shorts/xxxxxxxxxxx',where:'YouTube'},
];
```

- One link: the button opens it in a new tab.
- Two or more: the button opens a small list, each link opening in a new tab.
- Only `https://` links are shown.

## Rules for the videos

- Clean comedy: laugh with the characters, never at them. Cute and friendly.
- No brand names of hotels, apps or ratings; no real people. The owner's name never appears.
- Hook in the first 2 seconds, captions burned in, end card "Mapachez Manor. Play free. Earn a certificate."
- Character pictures for video tools: project files `video-dramas/characters/` (drawn from the game's own code).

Scripts, AI video prompts, voices and per-platform posting notes live in the "Mapachez Manor Video Dramas" doc.

Tests: `python tests/test_dramas.py`.
