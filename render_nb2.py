#!/usr/bin/env python3
"""
Godiva Mindset — Nano Banana 2 Thumbnail Renderer (Cinematic Financial Documentary)
====================================================================================
Renders thumbnails through Gemini Nano Banana 2 (gemini-3.1-flash-image-preview)
via raw REST. Bakes in the Godiva master style: Cutout Pop subject treatment,
the three-zone Problem/Center/Solution layout, chocolate/gold/cream/bronze palette.

NEW: per-concept STYLE VARIANTS. The three-zone layout stays constant; each concept
can carry a "style" field that changes the visual treatment so 4 concepts become 4
distinct bets instead of one template with swapped words.

STYLES: cinematic_text | interface_trust | anti_thumbnail | engineered_candid | classic

SETUP (one time):
    pip install pillow   (only needed for --crop)
    GEMINI_API_KEY in .env  (format: GEMINI_API_KEY=AQ.xxxx)

USAGE:
    python render_nb2.py --still render-input/still.png --concepts concepts_video1.json
    Add --crop to center-crop output to exactly 1280x720.

CONCEPT SCHEMA (concepts_*.json) — each object:
    name, style, punch, main, sub, left, right, expression
"""
import argparse, base64, json, os, sys, urllib.request, urllib.error

MODEL = "gemini-3.1-flash-image-preview"   # Nano Banana 2

# ---------------------------------------------------------------------------
# STYLE VARIANTS — same three-zone layout, different visual treatment.
# Each block is appended to the base prompt to make the concept a distinct bet.
# ---------------------------------------------------------------------------
STYLE_VARIANTS = {
    "cinematic_text":
        "STYLE TREATMENT — CINEMATIC EMBEDDED TEXT: Pull the main headline INTO the "
        "scene so it shares the same depth and space as the man, embedded in the "
        "lighting and shadow like a film title card, not sitting in a flat bottom bar. "
        "Big, modern, high-contrast, three or four dominant words that own the frame. "
        "The text interacts with the scene's light. Cinematic depth of field. This "
        "should read like a still from a Netflix documentary, not a YouTube ad.",

    "interface_trust":
        "STYLE TREATMENT — INTERFACE / BORROWED CREDIBILITY: Render the LEFT problem "
        "zone and RIGHT solution zone as realistic official interfaces. Left: an "
        "authentic-looking FTC affidavit or credit bureau letter with correct spacing, "
        "seals, and a red stamp. Right: an official approval portal or stamped APPROVED "
        "document with a real score number. Match real document fonts and layout so it "
        "borrows the credibility of the real format. Keep headline text minimal; let the "
        "documents carry the believability.",

    "anti_thumbnail":
        "STYLE TREATMENT — ANTI-THUMBNAIL (QUIET DOCUMENTARY): Dark, restrained, serious. "
        "Muted near-black background, deep shadow. Keep the three zones but render the "
        "left and right cues FAINT and shadowed, barely lit. The man is tight in frame "
        "with intense direct eye contact, clearly the single brightest element. One short "
        "bold line of text only. This frame wins by being calm in a loud feed. No clutter, "
        "no bright stamps. Stillness and eye contact do the work.",

    "engineered_candid":
        "STYLE TREATMENT — ENGINEERED CANDID (REAL MOMENT): A believable captured-moment "
        "look. The man is physically holding or reacting to the key prop (the document, "
        "the letter, the report) as if caught mid-action. The side-zone elements feel like "
        "real objects in his space, not graphic overlays. Subtle, no loud stamps or arrows, "
        "no flat UI text bars. Light, tasteful decoration on a real-looking photo. It should "
        "look like a frame you genuinely captured in the moment.",

    "transformation_arc":
        "STYLE TREATMENT — TRANSFORMATION ARC (PROOF, NOT HYPE): A clear left-to-right "
        "before-and-after built on ONE clean sweeping arrow rendered in GOLD or CREAM, "
        "never bright guru red or yellow. Show the SAME artifact at two values so it reads "
        "as undeniable proof: a low credit report or score on the LEFT and the same report "
        "at a high score on the RIGHT; or a DENIED screen left and an APPROVED screen right. "
        "The man is centered, calm, present between the two states or gesturing toward them. "
        "Chocolate cinematic background, restrained grade, soft rim light. The arrow does the "
        "eye-path work, the matched documents do the convincing. No neon, no loud stamps, no "
        "shouting. It should feel like evidence laid side by side, not a get-rich ad.",

    "classic":
        "STYLE TREATMENT — CLASSIC GODIVA: Clean designed three-zone composition with a "
        "lower-third text block, bold and direct. The standard recognizable Godiva look.",
}

