# The manor's heart (HEART v1)

The whole game speaks in one gentle, dreamy, kind voice, with a light touch of quiet mystery.
It is shown, never named: no personality labels appear anywhere players can see.
The code sits between `HEART v1` markers at the end of the main script in `index.html`,
with its styles marked `/* HEART v1 */`. Every word is written ahead of time in English
and Spanish (`HEART_TEXT`), so it costs nothing to run.

## What players see

- **Title screen:** a few drifting gold motes (hidden with reduced motion) and
  *Tonight's little thought*, one per day, the same for everyone. After a day away it
  first says "Welcome back. The manor kept a lamp on for you."
- **Warm verdicts:** best answers, close answers and misses each get a rotating line
  (✨, 🌱, 🌙). Misses are met with warmth ("Not this time, and that's alright."). The
  best answer and the Silver Key standard always follow, and silly picks keep their
  raccoon joke.
- **Before you go:** one soft line at the end of every quick shift.
- **Glimmers inside the manor:** one find at a time appears somewhere walkable, about
  every 40 to 80 seconds. Most are small wonders (a soft light, 30 lines) or notes slipped
  under doors (a folded note, 12 lines). Rarely, a gold star brings a one-of-a-kind
  keepsake (6 in all), each only ever found once.
- **Keepsake journal:** the 📖 Keepsakes button under the map lists every find, with soft
  blanks for what is still out there.
- **Three pins:** Small Wonders (5 finds), A Jar Full of Wonders (every wonder and note),
  and the secret One of a Kind.

Guests' hidden stories, uncovered bit by bit, already live in the regulars' letters
(FUN v1); this layer leaves them as they are.

## Saving

`mapachez_heart_v1` on the device: `found`, `notes`, `rare` (indexes) and `lastVisit`.
Bad or old data is cleaned on load.

## Writing rules

Short lines, kind to everyone, quiet wonder over drama, never gloomy, no room numbers
outside 201 to 206, and Muffin is only ever a cat.

## Checks

```sh
python tests/test_heart.py
```
