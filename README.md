# pipdrop editing style

A Claude Code skill for **picture-in-picture-drop** edits of vertical (9:16) talking-head reels, built in
[HyperFrames](https://hyperframes.heygen.com). The speaker tells a personal story, and on the exact word that names a feeling a
precise image drops over or around them: a fine-art painting for the inner world, the speaker's own photo for their life, a
clean photo for a plain metaphor. Quiet cream captions, an optional handwritten hook title with hand-drawn line boil, one
recurring diagram that comes back changed, and a public-domain piano bed that follows the story's turn.

Not over-edited: the face carries the confessions, the pictures carry the emotion.

## Install

```bash
git clone https://github.com/nopefallacy/pipdrop-editing-style ~/.claude/skills/pipdrop-editing-style
```
Claude Code picks it up automatically ("edit this pipdrop style", "put images over me like my inspo", "green screen me over a
photo collage", "B-roll metaphors for this story", "add a handwritten hook title"…).

Needs the HyperFrames CLI (`npx hyperframes`), ffmpeg and Python 3 with Pillow. The browser tool is used for Unsplash search.
The hook title uses HyperFrames' `hw-write-title` registry item for its baked Caveat glyphs.

## Layouts

| kind | what the viewer sees |
|---|---|
| `card` | one image centred over the face (the default beat) |
| `top` | a full-width band above the head, face visible |
| `full` | full-bleed image while the voice carries on |
| `vcard` / `vfull` | the speaker's own clips |
| `stack` | 2-5 framed photos dropping in on successive words |
| `collage` | a full-frame wall of photos |
| `pip` | an image fills the frame and the speaker drops into a corner window |
| `green` | the room vanishes and the speaker stands in front of a photo or collage (local matting) |
| `title` / `words` | a serif question or stacked lines at the top |
| `chart` / `bars` | a rising line, or two bars that change state |
| hook title | serif words + one handwritten word writing on, circled, boiling |

## What's inside

| path | what |
|---|---|
| `SKILL.md` | the bar, the workflow, the layout menu: read first |
| `references/01-the-look.md` | frame, safe zones, captions, type, colour, cards, motion numbers |
| `references/02-layouts.md` | every layout with placement numbers, timing and pitfalls |
| `references/03-metaphor-method.md` | the arc, the beat map, recurring devices, a metaphor bank from real edits |
| `references/04-sourcing.md` | own photos, Wikimedia Commons, Unsplash, what to avoid, HEIC/HDR fixes |
| `references/05-hook-title.md` | the handwritten title and its line boil |
| `references/06-sound.md` | voice loudness and a bed that follows the story |
| `references/07-build-check-render.md` | project layout, generator, check/snapshot loop, previews, cloud render |
| `references/08-quality-gates.md` | the checklist |
| `references/09-feedback-log.md` | the creator's feedback that shaped every rule |
| `template/build_edit.py` | the generator: every layout, captions, punch-ins, music, from one shot list |
| `template/hook-title.html` | the handwritten hook title (configurable lines) |
| `scripts/` | Wikimedia search/fetch, Unsplash search snippet, re-encode, contact sheets, voice loudness, HDR→SDR, music bed, green-screen cutout, face grid, motion preview clip |
| `examples/` | two finished edits as beat maps, a 26-second all-layouts demo config, the iceberg recurring scene |

## Notes

- No media is included: the reference reels, paintings, photos and music stay with the creator. The examples describe them in words,
  with their Wikimedia titles where they're public domain.
- `template/hook-title.html` adapts the pen-velocity ease, glyph masking and boil helpers from HyperFrames' `hw-write-title` /
  `hw-boil` registry items (Apache-2.0). See `NOTICE`.
- The skill improves with use: add new feedback to `references/09-feedback-log.md` and let it change the rules.
