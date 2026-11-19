# Practice desk tidy-up and "Ask Delores"

The Silver Key practice desk (Training desk, **T**) had three layout problems:

1. **The HMS card floated over the page.** Guest HMS, Staff Profiles, Glossary, HMS Lab and
   Selected Record opened as a box hanging below the tab row, on top of whatever was under it
   (lessons, the Stargazing Lawn investor page), with its own little scroll bar.
2. **Too many scroll bars.** The left sidebar and that floating box each scrolled on their own,
   inside the page that also scrolled.
3. **Words broke apart.** Dotted glossary words ("clean", "arrival", "folio") jumped onto their
   own lines inside guest record cards, and the chips (TODAY'S DEPARTURE, ROOM REVIEW, FOLIO
   REVIEW) stacked instead of sitting in a row.

## What changed (`training/silver-key.html`, re-embedded into `index.html`)

- The HMS card now sits in the page under its tabs and pushes the content down. It never covers
  anything. Opening it while far down the page scrolls it into view; **Close** puts you back
  where you were.
- One scroll bar: the sidebar (career, scores, roles) scrolls with the page on desktop. Phones
  keep the existing folding "Career, roles, and comfort controls".
- Glossary words stay inside their sentence; chips sit in a row; record cards use one column on
  narrow screens; on phones the fifth tab spans the full row.
- HMS Lab's subtitle now says "Practice tools open right here. Press Close to go back to what
  you were doing."

## Ask Delores (`index.html`, practice desk toolbar)

A **🦝 Need help? Ask Delores** button sits beside "Return to the manor". It only appears as a
button; nothing pops up unless the player asks. Pressing it shows Delores (drawn with the same
code art as the desk computer lessons) with three short steps for the section the player is in:
Practice shifts, Training guest records, HMS practice, Night desk or Glossary.

**Teach me step by step** leaves the practice desk and opens the desk computer's five guided HMS
lessons, where Delores already teaches with a glowing next tap (see `docs/hms.md`).
**Got it, thanks** hides her again.

## Checks

`tests/test_practice_desk.py` (desktop 1880x930 and phone 390x844): the HMS card is in the page,
only the page scrolls, glossary words stay inline, opening far down brings the card into view and
Close returns, and Delores helps only when asked and opens the guided lessons.

Pictures: `docs/screenshots/practice-desk/`.
