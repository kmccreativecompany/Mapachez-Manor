# Silver Key practice inside the walkable manor

The integration uses the owner's `Mapachez_Manor_Latest.html` upload as the world
baseline. It includes the Yaupon Silent Sessions outdoor map, creator booths,
stage and soundchecks, local performer previews, Memory Book, lobby conversation,
and the existing Midnight Rehearsal story. It supersedes the older October 24
world that was on the repository's main branch.

Silver Key comes from the owner's `silver-key-hospitality-training-game-v3 (11).html`
upload. Its 52 scenario moments, 23 guest records, 13 staff profiles, 195 glossary
entries, seven career ranks, role selections, HMS lab, overnight board, drills,
wine-service and investor exercises are embedded into the world.

## Playing

Download **index.html** and open it in a modern browser. This remains a single
offline HTML game; no server, account, API key, paid service, or network request is
required for the game or training. Existing optional external artist links still
open only when the player chooses them.

Open **Training desk** on the title screen or in the game header, press **T**,
choose **Practice at the Silver Key desk** at the front desk after the briefing,
or visit the **festival welcome desk**. The practice desk includes shortcuts to
training shifts, training guest records, the HMS lab, night desk, and glossary.
Use **Return to the manor/festival**, the close button, or Escape from the main
training view to resume exploring. Escape first dismisses an open training dialog
or HMS panel. Training does not advance the story clock or change its inventory,
guest requests, Memory Book, or progress. Festival music pauses when training opens
and can be resumed explicitly afterward.

## Saves and feedback

- The original manor save, Memory Book, festival customizations, and comfort keys
  retain their names and formats. The original save version remains 2.
- Training retains its existing Career XP, comfort, and overnight-board keys.
- `mapachez_silver_key_active_shift_v1` stores an unfinished scenario shift,
  including role, moment, scores, streaks, original answer indices, and a shuffle
  seed. A previously answered moment restores its coaching without awarding XP
  again. Completed shifts bank their career result once and clear the active save.
- Answer positions vary across moments and remain stable when a saved shift is
  reopened. Feedback still refers to the correct original answer.
- Saves are local to the browser and origin/file location. This integration does
  not synchronize different browsers or import saves from unrelated file origins.
- The unfinished-shift save covers the 52-moment scenario sequence. Standalone
  practice drills and investor exercises retain their existing reset behavior;
  the overnight board and banked career totals persist separately.

The training guest roster is explicitly a practice roster. Existing story guest
names and identities remain unchanged. The five service roles share the source
scenario sequence with role framing; Investor retains its separate exercises.
These are not six newly authored campaigns.

Guest portraits supplied in the earlier v17 upload are reused unchanged. Records
whose linked images were not included in the uploads use initials cards. No
missing image files are required to play. Unmatched layout tags in the training
source are repaired, and phone layouts provide collapsible career/comfort controls.

## Source and verification

`training/silver-key.html` is the readable training source. `index.html` embeds
that exact file in a separate iframe document to keep its styles, controls,
storage, and keyboard handling from colliding with the walkable world. The
world's existing native dialog pauses movement, and a source-checked message
bridge handles shortcuts, progress display, and returning to the world.

After changing the training source, run:

```sh
python tools/embed_training.py
```

No build step is needed to play the committed index.html. Do not replace the
manor with the training source file.

Run the browser regressions using an installed Python Playwright and Chromium:

```sh
python tests/test_training_integration.py
```

Set `CHROMIUM_PATH` if Chromium is not at `/usr/bin/chromium`. Tests use isolated
storage and block external requests. Coverage includes walking, paused story
state, festival location and creator favorites, both in-world entry points,
answered and unanswered moment restoration, all 52 rounds and shuffled feedback,
one-time career awards, overnight-board persistence, mobile sizing, Escape,
corrupt-save recovery, and the first story order after returning from training.

## Verification result

Eight browser regression tests pass in Chromium, using a local HTTP origin with
external requests blocked and fresh storage. The suite completes all 52 training
moments, exercises desktop and 390-pixel phone controls, and checks the original
festival and first story interaction. JavaScript syntax checks pass for both
documents. The embedded training matches its readable source byte for byte, and
the latest manor's original embedded artwork is unchanged.

The browser environment blocks direct `file://` navigation, so automated browser
checks used the local HTTP origin. The shipped artifact is still a self-contained
HTML file. This verification does not claim a complete playthrough of every
Midnight Rehearsal ending, every standalone drill, or every browser platform.
