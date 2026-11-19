# Cottage: spend your tips on your own little staff cottage

This layer sits between the `COTTAGE v1` markers at the end of `index.html`'s script. Like every
other layer, it is drawn with code, every word is written ahead of time (English and Spanish),
sounds are made with Web Audio, and nothing is downloaded or costs money to run.

## The idea in one line

Good work earns tips. Tips buy cosy things for your own cottage on the manor grounds.

## Earning tips (already in the game, unchanged)

- A best answer to a guest: 3 tips, plus 1 for each step of a combo (up to +3). A close answer: 1.
- Desk computer games and lessons (HMS), and peeking in the HMS before answering.
- Penny's coin checks: 2 for a new fact, 1 for a review.
- A gift box when you already own every gift: 15 tips.

The tip jar still fills from everything you **earn**. Spending tips never empties the jar, so
buying things for the cottage never slows down a gift box.

## Spending tips

`joy.tips` is now the player's wallet: buying something takes its price off. The sidebar, the
reward strip and the closet all show what is left to spend.

18 things, cheapest first (1,535 tips in all). The lamp costs 10, about one good quick shift.

| Thing | Tips | What it does when tapped |
| --- | --- | --- |
| Mushroom lamp | 10 | Turns its warm glow on and off |
| Round rag rug | 15 | Says its little line |
| Fern in a teacup | 20 | Sways gently |
| Patchwork quilt | 25 | Replaces the plain blanket |
| Lace curtains | 30 | |
| Tea table and teapot | 35 | Steam rises, the teapot hums |
| Little bookshelf | 45 | |
| Painting of the manor | 50 | |
| Squishy armchair | 60 | |
| Fairy lights | 70 | Twinkle |
| Goldfish in a bowl | 80 | Bubbles, "Blub." |
| Record player | 95 | Plays a sleepy tune (secret pin) |
| Cushion for Muffin | 110 | Muffin naps on it, very privately |
| Stone fireplace | 130 | Crackles and sparks |
| Brass telescope | 150 | A shooting star crosses the window |
| Cuckoo clock | 170 | A tiny raccoon pops out |
| Starry wallpaper | 200 | Turns the walls into a night sky |
| Tiny chandelier | 240 | Tinkles |

Players can buy any thing they can afford, not only the next one. A moving box marked STUFF
sits on the floor until the fourth thing arrives.

## What keeps people coming back

- **A goal you can always see.** "Next for your cottage" shows the cheapest thing still missing,
  a fill bar and "8 more tips". When it is affordable the card glows and a big "Buy it" button
  appears.
- **A nudge at the right moment.** When a best answer pushes the wallet past a price, the result
  card says "Enough tips for the Mushroom lamp!" (during a quick shift it says to spend them
  after the shift, so the shift is never interrupted). Tips from the desk computer and Penny show
  a short toast instead.
- **The pop.** Buying makes the thing bounce into the room with sparkles, hearts and a chime.
- **Coziness hearts.** Five levels: Bare and hopeful, A little lived-in (1), Getting cozy (4),
  Snug as a sock (9), Very, very snug (14), The coziest cottage on the grounds (18).
- **Visitors.** Delores drops by with a housewarming pie at 2 things, Penny Puffwing at 6.
  Once both have visited, one of them comes by each day. Tap them for another line.
- **Four pins:** Home Sweet Home (1 thing), Snug as a Sock (9), Coziest Cottage (all 18) and the
  secret Tiny Concert (play the record player).

## Rules it follows

- The window shows only the night sky and the manor across the lawn. Weather stays outdoors.
- Muffin is "a very private cat". Nothing says what else she might be.
- Clean, gentle comedy and the `docs/heart.md` voice.
- Reduce motion: the room is drawn once (no loop), no bouncing or glowing cards; taps still answer.

## Ways in

Title screen button, the 🏡 Cottage button in the sidebar (it glows when something is
affordable), "Your cottage" under the map, and the C key.

## Saves

`mapachez_cottage_v1` holds the things owned, tips spent, visits, the lamp switch, visitors met and
record plays. Tips themselves stay in `mapachez_joy_v1`. A missing or broken cottage save starts
fresh; unknown things are dropped.

## Checks

```sh
python tests/test_cottage.py
```

---

# Cottage v2: Staff Lane, rides, raises and a dream house

The cottage now gives every shift a purpose: good work earns tips and raises your pay, tips buy
things, and the big dreams (the flying car, your own house) are always on screen to chase.
The cottage screen has four tabs: **Inside**, **Rides**, **Cottages** and **Dream house**.

## Living on the grounds is a choice

The first visit shows Staff Lane and asks "Would you like to live on the grounds?" Players can
pick a cottage or say "Not now, I live in town". Town players still get rides and the dream
house, and can move in any time. Saves from v1 that already furnished a cottage simply live there.

## Four cottages on Staff Lane (free, move any time)

The Toadstool, The Little Lighthouse, The Treehouse and The Seashell. Each has its own outside
drawing and its own colours inside (walls, panelling and floor). Your things move with you.

## Rides (9)

Bought with tips in the Rides tab. The ride you choose is drawn under you as you walk the manor
and the festival grounds, and changes how fast you move (`world.options.speed`, a one-line hook in
the walking code).

| Ride | Tips | Speed |
| --- | --- | --- |
| Skateboard | 30 | 1.3x |
| Kick scooter | 45 | 1.4x |
| Bike with a basket | 60 | 1.55x |
| Giant snail | 75 | 0.75x (the slowest ride on the island; everyone waves) |
| Manor golf cart | 100 | 1.6x |
| Flying broom | 130 | 1.75x, flies |
| Magic carpet | 160 | 1.75x, flies |
| Flying teacup | 200 | 1.7x, flies |
| Flying car | 280 | 2x, flies |

"Walk instead" puts the ride away.

## Raises

Your pay grade comes from your Silver Key skill points (the three growth bars). Every best
answer earns the usual tips plus a raise bonus, shown as a green "+2 raise" chip.

| Grade | Skill points | Extra tips per best answer |
| --- | --- | --- |
| New night host | 0 | 0 |
| Trusted host | 80 | +1 |
| Senior host | 220 | +2 |
| Night lead | 450 | +3 |
| Silver Key host | 800 | +4 |

A new grade pops a "You got a raise!" celebration with a note from Delores. The pay card on the
Inside, Rides and Dream house tabs shows the current grade and how far the next raise is.

## The dream house: Willowbrook House

A sleepy old fixer-upper at the end of Staff Lane, for sale to staff for 500 tips. After buying
it, eight projects wake it up one at a time, each drawn on the house: wash the windows (60), a new
front door (80), a white picket fence (90), mend the porch (100), fix the roof (120), paint the
house (150), plant a garden (170) and a porch swing (200). When all eight are done, players can
live there; it becomes a fifth home with soft blue walls inside.

Nothing ever breaks again and there is no upkeep: every project only makes the house lovelier.

## New pins

Wheels, Sky High, Whole Garage, Slow and Steady (secret), First Raise, Homeowner, Labour of Love.

## Saves

Still `mapachez_cottage_v1`, with new fields `live`, `home`, `rides`, `ride`, `snail`, `grade` and
`house`. Unknown values are dropped.
