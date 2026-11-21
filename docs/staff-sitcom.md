# Staff Room Confidential (STAFF SITCOM v1)

Mapáchez Manor combines **whimsical appearance with grounded workplace sitcom dialogue**.
The joke is human behavior, not a character's species, appearance or supernatural identity.

## How to play

- From the title screen, select **🎭 Staff sitcom**.
- During a shift, visit the front desk and choose **Overhear the staff room**.
- Choose an episode, read three introductory lines, then select **Keep listening** to reveal the rest, stage direction and private thought.
- Choose **Next staff scene** or return to the episode list. Episodes can be replayed.
- This is optional entertainment, not a graded Silver Key question. Opening dialogue does not advance the in-world clock.

## Nine scenes

| id | Episode | Main joke |
| --- | --- | --- |
| meeting | The Five-Minute Meeting | A meeting about reducing meetings lasts 43 minutes |
| recognition | Employee of the Month | Recognition comes with three more jobs |
| procedures | The Keeper of Every Procedure | A veteran memorized all the retired policies |
| printer | The Luxury Hotel Printer | The printer finally produces yesterday's arrivals |
| groupchat | The Workplace Group Chat | Twenty-four acknowledgments to a memo about fewer messages |
| checkout | The Guest Who Hasn't Checked Out | The departing guest orders lunch at 12:35 |
| trust | The Team-Building Exercise | Engineering knows how unreliable the chairs are |
| promotion | The Promotion Interview | An aspiring manager can identify problems but not solve them |
| favor | The Tiny Favor | A small favor turns out to be a whole overnight shift |

The rejected golf cart joke is **not** part of the sitcom catalog.

## Implementation

The offline single-file `index.html` holds both English and Spanish scripts in
`STAFF_SITCOM`. The feature adds a menu button, a front-desk interaction option,
a dialogue modal and a private-thought reveal. It uses the existing read-aloud
capability, keyboard-focusable buttons, and responsive modal styling.

Save key: `mapachez_staff_sitcom_v1`, version 1, with only a `heard` ID array.
It is separate from all existing saves, story flags, guest conversations, scores
and reward progress. Corrupt or missing data starts with an empty heard list.

## Writing standard

- Contrast a charming fantasy hotel with **recognizably real** human problems.
- Punchlines should make sense without knowledge of the game's lore.
- Keep staff emotionally intelligent, not cruel. Management and staff both make
  mistakes; no one group is always the joke.
- The final line or stage reveal should carry the comedic turn.
- Preserve the competent overnight team's professionalism when dealing with guests.

## Verification

Run `python tests/test_staff_sitcom.py` with Playwright and local Chromium available.
This covers dialogue data, menu access, reveal, saved progress, desk access and
small-screen layout. Existing guest dialogue and Silver Key tests remain separate.
