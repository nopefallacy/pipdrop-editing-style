# 07 · Build, check, preview, render

## Project layout (inside the video's own folder)
```
video-N/
  <the raw take>.mp4
  edit/                      ← npx hyperframes init edit --video "<take>.mp4" --resolution portrait --skip-transcribe
    assets/talkinghead.mp4   ← voice-normalised take
    assets/transcript.json   ← word timings
    assets/web/ assets/img/ assets/video/ assets/cutout/ assets/audio/music.m4a
    tools/build_edit.py      ← copied from the skill's template/, holds the shot list
    compositions/            ← generated chapters + captions (+ hand-authored hook-title.html)
    SPEC.md  SHOTS.md  REVIEW.md
    renders/
```
`init` refuses a non-empty folder, so create `edit/` through it, then copy assets in.

## Generate
`python3 tools/build_edit.py` writes `index.html`, `compositions/ch-*.html`, `compositions/captions.html` and `SHOTS.md`.
- Chapters: group 2-6 overlays per sub-composition and alternate tracks (2, 3) so Studio lanes stay readable.
- Never time a `<video>` and its wrapper both. The generator already places timed videos inside untimed boxes, and keeps
  the green-screen cutout outside its timed background clip.
- `nested_media_start_basis_ambiguous` warnings on nested clips are expected: their times are local to the chapter.

## Check and look
1. `npx hyperframes check --json`: 0 errors. Read every warning: `line_unread` means hold the text longer;
   `gsap_fullscreen_overlay_starts_visible` means give the box `opacity: 0` in CSS.
2. `npx hyperframes snapshot --at t1,t2,… --no-end -o .hyperframes/snapX`: one frame inside every overlay, plus the seams. Read the contact sheets.
3. Motion that stills can't show (the boil, a PIP drop, a stack cascade): `scripts/preview_clip.sh <start> <secs> renders/preview.mp4`.
4. Fix, rebuild, re-snapshot only what changed.

## Render
- **Cloud (preferred).** On an 8 GB laptop a local render captures about 3.4 frames/s whatever the worker count (a 2-minute reel takes about 20 min).
  With a Modal pipeline like the creator's `hfcloud.py` (L4 GPU, several workers), a 2.5-minute reel renders in about 3.5 min.
  Two reels in parallel, each compressed in the cloud under Instagram's 300 MB limit and levelled to -14 LUFS, take about 12 min end to end:
  ```bash
  HF_MODAL_CPU=16 modal run <path>/hfcloud.py::deliver --projects "<abs edit dir>,<abs edit dir>" --name final --extra "--workers 4 --quality high"
  ```
  Output lands at `<project>/renders/<parent-folder>-<name>.mp4`; rename it. Pass `--workers` explicitly, because the auto picker can drop to 1.
  The cloud image may pin an older HyperFrames: check a frame strip of the first cloud render against the local preview.
- **Local fallback:** `npx hyperframes render --quality high --sdr -o renders/x.mp4`, then two-pass H.264 under 285 MB if it's bigger.
- Don't make low-res preview copies unless asked; send previews as short clips instead.

## Verify the file
- `ffprobe`: 1080 × 1920, H.264, bt709, the expected duration. Loudness: see `06-sound.md`.
- A 12-16-frame strip across the film: the title, a few overlays, the diagram, the end.
- Write `REVIEW.md`: creative calls, sources, what was measured vs looked at, the weakest shot, how to rebuild.
