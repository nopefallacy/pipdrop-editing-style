# 06 · Sound

## Voice first
- Phone and webcam takes come in quiet (measured -27 to -29 LUFS). Normalise to **-15 LUFS, -1.5 dBTP** with two-pass loudnorm
  and a 70 Hz high-pass: `scripts/normalize_voice.sh in.mp4 assets/talkinghead.mp4` (the video stream is copied).
- Don't cut the take unless asked: these takes are tight. Fillers leave the captions, not the audio.

## The bed follows the story
- One soft piano piece per act. Brooding for the wound (Satie, *Gnossienne No. 1*), tender for the reflection
  (*Gymnopédie No. 1*), and a lift for the turn (Debussy, *Première Arabesque*).
- Sit it about 17 dB under the voice (≈ -32 LUFS integrated) and swell to about -28 on the payoff.
- **Stillness before the turn:** dip almost to silence 1-2 s before the key line ("But after further investigation…",
  "The underlying insight…"), then bring the next piece in on the turn.
- Fade out over the last 2-3 s, ending under the final title.
- Bake it with `scripts/music_bed.py bed.json`: tracks on the film's clock, `from` skips each file's leading silence,
  and `keys` are `[film_second, gain]` points.

```json
{"duration": 151.4, "out": "assets/audio/music.m4a", "tracks": [
  {"src": "music/gnossienne1.ogg", "at": 0, "from": 0, "fade_in": 0.8, "keys": [[0, 0.9], [113.9, 0.9], [115.7, 0]]},
  {"src": "music/arabesque1.ogg", "at": 117.2, "from": 2.39, "fade_in": 1.6, "fade_out": 2.4,
   "keys": [[117.2, 0.85], [138.0, 0.85], [139.7, 1.05]]}
]}
```

## Effects
None by default; the reference reels use none. If a moment truly needs one (the wave tremor), use a single soft low hit,
3-6 dB over the bed, landing one frame after the picture.

## Check
- `ffmpeg -nostats -i out.mp4 -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary`: about -15 LUFS integrated for the
  project render. The cloud delivery levels to -14 LUFS, -1 dBTP.
- Nobody can hear from here: say in the delivery note that loudness was measured, not listened to.
