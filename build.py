#!/usr/bin/env python3
"""
build.py  -  Godiva Mindset Thumbnail 3.0 one-command build

Turns concepts_videoN.json into finished thumbnails with a single command.
It just runs the two real engine steps in order:

    1. render_nb2.py  --still <still> --concepts <json> --scene-only --crop
    2. finish_text.py --concepts <json>

Result: outputs/<name>_final.png for each concept.

Usage:
    python build.py --video 2
    python build.py --video 2 --count 6
    python build.py --video 2 --still stills/video2.png
    python build.py --concepts concepts_video2.json --still render-input/video2_still.png

Notes:
- Scene-only render + PIL text finishing is the locked path: NB2 makes the picture,
  finish_text.py stamps flawless font text. Per-concept "ghost": true is honored
  automatically by finish_text.py.
- Per-pose stills: render-input/videoN_<pose>.png is used for a concept when present,
  otherwise the single still is the fallback (see GESTURE_KIT.md).
- A render flake on one concept does not stop the others; rerun a miss individually.
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd):
    print("   $ " + " ".join(str(c) for c in cmd))
    return subprocess.run(cmd).returncode == 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", type=int, help="video number; defaults still+concepts by it")
    ap.add_argument("--concepts", help="path to concepts json (overrides --video default)")
    ap.add_argument("--still", help="path to the still (overrides --video default)")
    ap.add_argument("--no-crop", action="store_true", help="skip the 1280x720 center-crop")
    ap.add_argument("--count", type=int, default=4,
                    help="how many concepts to build (default 4, max 6)")
    args = ap.parse_args()

    if args.count < 1 or args.count > 6:
        ap.error("--count must be between 1 and 6 (4 is default; 6 is the distinct-concept ceiling)")

    if not args.concepts and args.video is None:
        ap.error("pass --video N or --concepts <path>")

    concepts = Path(args.concepts) if args.concepts else Path(f"concepts_video{args.video}.json")

    # Resolve the base still. Priority: explicit --still, then render-input/videoN_still.png,
    # then the canonical render-input/video1_still.png. The fallback is ANNOUNCED, never
    # silent, so you always know which face is being rendered.
    if args.still:
        still = Path(args.still)
    elif args.video is not None:
        named = Path(f"render-input/video{args.video}_still.png")
        canonical = Path("render-input/video1_still.png")
        if named.exists():
            still = named
        elif canonical.exists():
            still = canonical
            print(f"   NOTE: {named} not found. Using canonical still {canonical}. "
                  f"If video {args.video} has its own shoot, drop it at {named} first.")
        else:
            still = named  # fails the existence check below with a clear message
    else:
        still = Path("render-input/video1_still.png")

    if not concepts.exists():
        sys.exit(f"!! concepts file not found: {concepts}")
    if not still.exists():
        sys.exit(f"!! no still found. Drop your still at render-input/video{args.video}_still.png "
                 f"(or pass --still), then rerun.")
    print(f"   still: {still}")

    data = json.loads(concepts.read_text())
    if not isinstance(data, list) or not (1 <= len(data) <= 6):
        sys.exit(f"!! {concepts.name} must be a JSON array of 1 to 6 concepts.")
    if len(data) != args.count:
        print(f"   note: {concepts.name} has {len(data)} concepts; --count was {args.count}. "
              f"Building all {len(data)} in the file.")

    # Per-pose stills: if render-input/videoN_<pose>.png exists, that concept renders from it.
    # Otherwise everything falls back to the single still resolved above. This lets a gesture
    # kit (GESTURE_KIT.md) plug in without changing the command.
    pose_file = {"authority": "authority", "presenting": "presenting", "pointing": "pointing",
                 "open_palm": "openpalm", "considering": "considering"}

    def still_for(concept):
        if args.still or args.concepts and not args.video:
            return still  # explicit still wins
        if args.video is not None:
            tag = pose_file.get(concept.get("pose", ""), "")
            cand = Path(f"render-input/video{args.video}_{tag}.png") if tag else None
            if cand and cand.exists():
                return cand
        return still

    # 1) render all N scenes on NB2
    stills_used = {c.get("name", f"c{i}"): still_for(c) for i, c in enumerate(data)}
    multi_still = len(set(str(s) for s in stills_used.values())) > 1
    crop = [] if args.no_crop else ["--crop"]

    if multi_still:
        # different stills per concept: render one at a time with its matched still
        print(f"[1/2] Rendering {len(data)} scenes from {concepts.name} on NB2 (per-pose stills)")
        import json as _json
        for c in data:
            name = c.get("name", "concept")
            s = stills_used[name]
            single = Path(".build_tmp"); single.mkdir(exist_ok=True)
            jf = single / f"{name}.json"; jf.write_text(_json.dumps([c]))
            print(f"   - {name}  <- {s}")
            run([sys.executable, "render_nb2.py", "--still", str(s),
                 "--concepts", str(jf), "--scene-only"] + crop)
    else:
        # one still for all: fast single batch call
        print(f"[1/2] Rendering {len(data)} scenes from {concepts.name} on NB2")
        if not run([sys.executable, "render_nb2.py", "--still", str(still),
                    "--concepts", str(concepts), "--scene-only"] + crop):
            print("   render step reported a non-zero exit; continuing to finish.")

    # 2) stamp text on all N
    print(f"[2/2] Finishing text from {concepts.name}")
    if not run([sys.executable, "finish_text.py", "--concepts", str(concepts)]):
        sys.exit("!! finish step failed.")

    finals = [Path(f"outputs/{c.get('name','concept')}_final.png") for c in data]
    print("\n" + "=" * 52)
    done = [f for f in finals if f.exists()]
    print(f"DONE. {len(done)}/{len(data)} finished.")
    for f in finals:
        print(f"   {'ok ' if f.exists() else '-- '}{f}")
    print("=" * 52)


if __name__ == "__main__":
    main()
