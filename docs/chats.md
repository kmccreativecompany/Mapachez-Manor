# Guest chats by the lobby chairs (CHATS v1)

Two guests sit by the lobby chairs and talk. Their speech bubble rotates through the first
three lines. Tap it (or walk over and press E) to listen. "Keep listening" shows the rest.

When you return to your evening, the last line stays a moment and the bubble fades. The two
guests turn and walk off in different directions, one west along the foyer and one south toward
the garden door, fading as they go. A toast says "The chairs are free" with how many chats you
have overheard. About 30 seconds later a new pair walks in and sits down. With reduced motion
there is no walking: the pair simply goes, and the next pair simply appears.

The code sits between `CHATS v1` markers at the end of the main script in `index.html`, with
styles marked `/* CHATS v1 */`. It replaces the old single fern conversation and reuses its
bubble, spot and Memory Book page (a chat with `memory:true` fills that page).

## The nineteen chats

Eighteen conversations are quick, relatable social jokes. One, the gold-sealed letter, is an optional mystery clue for the Memory Book. New players start with the marriage/sofa joke, then the workplace DNA-test joke. The older triangle/spoons conversation has been replaced, not merely hidden.

| id | Setup and punchline |
| --- | --- |
| blankets | A couple never goes to bed angry because their sofa is comfortable. |
| email | A boss says the staff is family, so an employee asks for a DNA test. |
| robot-terms | A robot spouse demands new terms and conditions before dinner. |
| bells | An older guest doesn't care what people think, except Margaret. |
| toast | Following a dream means becoming a professional napper. |
| beta-romance | A perfect boyfriend is still in beta testing. |
| time | A wealthy guest hasn't shopped for groceries since 1998. |
| sunday | A newly promoted director's responsibilities are still being aligned. |
| counselor-conspiracy | An AI marriage counselor agrees with the second opinion. |
| inbox | A private person makes seven videos announcing her privacy. |
| romance-update | A romantic spouse asks for a review after an update. |
| circle | Gossip is rebranded as distributing family updates. |
| photo | Money cannot buy happiness, but can fund crying on a yacht. |
| subscription-marriage | A quiet marriage is explained by a canceled subscription. |
| tuesday | An astrologically cautious date cancels because Mercury objects. |
| duchess | A pet influencer gets famous by napping. |
| wifi-ex | An ex cannot reconnect after a Wi-Fi password change. |
| letter | Optional story clue: an envelope addressed to Lady Vesper with two identical musical notes. |

The recurring guest name, character recipe and chat ID are preserved where practical. The letter still has `memory:true` and unlocks the existing Memory Book story page. The romantic robot cast is pinned to the same machine-built kind; the Calder spouses are pinned to the same human kind.

Each comedy conversation ends with a clearly labeled **Butler thought** reaction. The jokes are authored offline in English and Spanish. The reveal is the last dialogue line, so the punchline is understandable without having read earlier lore.

## AI relationship jokes and thought bubbles

Six AI-related jokes join twelve new socially relatable scenes about marriage, wealth, family gossip, workplace culture, astrology and online life. They are mixed through the lobby rotation and finish with an italic **Butler thought** bubble. Both English and Spanish are authored in the game, offline, with no AI service or network call.

Ada Rowan and Mira Moon use a consistent machine-built character look in the existing pixel-art cast. The robot-husband storyline depicts a robot married to another robot, not an inter-species marriage. No new inter-species marriages are introduced. The AI jokes concern fictional character relationships rather than player relationship mechanics.

Players with existing `mapachez_chats_v1` saves keep their previously heard conversation IDs and continue from their current saved rotation number. The All Ears pin now requires all nineteen chats.

## Tired little goodbyes

When a pair gets up to leave, one of them says why they have to go, in the toast:
"Zinnia Starling, getting up: “Sorry, I have a video meeting that really could have been an email.”"
Twelve goodbyes rotate (`byes` in `CHATS_TEXT`), and the two guests take turns saying them.
The count is saved as `bye`.

## Writing rules

- Fast setup, plain-language exchange and unmistakable punchline on the last line.
- Prefer observational humor about universal experiences over inside jokes. Only the letter is intentionally a mystery clue.
- Laugh with people, never at them. Hidden stories are hinted, never told. Nobody's kind of
  being is named (no "vampire", "alien", "monster"), and Muffin is only ever a cat.
- Lines stay under 70 characters so bubbles fit on phones. The first three lines are the teaser.

## Names

Guests and staff come from everywhere, with ordinary first and last names mixed in casually.
A name never comes with an accent, a joke or a cultural line about it, and nobody's kind of being
is tied to where a name is from (kinds still come at random from the name, as everywhere else).
The training cards that used to show only a job title now show a person too, with the job kept
at the front of their note: Tomás Ferreira (maintenance lead), Aiko Tanaka (new hire), Kwame
Mensah (driver), Ingrid Halvorsen (event planner), Priya Raman, Rosa Delgado, Aroha Ngata,
Femi Adeyemi and the Nguyen family.

## Editing and translating

All words live in `CHATS_TEXT.en` and `CHATS_TEXT.es`, with matching ids and speakers. Each chat
has `a` and `b` (a `cast` name keeps a guest's look the same as elsewhere), `lines` as
`[speaker, text]`, an optional `stage` line shown after the teaser, an `end` line and for jokes a `thought` reaction.

## Saving

`mapachez_chats_v1` on the device: `next` (which pair is in the chairs), `heard` (chat ids) and `bye` (which goodbye is next).
Hearing the letter chat still sets the evening's old fern flag for the Memory Book page. Hearing any chat
earns A Listening Ear; hearing all nineteen earns the All Ears pin (anyone who
already earned it keeps it).

## Checks

```sh
python tests/test_chats.py
```
