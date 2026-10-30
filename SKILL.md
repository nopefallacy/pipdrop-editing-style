---
name: pipdrop-editing-style
description: The creator's "pipdrop" (picture-in-picture drop) edit for vertical 9:16 talking-head reels in HyperFrames, built for personal storytelling. Precise found images drop over the speaker on the exact word that names them (fine-art paintings for the inner world, the speaker's own photos for their life, a few clean stock metaphors), as a centred card, a top band, full-bleed, a stack of several photos, a collage wall, a picture-in-picture window the speaker shrinks into, or a green-screen cutout of the speaker over a photo collage. Also covers a recurring drawn diagram (iceberg layers, two-bar comparisons, a rising line), an optional handwritten hook title that writes itself on with hand-drawn line boil, small cream captions, a public-domain piano bed that follows the story's turn, and a cloud render. Use this whenever the user wants a talking-head, vlog, story or coaching reel edited "pipdrop style", "like my inspo", "with images / photos / paintings / visual metaphors over me", "picture in picture", "green screen me over photos", wants B-roll or metaphor ideas for a personal story, an emotional reel that visualises pain, bonding or a turn, a hook title with a scribbled word, or drops a new take into a pipdrop video folder, even if they never name the style. Not for the 4:3 frosted-glass socialcontent edit or the origami-blue line-art edit.
---

# pipdrop editing style

A vertical talking-head reel where **the right picture arrives on the right word**. The speaker tells a personal
story. Each phrase that carries meaning gets one precise image, dropped over or around them: a painting for an
inner state, their own photo for their life, a clean photo for a plain metaphor. Small cream captions run
underneath. A soft public-domain piano bed follows the story's turn. It is *not* over-edited: the face carries
the stretches that need a face, and the pictures carry the emotion.

Read this file first. `references/` holds the depth, `template/` the working generator and title, `scripts/`
the sourcing, audio, cutout and preview helpers, and `examples/` two finished edits plus a layout demo.

## The bar (each rule came from real feedback, see `references/09-feedback-log.md`)

1. **Precise, not decorative.** An image earns its place only if a stranger, seeing it on that word, feels the
   sentence. "Betrayed by my mentor" gets Giotto's *Kiss of Judas* cropped to the kiss, not a sad stock face.
   Prefer the image that carries the *emotion* over the one that matches the *noun*.
2. **Context beats keyword.** If the literal subject belongs to someone else's context (another creator's
   webinar, a brand, a screenshot that drags in a different story), stay on the face. The user cut exactly
   these: *"different context, remove those images."*
3. **One beat, one picture, cut on the word.** Each overlay starts on the first syllable of the word that
   names it and ends before the next idea starts. Holding a picture past its sentence muddies the next one.
4. **Map the arc, not the sentences.** Find the story's turn first (the betrayal, the realisation, the answer).
   Then pick a visual family per act, for example bond → fall → repair, and one recurring device that returns
   changed (an iceberg visited three times, bars that flip). The gold accent appears only at the payoff.
5. **The face is a layout too.** Leave 20-40% of the runtime on the face: hooks, confessions, direct questions,
   "I really don't know how to…". Carry long face stretches with punch-ins, not filler images.
6. **Found images over drawn graphics.** Real paintings, real photos, the speaker's own photos and clips. Draw only
   what has no picture: a diagram, a number, a hand-written word.
7. **Readable on a phone, clear of the platform UI.** Words between 168 px and the caption line. Nothing important
   under the right-hand button rail. Every image fills its frame and has no watermark.
8. **The voice is the clock.** Work from word-level timings and snap every in/out to them.

## Workflow

1. **Set up inside the video's own folder:** `npx hyperframes init edit --video <take>` in `video-N/`, then move the
   take to `assets/talkinghead.mp4`. Normalise the voice to -15 LUFS (`scripts/normalize_voice.sh`).
2. **Read the references:** contact-sheet the inspiration reels (`scripts/inspo_sheet.sh`) and name their layout grammar.
3. **Transcribe** with word timings (`npx hyperframes transcribe … --json`, Parakeet if installed). Print it as
   `word@time` and read the whole story before planning.
