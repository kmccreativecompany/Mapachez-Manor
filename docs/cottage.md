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
