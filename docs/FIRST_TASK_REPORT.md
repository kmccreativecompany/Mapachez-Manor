# FIRST_TASK smoke-test report

Date: 2026-10-26. Baseline: `c2ebce9`. Review branch: `codex/first-task-smoke-test`.

## Environment and scope

The published managed cloud environment is attached, connected, and running (configuration revision 3). The clean checkout at `/workspace/Mapachez-Manor` has origin `https://github.com/kmccreativecompany/Mapachez-Manor.git`. Read `AGENTS.md` and `FIRST_TASK.md` before testing. No game source changes or bug fixes: no functional bug was confirmed in the tested flows. No merge, deployment, or additional assignment was performed.

Served the checkout with Python's static server at `http://127.0.0.1:8000`. Used installed system Chromium through Playwright, headless, with fresh nonpersistent browser contexts and no imported storage. Existing saves and the published Site were not touched. No project dependency installation was needed.

## Checks and results

- **Startup and movement:** Begin your night creates a playing save. Holding ArrowRight moves the player from approximately (260, 650) to (313, 650). Following the briefing task walks to the desk and opens dialogue. Numeric choice 1 accepts the briefing.
- **Complete evening:** Accept Lady Vesper's order; record her requirement in the ledger; obtain kitchen confirmation; select soup, cover, two spoons, napkin, water, and Room 203 ticket; inspect and pack; deliver at the doorway. Hear Ms. Vale's request, check the desk archive entry, retrieve AV-26, and return it with permission to play. Collect the used supper tray and return it to the kitchen. Meet Mr. Finch, read and record the property notice, and agree on the midnight rehearsal. Delegate the wet doorway to Pip, prepare the conservatory via the available route, invite Lady Vesper, deliberately wait for engineering, and confirm the repair. Read the finale, select handoff notes, and finish the shift. Result: `phase=ended`, supper and music loops closed, venue ready, hazard fixed, finale seen, handoff saved.
- **Menus:** House ledger guest search for 203 yields one matching guest; accessible-required room filter yields three rows. Shift journal contains the completed actions. Keyboard L and J open their menus; Escape closes dialogs. Places menu and quick travel navigate the tested destinations.
- **Settings:** Larger text updates the body styling. Quick travel and larger text persist across reload. Normal travel was tested for the initial briefing; quick travel was used for the complete evening.
- **Save/resume:** Reload during a briefed, in-progress evening exposes Continue and restores the same serialized state and three tasks. Return to title, then Begin with an existing playing save opens the replacement safeguard; Continue my saved evening preserves the state. Reload after finishing offers the ending and restores the same completed state.
- **Touch smoke test:** In a separate mobile context (390 x 844, touch enabled), tap Begin, tap the briefing task, travel to the desk, and tap the choice. Result: briefing completes and three guest tasks appear.
- **JavaScript:** Inline script passes `node --check`. No JavaScript page errors were captured during the completed desktop flow. Resume/keyboard/mobile checks also monitored page errors.

## Errors and limitations

No reproducible game error was observed in these flows. Browser launch initially targeted an absent Playwright bundled executable; using installed `/usr/bin/chromium` resolved the test-tool issue. Early automation attempts used incorrect or ambiguous button selectors; selectors were corrected to actual labels and scoped to the open modal before the complete run passed.

Direct `file:///workspace/Mapachez-Manor/index.html` navigation was attempted but failed with `net::ERR_BLOCKED_BY_ADMINISTRATOR`, before the game loaded. Thus direct-file offline execution remains unverified; this is an environment policy limitation, not a confirmed game bug. Local HTTP execution is verified. Audible sound/read-aloud quality, other browsers, every random clue, and alternate story branches were not verified. Mobile testing covers startup and briefing only, not the complete evening.

## Recommended next tasks (not started)

1. Verify direct-file offline play and save/resume in an owner-controlled browser.
2. Test the morning rehearsal and private-music branches.
3. Review keyboard-only navigation and read-aloud behavior with real audio output.
