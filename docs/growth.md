# Guest moments, growth bars and pins

This layer turns Silver Key practice into part of the manor. It stays inside the
single offline `index.html`: no server, account, network request or paid service.

## What players see

- **A guest who needs a hand.** After Delores's briefing, a guest with a gold `!`
  waits somewhere in the manor. Walk over and press **E** (or click them) to answer
  one Silver Key moment. A new guest appears in a new spot after each answer.
- **Quick shift.** Five guests in a row, about three minutes. Start it from the title
  screen, the sidebar card, or press **Q**. Ends with a summary from Delores.
- **Growth bars.** Guest trust, Care & safety and Teamwork fill with every answer:
  +10 for a best answer (+6 when repeating one already mastered), +3 for a close
  answer, +1 for a miss. Levels: Starting out, Bronze (20), Silver (60), Gold (120),
  Silver Key (200), Legend (320). Each new level gets a celebration.
- **Second chances.** A missed moment comes back three answers later, marked
  "second chance", until the player gets it right.
- **Nightly streak.** Playing on consecutive days counts nights in a row.
- **36 pins** (32 here plus four role pins from [setup](setup.md)) in the Memory Book under **Pins & wardrobe**, including three secret pins
  that stay hidden until earned. Story milestones (finishing an evening, all six seals,
  noticing something unasked, visiting the festival) count too.
- **Wardrobe.** Each level reached on any bar unlocks a coat colour for the player.
  Legend adds a floating key above the player and a glowing key at the front desk.

## Saves

Growth uses its own key, `mapachez_growth_v1`. The story save, Memory Book,
festival customisations, comfort settings and Silver Key desk keys are unchanged.
Guest moments never advance the story clock or change story meters. A corrupt
growth save resets growth only.

## Source

`training/silver-key.html` remains the source of the 52 moments. After editing its
`const rounds = [...]`, refresh both embedded copies:

```sh
python tools/embed_training.py
python tools/embed_guest_moments.py
```

The growth code sits between `GROWTH v1` markers near the end of `index.html`'s
script, and its styles are marked `/* GROWTH v1 */`.

## Checks

```sh
python tests/test_growth.py
python tests/test_training_integration.py
```

Set `CHROMIUM_PATH` if Chromium is not at `/usr/bin/chromium`. The growth suite
covers a perfect quick shift from the title, a missed moment returning, the in-world
guest leaving the story untouched, a level-up wardrobe unlock, corrupt-save recovery,
and the 390-pixel phone layout.
