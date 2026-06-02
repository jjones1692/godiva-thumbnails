# CONCEPT_ENGINE.md
### Godiva Mindset — Thumbnail 3.0 concept brain

Read this after `GODIVA_THUMBNAIL_STYLE.md`. The style master governs how a thumbnail
looks. This file governs **what the concepts are and how they get chosen**, so
Claude Code can turn a script into a clean `concepts_<video>.json` with zero concept
input from James. He picks the winner from the finished renders. He does not
brainstorm concepts.

---

## RULE 0 — SPECIFICITY OR IT FAILS

Video 1's `candid_verified` won on concrete artifacts pulled from the real story: the
held VERIFIED letter, the 762 on the updated report, the page stamped DELETED on the
desk. Specific gets clicked. Generic is invisible.

Before writing any concept, mine **this script** for:
- **Numbers** — scores (762), dollars ($77K), day counts (4 days, 14 days), counts of deletions.
- **Documents / artifacts** — the exact paper, letter, portal, form, stamp, or screen the story turns on.
- **Named entities** — FTC, the bureaus, a lender, a portal, a government action (shutdown).
- **The emotional turn** — the precise moment of loss or win.

A concept that could be pasted onto a different video without changing a word is **banned**.
No "man stressed at a credit report." No "person celebrating." Pull the real object out
of the script and put it in the frame.

---

## THE CONCEPT SCHEMA (this is what render_nb2.py and finish_text.py actually read)

Write `concepts_<video>.json` as a JSON array of objects. Default **4** concepts. The
count is flexible from 4 up to a ceiling of **6**, set by James per video (`build.py
--count N`, or the autopilot trigger `autopilot video N count 6`). Four is the turnkey
default and the fast-decision sweet spot. Use 5 or 6 only when a video genuinely earns
wider exploration. Never exceed 6: beyond that the framing and component axes run out of
distinct combinations and concepts start repeating, which brings back the sameness the
whole system exists to prevent. Whatever the count, every concept must stay genuinely
distinct per the DIVERSITY MANDATE.

```json
{
  "name": "v2_candid_verified",
  "style": "engineered_candid",
  "framing": "centered",
  "pose": "presenting",
  "component": "stamped_document",
  "punch": "DELETED",
  "main": "VERIFIED IS NOT FINAL",
  "sub": "THE STEP THEY SKIP",
  "left": "specific problem artifact pulled from the script, red/shadow zone",
  "right": "specific solution artifact pulled from the script, green/gold/cream zone",
  "expression": "knowing confident look mid-explanation",
  "ghost": false
}
```

Field rules:
- **name** — `v<N>_<lanetag>`, unique across the set. The renderer writes `outputs/<name>.png` and the finisher writes `outputs/<name>_final.png`.
- **style** — one of the six lanes (below). First object is always `engineered_candid`.
- **framing** — the SILHOUETTE of the shot. One of `centered`, `tight_face`, `subject_left`, `subject_right`, `split`. A range lever; see the DIVERSITY MANDATE below.
- **pose** — the GESTURE. One of `authority`, `presenting`, `pointing`, `open_palm`, `considering`. This maps to which gesture still James shot for the video (see the gesture kit below). Gesture is the strongest eye-grab lever, but it is REAL only when the source still shows it. Do not invent a gesture the still does not have; that is where AI hands break and the likeness drifts. If only one still exists for a video, set every concept to the pose that still actually shows and rely on framing, component, and expression for range instead.
- **component** — the ELEMENT TYPE carried in the frame. One of `stamped_document`, `interface_panel`, `before_after_card`, `notification`, `hero_object`, `marked_up_document`. This is what makes the concepts feel like different ideas rather than the same document. See the component library and the DIVERSITY MANDATE.
- **punch** — one hard word (DELETED, BLOCKED, BACK, WIPED). Only drawn when `ghost` is true, as the low-opacity background title card. Still set it; it costs nothing and arms the ghost option.
- **main** — the headline. Emotion / problem. First person, specific, an outcome and a time frame where the script gives one.
- **sub** — the solution / method line, in gold.
- **left** — LEFT zone hero prop. The problem artifact. Specific.
- **right** — RIGHT zone hero prop. The solution artifact. Specific.
- **expression** — James's FACE only (the look in his eyes and mouth), distinct from `pose` which is his hands and body. Never describe altering his face, beard, glasses, durag/beanie, chain, or shirt. The renderer's face refinement handles slimming and cleanup. Vary it across the set: calm-intense, knowing, serious, quietly confident.
- **ghost** — keep `false`. The faint background word competes with the stamped headline and reads muddy over a cutout subject on a busy background. Do not use it unless James explicitly asks for it on a specific concept. A `cinematic_text` concept gets its distinctiveness from framing and embedded composition, not from a ghost overlay.

