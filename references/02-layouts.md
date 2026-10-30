# 02 · Layouts

All layouts are `kind`s in `template/build_edit.py`. Times are absolute seconds in the take. Each item sits in a
chapter (one sub-composition, about 3-6 items, chapters on alternating tracks).

## card (the default)
`dict(kind="card", src, ar, start, end, pos="50% 50%", zoom=(scale, "x% y%"), cy=None)`
- Covers the eyes and nose; the mouth and chin often stay visible, which keeps the speaker present.
- `zoom` crops into a detail (Judas and Jesus kissing: `(1.9, "41% 47%")`; the hands of *Creation of Adam*: `(2.1, "50% 40%")`).
- `cy` pushes a card down, for example under a hook title (`cy=905`).
- Length 1.2-3.5 s. Under 1.0 s it doesn't read; over 4 s it goes stale unless the image is the hero.

## top
`dict(kind="top", src, start, end, pos)`: a 1080 × 640 band from the top edge, face visible below. Use it for landscape
images (a desk, an office at night, a screenshot) and when the face's reaction matters at the same time.

## full
`dict(kind="full", src, start, end, pos, zoom, shake=t)`: the strongest beats. Portrait paintings crop beautifully
(Sisyphus, Daedalus, the Fall of Icarus). Landscape ones need `pos` on the subject (Friedrich's monk: `34% 50%`).
`shake` adds a decaying 0.5 s tremor (Hokusai's wave on "shook me").

## vcard / vfull
The speaker's own clips. Convert iPhone HDR first (`scripts/hdr_to_sdr.sh`), or the whole render turns HDR HEVC.
The `<video>` is the timed element; its box is an untimed wrapper.

## stack (several photos)
`dict(kind="stack", start, end, photos=[dict(src, ar, at, pos), ...], frame=True)`
- 2-5 framed prints drop in on successive words (`at` = each word's start), scattered with small tilts, overlapping.
  All leave together at `end`.
- Use it for lists said aloud ("my parents, my sister, my friends"), memories piling up, "all the times I…".
- Order the drops so the most important photo lands last (it ends on top).
- Slots and widths are tuned for `card_cy` 760-820; 4-5 photos reach from about y = 340 to 1260.

## collage (photo wall)
`dict(kind="collage", start, end, photos=[src, ...], cols=None, at=start)`
- Fills the frame with a grid (2 columns up to 4 photos, then 3), 6 px dark gutters. Cells cascade in 0.06 s apart, then the wall pushes in 5%.
- Use it for "everything", "my whole life", overwhelm and chaos, or a mood board of a world. It's dense, so give it at least 2.5 s.

## pip (picture-in-picture drop)
`dict(kind="pip", src, start, end, corner="tr", pos, video=False)`
- The image fills the frame and the speaker shrinks (0.55 s, power3.inOut) into a 400 × 520 rounded window with a cream ring,
  in a corner (`tl`, `tr`, `bl`, `br`). At the end the window grows back to full frame.
- How it's built: a muted copy of the take plays in the window (`data-media-start` = `start`), so lips stay in sync with the A-roll's voice.
  The window is a clip-path; the speaker is scaled and moved around `CONFIG["face"]`, so the face lands centred in the window.
- Use it when the speaker steps back to *show* something: a place, a painting they describe, "look at this".
- Pick the corner away from the image's subject. Avoid the bottom right on platforms with a button rail.

## green (green screen over photos)
`dict(kind="green", cutout="assets/cutout/x.webm", bg=[src, ...], start, end, scale=1.0, x=0, y=0)`
- The room disappears and the speaker stands in front of one image (`bg` with one item) or a collage (several).
- Make the cutout first: `scripts/cutout.sh assets/talkinghead.mp4 <start> <dur> assets/cutout/x.webm`. It's a transparent WebM
  from HyperFrames' local matting model, about 0.8-2 frames/s (75 frames ≈ 90 s on an M2), so keep segments to 2-6 s.
- The cutout is frame-aligned with the A-roll, so with `scale=1` the speaker doesn't move at the seams. Keep punch-ins off in the window.
  `scale` < 1 with `y` > 0 shrinks the speaker towards the bottom (pivot at the bottom centre).
- Use it for "I was surrounded by…", the inner world, dreams, placing the speaker inside a memory.

## title / words
- `title`: the thesis question, word by word on its spoken words (`words_at`). It may hold to the end of the film.
- `words`: stacked lines that appear as each is said ("a coach / a consultant / an expert", "36 hours, / 42 hours straight.").

## chart / bars (drawn diagrams)
- `chart`: a cream line drawn up to a gold point on "results". Use it once.
- `bars`: `head` plus two bars whose values change at spoken words: `steps=[(t, value, color?)]`. The second visit flips the story
  ("who I trusted" → "who I trust now", with "me" filling in gold). Over the footage at 86% veil.
- Custom recurring devices (an iceberg photo with labels, visited three times with a camera that descends) are hand-authored
  scenes mounted via `CONFIG["extra_hosts"]`. See `references/03-metaphor-method.md`.

## Hook title
Hand-authored `compositions/hook-title.html`, mounted with `extra_hosts`, z-index 20 (under the captions). See `05-hook-title.md`.

## Density
- About 25 overlays in 2 minutes, with 20-40% of the runtime on the face.
- Mix layouts so no three beats in a row share one. Cards are the bread; full-bleed, stack, PIP and green are spices.
