# Talking trees (TALKING TREES v1)

Three little trees with faces live in the Yaupon Festival Garden. They are outdoors only, like the weather.

| Tree | Where | Voice | What they talk about |
| --- | --- | --- | --- |
| Willa the willow | Top left, leaning over the fountain | Soft and dreamy, long lashes, a white lily | Hints about guests' untold stories, the lily mystery, notes under doors, rare keepsakes, Muffin's seasonal spot |
| Old Oakley | Top right corner | Slow and wise, mossy eyebrows | Guest-care tips: names, calm voices, repeat the request, "here's what I can do", safety, privacy, follow-up |
| Little Pip | Bottom path, left of the way back to the manor | Small, eager, encouraging | Gentle encouragement after mistakes, breathing, small progress |

## How it plays

- Walk close to a tree and it says something once. It won't repeat itself until you wander off and come back.
- Tap a tree (or press E beside it) to hear the next thing. Unheard lines come first, in order.
- The words show in the usual toast at the bottom, so screen readers announce them. A small bubble ("Hmm? Oh, hello.") pops above the tree while it talks.
- A tiny ♪ floats over a tree that still has new things to say.
- 30 sayings in all (10 each). Progress is saved on the device under `mapachez_trees_v1`.
- Two pins: **Tree Friend** (hear all three) and **Tree Whisperer** (hear everything).

## Little touches

- They blink, sway softly and their eyes follow you as you walk past. With reduced motion on, they stand still.
- Seasons: spring blossoms, summer cherries on Pip, autumn colours and acorns, winter snow with a scarf for Oakley and a knitted hat for Pip. Willa turns gold in autumn.
- Weather: rain makes them close their eyes happily, storms make them wide-eyed, fireflies circle them, petals and leaves drift down. Sometimes they mention the weather (rain, storm, snow, fireflies, petals, leaves).

## Rules for new lines

Follow `docs/heart.md`: gentle, kind, a little mysterious, never gloomy or confusing. Show the feeling, never name it. Clean comedy only. No room numbers. Add the Spanish line in the same position in `TREE_TEXT.es` (gender-neutral toward the player).

## Code

All in one block at the end of `index.html` (`TALKING TREES v1`). It wraps `drawMuffinScene` (trees behind Muffin and the walker), `world.drawVisitor` (a tree nearer the bottom than the walker is drawn in front), `world.options.extras` and `interact`. Nothing else in the file was changed. Each tree is a handful of canvas shapes drawn live, so it costs nothing to run.

Tests: `python tests/test_trees.py` (set `CHROMIUM_PATH`).
