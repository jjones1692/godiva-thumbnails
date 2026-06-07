#!/usr/bin/env python3
# ============================================================================
# DEPRECATED, DO NOT USE FOR FACES. AI face-swap drifts and produces a WRONG,
# generic face (this caused a full set of wrong-face renders). The rule now:
# the base still must be ONE real, untouched photo of the actual person. Never
# swap or generate a face. Kept only for reference.
# ============================================================================
"""
make_identity_still.py - face-only swap to build a corrected base still.

Use when the best SCENE/pose still and the best FACE still are different photos
(e.g. a new outfit shot whose face drifts, plus an older shot with a locked
likeness). Produces one photorealistic still: the scene photo unchanged, with
ONLY the face replaced to match the face photo. Feed the result to build.py as
the normal --still.

    python make_identity_still.py --scene S1.png --face S2.png --out corrected.png
"""
import argparse, base64, json, sys, urllib.request
from render_nb2 import load_key, _img_part, MODEL

PROMPT = (
    "You are performing a precise, photorealistic FACE-ONLY swap between two photos of the "
    "same brand. There are TWO attached images.\n\n"
    "IMAGE 1 is the TARGET SCENE. Keep it EXACTLY as it is: same camo bucket hat worn on his "
    "head, same clear eyeglasses, same black 'Rockstar Original' t-shirt, same gold cuban-link "
    "chain, same open-hands pose and the exact same hands and fingers, same dark podcast room, "
    "same 'God's Plan' neon, same plant, lamp, microphone, same framing, crop, and lighting.\n\n"
    "IMAGE 2 is the FACE REFERENCE only. Take from it ONLY his facial identity and likeness: "
    "bone structure, jawline, eye shape and spacing, nose, lips, beard character, and skin tone.\n\n"
    "OUTPUT: image 1, completely unchanged, EXCEPT his face is now unmistakably the man from "
    "image 2. Critical constraints: KEEP THE CAMO BUCKET HAT ON HIS HEAD, he is NOT wearing a "
    "durag; KEEP the 'Rockstar Original' shirt, do NOT use the other shirt; do NOT change the "
    "hat, glasses, outfit, chain, hands, pose, room, or background; do NOT restyle, add text, or "
    "turn this into a graphic. Natural photo, same lighting and grade. Only the face changes. He "
    "must read as the same man as image 2 while everything else stays the scene of image 1."
)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scene", required=True, help="the photo whose scene/pose/outfit to keep")
    ap.add_argument("--face", required=True, help="the photo whose face/likeness to use")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    key = load_key()
    parts = [_img_part(a.scene), _img_part(a.face), {"text": PROMPT}]
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={key}"
    payload = json.dumps({"contents": [{"parts": parts}],
                          "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}}).encode()
    req = urllib.request.Request(url, data=payload,
                                 headers={"Content-Type": "application/json"}, method="POST")
    data = json.loads(urllib.request.urlopen(req, timeout=180).read())
    for p in data.get("candidates", [{}])[0].get("content", {}).get("parts", []):
        inl = p.get("inline_data") or p.get("inlineData")
        if inl and "data" in inl:
            open(a.out, "wb").write(base64.b64decode(inl["data"]))
            print(f"saved -> {a.out}")
            return
    print("no image returned:", json.dumps(data)[:300]); sys.exit(1)


if __name__ == "__main__":
    main()
