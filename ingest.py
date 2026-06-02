#!/usr/bin/env python3
"""
ingest.py - drop a still + a script, get them placed for a build.

THE FLOW:
  1. Put ONE still image and ONE script (.txt or .md) into the  drop/  folder.
  2. Run:  python ingest.py
  3. It figures out the next video number, places the files where the engine
     expects them, backs up anything it would overwrite, and tells you the one
     next step.

No paths to type, no naming rules to remember. Everything is relative to the
repo, so it works the same on any machine and inside Claude Code.

OPTIONS:
  python ingest.py                 auto-pick the next video number
  python ingest.py --video 1       force the number (use 1 to refresh video 1)
  python ingest.py --video 1 --build   place files AND build if concepts exist

MULTIPLE STILLS (gesture kit): name a dropped image with a pose tag and it lands
as a pose still, e.g. drop/pointing.png -> render-input/videoN_pointing.png.
A plain image becomes the base render-input/videoN_still.png. Pose tags:
authority, presenting, pointing, openpalm, considering.
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

DROP = Path("drop")
RENDER_IN = Path("render-input")
SCRIPTS = Path("scripts")
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}
TXT_EXT = {".txt", ".md"}
POSE_TAGS = {"authority", "presenting", "pointing", "openpalm", "considering"}


def backup_if_exists(target: Path):
    """Never silently clobber. Move an existing target to *.prev and announce."""
    if target.exists():
        prev = target.with_suffix(target.suffix + ".prev")
        shutil.move(str(target), str(prev))
        print(f"   backed up existing {target.name} -> {prev.name}")


def next_video_number():
    """Highest N seen across concepts/scripts/stills, plus one. 1 if none."""
    nums = []
    for p in list(Path(".").glob("concepts_video*.json")) + \
             list(SCRIPTS.glob("video*.txt")) + \
             list(RENDER_IN.glob("video*_still.png")):
        m = re.search(r"video(\d+)", p.name)
        if m:
            nums.append(int(m.group(1)))
    return (max(nums) + 1) if nums else 1


def pose_of(name: str):
    stem = name.lower()
    for tag in POSE_TAGS:
        if tag in stem:
            return tag
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", type=int, help="video number (default: next available)")
    ap.add_argument("--build", action="store_true",
                    help="after placing, run build.py if concepts already exist")
    ap.add_argument("--count", type=int, default=4, help="passed to build.py if --build")
    args = ap.parse_args()

    for d in (DROP, RENDER_IN, SCRIPTS):
        d.mkdir(exist_ok=True)

    images = [p for p in DROP.iterdir()
              if p.suffix.lower() in IMG_EXT and not p.name.startswith(".")]
    scripts = [p for p in DROP.iterdir()
               if p.suffix.lower() in TXT_EXT
               and not p.name.startswith(".")
               and p.stem.lower() != "readme"]

    if not images:
        sys.exit(f"!! No still found in {DROP}/. Drop one image (png/jpg) in there and rerun.")
    if not scripts:
        sys.exit(f"!! No script found in {DROP}/. Drop one .txt or .md script in there and rerun.")
    if len(scripts) > 1:
        sys.exit(f"!! More than one script in {DROP}/: {[p.name for p in scripts]}. "
                 f"Keep one and rerun.")

    # one plain (base) still allowed; the rest must be pose-tagged
    plains = [p for p in images if pose_of(p.name) is None]
    if len(plains) > 1:
        sys.exit(f"!! More than one untagged still in {DROP}/: {[p.name for p in plains]}. "
                 f"Keep one as the base, or tag the others with a pose "
                 f"(authority/presenting/pointing/openpalm/considering).")

    n = args.video if args.video is not None else next_video_number()
    print(f"Ingesting as video {n}")

    # place the still(s)
    for img in images:
        pose = pose_of(img.name)
        if pose:
            target = RENDER_IN / f"video{n}_{pose}.png"
        else:
            target = RENDER_IN / f"video{n}_still.png"
        backup_if_exists(target)
        shutil.copy(str(img), str(target))
        print(f"   still: {img.name} -> {target}")

    # place the script
    script_target = SCRIPTS / f"video{n}.txt"
    backup_if_exists(script_target)
    shutil.copy(str(scripts[0]), str(script_target))
    print(f"   script: {scripts[0].name} -> {script_target}")

    concepts = Path(f"concepts_video{n}.json")
    print("")

    if concepts.exists():
        print(f"concepts_video{n}.json already exists.")
        if args.build:
            print("Building now...\n")
            sys.exit(subprocess.run(
                [sys.executable, "build.py", "--video", str(n), "--count", str(args.count)]
            ).returncode)
        print(f"NEXT: python build.py --video {n}")
    else:
        print(f"NEXT (one step): write concepts_video{n}.json, then build.")
        print(f"  In Claude Code, paste:")
        print(f"    Read GODIVA_THUMBNAIL_STYLE.md, CONCEPT_ENGINE.md, and GESTURE_KIT.md.")
        print(f"    Read scripts/video{n}.txt. Write {concepts.name} per CONCEPT_ENGINE.md")
        print(f"    (default 4 concepts, all diversity axes), then run python build.py --video {n}.")


if __name__ == "__main__":
    main()
