# Extra cute raccoons (EXTRA CUTE v1)

Delores, her family and every raccoon guest got a cuter face and little bits of life. All of it is code-drawn
in the pixel kit (`pxPaint` / `drawBeing` in `index.html`), with no pictures.

## Face (Plush style, the default)
- Bigger, rounder head.
- Big glossy eyes: a large top-left shine, a warm brown glow at the bottom and a tiny sparkle.
- Softer, lighter mask so the eyes stand out.
- Bigger rosy cheeks with a little shine.

## Moods
`pxPaint(r, dir, blink, frame, mood)` takes a short mood string. Each combination is painted once and cached.
- `L` / `R`: tail swished left or right.
- `t`: one ear twitch.
- `h`: happy face, closed ^ ^ eyes and an open smile.

`racMood(r, t, step)` picks the mood each frame:
- Standing: slow tail swish, a soft breathing bob, an ear twitch every few seconds, and blinking.
- Walking: a tiny hop on every step.
- Happy: a bouncy hop and two floating pixel hearts (`racHearts`).

`racCheer(r)` makes a raccoon happy for a moment. Right now, when the player walks up to the front desk,
Delores and a raccoon player both light up. Delores is drawn every frame (not in the cached map layer), and the
desk is cut out of her drawing so it stays in front of her.

Reduced motion: no swish, hop or floating; the happy face and still hearts can still show.

Tests: `tests/test_cute.py`. Picture: `docs/screenshots/cute/raccoons-before-after.jpg`.
