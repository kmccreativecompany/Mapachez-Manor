# MORE COURSES v1: three more e-courses and a Master Certificate

Three more Silver Key e-courses sit beside the check-in course (`docs/course.md`), built the same
way: Delores explains **how**, a green **💡 Why it matters** box explains **why**, one tap-to-check
question per lesson, then a final check. The code is the `MORE COURSES v1` block at the end of
`index.html`; the check-in course block is left as it is. Everything is drawn with code, in English
and Spanish, and nothing costs money to run.

| Course | ID prefix | Lessons |
| --- | --- | --- |
| 🛎️ Front Desk Check-In & Guest Registration Fundamentals | `SKC-CHK` | see `docs/course.md` |
| 💬 Luxury Guest Service Language & Communication | `SKC-LUX` | Names and warm welcomes · Words that sound like velvet · Never a flat “no” · Notice before they ask · Walk them there · A graceful goodbye |
| 📞 Front Desk Telephone Etiquette & Call Handling | `SKC-PHN` | Answer with a smile · May I place you on hold? · Warm transfers · Taking a message · Guest privacy on the phone · Closing the call |
| 🧹 Housekeeping Standards & Guest Room Inspection | `SKC-HSK` | Knock, announce, wait · Do Not Disturb (text first, calling disturbs) · Which room first? · Top to bottom, clean to dirty · Cleaned is not inspected · Lost and found |
| 👑 Master Certificate: Hotel Front Office & Guest Services | `SKC-MST` | Earned automatically when all four are passed |

## Same rules as the check-in course

- Each lesson: +2 tips the first time. Wrong taps get a kind hint and can be tried again.
- Final check: six shuffled questions, 5 of 6 passes, unlimited tries, nothing taken away for a miss.
  Passing gives +5 tips, confetti and a pin (Silver Tongue, Golden Voice, White Glove).
- The right answer is not always the longest: across the new courses it is the longest, the
  shortest or in the middle, and `tests/test_courses.py` checks that no length rule wins more than
  60% of the time.
- Make-believe details only: 555-01xx numbers with area codes, no real hotels or brands.

## One name on every certificate

The name works like the check-in course: asked once, locked when a certificate is earned. Once any
certificate carries a name, every later certificate (and the Master) uses that same name, so a
player can't put a different name on each one. Someone who passed without a name can add it once
on the certificate screen.

## Certificates

Each one uses the same Silver Key design as the check-in certificate (issued and signed by KMC
Creative Company, LLC, "gamified e-course", "not an accreditation or license", locked name,
certificate ID, PNG download and LinkedIn "Add to profile" link). The Master Certificate has a
double gold frame, a crown seal marked MASTER and green ribbons, and lists all four courses.
The drawing lives in `mcDrawCert` inside the new block, so the check-in certificate code is untouched.

## Where players find them

- The title button is now **🎓 E-courses · certificates · n / 4**, and opens the catalog of all
  four courses plus the Master Certificate (it is still unlocked with the desk computer, night 3).
- The desk computer's check-in course button is unchanged; the check-in course has an
  **🎓 All e-courses** button that goes back to the catalog.

## One new thing per night

The three new courses are steps 11, 12 and 13 of NEW NIGHTS (`docs/nights.md`), after everything
else. Until then the catalog shows them locked with a gentle "🌙 Opens after your next shift" or
"Opens in n more shifts", so there is always something to look forward to. Players with
**Show everything now** (or older saves) see them all at once.

## Saves and tests

Save key `mapachez_courses_v1`: `{version:1, courses:{lux|phn|hsk:{mods,tries,best,passed,salt,name}}, master:{passed,salt,name}}`.
Junk saves recover to a fresh start. Tests: `tests/test_courses.py`
(`CHROMIUM_PATH=/opt/pw-browsers/chromium python tests/test_courses.py`, one file per process).
