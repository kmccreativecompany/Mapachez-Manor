# First minute fixes (2026-11-26 review)

- **Name box once.** After the first guest, "Explore the manor" asks for a name one time. Save or Skip closes the box and walks straight into the manor (it used to stay open, so a second tap asked a brand-new player to start over).
- **Next step under the map (phones).** A gold "Next" button under the map mirrors the top thread in "Threads to follow" and stays in view while scrolling the map area. Desktop keeps the sidebar only.
- **Continue first.** With an evening in progress, "Continue your evening" is the big gold button and sits first; "Begin your night" stays, as a plain button.
- **Pin pop-up.** On phones the "Pin earned" pop-up is smaller and higher, so the tip counter stays visible.
- **Fair answers.** Wrong answers now use "ask", "confirm", "offer" and "check" too, so those words no longer give the best answer away (`tests/test_answers.py` test 05). The garlic question's answers now talk about garlic, not fish.
- **12 new guest moments** (64 in total, English and Spanish), edited in `training/silver-key.html` and `training/moments-es.json`, then embedded with `tools/embed_guest_moments.py` and `tools/embed_spanish.py`.
- **Saves.** Growth saves now record how many core moments existed (`core`). When core moments are added, a hotel pack's saved progress moves along with it.

Tests: `tests/test_first_minute.py`.
