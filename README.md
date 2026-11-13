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
