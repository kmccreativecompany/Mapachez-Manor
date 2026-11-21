# Mapáchez Manor
A cozy hotel game by Silver Key Games / KMC Creative Company.

## Play the prototype
Download index.html and open it in a modern browser. The game is a standalone HTML file with embedded assets and training.

For development:
```sh
python3 -m http.server 8000
```
Open http://localhost:8000.

## Integrated Silver Key practice desk

The current `index.html` combines the owner's latest walkable manor (including
the outdoor festival booths and Memory Book) with Silver Key hospitality
practice. Choose **Training desk**, press **T**, or open it at the front desk or
festival welcome desk. Return to the manor or festival from the practice window.
The world and training remain playable from one offline HTML file.

See [integration notes](docs/silver-key-integration.md) for saves, source files,
and browser regression checks.

## Procedural guests and family origins

Unscripted guests now receive deterministic combinations of body textures, eye counts, hair, ears, wings, tails and other features. Biological relatives can share a species origin through an explicit `familyId` and `familyRole: 'biological'`. Adopted relatives, partners, stepfamily and pets are not forced to share that origin. Ghost or robot spouses can be given the same internal origin through `heritageId`, without losing their distinctive appearance. These internal identifiers are not shown to players, and the existing fixed cast stays intact. See [NPC families and forms](docs/npc-families-and-forms.md).

## Mix-and-match character creator

Choose **Who are you?** on the title screen to make a character from independent pixel-art parts. The creator supports 1, 2 or 3 eyes, 1A through 4C hair textures, bald styles and head coverings, plus interchangeable ears, horns, antlers, antennae, wings, mermaid and animal tails, fur, feathers, scales, metal and ghostly appearances. Choose optional facial hair, one round glasses style (three frame colors), and one classic manual wheelchair for any character. The homepage includes a prominent **Character Creator** button. All selections update the front, side and back preview. Use **Surprise me** or **Save my look**. There are no required species categories.

Previous saved players keep their original look until saved again. The experience stays offline, and story characters remain unchanged. See [character creator notes](docs/mix-and-match-creator.md) for controls and limitations.

## Guest moments, growth bars and pins

After the briefing, a guest with a gold **!** waits in the manor. Walk over and
press **E** to answer a Silver Key moment. Answers fill the Guest trust, Care &
safety and Teamwork bars through Bronze, Silver, Gold, Silver Key and Legend.
Press **Q** (or choose **Quick shift**) for five guests in about three minutes.
Missed moments come back for a second chance, nights in a row build a streak,
and 40 pins plus unlockable outfits live in the Memory Book. See
[growth notes](docs/growth.md).

## Play for fun or train with your hotel

On the first visit the game asks how you are playing. **Just for fun** goes
straight to a first guest with no sign-up. **Training with my hotel** asks for a
name, a role (front desk, housekeeping, dining, night shift, or a bit of
everything) and an optional hotel pack from the manager. Players get a skills
report, printable certificates per role, and a score code for a friendly weekly
team board. Managers use the **Manager corner** to add their hotel name, house
rules and their own guest scenarios, then share them as a code or file. Spanish
is built in, and `python3 tools/build_demo.py` makes a free demo night copy.
Everything stays offline and on the device. See [setup notes](docs/setup.md).

## Rush hour, regulars, the lily mystery and surprise nights

From the third quick shift, **rush hour** sometimes brings three guests at once: choose
who to help first (safety first) while a gentle lantern counts down for a bonus pin, or
switch to relaxed with no timer. **Regulars** remember how you treated them and grow
four hearts, each unlocking a little story. A **mystery** (who keeps moving the lobby
lilies?) drops one clue a day, solved in the **Manor notebook**. **Surprise nights**
(storm, wedding, power cut) change the map and the guests three days in seven. Best
answers wiggle the raccoon and build a chiming combo. See [fun notes](docs/fun.md).

## Original repository baseline
Imported from the saved October 24, 2026 file:
cMapachez_Manor_Midnight_Rehearsal_Offline_anticipation.html

That initial import preserved the original game code. FIRST_TASK.md records the initial browser-verification assignment; the integration notes describe the current build and its regression checks.

## Agent setup
- AGENTS.md contains creative direction and working rules.
- FIRST_TASK.md contains the first bounded assignment.
- Select this repository when setting up a Codex Cloud environment.
- Ask the coding agent: "Read AGENTS.md and carry out FIRST_TASK.md."
- Review changes and test results before merging.

This repository does not itself start an agent or create a recurring schedule. A cloud environment and a launched task are still required.

## Clean comedy

Every guest moment (but one tender one) has a clearly silly extra choice and a
funny line from the guest when you get it right. Running gags unfold between
guests, Delores closes each quick shift with a one-liner, and a new comment card
arrives each day. See [comedy notes](docs/comedy.md).
