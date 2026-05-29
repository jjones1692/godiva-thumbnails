# GODIVA MINDSET — Thumbnail Prompt System (Nano Banana / Image-Edit Models)

A reusable system for turning a raw still into a finished, high-CTR YouTube thumbnail using an image-editing AI model (Nano Banana / Gemini 2.5 Flash Image, or equivalent). Fill in three slots, keep the brand constants locked, and you get a prompt of consistent quality every time.

**Confirmed engine:** Nano Banana 2 (`gemini-3.1-flash-image-preview`) is the default for generation. Drop to base Nano Banana (`gemini-2.5-flash-image`) for cheap 4-concept exploration (free tier ~500 images/day), and only reach for Nano Banana Pro (`gemini-3-pro-image-preview`) if text ever renders warped, since Pro is the documented best-in-class for text. At 1280x720, 4K output is wasted, so the real choice is text accuracy and price, not resolution. The companion script `godiva_thumbnail.py` runs all three via the `--tier` flag (`v2` / `base` / `pro`).

---

## 1. Core principle

The model keeps the person identical and rebuilds everything around them. That is the whole game.

- The AI touches the **photo and scene only**: cut the subject out of his real room, drop in a designed background, add the supporting graphic that visualizes the hook.
- Identity is **locked**: same face, beard, glasses, durag/beanie, gold chain, shirt. The prompt must say this explicitly or the model drifts the face.
- **Text is the weak point.** AI text rendering is where thumbnails look "distorted." Either spell every word exactly and accept iteration, or use the Two-Pass Workflow (Section 6) and add text crisp in post. Sharp, undistorted text is the standard. Never ship warped type.

If a result looks "AI," it is almost always one of two things: the face got altered, or the text warped. Guard both.

---

## 2. The master prompt template

Copy this. Replace only the **[BRACKETED]** slots. Leave the KEEP IDENTICAL block and the STYLE block mostly as-is.

```
Transform the attached photo of the man into a high-CTR 16:9 YouTube thumbnail.

KEEP THE MAN IDENTICAL. Do not change his face, beard, glasses, black
beanie/durag, gold Cuban link chain, or brown "Lauryn Hill" t-shirt (or
whatever he is wearing in the attached still). Keep his exact likeness and
expression. Cut him out of his original room, keep him sharp and in crisp
focus, and place him from the chest up, slightly right of center.

BACKGROUND: Replace the room with a dark, cinematic, deep-blue blurred studio
backdrop. Soft bokeh, subtle glowing shapes for depth, a moody vignette around
the edges, dramatic high-contrast lighting on the man so he pops off the
background.

SUPPORTING GRAPHIC: [DESCRIBE THE ONE VISUAL THAT PROVES THE HOOK — see Section 3.4].

TEXT (lower-center, must be spelled exactly, crisp and undistorted):
- "[MAIN PUNCH WORD]" in heavy black condensed uppercase, inside a solid
  bright-red rectangular highlight box.
- Directly below: "[MAIN CAPTION]" in massive white heavy condensed uppercase
  with a thick black outline.
- Below that, smaller: "[SUB-CAPTION]" in white condensed uppercase.

STYLE: Ultra-bold, dramatic, high contrast. Deep blue background, white text,
bright red accents, gold chain. Photorealistic sharp subject, zero blur on the
person, clean sharp text. Final image 1280x720.
```

---

## 3. Section-by-section guide

### 3.1 Format line
Always state it: high-CTR, 16:9, YouTube thumbnail, 1280x720. This anchors the model to the right shape and intent.

### 3.2 KEEP IDENTICAL (the subject lock)
The single most important block. List every identity marker visible in the still: face, beard, glasses, head covering, chain, shirt. End with "keep his exact likeness and expression." This is what stops the model from giving you a stranger who looks "kind of like you."
- Position: "from the chest up, slightly right of center" is the default that leaves room for text and a left-side graphic. Move him left if the graphic lives on the right.

### 3.3 BACKGROUND
Default is the brand look: dark, cinematic, deep-blue, blurred, bokeh, vignette, dramatic lighting on the subject. Keep it abstract so it never fights the text. Only change this if the topic demands a specific setting.

### 3.4 SUPPORTING GRAPHIC — the hook made visual
This is the slot that changes most per video. Pick ONE clear visual that proves the title at a glance. Describe it plainly and tell the model where it sits (left side, behind shoulder, etc.). Examples by topic:
- **Sweep / deletion / dispute:** white credit-report page, tilted, with a thick hand-drawn red marker X slashing through it.
- **Time-frame hook (X days / fast result):** black split-flap flip-clock reading the exact number, e.g. "04 DAYS."
- **Approval / funding:** a document or card stamped with a green "APPROVED" mark, or a rising score arrow.
- **CPN / profile build:** a clean ID/profile card graphic.
- **Denied vs smarter play:** split frame, red "DENIED" stamp on the left, green check on the right.

Rule: one hero graphic, not three. Clutter kills click-through.

### 3.5 TEXT — exact strings only
Type the words in quotes exactly as they should appear. Three lines max:
1. **Punch word** in a red box (the emotional trigger: DELETED, DENIED, APPROVED, FROZEN).
2. **Main caption** huge, white, black outline (the outcome).
3. **Sub-caption** smaller (the promise / method line).
Keep total words low. A thumbnail is read in under a second.

### 3.6 STYLE / palette
Locked. Deep blue background, white text, red accents, gold chain, photorealistic sharp subject, clean text, 1280x720. This is the brand fingerprint that makes every thumbnail recognizably Godiva Mindset.

---

## 4. Brand constants (lock these every time)

