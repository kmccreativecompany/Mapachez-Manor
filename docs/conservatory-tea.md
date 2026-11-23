# Tea in the conservatory

An optional, five-part overheard conversation in the existing conservatory. There
is no new restaurant, map, dependency, network request or training requirement.
The manor's title now establishes it as a fictional five-star hotel.

## Finding and playing the scene

- Walk to the small tea table in the conservatory and press **E**, or tap the table.
- The conservatory's existing interaction also offers **Listen by the tea table**.
- When **Visit a place** is available, choose **Conservatory tea table**.
- Choose **Keep listening** to hear another few lines. **Listen a little longer**
  moves to the next encounter. Returning to work or closing the dialog leaves
  the current encounter available.
- Reading, leaving and replaying change neither the hotel clock nor training
  scores. The episode ends on **To be continued**; the next episode is not yet
  implemented. The ending offers a replay that preserves completion.
- English and Spanish use the same cast, beat order and saved cursor.

## Seated characters

Léonie Rusk and Nalin Desai sit facing each other across a linen-covered table
with porcelain cups, a teapot and biscuits. Their heads, hair and upper bodies
use the existing character renderer. Upholstered chair backs, cushions, bent
legs and shoes give them seated silhouettes. Corvin Rusk arrives standing and
takes the third chair in the following beat. All three have consistent human
recipes, so the spouses do not randomly acquire mismatched species.

The tea furniture participates in the manor's existing pathfinder. The piano,
rehearsal area and alternate conservatory entrance remain accessible. The old
loose chair near this spot is replaced by the tea seating; other rooms and
characters are unchanged.

## Saves and compatibility

The optional cursor lives at `state.sideStories.tea`, alongside the existing
`sideStories.fern` clue. Its version, beat, revealed-line count and completion
are validated when read. Old story saves need no migration. The same cursor
works in either language. Starting a genuinely new evening starts this story
again with that evening, rather than changing the account-wide training save.

## Author notes: spoilers

The opening suggests a secret romance. Léonie is actually consulting her divorce
lawyer because she fears Corvin's temper. She is not having an affair. Nalin has
been dating Corvin, and claims this will improve Léonie's settlement and his own
fee. This is the dishonest character's justification, not a statement of law or
an endorsed legal practice. Nobody treats his scheme as sound professional advice.

Corvin's message proves Nalin invited him. The final photograph and invoice
reveal that Corvin also paid Nalin to find out whether Léonie was leaving.
Exactly how the competing arrangements began remains for the next episode.
The reveal targets deception, greed and conflicts of interest. There is no
sexual content, hotel-room encounter, bedroom implication or physical attack.
The butler takes the tea request at face value and only offers ordinary service.
No new engineering repair subplot is introduced in this bounded episode.

The fresh names were checked against the existing repository before adding
them. The episode does not reuse Adrian, the existing Ms. Vale or other cast.

## Verification

Run `node --test tests/test_tea.mjs` for inline-script compilation, reveal order,
save/resume/replay behavior, malformed-save handling, bilingual speaker parity,
unaffected clocks/scores, and routes using the actual manor pathfinder.

Browser QA should additionally cover opening the scene through the map and
conservatory controls, all five encounters, leaving and resuming, the visible
seated poses, and existing briefing/festival navigation. Check narrow screens
and the browser console. Model tests do not establish visual correctness.
