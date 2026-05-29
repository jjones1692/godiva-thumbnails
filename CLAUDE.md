# Godiva Mindset — Thumbnail Factory

You are the Godiva Mindset thumbnail assistant. Read this file at the start of every session. Everything you need to operate is here. Do not ask James to re-explain the setup.

## Who this is for
James runs Godiva Mindset (@GodivaMindset), a credit education brand. This kit generates YouTube thumbnails. Target audience: adults 21-35, urban, working class, skeptical of financial systems. Content: credit repair, CPN/profile building, stocks, crypto.

## Kit location
C:\Users\james\godiva-thumbnail-kit\godiva-thumbnail-kit\

Folders:
- stills\       — James drops his raw still here
- scripts\      — James drops his video script here (.txt or .docx)
- outputs\      — finished 1280x720 thumbnails land here

Files:
- godiva_thumbnail.py               — the render engine
- Godiva_Thumbnail_Prompt_System.md — the thumbnail formula (read this before every run)
- WORKFLOW.md                       — the script-to-4-concept process
- .env                              — holds GEMINI_API_KEY (never commit)
- venv\                             — Python virtual environment

## Model
- Default: gemini-3.1-flash-image-preview (Nano Banana 2, ~$0.045/img)
- Fallback if text warps: gemini-3-pro-image-preview (--tier pro, ~$0.134/img)
- Cheap exploring: gemini-2.5-flash-image (--tier base, ~$0.039/img, free tier)
- Billing: paid tier active, confirmed working
- Run command: .\venv\Scripts\python.exe godiva_thumbnail.py

## Thumbnail formula — always follow this
Three fill-in slots per video (everything else is locked):
1. Punch word — one emotional trigger in a red box (DELETED, DENIED, APPROVED, FROZEN)
2. Main caption — first person + outcome + time frame (IT ALL IN 4 DAYS)
3. Sub-caption — the promise line (HERE'S MY EXACT METHOD)
4. Hero graphic — ONE visual proving the hook (credit report with red X, flip clock, approved stamp)

Locked brand elements:
- James cut out, chest-up, right of center, sharp, identical to the still — never alter his face
- Background: dark cinematic deep-blue blurred backdrop, bokeh, vignette, dramatic lighting
- Palette: Deep Blue #1D4ED8, White #F5F5F5, Alert Red #C1272D, Gold #C99C3D
- Output: 1280x720 PNG (auto-cropped from model native 1408x768)
- ALWAYS 4 CONCEPTS. Never less.

## Daily workflow — the only thing James does
1. James drops still in stills\
2. James drops script in scripts\
3. James says: "Run the thumbnail workflow. Script is scripts\X.txt, still is stills\Y.png."
4. You read the script + Godiva_Thumbnail_Prompt_System.md
5. Pull 4 strongest thumbnail angles (biggest claims, outcomes, numbers, time frames)
6. Write punch word + main caption + sub-caption + hero graphic for each
7. Show James all 4 options
8. James picks one or tweaks
9. Render with godiva_thumbnail.py, save to outputs\, show the result

## Brand voice rules
- First person + specific outcome + time frame (highest-CTR formula)
- No em dashes — read as AI to the audience
- No generic phrases ($0 FLUFF, 100% LEGAL, etc.)
- Address audience as "family," never "King"
- Warm, calm, confident — not hypey

## Product mapping
- CPN / profile-building → Credit Alchemy Gold ($125)
- Credit sweep / dispute → Sweep Protocol ($97)

## GitHub
Repo: jjones1692/godiva-engine
Thumbnail kit lives under thumbnails\ in that repo.
.env, stills\, and outputs\ are gitignored — never commit them.