# FRAMING controls the SILHOUETTE of the shot so a batch looks like several different
# pictures, not one layout repainted. Each concept carries "framing"; build_prompt swaps
# the subject placement sentence and the layout block based on it. Default: centered.
FRAMING_BLOCKS = {
    "centered": {
        "placement": "He sits CENTER, noticeably the BRIGHTEST and SHARPEST element, in "
                     "crisp focus, with generous negative space around him.",
        "layout": "THREE-ZONE LAYOUT (eye travels left to right, problem to solution):\n"
                  "- LEFT = PROBLEM: {left}. Reds and dark shadow tones.\n"
                  "- CENTER = THE MAN, brightest, sharpest, main focus.\n"
                  "- RIGHT = SOLUTION: {right}. Green, gold, and cream tones.\n\n",
    },
    "tight_face": {
        "placement": "He is framed TIGHT, head and shoulders filling most of the vertical "
                     "frame, the dominant mass of the image, in crisp focus. This is a "
                     "close, intense portrait, NOT a wide centered three-zone shot.",
        "layout": "SINGLE-CUE LAYOUT (not three symmetric zones): keep the background dark "
                  "and restrained with exactly ONE supporting element, {right}, kept smaller "
                  "and dimmer than him and set off to one side. No matching left/right "
                  "flanking props. His face and direct eye contact carry the frame.\n\n",
    },
    "subject_left": {
        "placement": "He stands on the LEFT THIRD of the frame, turned slightly inward "
                     "toward center, sharp and rim-lit. He is deliberately NOT centered.",
        "layout": "OFF-CENTER HERO LAYOUT (deliberately asymmetric): the RIGHT two-thirds of "
                  "the frame is dominated by ONE single hero element, {right}, rendered large "
                  "and cinematic with warm light and breathing negative space. Any problem cue "
                  "({left}) is small and faint near him, or omitted entirely.\n\n",
    },
    "subject_right": {
        "placement": "He stands on the RIGHT THIRD of the frame, turned slightly inward "
                     "toward center, sharp and rim-lit. He is deliberately NOT centered.",
        "layout": "OFF-CENTER HERO LAYOUT (deliberately asymmetric): the LEFT two-thirds of "
                  "the frame is dominated by ONE single hero element, {left}, rendered large "
                  "and cinematic with negative space. Any solution cue ({right}) is small and "
                  "faint near him, or omitted entirely.\n\n",
    },
    "split": {
        "placement": "He is set slightly smaller and centered ON the dividing seam of a hard "
                     "left/right split, strongly rim-lit so he separates cleanly from both "
                     "halves.",
        "layout": "TRUE BEFORE/AFTER SPLIT (not center-flanked): divide the frame down the "
                  "middle into two comparable halves of the SAME kind of artifact. LEFT HALF "
                  "= the BEFORE state: {left}, in red and shadow. RIGHT HALF = the AFTER "
                  "state: {right}, in green, gold and cream. The contrast between the two "
                  "halves IS the composition.\n\n",
    },
}

# POSE controls the GESTURE (hands and body). It is honored faithfully only when the source
# still actually shows it; the prompt asks to preserve, not invent, his hands. Default:
# authority (settled), the safest from a single neutral still.
POSE_BLOCKS = {
    "authority": "GESTURE: keep his hands and body as a calm, settled, authoritative posture, "
                 "arms relaxed or lightly crossed, no exaggerated motion. Preserve his real "
                 "hands exactly as in the source photo; do not invent new hand positions.",
    "presenting": "GESTURE: he is holding or presenting the key document toward the camera, as "
                  "in the source photo. Keep his real hands and fingers exactly as shot, clean "
                  "and undistorted; do not redraw or add fingers.",
    "pointing": "GESTURE: he is pointing toward the key element or number, directing the eye, "
                "as in the source photo. Preserve his real pointing hand exactly as shot; do "
                "not invent or warp fingers.",
    "open_palm": "GESTURE: one open palm raised in a calm 'here is the truth' explaining "
                 "gesture, as in the source photo. Keep his real hand exactly as shot, "
                 "undistorted.",
    "considering": "GESTURE: a hand resting near his chin in a considered, weighing posture, "
                   "as in the source photo. Preserve his real hand exactly as shot.",
}

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

