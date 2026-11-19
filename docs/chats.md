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

## The thirteen chats

| id | Pair | Joke engine |
| --- | --- | --- |
| letter | Zinnia Starling, Sunny Marrow | A secret letter for Lady Vesper, signed with one note drawn twice. Callback to Mr. Finch's one-note triangle. |
| bells | Gwendolyn Butterfield, Mr. Finch | Spoons, bells, one triangle. Her next obsession is set up last. |
| time | Ms. Chen, Dr. Merriweather | One has nine minutes, one has "centuries. I mean weeks." |
| muffin | Cece Wrenwood, Basil Thorne | Muffin and Admiral both play asleep. "Two professionals." |
| blankets | Mrs. and Mr. Calder | Forty years: patience, kindness, separate blankets. |
| tuesday | Mr. Alvarez, M. Nine | A delayed flight vs. a trip "through Tuesday. Twice." |
| duchess | Pippa, Lavinia Bloom | Is Duchess a real duchess? Callback to Miso's crown drawing. |
| email | Ms. Chen, Dr. Merriweather | A video meeting that could have been an email. Her day: one meeting that ran a century. |
| toast | Mr. Alvarez, Sione Taufa | Spread thin, like a little jam on very big toast. Said yes to four things; wanted one nap. |
| sunday | Zanele Dlamini, Arjun Mehta | The Sunday-night feeling, felt in horns and wings. Don't say Monday's name. |
| inbox | Ji-woo Park, Camila Rojas | Three thousand unread messages. Out-of-office: "Back soon. Stars permitting." |
| photo | Bramble Knox, Amara Diallo | Nobody eats until the photo is right. His day off "is also a review." (He writes about food; it is never said, only shown.) |
| circle | Basil Thorne, Noah Tremblay | "Quick questions" that take an hour, and circling back that never comes back. |

The five work-life chats (email, toast, sunday, inbox, circle) are spread through the rotation, so a
new player meets "Could have been an email" second. They are for tired workers to feel seen: the
guests are tired too, and they are kind about it. Nobody's boss, job or company is mocked by name.

## Tired little goodbyes

When a pair gets up to leave, one of them says why they have to go, in the toast:
"Zinnia Starling, getting up: “Sorry, I have a video meeting that really could have been an email.”"
Twelve goodbyes rotate (`byes` in `CHATS_TEXT`), and the two guests take turns saying them.
The count is saved as `bye`.

## Writing rules

- Rule of three, the funny word last, specific details, one small misdirection.
- Jokes come from who guests already are (callbacks to regulars, gags and guest moments).
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
`[speaker, text]`, an optional `stage` line shown after the teaser, and an `end` line.

## Saving

`mapachez_chats_v1` on the device: `next` (which pair is in the chairs), `heard` (chat ids) and `bye` (which goodbye is next).
Hearing the letter chat still sets the evening's old fern flag for the Memory Book page. Hearing any chat
earns A Listening Ear; hearing all thirteen earns the All Ears pin (anyone who
already earned it keeps it).

## Checks

```sh
python tests/test_chats.py
```
