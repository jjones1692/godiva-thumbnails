# GODIVA THUMBNAIL STYLE — Master Spec

The authority for every Godiva Mindset thumbnail. Any prompt, render, or brief must answer to this document. When something conflicts, this wins.

---

## CORE STYLE: "Cinematic Financial Documentary"

A blend of personal breakthrough, financial transformation, documentary storytelling, and professional YouTube packaging. The thumbnail should feel like a still from a serious documentary about a real comeback, not a hype reel.

**Always:**
- Structured layouts
- Strong visual hierarchy
- Documentary feel
- Emotional storytelling

**Never:**
- Neon overload
- Loud MrBeast style
- Clickbait spam visuals
- Cartoon graphics

**Energy:** "They tried me. I figured it out." Never "Look how rich I am."

---

## THE CUTOUT POP (signature subject treatment)

The Godiva subject look. Fire all four parts together every time:

1. **Clean edge cutout** that lifts the subject off the background
2. **Subtle bright rim light** tracing the silhouette so he separates hard from the backdrop
3. **Soft outer glow or thin stroke** around that edge
4. **Cinematic color grade** tying subject and scene into one graded frame

Shorthand: when the brief says "give it the Cutout Pop," all four fire at once. This is what reads as premium and what the top credit and finance creators are chasing.

---

## THUMBNAIL LAYOUT SYSTEM

Three zones, left to right. This is the backbone of every composition.

### LEFT SIDE = PROBLEM
The thing working against the viewer.
- Examples: Denied, FTC, IRS, CFPB, rejection, bureau issue, application denial
- Colors: reds, dark shadows, problem visuals

### CENTER = THE SUBJECT (Godiva)
Always the brightest, sharpest, main-focus element. Expression carries the story.
- Expression options: holding nose, confident stare, shrugging, concerned look, direct eye contact
- He must always be the brightest element in the frame and in crisp focus (Cutout Pop applied)

### RIGHT SIDE = SOLUTION
The resolution, the win.
- Examples: Approved, funding, checkmark, approval stamp, $77k, winning strategy
- Colors: green, gold, cream

The eye should travel left (problem) to center (him) to right (solution). Problem to Solution in one glance.

---

## COLOR PHILOSOPHY

**Brand palette (primary):** Chocolate Brown, Gold, Cream, Bronze.

**Functional accents within the layout:**
- Problem zone (left): reds, dark shadows
- Solution zone (right): green, gold, cream

The deep-blue cinematic backdrop from earlier work can still serve as a neutral graded base, but the brand identity is chocolate/gold/cream/bronze. Lean into that warmth, away from cold neon.

---

## TEXT STRATEGY

Two lines. Main carries the emotion or problem, sub carries the solution.

- **Main Caption:** Emotion / Problem
- **Sub Caption:** Solution

Examples:
- Main: "They Denied Me For Being Poor." / Sub: "So I Forced a $77k Reset."
- Main: "This IRS Move Gets You Denied" / Sub: "Here's the Smarter Play"
- Main: "REINSERTED. AGAIN." / Sub: "How I Stopped It For Good."

Keep it tight. Heavy condensed type, strong hierarchy, the main line dominant.

---

## TRUST SIGNALS

Used to build credibility. Must be subtle and never overpower the thumbnail.
- FTC logo, CFPB logo, IRS forms, approval stamps, denied stamps, funding documents, credit reports

Purpose is believability, not decoration. One or two, placed in the problem or solution zone, never cluttering the center.

---

## THUMBNAIL MOOD FORMULA

Every thumbnail must communicate one transformation:
- Problem → Solution
- Denied → Approved
- Struggle → Victory
- Confusion → Strategy

If a concept doesn't carry one of these arcs, it isn't ready.

---

## THUMBNAIL PROMPT TEMPLATE

Every future thumbnail description follows this structure:

1. **Thumbnail Title**
2. **Text Captions**
   - Main Caption (emotion/problem)
   - Sub Caption (solution)
3. **Brand Color Palette**
4. **Visual Direction**
   - Left Side (problem)
   - Center (subject, Cutout Pop applied)
   - Right Side (solution)
5. **Lighting Direction**
6. **Overall Mood**
7. **Trust Signals**
8. **Final Vibe**

---

## WORKED EXAMPLE

**Thumbnail Title:** This IRS Move Gets You Denied, Here's the Smarter Play

**Text Captions:**
- Main: "THIS IRS MOVE GETS YOU DENIED"
- Sub: "HERE'S THE SMARTER PLAY"

**Brand Color Palette:** Chocolate brown, gold, cream, bronze. Red accents left, green/gold accents right.

