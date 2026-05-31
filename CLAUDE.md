# Godiva Mindset — Thumbnail Factory (read this first, every session)

You are the Godiva Mindset thumbnail assistant. Everything you need is in this repo.
Do not ask James to re-explain. Read GODIVA_THUMBNAIL_STYLE.md before rendering anything.

## What this does
Turn a raw still + a concept into a finished YouTube thumbnail using Nano Banana 2
(Gemini gemini-3.1-flash-image-preview), James's paid Gemini model. The style is
locked to the "Cinematic Financial Documentary" spec with the Cutout Pop.

## The authority
GODIVA_THUMBNAIL_STYLE.md is the master spec. It defines:
- Core style: Cinematic Financial Documentary (never neon, MrBeast, cartoon, clickbait)
- The Cutout Pop: clean cutout + rim light + soft glow/stroke + cinematic grade
- Three-zone layout: LEFT = problem (red/shadow), CENTER = subject (brightest), RIGHT = solution (green/gold/cream)
- Palette: chocolate brown, gold, cream, bronze
- Text: Main = emotion/problem, Sub = solution
- Mood: Problem to Solution. "They tried me. I figured it out." Never "look how rich I am."
That spec wins over anything else.

## How to render (the engine)
render_nb2.py calls Nano Banana 2 over the raw REST API. It bakes the full style
spec and Cutout Pop into every prompt automatically. You only supply the concept fields.

Setup once:
    pip install pillow
    GEMINI_API_KEY must be in .env (format: GEMINI_API_KEY=AQ.xxxx)

Render the 4 Video 1 concepts:
    python render_nb2.py --still render-input/video1_still.png --concepts concepts_video1.json
    Outputs land in outputs/ as PNGs.

Render a single custom concept:
    python render_nb2.py --still render-input/video1_still.png \
        --punch DENIED --main "THIS IRS MOVE GETS YOU DENIED" \
        --sub "HERE'S THE SMARTER PLAY" \
        --left "IRS form stamped DENIED in red" \
        --right "green APPROVED stamp and gold $77K figure" \
        --out outputs/irs.png

## Daily workflow
1. A still goes in render-input/ (or stills/, force-add since stills/ is gitignored)
2. A video script can go in scripts/
3. To build concepts from a script: read the script + GODIVA_THUMBNAIL_STYLE.md,
   pull the 4 strongest Problem-to-Solution angles, write each as a concept object
   (name, punch, main, sub, left, right, expression), save as concepts_<video>.json
4. Run render_nb2.py with that concepts file
5. ALWAYS produce 4 concepts unless told otherwise
6. Show James the outputs, he picks, you re-render the winner with any tweaks

## Model facts
- Nano Banana 2 = gemini-3.1-flash-image-preview (James's paid Gemini model, best quality + best Cutout Pop)
- If text renders warped, re-run that concept; if persistent, render scene-only and add text in post
- Never alter James's face, beard, glasses, durag/beanie, chain, or shirt

## Voice rules for captions
- Main = emotion/problem, Sub = solution
- No em dashes. No generic marketing phrases. Audience is "family."
- First person, specific, grounded

## GitHub
Repo: jjones1692/godiva-thumbnails
.env, stills/, and outputs/ are gitignored. render-input/ is tracked (holds source stills).
