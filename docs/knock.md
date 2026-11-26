# KNOCK v1: door knocks, Do Not Disturb signs and texting the guest

Guest rooms in the East Wing stay **closed from the hallway** now. Each room shows its own
coloured wall and arched door, with a warm line of light under the door when someone is inside.
It lives at the end of `index.html` (`KNOCK v1` block). Everything is drawn with code, every word
is written ahead of time in English and Spanish, and nothing costs money to run. Progress is
saved under `mapachez_knock_v1`.

## Knocking

Walk to a guest room door and you knock and say who you are, based on the role picked at setup:

| Role | Bubble |
| --- | --- |
| Front desk | "Front desk!" |
| Housekeeping | "Housekeeping!" |
| Dining | "In-Room Dining!" |
| Night shift & leads | "Night manager!" |
| A bit of everything / just for fun | "Guest services!" |

The room's scene opens with a little hallway picture: you with a speech bubble, and the door
swinging open. The guest is caught **mid-activity**, picked at random each knock: reading,
napping, yoga, a midnight snack, knitting, watering a plant, dancing, painting, a jigsaw puzzle
or tea. One line describes it ("Mr. Finch is mid-yoga, holding a very confident tree pose").
On the map that room stays open while you're nearby, then closes again. Empty rooms answer
with "No answer. The room is quiet and tidy." The story scenes behind each door are unchanged.

## Do Not Disturb

After your first two knocks, one occupied door each shift wears a little hanging sign (a moon,
"zz" and "SHH"). Going to that door opens "A sign on the door" with three choices:

- **📱 Text their phone** (the right one): a text waits quietly until they're ready.
- **☎️ Call the room phone**: a sleepy "Is it breakfast?" The room phone rings by the bed.
- **✊ Knock anyway, softly**: "Mmmf. The sign… the sign says…"

Calling and knocking are gentle misses: a kind line explains why, and "Text" glows.
Then you pick the text itself on a phone screen. A kind, clear text that says who you are and
why ("Hi Ms. Vale! It's Housekeeping. Would you like fresh towels today? No rush…") gets a
warm reply, +3 tips, and the guest flips the sign off. "ARE YOU AWAKE?? 🚪🚪🚪" gets "I am now 😴",
and "hi" gets "…hi? Who is this?", each with a gentle hint. Then **Head in** knocks normally.

## Phone numbers and check-in

Story guests (202, 203, 204, 206) have fictional numbers on file, always with an area code
(for example (312) 555-0186). On the desk computer, the Guests tab shows **📱 Phone** for everyone,
and **✉️ Email** and **💳 Card on file** (masked, `•••• •••• •••• 4242`) for arrivals.

When you check a guest in on the desk computer (lesson 5 or exploring), the room is held and a
**🔑 Before the keys** card appears. Delores notes that every HMS looks a little different, but
most hotels check guests in this same way. Three things go on file, one tap each, with Delores
saying why after every right answer:

| Step | Right tap | Gentle misses |
| --- | --- | --- |
| 📱 Phone | “May I also have your area code?” | Save the 7 digits as they are; skip it |
| ✉️ Email | The address typed exactly | Two near-miss typos (read it back!) |
| 💳 Card | Check name and date, let the HMS hold it, hand it back | Copy it on a sticky note; skip it |

Only then does **🔑 Make the room keys** unlock. Keys come in a sleeve with the room number
written inside (never said out loud). Checked-in arrivals (Juniper Glow, Captain Barnaby Fuzz)
then live behind their door in the manor. Older saves that kept a number without an area code
are upgraded.

If that guest's door later says Do Not Disturb and there's **no number on file**, the phone
shows "No number on file" and Delores explains why we ask at check-in. You slide a kind note
under the door instead (+1 tip), and the sign comes off for the night. A guest checked in
without a number gets the sign more often, so the lesson comes up naturally.

## Pins

Knock Knock (knock on all six doors), Quiet Hands (text a Do Not Disturb guest kindly) and
Number, Please (save a phone number at check-in).

## Tests

`tests/test_knock.py` (run with `CHROMIUM_PATH=/opt/pw-browsers/chromium python tests/test_knock.py`).
