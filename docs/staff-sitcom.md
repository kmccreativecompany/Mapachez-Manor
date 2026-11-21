# Staff interactions (internal development notes)

The whimsical setting disguises grounded, recognizable workplace conversations.
The player should discover the humor organically. Do **not** advertise a sitcom, comedy mode, jokes, or episode collection in the game UI.

## In-world discovery

- No title-screen comedy button, labeled sitcom mode or visible episode catalog.
- During an ordinary shift, visit the front desk and select **Check in with the team**.
- A staff conversation starts directly. The first three lines sound like ordinary operational chatter.
- **Keep listening** reveals the conversation, scene payoff and private thought.
- **Back to the front desk** resumes the shift. **Check on another coworker** moves to an unheard conversation.
- Once every scene has been heard, conversations rotate on further check-ins.
- Viewing a conversation is optional; it does not advance the in-world clock or award training points.

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

The rejected golf cart joke is not included.

## Implementation

The offline single-file `index.html` holds both English and Spanish scripts in
`STAFF_SITCOM`. The feature adds only an unobtrusive front-desk interaction, a dialogue modal and a private-thought reveal. It uses the existing read-aloud
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
This covers dialogue data, natural discovery, reveal, saved progress, desk access and
small-screen layout. Existing guest dialogue and Silver Key tests remain separate.
