#!/usr/bin/env python3
"""
Godiva Mindset — Nano Banana 2 Thumbnail Renderer (Cinematic Financial Documentary)
====================================================================================
Renders thumbnails through Gemini Nano Banana 2 (gemini-3.1-flash-image-preview)
using the raw REST API. No SDK version guesswork. Bakes in the Godiva master style:
the Cutout Pop, the three-zone Problem/Center/Solution layout, and the
chocolate/gold/cream/bronze palette.

SETUP (one time):
    pip install pillow
    Put GEMINI_API_KEY in a .env file or export it.

USAGE:
    python render_nb2.py --still stills/still.png --concepts concepts.json
    (concepts.json is a list of concept objects — see SCHEMA below)

    Or single concept inline:
    python render_nb2.py --still stills/still.png \
        --punch DENIED --main "THIS IRS MOVE GETS YOU DENIED" \
        --sub "HERE'S THE SMARTER PLAY" \
        --left "IRS form stamped DENIED in red" \
        --right "green APPROVED stamp and gold $77K figure" \
        --out outputs/irs.png

CONCEPT SCHEMA (concepts.json):
[
  {
    "name": "irs_denied",
    "punch": "DENIED",
    "main": "THIS IRS MOVE GETS YOU DENIED",
    "sub": "HERE'S THE SMARTER PLAY",
    "left": "IRS form stamped DENIED in red, dark shadow",
    "right": "green APPROVED stamp and a gold $77K figure on a cream panel",
    "expression": "confident direct eye contact"
  }
]
"""
import argparse, base64, json, os, sys, urllib.request, urllib.error

MODEL = "gemini-3.1-flash-image-preview"   # Nano Banana 2

def load_key():
    k = os.getenv("GEMINI_API_KEY")
    if not k and os.path.exists(".env"):
        for line in open(".env"):
            line = line.strip()
            if line.startswith("GEMINI_API_KEY"):
                k = line.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("GEMINI_API_KEY not found. Put it in .env or export it.")
    return k

def build_prompt(c):
    """Compose the Godiva master-style prompt for one concept."""
    expression = c.get("expression", "confident direct eye contact")
    left = c.get("left", "a red DENIED stamp and dark shadow representing the problem")
    right = c.get("right", "a green APPROVED stamp and gold accent representing the solution")
    return (
        "Transform the attached photo into a high-CTR 16:9 YouTube thumbnail in the "
        "style of a CINEMATIC FINANCIAL DOCUMENTARY. Serious, grounded, premium. "
        "Not neon, not MrBeast-loud, not cartoonish, not clickbait spam.\n\n"

        "KEEP THE MAN IDENTICAL. Do not change his face, beard, glasses, head covering, "
        "gold chain, or shirt. Keep his exact likeness. His expression should read as: "
        f"{expression}.\n\n"

        "SUBJECT TREATMENT (THE CUTOUT POP, apply all four): "
        "1) clean edge cutout that lifts him off the background; "
        "2) a subtle bright rim light tracing his silhouette so he separates hard from "
        "the backdrop; 3) a soft outer glow or thin stroke around that edge; "
        "4) a cinematic color grade tying him and the scene into one graded frame. "
        "He sits in the CENTER, is the BRIGHTEST and SHARPEST element, in crisp focus.\n\n"

        "THREE-ZONE LAYOUT (eye travels left to right, problem to solution):\n"
        f"- LEFT SIDE = PROBLEM: {left}. Use reds and dark shadow tones here.\n"
        "- CENTER = THE MAN, brightest, sharpest, main focus.\n"
        f"- RIGHT SIDE = SOLUTION: {right}. Use green, gold, and cream tones here.\n\n"

        "COLOR PALETTE: chocolate brown, gold, cream, bronze as the brand base. "
        "Red accents only in the left problem zone, green and gold only in the right "
        "solution zone. Warm, documentary, never cold neon.\n\n"

        "TEXT (spelled EXACTLY, crisp, bold, heavy condensed sans, undistorted):\n"
        f"- The word \"{c['punch']}\" in heavy black condensed uppercase inside a solid "
        "bright-red rectangular box.\n"
        f"- Main caption (emotion/problem) in massive white heavy condensed uppercase with "
        f"a thick black outline: \"{c['main']}\".\n"
        f"- Sub caption (solution) smaller, in gold or cream condensed uppercase: "
        f"\"{c['sub']}\".\n\n"

        "TRUST SIGNALS: keep any logos, stamps, forms, or documents subtle and in the "
        "side zones. Never overpower the center or the text.\n\n"

        "FINAL VIBE: 'They tried me. I figured it out.' Problem to solution in one glance. "
        "Photorealistic sharp subject, zero blur on the person, clean sharp text. 1280x720."
    )

def render(still_path, concept, out_path, key):
    with open(still_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    mime = "image/png" if still_path.lower().endswith("png") else "image/jpeg"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    payload = json.dumps({
        "contents": [{"parts": [
            {"inline_data": {"mime_type": mime, "data": b64}},
            {"text": build_prompt(concept)}
        ]}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:300]}")
        return False
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        inline = p.get("inline_data") or p.get("inlineData")
        if inline and "data" in inline:
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            with open(out_path, "wb") as out:
                out.write(base64.b64decode(inline["data"]))
            print(f"  saved -> {out_path}")
            return True
    print(f"  no image returned. response: {json.dumps(data)[:300]}")
    return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--concepts", help="path to concepts.json (list of concept objects)")
    ap.add_argument("--punch"); ap.add_argument("--main"); ap.add_argument("--sub")
    ap.add_argument("--left"); ap.add_argument("--right"); ap.add_argument("--expression")
    ap.add_argument("--out", default="outputs/thumbnail.png")
    args = ap.parse_args()
    key = load_key()

    if args.concepts:
        concepts = json.load(open(args.concepts))
        print(f"Rendering {len(concepts)} concepts on Nano Banana 2...")
        for i, c in enumerate(concepts, 1):
            name = c.get("name", f"concept_{i}")
            print(f"Concept {i} ({name}):")
            render(args.still, c, f"outputs/{name}.png", key)
    else:
        c = {"punch": args.punch or "DENIED",
             "main": args.main or "THEY TRIED ME",
             "sub": args.sub or "I FIGURED IT OUT",
             "left": args.left or "", "right": args.right or "",
             "expression": args.expression or "confident direct eye contact"}
        render(args.still, c, args.out, key)
    print("Done.")

if __name__ == "__main__":
    main()
