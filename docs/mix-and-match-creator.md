# Mix-and-match character creator

## What changed

The title-screen **Character Creator** button opens a playable, offline character creator with tabs for **Body & Eyes**, **Hair & Coverings**, **Face & Glasses**, **Ears & Extras**, **Surface**, **Tail & Mobility**, and **About Me**. There is no species selection, and no category labels for a character's identity.

The panels show code-drawn pixel thumbnails and a front, side and back live preview. Choose the pieces independently, use **Surprise me** for a random combination, then **Save my look**. Your character appears in the manor using the existing 32 x 44 pixel-art renderer.

## Current choices

| Area | Supported choices |
| --- | --- |
| Eyes | 1, 2 or 3 for any created body, including metal |
| Body | Round, tall, soft, petite (subtle sprite silhouette variations) |
| Hair | 1A through 4C, bald, short, bun / updo; broad straight, wavy, curly and coily appearances |
| Head coverings | Hijab, scarf, headwrap, turban, kufi, bandana |
| Ears | Small, pointed, cat-like, long/rabbit, floppy, round |
| Other head features | Short or curled horns, antlers, paired antennae |
| Back features | Feathered, butterfly or bat wings |
| Tail | None, striped, fluffy, curved, reptilian, plumed or mermaid fin |
| Surface | Smooth skin, fur, feathers, scales, metal, ghostly |
| Texture | Several options per surface, including short/fluffy/curly/shaggy fur, layered feathers and plated scales |
| Markings | Spots, stripes, freckles and eye mask |
| Colors | Body, hair and covering palettes |
| Facial hair | None, stubble, mustache, handlebar, goatee, several beard styles, sideburns, mutton chops or whiskers; independent color |
| Glasses | One small round frame, off/on; gold, black or silver; drawn for 1, 2 or 3 eyes |
| Mobility | One classic manual wheelchair, optional for any character, burgundy seat by default, selectable seat color and mermaid-tail support |
| Identity | Optional, locally saved pronouns and custom words |

No category determines whether other features are available: for instance, a smooth-skinned character can have antlers, wings and three eyes. The player can change any combination later.

## Existing saves and named characters

- Existing saved players load in their original appearance until edited. Opening the editor converts the edit session to the independent-part format; only **Save my look** replaces their saved recipe.
- Player settings continue to be stored in `mapachez_player_v1`. There is no server account or external request.
- Existing named and pinned story characters, the Delores raccoon family, ghost guests and Muffin are not regenerated or reclassified.
- Outfits at work still follow the existing uniform rules.

## Visual scope and limitations

This is a **functional first-pass pixel renderer**, not a pixel-perfect import of the concept poster. Texture grades such as 1A / 1B / 1C are subtle at 32 x 44 pixels. Some overlapping accessories may obscure each other when deliberately combined. Body silhouette variations are modest because collision footprints remain unchanged. Voice and detailed full-body pattern layering are future work.

There are no bitmap assets or downloaded image dependencies. The icon previews are drawn with Canvas, as are the game characters. The design keeps the warm, cozy and whimsical style, while identities remain part of the story rather than visible classification labels.

## Testing

The developer validated both inline JavaScript blocks for parsing. The pure `pxPaint` function rendered 960 combinations across four directions and produced distinct 1-, 2- and 3-eye sprites for both ordinary and mechanical looks, with no exceptions. Browser regression tests in `tests/test_cast.py` have been updated for mixed saves and independent feature combinations, but have **not been executed in Playwright** yet.

For browser verification run `CHROMIUM_PATH=/usr/bin/chromium python tests/test_cast.py` from the repository root with Playwright installed, in a fresh test profile. Confirm preview changes, saving, refreshing, character drawing while walking, keyboard/touch usability, ghost alpha, and no console errors.

## Website access and added controls

The live GitHub Pages landing screen contains a persistent **🎨 Character Creator** button next to **Begin your night**. Selecting it opens the five original customization tabs plus **Face & Glasses** and **Tail & Mobility**. Save with **Save my look**. Facial hair, glasses, mermaid fins and a single manual wheelchair render in the shared 32 x 44 sprites in the game, including chair-wheel changes as the character moves.

A wheelchair is an independent mobility selection and never automatically assigned based on tail or appearance. The wheelchair is one consistent pixel-art manual model, not six themed models. Mermaid tails work with or without the chair. These are compact sprite approximations of the larger design concept illustration.

## Refined character studio (November 21, 2026)

The creator is now designed as a **large two-column studio**, still in the same offline, single-file HTML game.

- The **left column** is a large, continually visible pixel-art character preview with smaller side and back views. It remains visible while the right-side choices scroll.
- **Five navigation tabs** replace the former seven: **Body**, **Hair**, **Face**, **Features** and **Mobility**.
- No options were removed: surface and markings moved under Body; pronouns moved under Face; tail choices moved under Mobility.
- Each **1A to 4C** selection now has its own 40 × 40 code-drawn miniature portrait. Straight, wavy, curly and coily strand patterns vary in both the selection icon and the existing 32 × 44 in-game sprite.
- Hair coverings and bald/short/updo styles have enlarged, more recognizable pixel icons.
- The options pane scrolls independently on wide screens; the preview stays visible. On small screens the preview compresses into a fixed header above horizontally scrollable tabs and a scrollable option panel.
- The buttons are at least 44 px high, with a visible selection state and focus outline. The creator preserves the option-pane scroll position and restores keyboard focus after an option update.
- Existing saves, story cast, other gameplay, and the local-storage save key are unchanged.

### Verification and caveats

The developer checked JavaScript syntax, independently generated 12 different hair sprites and 12 distinct hair thumbnails, and exercised all five tab states in a simulated DOM environment. Browser-based layout inspection, keyboard/touch testing, and the Playwright regression suite remain to be run before publishing. 32 × 44 character sprites remain intentionally stylized and simpler than the original high-resolution concept artwork.
