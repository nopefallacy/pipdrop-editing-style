# 05 · The handwritten hook title (optional per video)

An opening line that tells the viewer what the reel will answer. Serif words, plus **one** handwritten word in the accent
colour that writes itself on in real pen order. A marker loop then circles it, and the drawing keeps a hand-drawn
"line boil" while it is on screen.

Examples: "What is your **why?**" · "**Why** you need to / trust in yourself".

Skip it when the first spoken line is already a perfect hook, or when the user says so. Ask if unsure.

## Setup
```bash
npx hyperframes add hw-write-title          # adds assets/baked/caveat-pen.js and assets/fonts/Caveat-700-latin.woff2
rm compositions/hw-write-title.html         # only its baked glyphs and font are used
cp <skill>/template/hook-title.html compositions/hook-title.html
```
In `tools/build_edit.py`: `CONFIG["extra_hosts"] = [("hook-title", 0, D, 20)]` (z 20 sits under the captions).

## Configure (the CONFIG block in hook-title.html)
- `lines`: rows of items, with exactly one `{hw: "..."}`:
  - `[[{serif: "What is your"}, {hw: "why?"}]]`
  - `[[{hw: "Why"}, {serif: "you need to"}], [{serif: "trust in yourself"}]]`
- `D` = slot length: keep `data-duration` (twice in the file) and the host duration equal. `exitAt` is about `D - 0.3`.
- `hwSize` 180-200, `serifSize` 88, `top` 178.
- Order: serif words before the handwriting appear first, the pen writes (about 1.25 s), the loop closes (0.5 s), and serif words
  after the handwriting fade in as the pen lifts.

## Placement
- Above the head, below the status bar. The block is about 230 px tall for one line and about 300 px for two.
- Move the first overlays below it with `cy` (cards) so nothing collides. Keep about 25 px of air.
- The loop overhangs the handwritten word by about 20% of its width: `hw-last` lines get right padding automatically.
  Check the loop clears the serif word next to it and stays inside the frame (~30 px margin).

## How the boil works (seek-safe)
- `step = floor(time × 30 / 3)`: a new drawing every 3 frames (10 a second, like hand-drawn animation).
- Per step: the handwriting jitters about 1.4 px and turns 0.45°, an SVG feTurbulence displacement re-seeds (edges wobble), and the loop
  path is regenerated with a new seed (5-pose cycle). It's all a function of timeline time, so scrubbing and rendering match.
- The handwriting is the baked Caveat outlines revealed through masks of their centreline strokes, with a pen-velocity ease
  (from HyperFrames' `hw-write-title`). Characters outside the baked table are skipped with a console warning.

## Verify
- Snapshot 4 times 0.1 s apart and stack them: the loop and the letters must differ slightly in each.
- Make a 3 s motion preview with `scripts/preview_clip.sh 0 3.3 renders/preview_title.mp4`.
