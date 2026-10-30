"""Bake the music bed: one or more tracks placed on the film's clock, each with a gain envelope, mixed, limited.

Usage: python3 -I music_bed.py bed.json
bed.json:
{
  "duration": 151.4,
  "out": "assets/audio/music.m4a",
  "tracks": [
    {"src": "music/gnossienne1.ogg", "at": 0, "from": 0, "fade_in": 0.8,
     "keys": [[0, 0.9], [113.9, 0.9], [115.7, 0]]},
    {"src": "music/arabesque1.ogg", "at": 117.2, "from": 2.39, "fade_in": 1.6, "fade_out": 2.4,
     "keys": [[117.2, 0.85], [138.0, 0.85], [139.7, 1.05]]}
  ]
}
- at:   film second where the track enters.  from: second inside the source file to start from (skip silence).
- keys: [film_second, gain] points, linear in between, held outside. Gain 1.0 = the file's own level.
- The last track's fade_out ends at "duration".
Target: the bed sits about 17 dB under a -15 LUFS voice (around -32 LUFS), swells to about -28 on the payoff.
Measure after:  ffmpeg -nostats -i <out> -af ebur128 -f null - 2>&1 | grep -A14 Summary
"""
import json
import subprocess
import sys


def gain_expr(keys, at):
    """Piecewise-linear gain in track-local time t (film time - at)."""
    pts = [(k[0] - at, k[1]) for k in keys]
    expr = f"{pts[-1][1]}"
    for (t0, g0), (t1, g1) in reversed(list(zip(pts, pts[1:]))):
        seg = f"{g0}+({g1}-{g0})*(t-{t0:.3f})/{max(t1 - t0, 1e-3):.3f}" if t1 > t0 else f"{g1}"
        expr = f"if(lt(t,{t1:.3f}),{seg},{expr})"
    return f"if(lt(t,{pts[0][0]:.3f}),{pts[0][1]},{expr})"


def main():
    spec = json.load(open(sys.argv[1]))
    dur = spec["duration"]
    args, chains, labels = [], [], []
    for i, tr in enumerate(spec["tracks"]):
        args += ["-i", tr["src"]]
        at, frm = tr.get("at", 0.0), tr.get("from", 0.0)
        length = dur - at
        f = [f"[{i}:a]atrim=start={frm}:end={frm + length:.3f}", "asetpts=PTS-STARTPTS", "aresample=48000",
             f"volume='{gain_expr(tr['keys'], at)}':eval=frame"]
        if tr.get("fade_in"):
            f.append(f"afade=t=in:st=0:d={tr['fade_in']}")
        if tr.get("fade_out"):
            f.append(f"afade=t=out:st={length - tr['fade_out']:.3f}:d={tr['fade_out']}")
        if at > 0:
            ms = int(round(at * 1000))
            f.append(f"adelay={ms}|{ms}")
        chains.append(",".join(f) + f"[t{i}]")
        labels.append(f"[t{i}]")
    mix = (f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest," if len(labels) > 1 else f"{labels[0]}anull,")
    graph = ";".join(chains) + ";" + mix + f"atrim=0:{dur},alimiter=limit=0.89[out]"
    cmd = ["ffmpeg", "-v", "error", "-y", *args, "-filter_complex", graph, "-map", "[out]", "-ac", "2",
           "-c:a", "aac", "-b:a", "192k", spec["out"]]
    subprocess.run(cmd, check=True)
    print("wrote", spec["out"])


if __name__ == "__main__":
    main()
