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
