#!/usr/bin/env python3
"""
Godiva Mindset — Text Finisher
==============================
Stamps perfect, pixel-sharp text onto a scene-only Nano Banana 2 render.
Text is drawn by a real font engine, so it is NEVER warped, doubled, or misspelled.
This is the second half of the hybrid: NB2 makes the scene, this adds flawless text.

USAGE:
    # finish one render
    python finish_text.py --image outputs/v1_interface_ftc.png \
        --punch BLOCKED --main "ONE DOCUMENT BLOCKED IT ALL" --sub "THEY NEVER TOLD YOU" \
        --out outputs/v1_interface_ftc_final.png

    # finish a whole concepts file (expects scene renders already in outputs/<name>.png)
    python finish_text.py --concepts concepts_video1.json

LAYOUT: punch word in a red box (upper area), main caption as one clean white block
with a heavy black outline (lower third), sub caption in gold below it. Tuned to sit
in the open zones a scene-only render leaves clear.
"""
import argparse, json, os, textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_MAIN = os.path.join(HERE, "fonts", "Anton-Regular.ttf")
FONT_SUB  = os.path.join(HERE, "fonts", "BarlowCondensed-SemiBold.ttf")

GOLD = (201, 156, 61)
RED  = (193, 39, 45)
WHITE = (245, 245, 245)
BLACK = (10, 10, 10)

def font(path, size):
    return ImageFont.truetype(path, size)

def text_size(draw, s, f):
    b = draw.textbbox((0, 0), s, font=f)
    return b[2] - b[0], b[3] - b[1]

def fit_font(draw, text, path, max_w, start, min_size=28):
    """Shrink font until text fits max_w."""
    size = start
    while size > min_size:
        f = font(path, size)
        w, _ = text_size(draw, text, f)
        if w <= max_w:
            return f
        size -= 2
    return font(path, min_size)

def draw_outlined(draw, xy, text, f, fill, outline=BLACK, ow=6, anchor="la"):
    x, y = xy
    for dx in range(-ow, ow + 1, 2):
        for dy in range(-ow, ow + 1, 2):
            draw.text((x + dx, y + dy), text, font=f, fill=outline, anchor=anchor)
    draw.text((x, y), text, font=f, fill=fill, anchor=anchor)

def wrap_to_width(draw, text, f, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        test = (cur + " " + w).strip()
        if text_size(draw, test, f)[0] <= max_w or not cur:
            cur = test
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def finish(image_path, punch, main, sub, out_path):
    im = Image.open(image_path).convert("RGB")
    W, H = im.size
    draw = ImageDraw.Draw(im)
    margin = int(W * 0.04)

    # MAIN caption: one clean block, lower third, white + heavy black outline
    main = main.upper()
    main_f = fit_font(draw, main, FONT_MAIN, int(W * 0.92), int(H * 0.13))
    main_lines = wrap_to_width(draw, main, main_f, int(W * 0.92))
    if len(main_lines) > 2:  # keep to 2 lines max, refit smaller
        main_f = fit_font(draw, main, FONT_MAIN, int(W * 0.46), int(H * 0.12))
        main_lines = wrap_to_width(draw, main, main_f, int(W * 0.46))
    lh = text_size(draw, "Ag", main_f)[1] + int(H * 0.02)
    block_h = lh * len(main_lines)
    y = int(H * 0.78) - block_h
    for line in main_lines:
        lw, _ = text_size(draw, line, main_f)
        draw_outlined(draw, ((W - lw)//2, y), line, main_f, WHITE, ow=max(4, main_f.size//14))
        y += lh

    # SUB caption: gold, just under main
    if sub:
        sub = sub.upper()
        sub_f = fit_font(draw, sub, FONT_SUB, int(W * 0.7), int(H * 0.055), min_size=20)
        sw, sh = text_size(draw, sub, sub_f)
        sy = y + int(H * 0.005)
        draw_outlined(draw, ((W - sw)//2, sy), sub, sub_f, GOLD, ow=3)

    # PUNCH word: black text in a solid red box, upper area, offset from center
    if punch:
        punch = punch.upper()
        pf = font(FONT_MAIN, int(H * 0.085))
        pw, ph = text_size(draw, punch, pf)
        padx, pady = int(pw * 0.12), int(ph * 0.28)
        bx, by = margin, int(H * 0.06)
        draw.rectangle([bx, by, bx + pw + padx*2, by + ph + pady*2], fill=RED)
        draw.text((bx + padx, by + pady - int(ph*0.1)), punch, font=pf, fill=BLACK)

    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    im.save(out_path)
    print(f"  finished -> {out_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--image"); ap.add_argument("--concepts")
    ap.add_argument("--punch", default=""); ap.add_argument("--main", default="")
    ap.add_argument("--sub", default=""); ap.add_argument("--out", default="outputs/final.png")
    args = ap.parse_args()
    for p in (FONT_MAIN, FONT_SUB):
        if not os.path.exists(p): raise SystemExit(f"Missing font: {p}")
    if args.concepts:
        for c in json.load(open(args.concepts)):
            name = c.get("name", "concept")
            scene = f"outputs/{name}.png"
            if not os.path.exists(scene):
                print(f"  skip {name}: no scene render at {scene}"); continue
            finish(scene, c.get("punch",""), c.get("main",""), c.get("sub",""),
                   f"outputs/{name}_final.png")
    else:
        finish(args.image, args.punch, args.main, args.sub, args.out)
    print("Done.")

if __name__ == "__main__":
    main()
