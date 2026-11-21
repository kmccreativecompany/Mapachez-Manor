# Hair silhouette refresh (review branch)

## Creative direction
The character creator's hair should read at real **32 x 44 pixel sprite** size: recognizable silhouettes first, tidy highlight clusters second. A hairstyle is a cut/shape; a separate **Strand texture** control adjusts straight, wavy, curly or coily detail. Player-facing choices use friendly names rather than a numeric texture code.

## The prioritized twelve

| Priority | ID | Player label | Default texture | Front silhouette | Side/back requirement |
| --- | --- | --- | --- | --- | --- |
| Hero | sleek-bob | Sleek Bob | 1B | Straight blunt jaw-level ends, soft part | Blunt lower perimeter |
| Hero | soft-waves | Soft Waves | 2B | S-shaped shoulder falls | Distinct shoulder volume |
| Hero | long-curls | Long Curls | 3B | Defined tumbling large ringlets | Long, clustered curls |
| Hero | cloud-curls | Cloud Curls | 4B | Wide rounded coil mass | Full back silhouette |
| Hero | high-puff | High Puff | 4C | Raised gathered crown and circular puff | Raised puff and gathered nape |
| Hero | soft-pixie | Soft Pixie | 1C | Short layered, asymmetric fringe | Short sides and textured crown |
| Expansion | close-crop | Close Crop | 4A | Close-fitting textured cap | Clean short back |
| Expansion | wavy-bob | Wavy Bob | 2C | Chin-length waves | Curved chin-level ends |
| Expansion | curly-bob | Curly Bob | 3C | Bouncy ringlets near jaw | Compact curl clusters |
| Expansion | shoulder-straight | Shoulder Length | 1A | Smooth shoulder-length locks | Straight shoulder silhouette |
| Expansion | long-waves | Long Waves | 2A | Loose cascading lower waves | Length past shoulder |
| Expansion | low-bun | Low Bun | 1B | Smooth swept crown | Visible knot at the nape |

All twelve are available in this first graphics pass, not only the hero six. Original 1A–4C internal keys remain available for compatibility, but the picker labels them **Silky straight**, **Loose waves**, **Spring curls**, **Dense coils**, etc. Players can change textures independently after choosing a style.

## Implementation
- The game continues as a **single offline HTML file**. No sprite sheets or image downloads are needed.
- `MIX_HAIR_STYLES` is a set of 12 stable style IDs. New mix characters default to Soft Waves. Random characters use the same roster.
- `styledHair` draws distinct front, side and back pixel-art silhouettes; a style-specific `longBack` draws hair behind the shoulders before the torso.
- Thumbnail portraits are cropped directly from the **same 32 x 44 game sprite renderer**, so an option is not represented by a misleading hand-drawn swatch.
- Existing mix saves lacking `hairStyle` still go through the prior `hairDo` and `longBack` rendering. The legacy `hairdo:'bald'` takes precedence over a style.
- The existing player save key, head coverings, facial hair, mobility, three-eye support and unrelated guest/staff dialogue are unchanged.
- The construct/robot head uses a separate renderer and does not yet display these new hairstyle silhouettes. That is future work, not a promised feature in this pull request.

## Verification
The new in-world `pxPaint` renderer was exercised independently for all twelve styles in **front, left, right and back** directions, and all twelve yielded unique full-sprite pixel signatures for each view. Legacy and bald rendering still worked, and both inline game scripts passed JavaScript syntax parsing.

See `tests/test_hair_styles.py` for browser checks of thumbnails, live preview, saving, mobile use and existing-save compatibility. The browser Playwright suite has **not been run** as part of this branch: reviewers should run `python tests/test_hair_styles.py` and `python tests/test_cast.py` before merging.
