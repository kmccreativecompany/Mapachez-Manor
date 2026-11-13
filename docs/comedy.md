# Clean comedy

The comedy layer sits between `COMEDY v1` markers right after the growth code in
`index.html`, with its styles marked `/* COMEDY v1 */`. Every line is written into
the file ahead of time. Nothing is generated while playing, so it costs nothing to run.

## What players see

- **A silly choice.** Each guest moment gets one clearly absurd extra answer, such as
  “Name the noise Gerald and hope he settles down.” Picking it gets a kind raccoon
  reaction, then the best answer and the Silver Key standard as usual. It counts as a
  miss, so the guest comes back for a second chance.
- **The guest's reaction.** A best answer earns a short funny line from the guest,
  shown a beat after the verdict.
- **Meanwhile in the manor.** After every second answer, a running gag moves one step:
  the wandering lobby fern, calls from a Room 13 that does not exist, Mr. Finch's one
  triangle note, and the raccoon's own instincts. Each gag escalates over five beats
  and pays off on the last one.
- **Delores's one-liners** close each quick shift, rotating so they rarely repeat.
- **Comment card of the day.** One absurd, affectionate guest review, the same for
  everyone that day.
- **Four pins:** Did Not Eat the Buffet, plus three secret ones for the silly choice,
  the Room 13 payoff and the fern payoff.

## Writing rules

- Laugh with people, never at them. No jokes about accents, looks, bodies or real groups.
- Harmless surprises only: something is off, but nobody gets hurt.
- The funny word goes last. Keep lines short.
- Jokes come from who characters already are. Reveal unusual traits through behavior,
  never by naming them.
- Tender moments stay tender. "The flower that matters" has no joke on purpose.
- The lesson stays clear. Comedy never replaces the best answer or the standard.

## Editing and translating

All words live in `COMEDY_TEXT.en`. The `silly` and `win` lists are keyed by the
moment's English title. To translate, add a sibling block (for example `es`) with the
same keys; the game picks the block that matches the page language. Running-gag
progress is worked out from the answer count, so no new save data is needed, and the
payoff flags reuse the existing `mapachez_growth_v1` flags.

## Checks

```sh
python tests/test_comedy.py
```

It checks that every moment except the tender one has jokes, that a silly pick is kind,
counts as a miss and still teaches, that best answers and shifts show their lines and
the comment card, and that the Room 13 gag pays off with its pin.
