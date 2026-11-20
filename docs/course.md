# COURSE v1: the Front Desk Check-In e-course, with a certificate

Delores teaches check-in the way a friendly e-course would: one small step at a time, and always
with the **why**. It lives at the end of `index.html` (`COURSE v1` block). Everything is drawn with
code, every word is written in English and Spanish, and nothing costs money to run. Progress is
saved on the device under `mapachez_course_v1`.

## Every HMS is different

Delores says it in lesson 1 and on every real check-in: each hotel uses its own HMS, and the
buttons and names change, but almost every one follows the same path:

👋 Greet → 📅 Booking → 🪪 ID → 📱 Phone (with area code) → ✉️ Email → 💳 Card on file → ✨ Room ready → 🔑 Keys

## Where players find it

| Where | What |
| --- | --- |
| Title screen | "🎓 Check-in e-course · certificate · n / 6 →" |
| Desk computer home (H) | "🎓 E-course: Front Desk Check-In", right under the HMS skill bar |

## Lessons (six, about 30 seconds each)

Each lesson has Delores explaining **how**, a green **💡 Why it matters** box, and one tap-to-check
question. Wrong taps get a kind hint and can be tried again. A new lesson gives +2 tips.

1. The check-in path (the eight stops, and that keys come last)
2. Find the booking, check the ID
3. Phone number, with the area code
4. Email address (type it, then read it back)
5. A card on file (a hold, not a charge; never write a number down)
6. Then, the keys (only when everything is on file and the room is ✨ inspected)

## Final check

Six questions in a shuffled order. Every answer shows a one-line reason. 5 of 6 passes; there is no
limit on tries and nothing is taken away for a miss. Passing gives +5 tips, confetti and the
**Certified!** pin.

## Whose certificate: the name

- Right after a new player's very first guest (so the first guest is still one tap away), Delores
  explains that the game is also a gamified e-course and offers to put their first and last name on
  certificates for their resume. It's optional ("Skip for now"), and asked once.
- The course home shows a gentle reminder until a name is saved, and the final check asks once more
  ("Whose certificate is this?"), with "Take the check without a name" as the way past.
- A name must have at least two words (first and last).
- When the final check is passed, the name is **locked** onto the certificate (saved as `name` in
  `mapachez_course_v1`). The certificate screen has no name box, and changing the profile name later
  doesn't change it. Someone who passed without a name can add one, once; then it locks too.
- Once locked, the progress report's name box is locked to the same name.

## The certificate

Drawn on a canvas on the device (1200 × 850): the player's name, the date they passed, the
course name, a signature line reading "Issued by KMC Creative Company, LLC" and a gold seal
(no character signs it, so it reads as a real credential; Delores still cheers in the game). Each certificate has an ID like
`SKC-CHK-1A2B-3C4D`, made from the name, date and a random salt saved on the device.

- **⬇️ Save the picture** downloads a PNG.
- **Add to LinkedIn** opens LinkedIn's free "Add to profile" form with the course name, the
  organization (KMC Creative Company, LLC, the issuer) and the name "Silver Key Certificate: Front Desk Check-In & Guest Registration Fundamentals", the month and year, and the certificate ID filled in.

The certificate calls it a gamified e-course, and both the certificate and the screen say it is a
certificate of completion, not an accreditation or license.

## The check-in itself now teaches this too

On the desk computer, picking a ✨ room no longer hands over keys right away. A **🔑 Before the
keys** card asks for three things, one tap each, and the key button stays locked until all three
are on file. See `docs/knock.md` for details.

All the details are make-believe: 555-01xx phone numbers (reserved for fiction) with area codes,
`example.com` emails (a domain set aside for examples) and test card endings shown only as
`•••• 4242`.

## Tests

`tests/test_course.py` (run with `CHROMIUM_PATH=/opt/pw-browsers/chromium python tests/test_course.py`).
