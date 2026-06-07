# GO_LIVE — the bulletproof per-video workflow

The factory has two environments that CANNOT talk to each other:
- **Chat assistant** (claude.ai): great at reading any file, generating concepts. Cannot reach Gemini/Envato.
- **Claude Code** (local): reaches Gemini NB2 + Envato MCP, renders. Bad at reading messy files; inline images do NOT land on disk.

So split the work by strength. **Chat reads and thinks. Claude Code renders.**

## The flow (do this every video)
1. **In CHAT**, upload TWO real file attachments:
   - the still image (a real file, NOT pasted inline — inline never lands on disk)
   - the script (any format: .txt, .docx, the exported "pdf" bundle, anything)
2. **Chat** extracts the script, generates `concepts_<video>.json`, commits the cleaned
   `scripts/<video>.txt`, the concepts, and the still as `render-input/<video>_still.png`,
   and pushes to the repo.
3. **In CLAUDE CODE**, two commands only:
   ```
   git pull
   python build.py --concepts concepts_<video>.json
   ```
   (or the scene-only + finish_text pair). Claude Code does NOT read scripts or invent
   concepts. Everything it needs is already on disk.
4. Pick the winner from the finished renders. Ship.

## Why this kills the recurring failures
- **Inline still never lands** -> chat pushes the still to render-input/ as a real file; `git pull` puts it on disk. No inline dependency.
- **Script won't parse** -> chat reads it (and `read_script.py` handles the zip-bundle/docx/pdf cases on either side). Claude Code never parses a raw script again.
- **Concept struggle** -> concepts are already written and pushed before Claude Code runs.

## Preflight (Claude Code refuses to flail)
Before rendering, confirm:
- `render-input/<video>_still.png` exists and is a real image (not 0 bytes).
- `concepts_<video>.json` exists.
If either is missing, STOP and say exactly which one, do not try to extract or invent it.

## read_script.py
`python read_script.py <file>` extracts script text from .txt/.md, .docx, the exported
"pdf" zip bundle (page images + N.txt inside), or a real text-layer PDF. Use it if a raw
script ever lands in either environment.

## THE FACE RULE (non-negotiable, learned the hard way)
A full set of renders came back with the WRONG FACE because the base still was an
AI face-swap (make_identity_still.py) and a two-photo identity merge. NB2 preserves a
real face but INVENTS a generic one whenever asked to swap or merge faces.

- The base still is ALWAYS one real, untouched photo of James's actual face, in the outfit
  he actually filmed in. Pull a real frame from the footage.
- NEVER use make_identity_still.py or the --identity two-photo merge to manufacture a face.
- NB2's job is only to rebuild the background and add props AROUND his real face.
- If a render comes back not looking like him, the base still is the problem, not the prompt.

## FACE LIBRARY (render-input/library/)
A set of real, clean, front-facing frames of James across looks. Use it to PICK the single
best base still per video, the clearest, most front-facing frame, or one whose outfit fits.
NEVER merge two of these into one render (merging invents a wrong face). One frame in, per render.
`face_navy_dog_tee.png` is the current canonical, cleanest front-facing face lock.