4. **Measure the face** (`scripts/face_grid.sh`): hair top, eyes, chin. Set `card_cy`, `caption_top`, `face` in the config.
5. **Beat map:** the story's turn, the arc (2-4 acts), the recurring device, then a beat list:
   `time · phrase · emotion · image idea · layout`. Method and metaphor bank: `references/03-metaphor-method.md`.
6. **Decide the per-video switches** (ask if the request does not settle them): hook title yes/no and its words;
   personal photos yes/no (look at the photo folder on a contact sheet before deciding who is who); multi-photo
   stacks, collage, PIP drop or green screen where the story wants density; music on/off.
7. **Source** (`references/04-sourcing.md`): Wikimedia Commons for paintings and public-domain music, Unsplash for clean
   photos, the speaker's own folder. Look at a contact sheet of every candidate. Re-encode everything through `scripts/reencode.py`.
8. **Build:** copy `template/build_edit.py` to `tools/`, fill `CONFIG`, `CHAPTERS` and `PUNCHES`, then run it. Add the hook
   title (`references/05-hook-title.md`) and green-screen cutouts (`scripts/cutout.sh`) where planned. Bake the music bed
   (`scripts/music_bed.py`).
9. **Check and look:** `npx hyperframes check --json` (0 errors), then snapshot every overlay and every seam and fix what reads badly
   (`references/08-quality-gates.md`). For motion (the title's boil, a PIP drop), make a short clip with `scripts/preview_clip.sh`.
10. **Render in the cloud** when the user has a cloud pipeline (`references/07-build-check-render.md`), into Instagram's size
    limit, then verify the file: duration, loudness, a frame strip. Write `REVIEW.md` in the project.

## Layout menu (details and numbers: `references/02-layouts.md`)

| kind | what the viewer sees | reach for it when |
|---|---|---|
| `card` | one image centred over the face | the default beat: a painting, a photo, a metaphor |
| `top` | full-width band above the head, face visible | landscape images, screenshots, "where I was" |
| `full` | full-bleed image, the voice carries on | the strongest emotional beats; paintings |
| `vcard` / `vfull` | a clip in a card / full-bleed | the speaker's own footage (convert HDR first) |
| `stack` | 2-5 framed photos dropping in on successive words | lists, memories, "all of these…", montage beats |
| `collage` | a full-frame wall of photos | "everything", "my whole life", a busy or chaotic state |
| `pip` | an image fills the frame, the speaker drops into a corner window | the speaker steps back to *look at* something |
| `green` | the room vanishes and the speaker stands in front of photos | "I was surrounded by…", inner worlds, re-placing the speaker |
| `title` / `words` | serif question or stacked lines at the top | the thesis question, a list said aloud |
| `chart` / `bars` | a rising line / two bars that change state | results, "him vs me", before and after |
| hook title | handwritten word writing on, circled, line boil | the opening promise (optional per video) |

## What lives where

- `references/01-the-look.md`: captions, type, colour, cards, shadows, motion numbers.
- `references/02-layouts.md`: every layout with placement numbers, timing and pitfalls.
- `references/03-metaphor-method.md`: beat map, arc, recurring device, metaphor bank, what to leave on the face.
- `references/04-sourcing.md`: personal photos, Wikimedia, Unsplash, what to avoid, HEIC/HDR/rotation fixes.
- `references/05-hook-title.md`: the handwritten title, its line boil, placement and timing.
- `references/06-sound.md`: voice loudness, public-domain beds, the envelope that follows the story.
- `references/07-build-check-render.md`: project layout, generator, check/snapshot loop, previews, cloud render.
- `references/08-quality-gates.md`: the checklist before anything goes to the user.
- `references/09-feedback-log.md`: the creator's own feedback, oldest first.
- `template/`: `build_edit.py` (all layouts, captions, punch-ins) and `hook-title.html`.
- `examples/`: two finished edits as beat maps and configs, plus `layouts-demo.py` (every layout in 26 s).
