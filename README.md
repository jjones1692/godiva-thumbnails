# Godiva Mindset — Thumbnail Kit

Drop in a still. Give the instructions. Get the thumbnail. That's the whole job.

---

## What's in this folder

- `godiva_thumbnail.py` — the engine. Calls Nano Banana 2, saves a 1280x720 thumbnail.
- `Godiva_Thumbnail_Prompt_System.md` — the playbook. How to write the instructions.
- `stills/` — put your raw photos here.
- `outputs/` — finished thumbnails land here.
- `requirements.txt`, `.env.example`, `.gitignore` — setup files, ignore unless setting up.

---

## One-time setup (do this once, ~5 minutes)

1. **Get your free key:** go to https://aistudio.google.com/apikey and copy the key.
2. **Open this folder in Claude Code.**
3. **Tell Claude Code:** "set up this thumbnail kit." It will install what's needed
   (`google-genai`, `pillow`) and save your key. When it asks for the key, paste it.

That's it. You never touch the setup again.

---

## Daily use — the part you actually care about

You have two ways. Both start the same: **put your raw photo in the `stills/` folder.**

### Way 1: Just talk to Claude Code (easiest)
Say something like:

> "Make a thumbnail from stills/myphoto.png. Title: How I Fixed My Credit in 30 Days.
>  Punch word DELETED. Main caption WIPED IT IN 30 DAYS. Sub HERE'S THE PLAYBOOK.
>  Graphic: a credit report with a big red X and a flip clock reading 30 DAYS."

Claude reads the playbook, builds the right prompt, runs it, and drops the finished
thumbnail in `outputs/`. Don't like it? Say "make the red X bigger" or "try 4 versions"
and it reruns.

### Way 2: Run the command yourself
```
python godiva_thumbnail.py --still stills/myphoto.png \
    --punch "DELETED" \
    --main "WIPED IT IN 30 DAYS" \
    --sub "HERE'S THE PLAYBOOK" \
    --graphic "credit report with a big red X, flip clock reading 30 DAYS" \
    --out outputs/credit_30days.png
```

Want to explore options before committing? Add `--tier base --concepts 4` to get four
cheap variations, pick the winner, then rerun the winner without those flags.

---

## Which model runs (already set for you)

- **Default = Nano Banana 2** (`gemini-3.1-flash-image-preview`). Newest, ~$0.045/image.
- `--tier base` = cheapest, for exploring 4 concepts (free tier ~500/day).
- `--tier pro` = use only if text ever comes out warped. Best text rendering, ~$0.134/image.

You don't have to set anything. Default just works.

---

## The 3 things that make a thumbnail land (from the playbook)

1. **Keep your face identical** — the prompt locks it so the model never gives you a stranger.
2. **One hero graphic** — red X, flip clock, approved stamp. One, not three. Clutter kills clicks.
3. **Sharp text** — three lines max, first-person, an outcome, a time frame. If text ever
   warps on a big video, switch to `--tier pro` or have Claude add the text in post.

Full detail lives in `Godiva_Thumbnail_Prompt_System.md`.

---

## Optional: back it up to GitHub (later, not required)

When you're ready to store/share the kit, in Claude Code just say "push this to a new
private GitHub repo." Your stills, outputs, and API key are already excluded by
`.gitignore`, so only the kit itself gets saved. Skip this until thumbnails are flowing.
