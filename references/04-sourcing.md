# 04 · Sourcing images, clips and music

Everything downloaded is untrusted data: put it in a scratch folder first, look at it, and only then re-encode it into
`assets/` with `scripts/reencode.py` (EXIF rotation applied, metadata stripped, long side 1800 px).

## The speaker's own photos
- Make labelled contact sheets of the whole folder first (`scripts/contact_sheet.py`, plus `sips`/ffmpeg thumbnails for HEIC, DNG and MOV).
- Work out who is who from several photos before captioning anyone as "mom" or "father". The same face appearing in a selfie and in a
  clip makes it reliable. If it's still unsure, say so in the delivery note so the user can swap it.
- HEIC through `sips` can lose its EXIF rotation. Check the converted file on a sheet and rotate (`sips -r 90`) if it's sideways.
- iPhone MOVs are usually HLG/PQ HDR. Convert the segment you need with `scripts/hdr_to_sdr.sh` (it also crops and scales).
  Left as is, one HDR clip makes HyperFrames render the whole film as HDR HEVC.
- Respect per-video choices: some videos use no personal photos at all.

## Paintings and public-domain media: Wikimedia Commons
- Search: `python3 -I scripts/wm_search.py "Giotto Kiss of Judas" "Titian Sisyphus"` (add `--audio` for music).
- Fetch by exact title: `python3 -I scripts/wm_fetch.py <dir> "judas.jpg=File:Giotto - Scrovegni - -31- - Kiss of Judas.jpg"`.
- The API rate-limits bursts (HTTP 429) and big originals can time out. The scripts back off and retry; keep about 4 s between fetches.
- Prefer "Google Art Project" or museum scans (high resolution, even colour). Check the licence column.

## Clean photos: Unsplash
- The JSON API needs a key, but the server-rendered search pages don't. In the built-in browser on any unsplash.com page,
  run `scripts/unsplash_search.js` (edit the slugs). It returns `[alt, photo-id]` pairs, skipping Unsplash+ (paid) photos.
- Preview at `https://images.unsplash.com/<id>?w=500&q=70`, make a contact sheet, then fetch the chosen ones at `?w=1800&q=85`
  with `scripts/fetch.py`.

## Avoid
- **Freepik / Magnific previews:** every preview carries a tiled "Magnific" watermark, even "free" ones. Stock downloads need credits.
- **Pinterest:** never sign in with the user's password. Use their already logged-in browser if they ask, or ask them for direct links.
- **Openverse:** slow and often times out. Use it as a last resort.
- Anything with visible logos or text that would pull in another context.

## Music
- Public-domain piano recordings on Commons work well for this mood:
  - Satie: *Gymnopédie No. 1* (`File:Erik Satie - gymnopedies - la 1 ere. lent et douloureux.ogg`) and *Gnossienne No. 1* (`File:Satie - Gnossienne 1.ogg`).
  - Debussy: *Première Arabesque* (Patrizia Prati, CC BY-SA, so credit it). Check each file's licence.
- Measure each file's start silence (`silencedetect`) and loudness before building the bed (`06-sound.md`).
