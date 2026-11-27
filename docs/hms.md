# HMS v1: learning the desk computer

HMS means **hotel management system**: the desk computer where every booking, room, guest note
and bill lives. HMS v1 makes learning it part of play, and turns the desk jobs that feel dull in
real life into quick, sparkly games. It lives at the end of `index.html` (`HMS v1` block).

Everything is drawn with code, every word is written ahead of time in English and Spanish,
nothing is downloaded and nothing costs money to run. Progress is saved on the device under
`mapachez_hms_v1`.

## Where players meet the HMS

| Where | What happens |
| --- | --- |
| Title screen | "🖥️ Learn the HMS, the desk computer · 0 / 5 →" |
| Front desk in the manor | The monitor on the desk glows, with a green "!" until all lessons are done. Walk up and press E, tap it, or press **H** anywhere. |
| Sidebar | "🖥️ HMS · *level*" button under the tip jar. |
| House ledger (L) | A "🖥️ Desk computer" tab. |
| Guest moments that depend on a record | "💡 This guest has a record in the HMS. 🖥️ Peek first". Peeking shows the guest's notes; answering after a peek earns +1 tip. Without a peek, a soft "Next time, peek in the HMS" line. |
| Every third guest in the manor | A guest asks something only the HMS knows ("Is my room ready yet?"). The hint names the tab, and the tab glows once the HMS opens. |
| Quick shifts | After the first lesson, guest 2 of every quick shift is an HMS question (skipped when rush hour starts that early). |

## The desk computer home (HMS FRIENDLY v1)

The home is sorted so there is always one obvious thing to do. Nothing was removed.

1. Delores's greeting (her first-visit hello, then "Back at the keys?").
2. **✨ Your next step**: one glowing card with one big button. It walks the player through the
   five lessons, then the Check-in e-course, then any desk game not tried yet, and after that it
   always offers "A guest is waiting at the practice hotel".
3. Two big tiles: **🏨 Practice hotel** and **🔎 Browse records** (the real manor HMS screen).
4. **More**: the HMS skill bar, the e-course button, all five lessons, all three desk games and
   "Explore on my own", exactly as before.

## The practice hotel (nothing counts)

A pretend HMS for poking around freely. No tips, no HMS points and nothing saved, so mistakes
cost nothing. A big **↩️ Undo** sits at the bottom and takes back any tap (up to 60), and
**🔄 Start fresh** deals a new hotel (also undoable).

