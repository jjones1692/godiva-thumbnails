#!/usr/bin/env python3
"""
Godiva Mindset — Nano Banana Thumbnail Generator
=================================================

Turns a raw still into a finished 1280x720 YouTube thumbnail using Google's
Nano Banana (Gemini image models) via the Gemini API.

Run this in Claude Code (or any terminal) on your own machine. It uses YOUR
Gemini API key, saves real files to disk, and can loop multiple concepts.

SETUP (one time)
----------------
1. Get a free Gemini API key:  https://aistudio.google.com/apikey
2. Install dependencies:
       pip install google-genai pillow
3. Set your key as an environment variable:
       macOS/Linux:   export GEMINI_API_KEY="your_key_here"
       Windows (PS):  setx GEMINI_API_KEY "your_key_here"

USAGE
-----
Single finished thumbnail (Nano Banana 2, the default — omit --tier or use v2):
    python godiva_thumbnail.py --still raw.png \
        --punch "DELETED" \
        --main "IT ALL IN 4 DAYS" \
        --sub "HERE'S MY EXACT METHOD" \
        --graphic "white credit-report page, tilted, with a thick bold hand-drawn red marker X across it, and a black flip-clock reading '04 DAYS' behind his right shoulder" \
        --out deleted_4days.png

Explore 4 cheap concepts first (base model), then render the winner on v2 (or pro if text warps):
    python godiva_thumbnail.py --still raw.png --tier base --concepts 4 ... 

MODEL TIERS
-----------
  v2    -> gemini-3.1-flash-image-preview  (~$0.045/img, newest)   — DEFAULT, your pick
  base  -> gemini-2.5-flash-image          (~$0.039/img, free tier ~500/day) — cheap exploring
  pro   -> gemini-3-pro-image-preview      (~$0.134/img, best TEXT) — fallback if text warps

NOTE: model IDs change. If a call errors on the model name, check the current
ID at https://ai.google.dev/gemini-api/docs/models and update MODELS below.
"""

import argparse
import os
import sys
from io import BytesIO

try:
    from google import genai
    from PIL import Image
except ImportError:
    sys.exit("Missing deps. Run:  pip install google-genai pillow")

# ---------------------------------------------------------------------------
# Model registry — update IDs here if Google renames them
# ---------------------------------------------------------------------------
MODELS = {
    "base": "gemini-2.5-flash-image",        # workhorse, cheapest
    "pro":  "gemini-3-pro-image-preview",    # best text rendering — use for finals
    "v2":   "gemini-3.1-flash-image-preview" # newest, 4K capable
}

# ---------------------------------------------------------------------------
# Godiva Mindset locked brand block — do not edit per-video
# ---------------------------------------------------------------------------
BRAND_BLOCK = (
    "KEEP THE MAN IDENTICAL. Do not change his face, beard, glasses, head "
    "covering, gold Cuban link chain, or his shirt. Keep his exact likeness and "
    "expression. Cut him out of his original room, keep him sharp and in crisp "
    "focus, and place him from the chest up, slightly right of center. "
    "BACKGROUND: replace the room with a dark, cinematic, deep-blue blurred "
    "studio backdrop, soft bokeh, subtle glowing shapes for depth, a moody "
    "vignette, dramatic high-contrast lighting so he pops off the background. "
)

STYLE_BLOCK = (
    "STYLE: ultra-bold, dramatic, high contrast. Deep blue background "
    "(#1D4ED8 family), white text, bright red accents, gold chain. "
    "Photorealistic sharp subject, zero blur on the person, clean sharp "
    "undistorted text. Final image 16:9, 1280x720."
)


def build_prompt(punch, main, sub, graphic):
    """Assemble the full Godiva thumbnail prompt from the editable slots."""
    text_block = (
        "TEXT (lower-center, spelled EXACTLY as written, crisp and undistorted): "
        f'- "{punch}" in heavy black condensed uppercase inside a solid '
        "bright-red rectangular highlight box. "
        f'- Directly below: "{main}" in massive white heavy condensed uppercase '
        "with a thick black outline. "
        f'- Below that, smaller: "{sub}" in white condensed uppercase. '
    )
    graphic_block = f"SUPPORTING GRAPHIC: {graphic}. " if graphic else ""
    return (
        "Transform the attached photo of the man into a high-CTR 16:9 YouTube "
        "thumbnail. "
        + BRAND_BLOCK
        + graphic_block
        + text_block
        + STYLE_BLOCK
    )


def fit_1280x720(img):
    """Center-crop/cover the model output to an exact 1280x720 thumbnail."""
    target_w, target_h = 1280, 720
    src_w, src_h = img.size
    scale = max(target_w / src_w, target_h / src_h)
    new_size = (round(src_w * scale), round(src_h * scale))
    img = img.resize(new_size, Image.LANCZOS)
    left = (img.width - target_w) // 2
    top = (img.height - target_h) // 2
    return img.crop((left, top, left + target_w, top + target_h))


def generate(client, model_id, prompt, still_path, out_path):
    """One generation call -> saved 1280x720 PNG. Returns out_path or None."""
    still = Image.open(still_path)
    resp = client.models.generate_content(model=model_id, contents=[prompt, still])
    for part in resp.candidates[0].content.parts:
        if getattr(part, "inline_data", None) is not None:
            img = Image.open(BytesIO(part.inline_data.data))
            fit_1280x720(img).save(out_path, "PNG")
            print(f"  saved -> {out_path}")
            return out_path
        if getattr(part, "text", None):
            print(f"  model said: {part.text[:160]}")
    print("  no image returned for this call")
    return None


def main():
    ap = argparse.ArgumentParser(description="Godiva Mindset thumbnail generator")
    ap.add_argument("--still", required=True, help="path to the raw still image")
    ap.add_argument("--tier", default="v2", choices=MODELS.keys(),
                    help="v2 = Nano Banana 2 (default) | base = cheap explore | pro = best text fallback")
    ap.add_argument("--punch", default="DELETED", help="red-box punch word")
    ap.add_argument("--main", default="IT ALL IN 4 DAYS", help="main caption")
    ap.add_argument("--sub", default="HERE'S MY EXACT METHOD", help="sub-caption")
    ap.add_argument("--graphic", default="", help="the one hero graphic that proves the hook")
    ap.add_argument("--concepts", type=int, default=1, help="how many variations to generate")
    ap.add_argument("--out", default="thumbnail.png", help="output filename (concepts add _1, _2 ...)")
    args = ap.parse_args()

    if not os.getenv("GEMINI_API_KEY"):
        sys.exit("GEMINI_API_KEY not set. See SETUP at the top of this file.")

    client = genai.Client()
    model_id = MODELS[args.tier]
    prompt = build_prompt(args.punch, args.main, args.sub, args.graphic)

    print(f"Model: {model_id}  ({args.tier})")
    print(f"Generating {args.concepts} concept(s)...")

    if args.concepts == 1:
        generate(client, model_id, prompt, args.still, args.out)
    else:
        stem, ext = os.path.splitext(args.out)
        for i in range(1, args.concepts + 1):
            print(f"Concept {i}:")
            generate(client, model_id, prompt, args.still, f"{stem}_{i}{ext}")

    print("Done.")


if __name__ == "__main__":
    main()
