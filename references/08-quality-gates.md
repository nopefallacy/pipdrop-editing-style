# 08 · Quality gates

Before anything goes to the user:

**Story**
- [ ] The turn is identified, and the accent colour appears only there (and on the hook's handwritten word, if used).
- [ ] Every overlay passes the stranger test: one sentence describes it, and it matches the feeling of its phrase.
- [ ] No image drags in another context (someone else's webinar, brand or screenshot). When in doubt, use the face.
- [ ] 20-40% of the runtime is on the face, including the confessions and direct questions.

**Frames**
- [ ] No overlay collides with the hook title, captions, or another overlay's edge (check the first card under a title).
- [ ] Captions sit under the chin in every frame. If the speaker leans in, the caption may touch the beard: lower `caption_top`.
- [ ] Every image fills its box and is cropped on its subject; nothing is sideways (HEIC) or watermarked.
- [ ] No nudity at the centre of the frame.
- [ ] Words stay between 168 px and the caption line, clear of the right-hand rail.

**Timing**
- [ ] Every overlay starts on the first syllable of its word and lasts at least 1.0 s (titles 0.5 s + 0.3 s a word).
- [ ] `check` reports 0 errors, and every warning is either fixed or explained.
- [ ] The PIP and green windows have no punch-ins inside them, and the speaker doesn't jump at the seams.

**Media**
- [ ] No HDR promotion (`check` → `hdr.autoPromotion` is null).
- [ ] Voice at about -15 LUFS; the bed about 17 dB under it; silence before the turn.
- [ ] The final file is under 300 MB, 1080 × 1920, the right duration, with a verified frame strip.

**Delivery note**
- [ ] Who is who in personal photos, and how sure you are.
- [ ] Sources and licences, especially for CC BY-SA music.
- [ ] Measured vs listened: sound is measured only.
