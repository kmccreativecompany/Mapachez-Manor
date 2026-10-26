# First cloud agent task

Inspect index.html and establish whether the prototype can be run and tested in this environment.

1. Start a local static server and launch a browser if browser tools are available.
2. Smoke-test starting a new game, movement, guest interactions, task progression, menus, settings, and save/resume where implemented.
3. Record any reproducible errors with exact steps and observed behavior.
4. Fix at most one confirmed, small functional bug. If no bug is confirmed, return the test report without speculative changes.
5. Re-test the affected flow and check for JavaScript errors.
6. Leave changes on a separate branch or pull request for the owner to review.

Follow AGENTS.md. Preserve the art, dialogue, character secrets, and existing gameplay. Do not redesign the game, deploy it, or merge changes.
If a required tool or access is missing, explain the blocker. Do not claim checks passed without running them.

Deliver a short summary of what works, the bug fixed (if any), verification performed, and up to three recommended next tasks.
