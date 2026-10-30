# 01 · The look

The footage is the ground. Everything added is quiet, warm and readable, so the pictures do the talking.

## Frame and safe zones (1080 × 1920, 30 fps)
- Platform UI: nothing readable above **168 px** (status/search bar) or under the right-hand button rail
  (x > 960 from about y = 1000 down). The bottom ~350 px carries the handle and caption, so only texture goes there.
- Measure each take's face with `scripts/face_grid.sh`. Two takes from the same creator differed by 200 px:
  - Take A: hair top 430, eyes 890, chin 1250 → `card_cy` 760, `caption_top` 1345.
  - Take B: hair top 180, eyes 870, chin 1350 → `card_cy` 800, `caption_top` 1460.

## Captions
- Open Sans 600, 50 px, line-height 1.22, colour `#FFF4DC` (warm cream), max width 880 px, centred.
- Shadow `0 2px 4px rgba(0,0,0,.65), 0 0 18px rgba(0,0,0,.4)`. No box, no highlight, no per-word pop.
- Groups of 2-5 words. Break at sentence ends, commas, pauses ≥ 150 ms, or about 26 characters.
  Drop fillers ("uh", "um") from captions only; never cut them from the audio unless asked.
- Placed just under the chin, on the collar. Captions stay on over every layout, including full-bleed images.

## Display type
- EB Garamond italic 500 (bundled), cream `#FFF6E3`, 84-104 px, `text-wrap: balance`, same shadow as captions.
- Top-of-frame titles get a scrim: a linear gradient from rgba(0,0,0,.55) to 0 over the top 640 px.
- Titles land word by word (blur 6 px → 0 and opacity 0 → 1 in 0.13 s, 0.067-0.08 s apart, no slide), hold dead still, and blur out in 0.2 s.
- Handwriting (hook title only): Caveat 700 via baked glyph strokes, in the accent colour.

## Colour
- One accent: warm gold `#F4C66B`. It means "the answer": the deepest layer of the iceberg ("my mom"), the "me" bar when it wins,
  the end of the results line, the handwritten "why". Use it once or twice per film, never as decoration.
- Diagram ink is cream on a warm near-black veil `rgba(12,10,8,.86)` over the footage, so the speaker stays faintly visible.

## Cards and photos
- Cards: no border, 4 px radius, shadow `0 24px 60px rgba(0,0,0,.45)`, centred on `card_cy`.
  Portrait cards 700 wide (max 930 tall), square 820, landscape 920.
- Stack photos: cream frame (12 px `#f3eee4`, like a print), shadow `0 18px 44px rgba(0,0,0,.5)`, tilted ±2-5°.
- Every image fills its box (`object-fit: cover`). Choose `object-position` or a `zoom` crop so the subject sits where the eye lands.

## Motion numbers
- Card in: opacity 0.1 s plus scale 1.035 → 1 in 0.35 s (power3.out); out: 0.08 s fade, which reads as a cut.
- Inside every image: a slow push, 1.0 → 1.045 for cards and 1.0 → 1.07 for full-bleed, linear over the shot.
- Full-bleed in: blur 8 → 0 px plus opacity in 0.15 s. Top band: clip-path wipe down in 0.3 s, up in 0.2 s.
- Punch-ins on the A-roll: hard sets to 1.05-1.08 on emphasis, one slow 3-4 s push into the payoff line.
  Keep them off during `pip` and `green` windows.
- Nothing idles. Once landed, text holds still until it leaves.
