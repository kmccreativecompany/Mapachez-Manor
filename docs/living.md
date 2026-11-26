# The living manor: routines, Manor Radio and little surprises

Three small things that make the manor feel alive and give players a reason to come back.
Everything is written ahead of time and drawn with code: no pictures, no network, no cost.
They open after the player's first finished shift, so night one stays simple.

## 1. Daily routines
Eight guests each keep a little routine at their own time of the player's real day.
A different guest is up to something every three hours, so coming back later shows someone new.

| Time | Who | Where | Routine |
| --- | --- | --- | --- |
| 12 AM | Mr. Finch | Conservatory (piano) | The midnight cello |
| 3 AM | Lady Vesper | Guest corridor | Counting the windows |
| 6 AM | Ms. Vale | Conservatory (piano) | A song for the sunrise |
| 9 AM | M. Nine | Kitchen | The four-minute kettle |
| 12 PM | Ms. Butterfield | Conservatory | Lunch with the spoons |
| 3 PM | Mr. Lindqvist (ghost) | Guest corridor | The elevator, again |
| 6 PM | Dr. Merriweather | Kitchen | The sunset cocktail (no garlic anywhere nearby) |
| 9 PM | Ms. Eze (ghost) | Kitchen | Tea at nine |

- Tap the guest for a short sitcom exchange. The player speaks to guests in full, polite sentences (see `service-language.md`).
- The first time a routine is spotted: +2 tips. A card shows "The manor's day": spotted routines by name, unseen ones only as "Someone in the kitchen", and which one is on now.
- Pin: **Clockwork Manor** (spot all eight).

## 2. Manor Radio
A little Art Nouveau radio in the kitchen, with notes floating out of it.

- The first listen each night is a five-star review about the player (by first name when they gave one): +2 tips.
- Then it alternates pretend ads (Odd Pair socks, Plain Toast, the Polite Toaster...) and five-star guest reviews. All gentle, laughing with people, no brand names, rooms 201 to 206 only.
- Pin: **Loyal Listener** (hear twelve segments).

## 3. Little surprises
After about 40 seconds in the manor, and then every few minutes of play, a gold "!" appears with a toast saying where. At most three a day, new ones before repeats.

Eight surprises: the minibar heist (two tiny garden raccoons), a surprise wedding party, eleven pizzas for Room 207, a duck checks in, Muffin takes the elevator, Delores's surprise party, the floating suitcase and a guest snoring like a tiny trumpet.

Each one is a quick, kind service choice with a real lesson (never charge a guest for what they did not use, never share a room number, reunite a pet with its owner, give a real time). Best answer +3 tips, good answer +1. Pin: **Expect the Unexpected** (handle all eight).

## Code and saves
- `index.html`: the `LIVING MANOR v1` block near the end of the script (`LIV_TEXT` holds every English and Spanish line).
- Save key `mapachez_living_v1` (routines spotted, radio progress, surprises done, today's count).
- Tests: `tests/test_living.py`.
