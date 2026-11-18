# Joy: sparkle-and-pop feedback, gift boxes and the mystery guest

This layer sits between the `JOY v1` markers at the end of `index.html`'s script. Its styles
are added by the same block. Every word is written ahead of time (English and Spanish), all
graphics are drawn with code (canvas pixels and CSS), and every sound is made with Web Audio.
Nothing is downloaded and nothing costs money to run.

The rule behind every reward: it grows out of real hotel skills. Best answers earn tips, good
quick shifts earn gift boxes, and finished shifts unfold the mystery guest's story.

## What players see

- **Sparkle and pop on every answer.** A reward strip appears above the verdict: your own
  character hops (happy ^ ^ face for raccoons), sparkles and a ring burst out of the verdict,
  gold coins fly into the tip counter with a rising "ding" each, and the tip jar fills.
  Combos grow the burst, add hearts at ×2 and rainbow sparkles at ×5, float a word ("Nice!",
  "Sparkle streak!", "On a roll!"…) and give the dialog a soft gold glow from ×3. A close
  answer gets a small nod; a miss gets a gentle sway and "Best answers earn tips." Answer
  buttons lift on hover and squish when pressed.
- **Tips.** A best answer is worth 3 tips plus 1 for each step of the combo (up to +3). A close
  answer is worth 1. Nothing is ever taken away.
- **The tip jar.** Every 40 tips fills the jar and drops a gift box.
- **Gift boxes.** A quick shift with 3 or more best answers earns one; a perfect shift earns one
  with better odds. The box hints at its rarity (pink: lovely, blue glow: rare, gold rays:
  super rare). Tap it three times: it shakes harder with a rising note each tap, then bursts
  open with sparkles, confetti and a chord. The gift tag thanks you for a skill you showed in
  the shift (for example "for your allergy awareness"). Reduce motion opens it in one tap.
- **19 gift treasures, no duplicates until you have them all:** 12 outfits drawn in pixels on
  your character (pink bow, little sprout, painter's beret, party hat, daisy crown, chef's
  toque, tiny top hat, star wizard hat, shooting star clip, golden crown, firefly halo, moon
  circlet) and 7 treasures (a peppermint, a luggage tag, raccoon soap, a postcard, a snow globe,
  a warm teacup, and the super rare manor music box that plays a lullaby).
- **The closet** (🎀 in the sidebar) shows you wearing your outfit, every outfit and treasure,
  and "?" cards with their rarity for what is still out there. The outfit is drawn on your
  character in the manor too and follows every step and hop.
- **The mystery guest.** One guest checks in on a new day: a shy fluffy monster, a three-eyed
  postcard writer, an elegant lady with a second teacup, a tiny gentleman who loves the pond,
  a robot with a suitcase of pencils, or a moth-winged guest with a chirping suitcase. Their
  story has four parts. Part 1 arrives with them; each finished quick shift (or 5 guests helped
  in the manor) unlocks the next. Players guess the secret early; a right guess earns a bonus
  gift box. The last part reveals the secret, a Silver Key lesson and a keepsake. The guest
  walks the manor with a purple "?" and opens their case file when visited. Unfinished stories
  wait kindly: a new guest only arrives once the last one's story is finished.
- **Title screen:** "A mystery guest checked in tonight" and "🎁 gift waiting" buttons.
- **Seven pins:** Unwrapped, Full Jar, Dressed Up, Secret Keeper, Good Instincts, Collector
  and the secret Lucky Paws (a super rare gift).

## Saves

`mapachez_joy_v1` holds tips, jar, gifts waiting, owned items, the outfit being worn and the
mystery guest's progress. Other saves keep their formats. A missing or corrupt joy save starts
fresh.

## Writing

All words are in `JOY_TEXT`, `GIFTS` and `MG_GUESTS` (each with `en` and `es`). Follow the
`docs/heart.md` voice: gentle, kind, a little dreamy, never gloomy. Show traits through what
guests do. No room numbers.

## Checks

```sh
python tests/test_joy.py
```

Covers the reward strip, tips and combo, sparkles appearing, a good and a weak shift, opening a
gift in three taps, no duplicates across all 12 outfits, wearing an outfit, the tip jar gift,
the mystery guest's guess and four parts over three shifts (with a rush hour in between), the
guest on the map, one-tap opening under reduce motion, and the reward strip on a 390-pixel
phone.