def build_prompt(c, identity=False):
    scene_only = c.get("scene_only", False)
    expression = c.get("expression", "confident direct eye contact")
    identity_block = (
        "FACE REFERENCE (use sparingly): a second photo is attached only as a gentle likeness "
        "reference. The FIRST photo's face is the base, keep it. Do not replace it wholesale or "
        "blend in a different face. If the two ever disagree, PRESERVE THE FIRST PHOTO'S ACTUAL "
        "FACE. He must look like himself, never a generic or invented man.\n\n"
        if identity else ""
    )
    left = c.get("left", "a red DENIED stamp and dark shadow representing the problem")
    right = c.get("right", "a green APPROVED stamp and gold accent representing the solution")
    style_key = c.get("style", "classic")
    style_block = STYLE_VARIANTS.get(style_key, STYLE_VARIANTS["classic"])
    framing_key = c.get("framing", "centered")
    fb = FRAMING_BLOCKS.get(framing_key, FRAMING_BLOCKS["centered"])
    placement = fb["placement"]
    layout_block = fb["layout"].format(left=left, right=right)
    pose_block = POSE_BLOCKS.get(c.get("pose", "authority"), POSE_BLOCKS["authority"])
    return (
        "Transform the attached photo into a high-CTR 16:9 YouTube thumbnail in the "
        "style of a CINEMATIC FINANCIAL DOCUMENTARY. Serious, grounded, premium. "
        "Not neon, not MrBeast-loud, not cartoonish, not clickbait spam.\n\n"

        "ABSOLUTE LIKENESS LOCK (the single most important rule, overrides everything else): "
        "The attached photo is a real photograph of a specific real man. His face must come "
        "through UNCHANGED, the exact same bone structure, jawline, nose, eye shape and spacing, "
        "lips, beard, skin tone, and skin texture. Do NOT generate, swap, slim, reshape, "
        "beautify, de-age, or restyle his face into a different-looking person. The face in the "
        "output must be INDISTINGUISHABLE from the face in the photo, the same man, recognizable "
        "by his own family. If preserving the background or props would cost his real face, KEEP "
        "THE FACE and sacrifice the rest. A face that looks like a different man is the single "
        "worst possible failure of this task. "
        f"His expression should read as: {expression}.\n\n"

        f"{identity_block}"

        "OPTIONAL LIGHT POLISH (only if it does NOT change who he is): you may very subtly neaten "
        "the beard edges and reduce under-eye puffiness, barely perceptible retouching of the "
        "SAME man. Never reshape the jaw, never slim the face into a different person. Identity "
        "always overrides polish. If in any doubt, leave his face exactly as photographed.\n\n"

        "SUBJECT TREATMENT (THE CUTOUT POP, apply all four): 1) clean crisp edge cutout that "
        "lifts him off the background; 2) a clearly visible bright rim light tracing his "
        "silhouette; 3) a soft outer glow or thin stroke around that edge; 4) a cinematic "
        f"color grade. {placement}\n\n"

        f"{pose_block}\n\n"

        "CRITICAL ANTI-GIBBERISH RULE (the #1 thing that makes thumbnails look AI): On any "
        "document, report, screen, or form, the ONLY text allowed is: a SHORT 1 to 2 word label "
        "at the top (like 'Credit Report' or 'Credit Bureau'), PLUS a single bold STAMP WORD "
        "(BLOCKED, APPROVED, DENIED, DELETED, VERIFIED) and/or ONE large number (like 762). "
        "Absolutely NO long titles, NO multi-word headers, NO field-label rows (no 'Name:', "
        "'Address:', 'Code:' etc.), NO signature text, NO body paragraphs or sentences. Every "
        "other line on the document must be left BLANK or shown as soft featureless grey bars "
        "with no legible characters. AI cannot spell inside props, so give it nothing to spell. "
        "Clean symbols only: stamps, a seal shape, a green checkmark, a rising arrow, a number.\n\n"

        "COMPOSITION, KEEP IT CLEAN: ONE single hero element per side zone, maximum. No stacks "
        "of documents, no piles of props, no calendars plus phones plus arrows all at once. "
        "Generous negative space. Simplicity reads premium, clutter reads amateur. One clean "
        "prop per side, not five.\n\n"

        "NO REDUNDANT PROPS: the LEFT and RIGHT zones must show DIFFERENT things. Never repeat "
        "the same stamp, document, or symbol in two places. If one element already shows the "
        "outcome (e.g. a DELETED page), the other zone must show something else (a higher score, "
        "a clean report, a funding doc, a green check), so every prop adds new information.\n\n"

        f"{layout_block}"

        f"{style_block}\n\n"

        "COLOR PALETTE: chocolate brown, gold, cream, bronze base. Red accents only in the "
        "left problem zone, green and gold only in the right solution zone. Warm, "
        "documentary, never cold neon.\n\n"

        + (
            "TEXT: Do NOT render any headline, caption, punch word, or any large title text "
            "anywhere in the image. Leave the lower third and the side areas CLEAN and free of "
            "title text so text can be added in post. Only incidental prop marks (a single STAMP "
            "word on a document, a score number) are allowed. No big headline text at all.\n\n"
            if scene_only else
            "TEXT (spelled EXACTLY, crisp, bold, heavy condensed sans, undistorted):\n"
            f"- \"{c['punch']}\" in heavy black condensed uppercase inside a solid bright-red box.\n"
            f"- Main caption: \"{c['main']}\" as ONE solid clean block of massive white heavy "
            "condensed uppercase with a thick black outline. Never split the headline across the "
            "subject's body; keep it as one unbroken line or stacked block in clear open space.\n"
            f"- Sub caption: \"{c['sub']}\" smaller, in gold or cream condensed uppercase.\n\n"
        ) +

        "Keep trust signals (logos, stamps, forms) subtle and in the side zones, never "
        "overpowering the center or text.\n\n"

        "FINAL VIBE: 'They tried me. I figured it out.' Problem to solution in one glance. "
        "Photorealistic sharp subject, zero blur on the person, clean sharp text. 1280x720."
    )

