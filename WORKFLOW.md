# Godiva Mindset — Script to Thumbnail Workflow (3.0)

The engine is `render_nb2.py` (Nano Banana 2). The concept brain is `CONCEPT_ENGINE.md`.
Text is stamped by `finish_text.py`. The old `godiva_thumbnail.py` / `--tier` / `--graphic`
path is retired; do not use it.

## Trigger
> `autopilot video N`   (optionally: `autopilot video N count 6`)

Preconditions:
- still at `render-input/videoN_still.png` (plus any `render-input/videoN_<pose>.png` gesture stills)
- script at `scripts/videoN.txt`
- `GEMINI_API_KEY` in `.env` (format `AQ.xxxx`)

If one of those files is genuinely missing, say which in one line and stop. Ask nothing else.

## The run (no stops)
1. Read `GODIVA_THUMBNAIL_STYLE.md`, then `CONCEPT_ENGINE.md` (and `GESTURE_KIT.md` for poses). Style master wins on visuals.
2. Read `scripts/videoN.txt`. Run the CONCEPT_ENGINE procedure:
   - Mine the specific numbers, documents, named entities, and emotional turn (RULE 0).
   - Build the concepts (default 4, up to 6 if James asked for a count). Object 1 is always `engineered_candid`; pick the other lanes to fit this script.
   - Run the self-check gate, including the DIVERSITY MANDATE; fix anything that fails.
3. Write `concepts_videoN.json` to the schema in `CONCEPT_ENGINE.md`
   (name, style, framing, pose, component, punch, main, sub, left, right, expression, ghost).
4. Run the build:
   ```
   python build.py --video N            # default 4
   python build.py --video N --count 6  # wider exploration
   ```
   Renders each scene-only + cropped on NB2 (matched pose still when present), then stamps
   text, producing `outputs/<name>_final.png` for each.
5. Show James the finals. Nominate PRIMARY and an A/B CHALLENGER with one line each, rest
   listed in one line. He picks and ships.

## Rules
- Default 4 concepts. Flexible 4 to 6 via build.py --count N (ceiling 6, where the axes run out of distinct combinations). Use 5-6 only when a video earns wider exploration.
- Specific artifacts from this script in every frame. No generic stand-ins.
- One hero element per zone. No duplicate hero prop across the set.
- Never alter James's face, beard, glasses, durag/beanie, chain, or shirt.
- No em dashes. No generic marketing phrases. Audience is "family," never "King."
- If text warps on a scene render, rerun that concept; the scene-only + finish_text path
  keeps text clean because it is font-rendered, not model-rendered.