Do not invent fields. These are the contract.

---

## THE LANES

Six style keys exist: `engineered_candid`, `cinematic_text`, `interface_trust`,
`anti_thumbnail`, `transformation_arc`, `classic`.

- **Object 1 is always `engineered_candid`.** The proven workhorse. Always present.
- **The rest** are the best-fitting lanes for this script, chosen from the remaining five
  for contrast. The finals should be different bets on why a viewer clicks, not one idea
  several ways.

Pick from these by what the script supports:
- `interface_trust` — the win is provable on a screen, portal, or document (scores, APPROVED, DELETED, BLOCKED/VERIFIED states).
- `anti_thumbnail` — the hook is absence or gloom: went dark, disappeared, shutdown, denial, "came back."
- `cinematic_text` — one dramatic line worth embedding into the scene like a film title.
- `transformation_arc` — **reach for this whenever the script has a clean numeric or status jump**: a score moving X to Y, denied to approved, $0 to a funded figure, broke to a result. Build it as the SAME artifact at two values: `left` is the low state, `right` is the high state of that same object (a 512 report on the left, a 762 report on the right). The render adds one gold or cream arrow, never guru red. This is proof laid side by side, not hype. If a script has no real before/after number or status, do not force this lane.
- `classic` — the cleanest direct red-problem / gold-solution split tells it best.

---

## THREE-ZONE MAPPING (every concept)

- **LEFT (`left`) = problem.** Red / shadow. The loss, denial, or the artifact of the pain.
- **CENTER = James.** Brightest, sharpest. The still, refined by the renderer.
- **RIGHT (`right`) = solution.** Green / gold / cream. The proof, win, or result document.

One hero element per zone. No duplicate hero prop across the concepts. No fake body
text inside a prop, only a short label plus one stamp or one number.

---

## CAPTION RULES (main / sub)

- main = emotion/problem, sub = solution. No em dashes. First person, specific, grounded.
- No generic marketing phrases. Banned: "$0 FLUFF", "100% LEGAL", "GUARANTEED", anything low-trust.
- "Family" if an address is needed. Never "King".
- Keep main to one clean block, short enough to read at a glance.

---

## COMPONENT LIBRARY (the element types, one per concept)

These are the trust-grade equivalents of what makes a varied grid catch the eye. Range
filtered to a credit authority a skeptical audience trusts. Each concept carries ONE
`component`. Across the set, use DIFFERENT ones.

- `stamped_document` — a real bureau letter or dispute page with a single stamp word (DELETED, VERIFIED, BLOCKED, DENIED). The workhorse.
- `interface_panel` — a realistic bureau or portal screen: a score field, a status chip, a clean back-end panel. Borrows the credibility of the real format.
- `before_after_card` — two comparable values of the same artifact, low then high (a 512 report and a 762 report, a $0 and a funded figure). Pairs with `split` framing.
- `notification` — a single alert or message: a funding-approved text, a bureau update alert, a short message-request stack. Keep it sparse, no legible body text, one number or status only.
- `hero_object` — one dominant grounded object that stands for the win: a building, a set of keys, a funded account card. Pairs with `subject_left`/`subject_right`.
- `marked_up_document` — a real document with ONE clause circled or one line highlighted, like a teacher marking the key thing.

Banned, off-brand for this audience: tier lists, rainbow rankings, burning maps, surreal
gimmicks, lifestyle flex props (stacks of cash fanned for show, lying back). Those read as
guru bait to a burned audience.

## ENVATO ASSETS (real assets layered on top, for crispness)

Generated props soften and garble text. For the components where sharpness is the trust
signal, use a REAL Envato asset layered on top of the NB2 scene instead of letting the
model draw it. Priority components:

- `interface_panel` — real UI / dashboard / app-screen mockup.
- `stamped_document` / `marked_up_document` — real rubber-stamp or document graphic.
- `before_after_card` — real chart / graph / data-card asset.

Leave `hero_object` and atmosphere (buildings, keys, lighting, the man) to NB2; a stock
comp looks pasted, NB2 renders it into the scene light.

When a concept should use a real asset, add an `asset` block:

```json
"asset": { "type": "interface_panel", "id": "<envato_id>", "zone": "right", "scale": 0.46 }
```

- `id` — the Elements item id. Claude Code resolves and downloads it via the connected
  Envato MCP into `assets/envato/<id>.png` before the build.
