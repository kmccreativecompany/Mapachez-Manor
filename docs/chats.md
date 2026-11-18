# Guest chats by the lobby chairs (CHATS v1)

Two guests sit by the lobby chairs and talk. Their speech bubble rotates through the first
three lines. Tap it (or walk over and press E) to listen. "Keep listening" shows the rest.

When you return to your evening, the last line stays a moment and the bubble fades. The two
guests turn and walk off in different directions, one west along the foyer and one south toward
the garden door, fading as they go. A toast says "The chairs are free" with how many chats you
have overheard. About 30 seconds later a new pair walks in and sits down. With reduced motion
there is no walking: the pair simply goes, and the next pair simply appears.

The code sits between `CHATS v1` markers at the end of the main script in `index.html`, with
styles marked `/* CHATS v1 */`. It replaces the old single fern conversation and reuses its
bubble, spot and Memory Book page (a chat with `memory:true` fills that page).

## The seven chats

| id | Pair | Joke engine |
| --- | --- | --- |
| letter | Zinnia Starling, Sunny Marrow | A secret letter for Lady Vesper, signed with one note drawn twice. Callback to Mr. Finch's one-note triangle. |
| bells | Gwendolyn Butterfield, Mr. Finch | Spoons, bells, one triangle. Her next obsession is set up last. |
| time | Ms. Chen, Dr. Merriweather | One has nine minutes, one has "centuries. I mean weeks." |
| muffin | Cece Wrenwood, Basil Thorne | Muffin and Admiral both play asleep. "Two professionals." |
| blankets | Mrs. and Mr. Calder | Forty years: patience, kindness, separate blankets. |
| tuesday | Mr. Alvarez, M. Nine | A delayed flight vs. a trip "through Tuesday. Twice." |
| duchess | Pippa, Lavinia Bloom | Is Duchess a real duchess? Callback to Miso's crown drawing. |

## Writing rules

- Rule of three, the funny word last, specific details, one small misdirection.
- Jokes come from who guests already are (callbacks to regulars, gags and guest moments).
- Laugh with people, never at them. Hidden stories are hinted, never told. Nobody's kind of
  being is named (no "vampire", "alien", "monster"), and Muffin is only ever a cat.
- Lines stay under 70 characters so bubbles fit on phones. The first three lines are the teaser.

## Editing and translating

All words live in `CHATS_TEXT.en` and `CHATS_TEXT.es`, with matching ids and speakers. Each chat
has `a` and `b` (a `cast` name keeps a guest's look the same as elsewhere), `lines` as
`[speaker, text]`, an optional `stage` line shown after the teaser, and an `end` line.

## Saving

`mapachez_chats_v1` on the device: `next` (which pair is in the chairs) and `heard` (chat ids).
Hearing the letter chat still sets the evening's old fern flag for the Memory Book page. Hearing any chat
earns A Listening Ear; hearing all seven earns the new All Ears pin.

## Checks

```sh
python tests/test_chats.py
```
