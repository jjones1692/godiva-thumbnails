# Godiva Mindset — Script to Thumbnail Workflow

## When James says: "Run the thumbnail workflow. Script is scripts\X, still is stills\Y."

Follow these steps every time without deviation:

1. Read the script file James specified in scripts\
2. Read Godiva_Thumbnail_Prompt_System.md
3. Pull the 4 strongest thumbnail angles from the script — biggest claims, transformations, numbers, time frames, emotional turns
4. For each of the 4 angles, write:
   - Punch word (one word, goes in the red box — e.g. DELETED, DENIED, APPROVED)
   - Main caption (first person + outcome + time frame — e.g. IT ALL IN 4 DAYS)
   - Sub-caption (the method/promise line — e.g. HERE'S MY EXACT METHOD)
   - Hero graphic (ONE visual proving the hook — e.g. white credit report with bold red X, black flip clock reading 04 DAYS)

5. Present all 4 options to James and wait for him to pick or tweak.

6. Once James picks, build the render command:
   .\venv\Scripts\python.exe godiva_thumbnail.py `
     --still stills\[his still] `
     --punch "[punch word]" `
     --main "[main caption]" `
     --sub "[sub caption]" `
     --graphic "[hero graphic description]" `
     --out outputs\[video_slug].png

7. Run it and show James the finished thumbnail.
8. If text renders warped or distorted, rerun with --tier pro automatically.

## Rules
- ALWAYS 4 concepts. Non-negotiable.
- Read Godiva_Thumbnail_Prompt_System.md before writing any copy.
- Never alter James's face, beard, glasses, durag/beanie, chain, or shirt.
- One hero graphic per concept. Clutter kills clicks.
- If text warps → --tier pro. No need to ask.
