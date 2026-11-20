# New nights and fair answers

## Night one is one simple loop

A brand-new player sees only the main loop on night one: **Begin your night** or
**Quick shift**, the tips they earn, and **their cottage** to spend them on. Each
finished shift (or every five guests helped) opens one more part of the manor, in
this order:

1. Memory Book, pins and keepsakes
2. Closet
3. Desk computer (HMS)
4. Festival grounds and Visit a place
5. Mystery guests
6. The lily mystery
7. Penny
8. Star service
9. Training shortcut, house ledger and shift journal
10. Progress report and certificate (always shown for **Training with my hotel**)

Something new glows gold and a "New tonight" note appears until the player taps it.
A small line under Quick shift says something new opens next shift.

- Players who had progress before this update see everything straight away.
- **Comfort & sound → Show everything now** opens the whole manor at once.
- Keyboard shortcuts (T, L, J, M) and places inside the map keep working, so curious
  players can still find things early.
- Save key: `mapachez_nights_v1` (`all`, `seen`, `fresh`). Code: the NEW NIGHTS v1
  block at the end of `index.html`. Tests: `tests/test_nights.py`.

## Fair answers

The best answer used to be the longest choice in every guest moment, so tapping
the longest answer always won. The wording now varies: in English the best answer
is the longest in 16 moments, the shortest in 17 and in the middle in 19 (Spanish
is similar). `tests/test_answers.py` fails if always picking the longest, shortest
or middle answer would win more than 45% of the time.

When you add or change a guest moment, edit `training/silver-key.html` (and
`training/moments-es.json` for Spanish), then run `python3 tools/embed_guest_moments.py`,
`python3 tools/embed_training.py` and `python3 tests/test_answers.py`.
Note: `tools/embed_spanish.py` also rewrites the Spanish button words from
`training/words-es.json`, which is older than the words inside `index.html`, so
only copy its `MOMENTS_ES` line.
