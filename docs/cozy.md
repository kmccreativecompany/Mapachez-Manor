# Cozy foyer (test room)

A before-and-after test on one room, the Grand Foyer, to try a cozier look while staying Art Nouveau and manor green.
Pinks and lavenders are small accents only. Everything is drawn in code; there are no image files.

## What changed in the foyer

- **Patterned floor:** a soft sage-and-cream checker with a tiny lily bud and gold dot where the tiles meet.
- **Wallpaper band** along the north wall: manor green with cream lily buds, a gold trim, and two arched windows with bowed pink curtains and a lavender scalloped top.
- **Rounded rug** in front of the desk: lavender rim, cream centre, a green vine and pink dots.
- **Tea corner** by the lobby chairs: a round table with a scalloped pink cloth, a sage teapot, two cups and a lily in a bud vase.
- **Heart bubbles:** Delores shows a little heart when you walk up to the desk, and a pair of guests show hearts once you have listened to their chat.
- **Chunky dialogue box** for the foyer chatter: thick green border, gold inner line, a green name tag, a gold sparkle and a little bouncing ▼ arrow (still with reduced motion).

## Cost

The floor, wallpaper, windows, rug and tea table are painted once into the cached map layer, so they cost nothing per frame.
Only the hearts are drawn each frame, and only near the desk or the chatting pair. No weather was added (weather stays outdoors).

## Compare

Add `?cozy=0` to the address to see the old foyer. Pictures: `docs/screenshots/cozy/`.

Characters were left as they are for this test: the chibi kit is shared by every scene, so making them rounder belongs in its own change if this look is kept.

Tests: `python tests/test_cozy.py`.
