# Mapáchez Manor agent instructions

## Project
Mapáchez Manor is a cozy hotel game by Silver Key Games / KMC Creative Company.
The starting prototype is index.html, imported from the owner's saved October 24, 2026 Midnight Rehearsal HTML. Treat it as a baseline, not proof there are no newer versions.

## Creative direction
- Cozy, beautiful, peaceful, whimsical atmosphere with dramatic and funny misdirection. Avoid turning the game into horror.
- Preserve the six-room concept with guests rotating over time. This is design direction, not a claim all systems are implemented.
- Reveal unusual character traits through behavior. Do not explicitly label or spoil secret identities in player-facing titles, UI, or narration.
- Preserve the elderly guest and her opossum she calls her cat when present. Do not replace established characters or invent canon without a specific task.
- Keep dialogue emotionally intelligent and funny without cruelty.
- Keep keyboard, touch, readable text, and optional read-aloud accessibility in mind.

## Working rules
- Read existing code and reproduce an issue before changing it.
- Complete one bounded assigned task. Do not autonomously expand into a redesign or an endless backlog.
- Keep the single-file offline experience unless the owner explicitly requests a migration.
- Preserve embedded assets, saved-game compatibility, and unrelated behavior.
- Use fictional guest data only. Do not add real hotel guest information or credentials.
- Do not add paid services, analytics, external dependencies, publishing, or deployment without a task that calls for them.
- Make work reviewable on a separate branch or pull request. Do not merge automatically.
- Run checks appropriate to the change; never claim browser testing if only syntax was checked.
- Report what changed, reproduction steps, checks run, and remaining limitations.

## Running and checking
Open index.html directly in a modern browser for offline testing.
For local browser automation, serve the repository with:
python3 -m http.server 8000
Then open http://localhost:8000.
No package installation or build step is required for the imported prototype.
Use a fresh test browser profile or isolated storage to protect existing saves.