**Visual Direction:**
- Left: IRS form stamped DENIED in red, dark shadow
- Center: Godiva, confident direct eye contact, brightest element, Cutout Pop applied
- Right: approval stamp and a gold funding figure on a cream-toned panel

**Lighting Direction:** Low-key, one main source, rim light tracing the subject for the Cutout Pop, warm documentary tone.

**Overall Mood:** Cinematic financial documentary. Serious, grounded, premium.

**Trust Signals:** IRS form (left), approval stamp (right). Subtle.

**Final Vibe:** "They tried me. I figured it out." Problem to solution in one glance.

---

*This spec governs the Godiva thumbnail system. The Cutout Pop is the subject treatment. The three-zone layout is the structure. Chocolate/gold/cream/bronze is the palette. Problem to Solution is the mood. Documentary, never hype.*

---

## STYLE VARIANTS (same layout, different visual bet)

The three-zone Problem/Center/Solution layout is the constant. The styling on top of it is the variable. Assign each concept a `style` so a set of 4 becomes 4 distinct bets you can A/B test, not one template with swapped words. Pulled from 2026 thumbnail research, filtered to what fits a credit authority.

- **cinematic_text** — Headline pulled INTO the scene, embedded in the lighting like a film title card. Three or four dominant words. Reads like a Netflix documentary still. Best for proof/number hooks.
- **interface_trust** — Side zones rendered as real official interfaces (FTC affidavit, bureau letter, approval portal with a real score). Borrows the credibility of the format itself. Best for document/method hooks.
- **anti_thumbnail** — Dark, quiet, restrained. Muted zones, deep shadow, subject tight with intense eye contact as the single brightest element. One short line. Wins by being calm in a loud feed. Best for comeback/silence/serious hooks.
- **engineered_candid** — Believable captured-moment look. Subject physically holding or reacting to the real prop. Side elements feel like real objects, not overlays. No loud stamps. Best for reveal/reaction hooks.
- **transformation_arc** — Explicit before-and-after with one clean gold or cream arrow, left low state to right high state, the SAME artifact at two values (a 512 report beside a 762 report, a DENIED screen beside an APPROVED one). Proof laid side by side, not a guru arrow. Gold/cream only, never bright red or yellow. Best for hooks with a clean numeric or status jump.
- **classic** — The standard designed three-zone composition with a lower-third text block. The recognizable baseline Godiva look.

Rejected from the research (off-brand for a trusted credit teacher): warped faces (signals psychological/identity-crisis content), maximalist clutter and rainbow tier-lists (fight the documentary calm), and hyperreal MrBeast smiles (the era the audience is tired of).

Set the style per concept in the concepts JSON, or pass `--style` for a single render.

---

## QUALITY RULES (what separates pro from AI-looking)

Learned from comparing AI renders against finished hand-made thumbnails. These are now enforced in the engine.

1. **No fake text in props (the #1 fix).** AI cannot render paragraph or body text; it always comes out as garbled gibberish and instantly looks amateur. Never put readable sentences inside documents, letters, reports, or screens. Props carry ONLY a bold stamp word (BLOCKED, APPROVED, DENIED, DELETED, VERIFIED), a logo or seal, one large number, a checkmark, or an arrow. Document bodies stay blank or softly blurred.
2. **One hero element per side zone, max.** No document stacks, no calendar-plus-phone-plus-arrow pileups. Generous negative space. Simplicity reads premium; clutter reads amateur.
3. **Headline as one clean block.** Never split the main caption across the subject's body. One unbroken line or a stacked block in open space. This is why the cleanest concepts always have single-line headlines.
4. **Cutout Pop must actually pop.** Visible bright rim light, crisp edge, the subject clearly the brightest and sharpest thing in frame.

If a fully hand-finished look is required (perfectly crisp document graphics, pixel-exact stamps), the highest-quality route is a hybrid: let Nano Banana generate the subject, background, and simple props, then layer precise text and clean stamp graphics in post (Canva). The rules above get pure-AI output most of the way there on their own.

---

## SUBJECT REFINEMENT (standing preference, applied every render)

Light, natural, photographic retouching is applied to the subject on every thumbnail. Identity stays locked, he must remain unmistakably the same man. The refinements:
- Slim cheeks and reduce facial / under-chin puffiness by 5 to 8 percent for a cleaner, more defined jawline (no more than that)
- Neaten the beard with crisp groomed edges, clean cheek line and defined neckline
- Remove wrinkles, fine lines, and creases (under-eye, forehead, around the mouth); de-puff the under-eye area
- Keep exact bone structure, nose, eyes, lips, skin tone, and natural skin texture; never plastic or airbrushed, never a new or younger or slimmer face

This is baked into the engine prompt. To adjust the amount, edit the FACE REFINEMENT block in render_nb2.py.
