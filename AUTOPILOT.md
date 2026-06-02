# AUTOPILOT.md
### Godiva Mindset — drop a still + a script, get thumbnails

The whole machine in one place. No paths to type, no naming rules, no overwrite guessing.

## The flow (this is the entire thing)

1. Drop ONE still image and ONE script (.txt or .md) into the `drop/` folder.
2. In Claude Code, say:  **autopilot**
3. Pick your winner from the finished thumbnails.

That's it.

## What `autopilot` does (Claude Code runs these, no stops)

1. `python ingest.py`
   Auto-numbers the video, moves the dropped still to `render-input/videoN_still.png`
   and the script to `scripts/videoN.txt`, backs up anything it would overwrite, and
   prints the video number N.
2. Read `GODIVA_THUMBNAIL_STYLE.md`, then `CONCEPT_ENGINE.md`, then `GESTURE_KIT.md`.
3. Read `scripts/videoN.txt`. Mine the specific numbers, documents, named entities, and
   emotional turn (RULE 0). Write `concepts_videoN.json` per CONCEPT_ENGINE.md: default 4
   concepts (up to 6 if asked), object 1 always `engineered_candid`, and satisfy the
   DIVERSITY MANDATE (>=3 framings, distinct components, varied expression; pose varies
   only if multiple stills were dropped, else hold pose and lean on the other axes).
   Run the self-check gate; fix anything that fails.
4. `python build.py --video N`
   Renders every concept scene-only + cropped on NB2 (matched pose still when present),
   stamps text, writes `outputs/<name>_final.png`.
5. Show the finals. Nominate a PRIMARY and an A/B CHALLENGER, one line each, rest in one
   line. James picks and ships.

## Re-running or refreshing a video

- Refresh video N with a new still/script: drop them, `python ingest.py --video N`.
- Concepts already written and you just want to build: `python ingest.py --video N --build`,
  or simply `python build.py --video N`.

## Stills

- The dropped still becomes that video's own `render-input/videoN_still.png`.
- If a video has no still, the build falls back to `render-input/_canonical_still.png`
  (announced, never silent). Dropping a still for one video never changes another's face.
- Gesture kit: drop extra stills named with a pose tag (pointing.png, presenting.png,
  authority.png, openpalm.png, considering.png) to activate per-pose rendering. See GESTURE_KIT.md.

## Preconditions
- `GEMINI_API_KEY` in `.env` (format `AQ.xxxx`).
- That is the only setup. Everything else is in the repo.
