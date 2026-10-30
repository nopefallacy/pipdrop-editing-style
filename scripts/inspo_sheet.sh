#!/usr/bin/env bash
# 1 fps contact sheets of reference reels, to read their layout grammar before planning.
# Usage: inspo_sheet.sh <dir_with_mp4s> <out_dir>
set -euo pipefail
mkdir -p "$2"
for f in "$1"/*.mp4; do n="$(basename "${f%.*}")"; ffmpeg -v error -y -i "$f" -vf "fps=1,scale=180:-1,tile=8x8" -frames:v 1 "$2/${n}_sheet.jpg"; echo "$2/${n}_sheet.jpg"; done
