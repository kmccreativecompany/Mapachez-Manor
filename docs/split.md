# Split view: the manor and the desk computer side by side

When the desk computer (HMS) opens during play, the manor stays on screen.

- **Computers and tablets (900px wide and up):** the manor sits on the left, the HMS on the right.
- **Phones:** the HMS slides up as a drawer over the bottom half, with the manor above. Tap the
  little gold handle to make the drawer taller, and again to show more manor.
- **Rooms react:** whatever room board the HMS shows (Browse records, lessons, Room Rush, Booking
  Builder, practice hotel), each manor room wears a matching badge: 🧹 dirty, 🔍 cleaned,
  ✨ ready, 🛌 guest, 🔧 fixing. Change a room and it reacts on the map (bubbles, sparkles,
  a key and hearts). The room you're looking at, or the one housekeeping is radioing about,
  glows gold, and the camera slides to it on small screens. The desk computer gets a soft ring.
- **Nothing removed:** every HMS screen, lesson, game and button is unchanged. Only where the
  window sits changed. From the title screen, and for every non-HMS window, the window stays
  centered as before.

Code: `SPLIT v1` block after `HMS FRIENDLY v1` in `index.html`. Tests: `tests/test_split.py`
(set `SPLIT_SHOTS=<folder>` to save screenshots).
