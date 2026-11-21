# Whimsical storybook sprite direction

This branch introduces a **simplified chibi pixel-art face treatment** for the existing code-drawn character kit. It retains the current 32 × 44 grids, outfits, animation directions, deterministic named character appearances, and save format.

## Scope
- **People, monsters, aliens, fae, and ghost guests:** simpler, readable eyes and subtle cheeks; existing silhouettes, clothing and secret traits remain.
- **Raccoons:** smaller eye highlights and simplified expressions. Preserve Delores, her family, plush faces, ringed tails, and moods.
- **Robots:** simplified warm-lit face screens, with the same existing mechanical body and animation.
- **Other animals:** retain existing small animal scenes (including Muffin), without adding invented species labels or new animal assets. Additional pet sprites remain a follow-up task.

## Visual language
- Cozy, whimsical, calm and gently mysterious, **not horror**.
- Muted burgundy, cream, forest green, brass and walnut are the preferred environment palette. Creature colors may vary to make individual guests recognizable.
- Large clear silhouettes, simple facial expressions, limited highlights and few animation frames.
- Identity should be revealed by behavior and story, not labels or spoilers.
- Characters should remain recognizable at game scale and at enlarged dialogue scale.
- Skin tones, hair textures and styles, head coverings, and bald appearances should be represented respectfully in later creator expansion without gendered default labels.
- Sprite-sheet concept art is an **art reference**, not a directly importable sprite atlas. The shipped game currently draws characters procedurally.

## Implementation
- Added `CAST_STORYBOOK` flag to the existing renderer.
- Simplified human/creature face painting and robot/raccoon eyes.
- Avoided external dependencies, sprite downloads and save changes.

## Review & verification
- Verified syntactic parsing of both inline script blocks before pushing.
- Existing `tests/test_cast.py`, `tests/test_cute.py`, and `tests/test_ghosts.py` should be executed in a local Playwright/Chromium environment.
- Visually inspect 4 movement directions, front-desk conversations, raccoon mood animation, ghost transparency, the robot face, and display sizes.
- The concept image is a visual target; **the code is not a pixel-perfect reproduction**.