**Thumbnail palette** (distinct from the ebook palette):
- Deep Blue `#1D4ED8` — background base / brand
- Neutral Gray / Charcoal `#1E1E1E` — depth and shadow
- White `#F5F5F5` — primary text
- Alert Red `#C1272D` (or bright red) — problem, deletion, urgency callouts
- Approval Green `#00A86B` — solution / approved framing, when used
- Gold `#C99C3D` — brand accent (chain, logo, small touches)

**Type:** heavy condensed sans for all thumbnail text (Bebas Neue / Anton / Barlow Condensed feel). White with a thick black outline for max readability on any device.

**Copy voice (applies to the captions):**
- First person + specific outcome + time frame. This is the top-performing title formula. ("Deleted It All In 4 Days," "Approved With a CPN in 14 Days.")
- No em dashes anywhere. They read as AI to the audience.
- No generic marketing phrases ("$0 FLUFF," "100% LEGAL," etc.). They read as low-trust.
- Warm and grounded. Confident, not hypey.

**Layout defaults:** subject right-of-center, hero graphic on the open side, text block lower-center, text occupies roughly the bottom third to 40% of the frame.

**Product mapping** (for the CTA logic, not the thumbnail art itself):
- CPN / profile-building topics → Credit Alchemy Gold ($125)
- Credit sweep / dispute / bureau topics → The Sweep Protocol ($97)

---

## 5. Failure modes and mitigations

| Failure | Why it happens | Fix |
|---|---|---|
| Text misspelled or warped | AI models struggle with exact multi-line text + outlines | Two-Pass Workflow (Section 6), or regenerate and pick the clean one |
| Face looks "off" / like a different person | KEEP IDENTICAL block too weak | Strengthen the lock: name every feature, add "keep his exact likeness, do not alter his facial features" |
| Cluttered, hard to read | Too many graphics or too much text | One hero graphic, three text lines max |
| Subject looks soft or blurry | Model blurred the person with the background | Add "zero blur on the person, photorealistic sharp subject in crisp focus" |
| Wrong aspect ratio / bad crop | Model preserved the input shape | State 16:9 and 1280x720, crop in post if needed |
| Countdown / number is meaningless | Decorative timer that says nothing | Make the number reinforce the hook (e.g. "04 DAYS"), or drop it |

---

## 6. The Two-Pass Workflow (use when text must be perfect)

This guarantees the "sharp, clean, not distorted" standard.

**Pass 1 — Scene only (AI):**
Use the master prompt but replace the TEXT block with:
> "Leave the lower third of the image clean and empty for text to be added later. No text in the image."
The model produces the subject, background, and hero graphic with a clear text zone.

**Pass 2 — Text added in post (crisp):**
Drop the exact captions onto the clean zone afterward, in heavy condensed type, white with black outline, punch word in a red box. Rendered as real type, the text is pixel-sharp and never misspelled.

Use one-pass (text in the AI prompt) for speed and casual videos. Use two-pass for flagship videos where the thumbnail has to be clean.

---

## 7. Worked example — "How I Did a Credit Sweep in 4 Days"

**Inputs:**
- Raw still: brown Lauryn Hill shirt, durag, glasses, gold chain, neon-room background.
- Title: "How I Did a Credit Sweep in 4 Days (Full Breakdown)"
- Main caption: "Deleted It ALL in 4 Days"
- Sub-caption: "Here's My Exact Method"

**Filled prompt:**
```
Transform the attached photo of the man into a high-CTR 16:9 YouTube thumbnail.

KEEP THE MAN IDENTICAL. Do not change his face, beard, glasses, black
beanie/durag, gold Cuban link chain, or brown "Lauryn Hill" t-shirt. Keep his
exact likeness and expression. Cut him out of his original room, keep him sharp
and in crisp focus, and place him from the chest up, slightly right of center.

BACKGROUND: Replace the room with a dark, cinematic, deep-blue blurred studio
backdrop. Soft bokeh, subtle glowing shapes for depth, a moody vignette around
the edges, dramatic high-contrast lighting on the man so he pops off the
background.

SUPPORTING GRAPHIC: On the left side, add a white credit-report document page,
slightly tilted, with faint placeholder text lines and a small profile-photo
icon, and slash a thick bold hand-drawn red marker X straight across it. Behind
his right shoulder, add a black split-flap flip-clock countdown reading
"04 DAYS" with a small white label underneath.

TEXT (lower-center, must be spelled exactly, crisp and undistorted):
- "DELETED" in heavy black condensed uppercase, inside a solid bright-red
  rectangular highlight box.
- Directly below: "IT ALL IN 4 DAYS" in massive white heavy condensed uppercase
  with a thick black outline.
- Below that, smaller: "HERE'S MY EXACT METHOD" in white condensed uppercase.

STYLE: Ultra-bold, dramatic, high contrast. Deep blue background, white text,
bright red accents, gold chain. Photorealistic sharp subject, zero blur on the
person, clean sharp text. Final image 1280x720.
```

---

## 8. Quick checklist before you generate

1. Raw still attached? Highest resolution available?
2. Identity lock names every visible feature?
3. One hero graphic chosen that proves the hook?
4. Three text lines max, exact spelling, first-person + outcome + time frame?
5. No em dashes, no generic marketing phrases?
6. Palette and 1280x720 stated?
7. Text-perfect video? Use the Two-Pass Workflow.

---

*System notes: built from the Godiva Mindset Thumbnail 1.0 / 2.0 work. The AI handles photo and scene; text stays crisp. Update the palette or layout defaults here and every future thumbnail prompt inherits the change.*
