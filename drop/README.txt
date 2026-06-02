DROP FOLDER — your inbox for new thumbnails.

To make thumbnails for a new video:
  1. Drop ONE still image (png/jpg) and ONE script (.txt or .md) into this folder.
  2. From the repo root, run:   python ingest.py
  3. Follow the single NEXT step it prints.

That's it. No paths, no renaming. ingest.py auto-numbers the video, places your
files, and backs up anything it would overwrite. To refresh an existing video,
run:  python ingest.py --video N

Multiple poses? Name extra stills with a pose tag (pointing.png, presenting.png,
authority.png, openpalm.png, considering.png) and they become gesture stills.
