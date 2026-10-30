#!/usr/bin/env bash
# Three gridded frames of the take (grid every 192 px at full scale) to measure where the face sits:
# hair top, eyes, mouth, chin. Set card_cy over the eyes/nose, caption_top just under the chin.
# Usage: face_grid.sh <aroll.mp4> <out.jpg> [t1 t2 t3]
set -euo pipefail
src="$1"; out="$2"; shift 2; ts=("${@:-}"); [ -z "${ts[0]:-}" ] && ts=(10 40 80)
tmp="$(mktemp -d)"; i=0
for t in "${ts[@]}"; do ffmpeg -v error -y -ss "$t" -i "$src" -frames:v 1 -vf "scale=360:-1,drawgrid=w=360:h=64:t=1:c=red@0.7" "$tmp/$i.jpg"; i=$((i+1)); done
ffmpeg -v error -y -i "$tmp/0.jpg" -i "$tmp/1.jpg" -i "$tmp/2.jpg" -filter_complex hstack=3 "$out"
echo "$out  (each grid line = 192 px of the 1920 frame)"