- `zone` — left | right | center | full, matched to framing (split -> after-state right;
  tight_face -> a panel behind one shoulder, never over the face).
- `scale` — fraction of canvas width, 0.2 to 0.55.

`finish_text.py` layers the asset AFTER the scene render and BEFORE the headline, so it
stays pixel-sharp and text sits on top. Missing file = build still finishes the scene and
notes it. Keep the NB2 scene description light in whatever zone an asset will cover.

DISCOVERY NOTE: the Elements MCP is the path that both finds and downloads Elements assets.
The optional ENVATO_API_TOKEN in .env only searches the Envato MARKET catalog (metadata,
no Elements download); it is a lookup convenience, not the asset source.

## GESTURE KIT (the `pose` values, real only if shot)

These map to the stills James shoots on record day. Composed, never guru. See
`GESTURE_KIT.md` for the full shot list.

- `authority` — arms settled or lightly crossed, calm, no prop in hand. The baseline.
- `presenting` — holding or presenting the document toward camera. Pairs with `engineered_candid`.
- `pointing` — pointing at the evidence or the number, directing the eye.
- `open_palm` — one open palm, "here is the truth," mid-explanation.
- `considering` — hand near chin, weighing something, serious.

If the video has only one still, every concept uses the one pose that still shows. Never
prompt a gesture the still does not contain.

---

## DIVERSITY MANDATE — THE SET MUST NOT LOOK ALIKE

The recurring failure: valid lanes still render as versions of one picture, because
subject placement, prop load, and color temperature stay constant. A batch is a menu
James picks from. If they look the same, he is choosing between clones, not alternatives.
Channel-level consistency (palette, face treatment, bottom headline, Cutout Pop) stays
constant. Inside a single batch, the composition must diverge.

Across the concepts (call the count N, default 4, max 6), you MUST vary these axes:

1. **Framing** — use at least THREE distinct `framing` values, and as N grows toward 6,
   spread across more of the five. Never give them all `centered`. A strong 4 spread:
   - one `centered` (the classic flanked three-zone, the dark anchor),
   - one `split` (a true before/after, almost always the `transformation_arc` concept),
   - one `tight_face` (big intense portrait, one cue, usually `anti_thumbnail` or `interface_trust`),
   - one `subject_left` or `subject_right` (off-center single hero, great for vision beats).
   At N=5-6, add the remaining framings rather than repeating one.

2. **Component** — use N DISTINCT `component` types, one per concept, no repeats. There are
   six types, which is exactly why the ceiling is six: at N=6 every concept gets its own
   component and none repeat. This is the eye-grab lever. Different words on the same
   document is NOT a different component.

3. **Pose and expression** — vary the gesture and the face so the man is not doing the same
   thing twice. Pose is real only if the still shows it (see the gesture kit); if only one
   still exists, hold pose constant and lean harder on framing and component. Expression
   should still shift across the set even on a single still.

4. **Background temperature** — not all warm-brown. At least one COLD/dark frame and at
   least one WARM frame. The dark one is often the strongest and most distinct; keep it.

If any two concepts would sit side by side and read as the same picture, change one of
their framings or components before writing the file. Different lane is not enough.
Different silhouette and different element is the requirement, at any N.

## SELF-CHECK BEFORE WRITING THE FILE

1. Does each concept name a real number, document, or named entity from this script? (RULE 0)
2. Are the `main`/`right` pairs different bets, not one bet several ways?
3. DIVERSITY: at least three distinct `framing` values, N distinct `component` types, varied expression (and varied `pose` if more than one still exists), at least one cold and one warm frame? Would any two read as the same picture side by side? (If yes, fix.)
4. Is object 1 `engineered_candid`, and do the others fit the script?
5. No duplicate hero prop across the set?
6. No prop carries fake body text (label + one stamp/number only)?
7. Captions: main emotion, sub solution, no em dashes, no banned phrases, "Family" not "King"?
8. `ghost` is `false` unless James explicitly asked for it on a concept?
9. If a `transformation_arc` object is present: do `left` and `right` show the SAME artifact at two values (low then high), and does the script actually contain that numeric or status jump?

---

## NOMINATION (after the set renders)

Show James the finished `_final.png`, then nominate in tiers so the pick stays fast no
matter the count:
- **PRIMARY** — the most specific, highest-contrast bet. One line why.
- **A/B CHALLENGER** — the most *different* of the rest, ideally matching the video's literal hook. One line why.
- **Rest** — list the remaining names in one line, no per-image write-up. Backups, not a second decision.

James picks and ships. Stop there.
