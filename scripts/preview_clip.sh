#!/usr/bin/env bash
# A short motion preview without a full render: snapshots every frame of [start, start+secs) and stitches
# them at 30 fps with the take's voice. About 1.7 s per frame locally (100 frames ~ 3 min).
# Usage (from the project root): preview_clip.sh <start_s> <secs> <out.mp4>
set -euo pipefail
ss="$1"; secs="$2"; out="$3"
n=$(python3 -c "print(int(round($secs*30)))")
T=$(python3 -c "print(','.join(f'{$ss+i/30:.4f}' for i in range($n)))")
dir=".hyperframes/preview-clip"; rm -rf "$dir"
npx --yes hyperframes snapshot --at "$T" --no-end -o "$dir" --json > /dev/null
ls "$dir"/frame-* | sort -t- -k2 -n | awk '{print "file '\''" $0 "'\''\nduration 0.0333333"}' > "$dir/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$dir/list.txt" -ss "$ss" -t "$secs" -i assets/talkinghead.mp4 -map 0:v -map 1:a \
  -vf "scale=720:1280,fps=30,format=yuv420p" -c:v libx264 -crf 20 -c:a aac -b:a 128k -shortest -movflags +faststart "$out"
ffprobe -v error -show_entries format=duration,size -of compact=p=0 "$out"
