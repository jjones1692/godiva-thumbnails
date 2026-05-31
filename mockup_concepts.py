#!/usr/bin/env python3
"""
Godiva Mindset — concept LAYOUT MOCKUPS (not final renders).

Draws all 4 thumbnail concepts at 1280x720 in the brand palette so James can
SEE composition: punch box, captions, hero-graphic placement, subject zone.
The subject is a placeholder silhouette — the photoreal render with James's
real cutout happens on his machine via godiva_thumbnail.py.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

W, H = 1280, 720
DEEP_BLUE = (29, 78, 216)
DARK = (12, 20, 40)
WHITE = (245, 245, 245)
RED = (193, 39, 45)
GOLD = (201, 156, 61)
GREEN = (0, 168, 107)
BLACK = (10, 10, 12)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(sz):
    return ImageFont.truetype(FB, sz)

def bg():
    """Dark cinematic deep-blue gradient + vignette + bokeh."""
    img = Image.new("RGB", (W, H), DARK)
    top = (18, 34, 78)
    for y in range(H):
        t = y / H
        r = int(top[0] + (DARK[0] - top[0]) * t)
        g = int(top[1] + (DARK[1] - top[1]) * t)
        b = int(top[2] + (DARK[2] - top[2]) * t)
        ImageDraw.Draw(img).line([(0, y), (W, y)], fill=(r, g, b))
    # bokeh glows
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for (cx, cy, rad, col) in [(220, 200, 120, (30, 70, 190)),
                               (980, 150, 90, (40, 90, 220)),
                               (1120, 480, 140, (25, 55, 150)),
                               (120, 560, 80, (35, 80, 200))]:
        gd.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    img = Image.blend(img, Image.blend(img, glow, 0.6), 0.5)
    # vignette
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse([-260, -200, W+260, H+200], fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(160))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    img = Image.composite(img, dark, vig)
    return img

def subject(img):
    """Placeholder silhouette of James, chest-up, right of center, gold chain hint."""
    d = ImageDraw.Draw(img, "RGBA")
    cx = 930
    # rim light halo
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(halo).ellipse([cx-230, 120, cx+230, H+120], fill=(80, 120, 220, 90))
    halo = halo.filter(ImageFilter.GaussianBlur(40))
    img.paste(Image.alpha_composite(img.convert("RGBA"), halo).convert("RGB"), (0, 0))
    d = ImageDraw.Draw(img, "RGBA")
    body = (22, 18, 16, 255)  # brown tee / dark
    # shoulders/torso
    d.rounded_rectangle([cx-200, 470, cx+210, H+40], radius=80, fill=body)
    # head
    d.ellipse([cx-90, 200, cx+90, 410], fill=(46, 34, 28, 255))
    # beanie/durag
    d.pieslice([cx-95, 175, cx+95, 320], 180, 360, fill=(18, 18, 20, 255))
    # gold chain hint
    d.arc([cx-70, 400, cx+70, 480], 20, 160, fill=GOLD, width=7)
    # glasses hint
    d.line([cx-55, 290, cx+55, 290], fill=(15, 15, 15, 255), width=6)
    d.text((cx-80, H-44), "JAMES (cutout)", font=font(20), fill=(150, 170, 210))
    return img

def outlined(d, xy, text, fnt, fill=WHITE, outline=BLACK, ow=4, anchor="lm"):
    x, y = xy
    for dx in range(-ow, ow+1):
        for dy in range(-ow, ow+1):
            if dx or dy:
                d.text((x+dx, y+dy), text, font=fnt, fill=outline, anchor=anchor)
    d.text((x, y), text, font=fnt, fill=fill, anchor=anchor)

def punch_box(d, x, y, text, fnt):
    tb = d.textbbox((0, 0), text, font=fnt)
    tw, th = tb[2]-tb[0], tb[3]-tb[1]
    pad_x, pad_y = 26, 14
    d.rectangle([x, y, x+tw+pad_x*2, y+th+pad_y*2], fill=RED)
    d.text((x+pad_x, y+pad_y-tb[1]), text, font=fnt, fill=BLACK)
    return y+th+pad_y*2

def text_block(img, punch, main, sub):
    d = ImageDraw.Draw(img)
    x = 70
    y = 300
    bottom = punch_box(d, x, y, punch, font(58))
    outlined(d, (x, bottom+58), main, font(76), anchor="lm")
    outlined(d, (x, bottom+128), sub, font(34), fill=GOLD, ow=3, anchor="lm")

# ---- hero graphics (one per concept) ----
def report_x(img, label=None):
    d = ImageDraw.Draw(img)
    px, py, pw, ph = 70, 70, 300, 200
    rep = Image.new("RGBA", (pw, ph), (245, 245, 245, 255))
    rd = ImageDraw.Draw(rep)
    rd.rectangle([0, 0, pw-1, ph-1], outline=(120, 120, 120), width=2)
    rd.rectangle([14, 14, 70, 50], fill=(200, 200, 200))
    for i in range(5):
        rd.line([(86, 26+i*30), (pw-20, 26+i*30)], fill=(170, 170, 170), width=6)
    rep = rep.rotate(-7, expand=True, resample=Image.BICUBIC)
    img.paste(rep, (px, py), rep)
    d.line([(px+10, py+40), (px+pw-10, py+ph-10)], fill=RED, width=14)
    d.line([(px+pw-10, py+40), (px+10, py+ph-10)], fill=RED, width=14)

def report_x3(img):
    d = ImageDraw.Draw(img)
    px, py, pw, ph = 70, 60, 300, 230
    d.rectangle([px, py, px+pw, py+ph], fill=WHITE, outline=(120, 120, 120), width=2)
    d.text((px+14, py+8), "EQUIFAX", font=font(22), fill=(80, 80, 80))
    for i in range(3):
        ry = py+60+i*52
        d.rectangle([px+16, ry, px+pw-16, ry+38], outline=(170, 170, 170), width=2)
        d.line([(px+22, ry+8), (px+pw-22, ry+30)], fill=RED, width=9)
    d.text((px+pw-86, py+ph-58), "X3", font=font(64), fill=RED)

def flip_clock(img, num="60", unit="DAYS"):
    d = ImageDraw.Draw(img)
    bx, by, bw, bh = 120, 70, 300, 170
    d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=18, fill=(15, 15, 18))
    d.line([(bx, by+bh//2), (bx+bw, by+bh//2)], fill=(0, 0, 0), width=4)
    outlined(d, (bx+bw//2, by+bh//2-6), num, font(120), fill=WHITE, ow=2, anchor="mm")
    d.text((bx+bw//2, by+bh+22), unit, font=font(40), fill=GOLD, anchor="mm")

def verified_stamp(img):
    d = ImageDraw.Draw(img)
    px, py, pw, ph = 70, 70, 290, 210
    d.rectangle([px, py, px+pw, py+ph], fill=WHITE, outline=(120, 120, 120), width=2)
    for i in range(5):
        d.line([(px+20, py+30+i*34), (px+pw-20, py+30+i*34)], fill=(180, 180, 180), width=5)
    # red VERIFIED stamp tilted
    stamp = Image.new("RGBA", (220, 70), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([2, 2, 217, 67], outline=RED, width=5)
    sd.text((16, 16), "VERIFIED", font=font(34), fill=RED)
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (px+50, py+70), stamp)
    # red escalation arrow pointing down-right
    d.line([(px+pw-30, py+ph+6), (px+pw+70, py+ph+70)], fill=RED, width=12)
    d.polygon([(px+pw+70, py+ph+70), (px+pw+40, py+ph+62), (px+pw+64, py+ph+38)], fill=RED)

CONCEPTS = [
    ("concept1_sweep", "SWEEP", "THE FEDS DIDN'T. I DID.", "MY EXACT METHOD INSIDE", report_x),
    ("concept2_wiped", "WIPED", "3 BANKRUPTCIES AT ONCE", "A STRANGER RAN MY METHOD", report_x3),
    ("concept3_blocked", "BLOCKED", "GONE IN 60 DAYS", "VERIFIED 3X, THEN KEYS", flip_clock),
    ("concept4_verified", "VERIFIED", "ISN'T FINAL", "THE STEP THEY HOPE YOU MISS", verified_stamp),
]

os.makedirs("outputs/mockups", exist_ok=True)
paths = []
for name, punch, main, sub, hero in CONCEPTS:
    img = bg()
    img = subject(img)
    hero(img)
    text_block(img, punch, main, sub)
    d = ImageDraw.Draw(img)
    d.text((W-300, 16), "LAYOUT MOCKUP — not final render", font=font(18), fill=(140, 160, 200))
    p = f"outputs/mockups/{name}.png"
    img.save(p, "PNG")
    paths.append(p)
    print("saved", p)

# contact sheet
sheet = Image.new("RGB", (W+40, H*2+60), (8, 10, 18))
small = (W//2, H//2)
for i, p in enumerate(paths):
    im = Image.open(p).resize(small)
    x = 13 + (i % 2) * (small[0]+14)
    y = 20 + (i // 2) * (small[1]+20)
    sheet.paste(im, (x, y))
sheet.save("outputs/mockups/_all_four.png", "PNG")
print("saved outputs/mockups/_all_four.png")
