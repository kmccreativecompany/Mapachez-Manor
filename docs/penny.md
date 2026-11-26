# PENNY v1: Penny Puffwing, the manor's money dragon

Penny is a kawaii baby dragon who keeps the manor's books: a big round head, curled ivory horns,
a soft dragon muzzle with nostrils, visible back spines, broad bat-shaped wings with finger bones,
a little plated belly, tiny claws, huge sparkly eyes, rosy blush, a heart-tipped tail, pink toe beans
and a little green banker's visor.
She does a happy hop every couple of seconds, with little hearts when she lands.
Dragons hoard gold; Penny hoards facts about the hotel business, and shares them one at a time.
She lives at the end of `index.html` (`PENNY v1` block), is drawn with code only, and saves to
`mapachez_penny_v1` on the device. Nothing is downloaded and nothing costs money to run.

## Where players meet her

| Where | What happens |
| --- | --- |
| The manor | Penny sits on a little coin pile by the archive cabinet. A gold "$" bubble bobs over her when she has a new fact tonight. Walk up and press E, tap her, or press **P** anywhere. She puffs a tiny smoke ring shaped like a percent sign when you say hello. |
| Title screen | "🐉 Penny has a shiny money fact for you · 0 / 21 →" |
| Sidebar | "🐉 Penny · n/21" button in the tip-jar row. |
| House ledger (L) | A "🐉 Penny's coin book" tab. |

## The money minute

Each visit shows one fact card (title, one or two sentences using the manor's own six rooms as the
example) and a 3-choice **coin check**. Right: +2 tips into the tip jar, a coin burst, and the fact
goes into the coin book. A miss shows the answer kindly and the same fact comes back next time.
Up to **3 new facts a night**, so there is always a reason to return; after that, and once every
fact is collected, Penny offers **quick reviews** of collected facts (+1 tip each).

Her personality shows only through what she says: delighted by numbers, a little dramatic about
her hoard, generous with it, and gently funny ("I tried to breathe fire once. A tiny smoke ring
came out, shaped like a percent sign.").

## The 21 facts (`PENNY_FACTS`)

Occupancy, ADR, RevPAR, rooms are like fresh bread, revenue vs profit, the biggest cost (the team),
booking-site commissions, happy guests come back, cost per occupied room, fixed costs, tips are
income ($20 a month reporting rule), tip vs service charge, the 2025 to 2028 tip deduction (up to
$25,000), the overtime "half" deduction (up to $12,500), walking a guest, dynamic pricing, the folio,
card holds, a kind upsell, longer stays, and comps.

Facts are written plainly and neutrally (no political framing) and the coin book says "General
facts for learning, not tax advice." When rules change, edit the fact text in `PENNY_FACTS`; the
first option in each list is the right one (they are shuffled on screen).

The bill's political nickname never appears anywhere in the game, in English or Spanish (a test checks).
Penny talks about rules by year ("a U.S. tax rule for 2025 to 2028"), never by bill name.

## Pins

First Coin (1 fact), Coin Purse (10), Penny's Apprentice (all 21), and the secret Smoke Ring
(visit Penny seven times).

## Tests

`tests/test_penny.py` (run with `CHROMIUM_PATH=/opt/pw-browsers/chromium python tests/test_penny.py`).
