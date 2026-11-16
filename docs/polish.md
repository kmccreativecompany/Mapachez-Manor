# Visual polish pass (v1)

A look over every screen after the candy chibis and Plush raccoons, fixing the details that fell short of
"simple at a glance, happy for the eye, light on phones". Everything is drawn with code; no pictures were added.

| What | Where in `index.html` |
| --- | --- |
| Guest moment cards (quick shift, rush hour) show the guest's own chibi, the same being you see on the map. Initials stay as a fallback. | `momentPerson`, `avatarHTML`, `paintAvatars` |
| Every dialog with a speaker shows a big crisp bust; Delores's radio messages show Delores. Pass `speaker:'<cast key>'` to `scene()` for anyone else. | `paintBust`, `bustHTML`, `scene()` |
| The manor crest (title and header) is Delores in her Plush look, painted from the character kit at start-up. | `.crest-art`, `#crest-arch` |
| Rooms 201 to 206 each have their own soft colour (bed, curtains, rug) and bigger room number plaques. | `ROOM_HUES`, `room()` |
| Festival booths have scalloped candy awnings, gold-rimmed signs and clearer names. | `booth()` in the festival layer |
| Dialog titles no longer get a black focus box; corner swirls are smaller and never sit on words (phones and the training desk too). | `VISUAL POLISH v1` CSS |
| On phones the side panel stacks in one column instead of squeezing into two. | same CSS block |
| Training desk "Play as" cards line up at the top and keep glossary words inside their sentence. | `training/silver-key.html` (re-embedded with `tools/embed_training.py`) |

Cost: the busts reuse the cached 32 x 44 sprites, so a card paints in well under a millisecond, and the map
changes are in the cached map layer (no per-frame cost).

Checks: `tests/test_polish.py` plus the existing suites. Before-and-after pictures are in `docs/screenshots/polish/`.
