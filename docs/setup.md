# Play modes, hotel packs, reports and Spanish

This layer helps the game work both for curious people playing on their own and for
hotels training a team. It stays inside the single offline `index.html`: no server,
account, network request, tracking or paid service.

## What players see

- **A welcome choice on the first visit.** "Just for fun" opens the first guest
  straight away. "Training with my hotel" asks for a name (for certificates), a role
  and an optional hotel pack, then opens the first guest. Players who already have
  progress are not interrupted; the title shows "How are you playing? Choose".
- **The first minute.** The first answer earns the First Hello pin with confetti, and
  the result offers "Keep going: quick shift" or "Explore the manor".
- **Role tracks.** Front desk, Housekeeping, Dining, and Night shift & leads. Guests
  and quick shifts lean toward the chosen role first. Speaking prompts count for
  every role. Finishing every moment in a role earns that role's pin and certificate.
- **My report & certificates** (title screen, or **Report** on the growth card):
  points this week, skills by role, house rules, a printable certificate per finished
  role, a printable one-page skills report and the player's score code.
- **Score codes and the team board.** A score code is a line of text (`MM1-...`) with
  name, team, role, this week's points and skills finished. Paste codes into the team
  board to rank this week's points, see team totals, and print "who finished which
  skills". Codes have a typo check but are honest-play records, not exams.
- **Manager corner.** Hotel name, manager name (signs certificates), house rules and
  the hotel's own guest scenarios, written as a situation with a best answer, an
  optional okay answer and a wrong answer. Share as a pack code (`MMPACK1-...`) or a
  downloaded `.json` file; staff paste or load it during hotel setup.
- **Spanish.** English and Español buttons sit in the welcome choice and report.
  Guest moments, menus, reports and certificates switch language; the story chapter
  is still English for now.
- **Phone-first touches.** Big tap targets, the main button stays in reach at the
  bottom of long cards, no double-tap zoom, and room for the phone's home bar.

## Saves

New keys only: `mapachez_profile_v1` (mode, name, role, team, language, weekly
points), `mapachez_pack_v1` (the hotel pack) and `mapachez_board_v1` (pasted score
codes). Story saves, growth, the Memory Book, festival choices, comfort settings and
desk keys keep their formats. Hotel scenarios are added after the 52 built-in
moments; if a manager removes or reorders scenarios, a player's progress follows the
scenario it belongs to.

## Free demo night

```sh
python3 tools/build_demo.py
```

Writes `dist/mapachez-demo.html` (not committed): the story chapter and the first 12
guest moments, with hotel training, the manager corner, the training desk and
certificates showing a friendly "full edition" card. It is a sampler, not copy
protection: anyone can read the HTML.

## Translations

`training/words-es.json` holds every menu and button phrase, keyed by the English
text. `training/moments-es.json` holds the 52 guest moments, matched by English
title. After editing either, run `python3 tools/embed_spanish.py`. Adding another
language means a new pair of files and a new entry in `LANGS`. The Spanish was
written by an AI assistant; have a native speaker on the team read it before
hotels rely on it.

## Source

The code sits between `SETUP v1` markers just before and after the growth block in
`index.html`'s script, and its styles are marked `/* SETUP v1 */`.

## Checks

```sh
python tests/test_setup.py
python tests/test_growth.py
python tests/test_training_integration.py
```

Set `CHROMIUM_PATH` if Chromium is not at `/usr/bin/chromium`. The setup suite covers
the first-visit choice and first guest, existing players not being interrupted, role
quick shifts and certificate printing, a hotel pack travelling by code and keeping
progress when edited, score codes and the team board, Spanish, the demo copy, and
390-pixel phone screens. These run in Chromium only; Safari and real phones still
need a hands-on check.
