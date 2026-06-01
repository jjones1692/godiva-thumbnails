# GESTURE_KIT.md
### Godiva Mindset — record-day shot list for thumbnail range

Gesture is the strongest eye-grab lever and the one the engine cannot fake. If a gesture
is not in a real photo, the model has to invent hands, and invented hands are where AI
thumbnails fall apart (warped fingers, a hand that is not yours, the likeness drifting).
So we shoot the gestures. The engine assigns one per concept by the `pose` field.

Shoot these on every record day, same wardrobe, same lighting, so any of them can be
dropped into `render-input/` as the still for a concept.

## The five poses

1. **authority** — calm, arms relaxed at your sides or lightly crossed, nothing in hand.
   Settled, in control. This is the baseline and the safest default. Shoot this first.
   `render-input/videoN_authority.png`

2. **presenting** — holding a document or letter up toward the camera, as if showing the
   viewer the proof. Hands clearly visible, fingers clean. Hold a real page.
   `render-input/videoN_presenting.png`

3. **pointing** — pointing toward where the key element or number will sit (to your side,
   roughly where the prop lands). Direct, deliberate.
   `render-input/videoN_pointing.png`

4. **open_palm** — one open palm raised, calm "here is the truth" explaining gesture.
   `render-input/videoN_openpalm.png`

5. **considering** — a hand resting near your chin, weighing something, serious and quiet.
   `render-input/videoN_considering.png`

## Rules for the shoot

- Same shirt, chain, glasses, head covering, framing, and light across all five.
- Eyes to camera on authority, pointing, open_palm. Considering can look slightly off.
- Hands fully in frame and unobstructed on presenting, pointing, open_palm. Clean fingers,
  nothing cropping them. The model preserves what it sees; give it clean hands to keep.
- Keep it composed. No guru flex (no fanned cash, no lying back, no hands behind head).
- Minimum viable kit if you are short on time: shoot `authority` and `presenting`. Two
  poses already breaks the same-gesture sameness.

## How it connects

In a concept, `pose: "pointing"` tells the engine to use your pointing still and to
preserve those exact hands. The autopilot picks the still that matches each concept's
pose. If a video has only one still, every concept uses that one pose and range comes
from framing, component, and expression instead. Never set a `pose` you did not shoot.

## File naming the autopilot expects

`render-input/videoN_<pose>.png` where `<pose>` is one of:
`authority`, `presenting`, `pointing`, `openpalm`, `considering`.
A single fallback still at `render-input/videoN_still.png` is used for any pose not shot.