def crop_1280x720(path):
    try:
        from PIL import Image
    except ImportError:
        print("  (skip crop: pillow not installed)"); return
    im = Image.open(path).convert("RGB")
    tw, th = 1280, 720
    s = max(tw/im.width, th/im.height)
    im = im.resize((round(im.width*s), round(im.height*s)), Image.LANCZOS)
    l = (im.width-tw)//2; t = (im.height-th)//2
    im.crop((l, t, l+tw, t+th)).save(path)
    print("  cropped -> 1280x720")

def _img_part(path):
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    mime = "image/png" if path.lower().endswith("png") else "image/jpeg"
    return {"inline_data": {"mime_type": mime, "data": b64}}

def render(still_path, concept, out_path, key, crop=False, identity_path=None):
    parts = [_img_part(still_path)]
    if identity_path:
        parts.append(_img_part(identity_path))          # face/likeness reference (image 2)
    parts.append({"text": build_prompt(concept, identity=bool(identity_path))})
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    payload = json.dumps({
        "contents": [{"parts": parts}],
        "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
    }).encode()
    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  HTTP {e.code}: {e.read().decode()[:300]}"); return False
    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    for p in parts:
        inline = p.get("inline_data") or p.get("inlineData")
        if inline and "data" in inline:
            os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
            with open(out_path, "wb") as out:
                out.write(base64.b64decode(inline["data"]))
            print(f"  saved -> {out_path}  [style: {concept.get('style','classic')}]")
            if crop: crop_1280x720(out_path)
            return True
    print(f"  no image returned: {json.dumps(data)[:300]}"); return False

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--still", required=True)
    ap.add_argument("--identity", help="optional second photo used ONLY as the face/likeness "
                    "reference; scene/pose/outfit still come from --still")
    ap.add_argument("--concepts")
    ap.add_argument("--crop", action="store_true", help="center-crop output to exactly 1280x720")
    ap.add_argument("--scene-only", action="store_true", help="render scene with NO headline text, for Canva finishing")
    ap.add_argument("--punch"); ap.add_argument("--main"); ap.add_argument("--sub")
    ap.add_argument("--left"); ap.add_argument("--right"); ap.add_argument("--expression")
    ap.add_argument("--style", default="classic", choices=list(STYLE_VARIANTS.keys()))
    ap.add_argument("--out", default="outputs/thumbnail.png")
    args = ap.parse_args()
    key = load_key()
    if args.concepts:
        concepts = json.load(open(args.concepts))
        if args.scene_only:
            for c in concepts: c["scene_only"] = True
        print(f"Rendering {len(concepts)} concepts on Nano Banana 2... (scene_only={args.scene_only})")
        for i, c in enumerate(concepts, 1):
            name = c.get("name", f"concept_{i}")
            print(f"Concept {i} ({name}):")
            render(args.still, c, f"outputs/{name}.png", key, crop=args.crop, identity_path=args.identity)
    else:
        c = {"punch": args.punch or "DENIED", "main": args.main or "THEY TRIED ME",
             "sub": args.sub or "I FIGURED IT OUT", "left": args.left or "",
             "right": args.right or "", "expression": args.expression or "confident direct eye contact",
             "style": args.style, "scene_only": args.scene_only}
        render(args.still, c, args.out, key, crop=args.crop, identity_path=args.identity)
    print("Done.")

if __name__ == "__main__":
    main()