- **Room board**: six big tiles, 201 to 206, colored by status: 🧹 Dirty (peach),
  🔍 Cleaned, not inspected (yellow), ✨ Inspected & ready (green), 🛌 Occupied (blue, with the
  guest's face and first name). Tap a tile to act: housekeeping cleans it, a supervisor inspects
  it, mark it dirty, check a guest in, check out (the room turns dirty), move rooms (the old room
  turns dirty), or peek at their file.
- **Waiting at the desk**: bookings with ✅ Check in and ❌ Cancel, plus **＋ New booking**.
- **Check-in** keeps the real rules: only a ✨ room (a gentle "not inspected yet" on 🔍, "dirty"
  on 🧹), then 📱 phone with area code, ✉️ email read back and 💳 a card on file, and only then
  🔑 the keys. Delores says why after each one, and reminds players every HMS looks a little
  different but does these same jobs.
- Guests are make-believe, with names from all over the world and a random look (monster, alien,
  fae, construct and so on). Phone numbers use 555-01xx, emails use example.com and cards use
  well-known test endings, only ever shown masked.

Tests: `tests/test_hms_friendly.py`.

## The HMS screen

Four big tabs: 📅 Bookings, 🛏️ Rooms, 🙂 Guests, 🧾 Bills. The data is the manor's own six
rooms (201 to 206) and the story's guests (Mr. Finch, Lady Vesper, Ms. Vale, M. Nine) plus two
arrivals (Juniper Glow in 201, Captain Barnaby Fuzz in 205). Room status uses four pictures:
✨ Clean, inspected & ready (a supervisor has checked the room after cleaning), 🛌 Guest inside, 🧹 Needs a tidy, 🔍 Cleaned, not inspected, 🔧 Needs fixing. Important notes carry ⚠️.
Arriving guests have a ✅ Check in button that only accepts a ✨ room. A 🔍 room is cleaned but not
yet inspected by a housekeeping supervisor, so a guest cannot go in; picking one gets a gentle correction.
In Room Rush, housekeeping's "sparkling clean" call makes a room 🔍, and only the supervisor's inspection call makes it ✨.

## Lessons (about a minute each)

1. Find a booking. 2. Check a room. 3. Read guest notes. 4. Read a bill. 5. Check a guest in
(pick a ✨ room, then phone with area code, email and a card on file, and only then the keys).
The deeper why lives in the Front Desk Check-In e-course (`docs/course.md`).

Delores says what to tap and the next tap glows with a little pointing paw. Wrong taps do
nothing. Lessons 1 to 4 end with one gentle question ("Look again" on a miss, never a penalty).
Each new lesson: +3 tips, +10 HMS points, sparkles. All five: a gift box (`hms` reason).

## Look-it-up questions

12 questions in `HMS_QS`, each with the tab to look in and the HMS line that answers it.
Right after looking: +4 tips, +5 HMS points, counts as a best answer in a quick shift.
Right without looking: +2 tips and "Next time, peek in the HMS first."
Missed: the right answer and the HMS line are shown, and the question comes back later.
One question teaches privacy: a friend asks for Mr. Finch's room number, and the record says
not to share it.

## Desk games

- **🧹 Room Rush** (room status): six radio calls ("Room 205 is sparkling clean!"). Tap the room,
  then its new status. Tiles flip, coins pop, combos build. A count-up clock shows your time and
  best time; there is no time limit.
- **📝 Booking Builder** (data entry): a guest says their name, nights and a wish. Tap the right
  card for each field (the traps are typos like "Bramble Thistlewink"), then pick a ✨ room.
- **🔍 Bill Detective** (billing): one charge on each of five bills is wrong (a sesame bagel for a
  guest with a sesame allergy, a double charge, three nights for a one-night stay). Tap it, it
  gets stamped FIXED and the total counts down.

Each round: tips for every clean answer (+2 for a perfect round), +4 HMS points, confetti on a
perfect round. Slips are counted kindly and never take anything away.

## HMS skill and pins

Levels by HMS points: New at the desk (0), Finds things fast (12), Desk helper (35), HMS whiz (70),
Desk wizard (120). Ten pins join the Memory Book: First Login, First Lesson, HMS Graduate,
Peek First, Look It Up (5 looked-up answers), Room Board Hero, Neat Bookings, Bill Detective
(10 mistakes caught), Desk Wizard, and the secret Quick Paws (Room Rush under 40 seconds).

## The bigger lab

The full Silver Key practice HMS still lives at the training desk (T → HMS practice). The desk
computer's home links to it as "Big practice lab →" for later.

## Tests

`tests/test_hms.py` (run with `CHROMIUM_PATH=/opt/pw-browsers/chromium python tests/test_hms.py`).

## Room wait (ROOM WAIT v1)
In the practice hotel, picking a 🔍 (cleaned, not inspected) or 🧹 (dirty) room for a waiting guest opens a help card instead of a dead end:
- 📻 Radio or 💬 text Evelyn, the housekeeping supervisor, to inspect it (or ask housekeeping for a rush clean on a 🧹 room). A short sped-up wait runs, the room turns ✨, and check-in carries on.
- While the guest waits: offer a seat and a drink, keep their luggage in a secure (locked) luggage room, text them when the room is ready (mobile with area code, which also puts the phone on file), a garden stroll, or the best one, an honest time estimate with a promise to update. "One sec!" is the gentle miss.
- Any 🔍 or 🧹 room card also has the radio and text buttons; the quick buttons stay. Tests: tests/test_room_wait.py.

## Luggage room, 4 PM and guest programs (LUGGAGE v1)
- 🔒 Luggage room as its own walled room in the foyer's south-west corner on the manor map, by the front entrance and a new valet stand (shelves of tagged bags, the luggage cart, a locked door with keypad facing the entrance; walk up and press E): opens with the master key or the door code (4-1-6, "4 PM is 16:00"). The valet loads bags on a cart and tags each piece with the guest's name and departure date, never the room number. A desk-check line under each tag shows whether the guest is still waiting; deliver bags once they have keys ("Bell service").
- 🕐 Practice clock starts at 1:00 PM. Standard check-in is 4 PM because housekeeping needs the day to clean and inspect. Early rooms are a bonus; past 4 PM a waiting guest is urgent.
- Impatient guests: best answer is sorry + why + honest time. Snag: the second inspection finds a dripping faucet; update the guest first.
- Two invented consortia: Opal Card Stays (card-member, 12 PM early check-in subject to availability, guaranteed 4 PM late check-out, welcome letter) and Compass Circle (travel-advisor network, perks when available, no guaranteed late check-out). Lesson + 3-question quiz. Tests: tests/test_luggage.py.
