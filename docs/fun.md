# The fun list: rush hour, regulars, the lily mystery and surprise nights

This layer sits between `FUN v1` markers at the end of `index.html`'s script, with its
styles marked `/* FUN v1 */`. Every line is written into the file ahead of time, nothing
is generated while playing, and nothing touches the network. It costs nothing to run.

## What players see

- **Rush hour.** From the third quick shift on (every other shift, and every shift on a
  wedding night), guests 3 to 5 arrive at once. A board shows all three with their notes
  and the player chooses who to help first. Every rush includes one health or safety need
  (an allergy, an escape-risk cat, a feeding safety rule), and choosing it first earns
  "Good call. Health and safety first." A lantern counts down 2 minutes 30 seconds for a
  bonus pin only. When it runs out the guests are "happy to wait", and nothing is lost.
  **Relaxed: no timer** turns the lantern off and is remembered. The timer pauses while
  the tab is hidden and never animates under reduce motion.
- **Guests who remember you.** Twenty named guests and teammates remember how the last
  visit went and say so, kindly, even after a miss. Five regulars (Dr. Merriweather,
  Ms. Chen, Dr. Vale with Pippa and Miso, Cece with Muffin, Gwendolyn) grow four hearts
  with best answers. Each new heart unlocks a short story beat. Quick shifts invite back a
  regular you have met, so they really do return.
- **The lily mystery.** "Who keeps moving the lobby lilies?" One clue a day, earned by
  finishing a quick shift or helping five guests in the manor. After five clues the player
  can name a suspect in the **Manor notebook**. Wrong guesses get a kind, funny line and
  are ruled out. The answer ends on a teamwork lesson. The vase on the map moves with each
  clue.
- **Surprise nights.** Three days in seven, the same for everyone that day: a storm, a
  wedding or a power cut. The map gets rain, petals or candlelight, the caption above the
  map changes, the first guest of each shift brings Delores's radio line and a tip, and the
  shift leans toward fitting moments (delays and recovery in a storm, details and timing at
  a wedding, calm plans and safe entry in the dark).
- **Juicy feedback.** Best answers wiggle the raccoon, light up the guest with a smile,
  and show a "Combo ×n" chip. With sound on, each combo chimes one note higher.
- **A warm "see you tomorrow".** Each shift summary ends with tomorrow's clue number and
  the forecast. It never mentions missing a day.
- **Nine pins:** Rush Hour Hero, Cool Head, Before the Lantern Fades, Storm Keeper,
  Wedding Bells, Candlelight Service, Known by Name, Lily Detective and the secret Perfect
  Pitch (ten best answers in a row).

Left for later: the ten-second mini-games and decorating your own staff room.

## Saves

Fun progress uses its own key, `mapachez_fun_v1` (regulars met, mystery clues, rush
stats, nights played, best combo). Story, growth, profile, pack and board saves keep
their formats. A missing or corrupt fun save starts the fun layer fresh and leaves growth
alone. Nothing is saved until the first answer.

## Writing and translating

All English words are in place in the `FUN v1` block (`NIGHTS`, `REGULARS`, `MYSTERY` and
the `t('...')` calls). Spanish lives in `training/words-es.json`, keyed by the English
text; run `python tools/embed_spanish.py` after editing. Regulars are keyed by English
guest name (`GUEST_EN`, captured before the language swap), so Spanish players keep the
same friendships. Muffin and Dr. Merriweather keep their secrets: traits show through
behaviour only.

## Checks

```sh
python tests/test_fun.py
```

It covers calm first shifts, combo and cheer feedback, one clue a day, regulars who
remember a miss kindly and warm up, a keyboard-picked rush with the safety-first call,
relaxed rush with no timer, a wedding night with its pin and forced rush, naming the
wrong and right suspect, a Spanish storm night with still rain under reduce motion, a
corrupt fun save, and the rush board on a 390-pixel phone. The browser clock is fixed so
surprise nights are predictable.
