#!/usr/bin/env bash
# Green-screen cutout of the speaker for one segment: trims [start, start+dur) frame-exactly from the A-roll
# and removes the background with HyperFrames' local matting model -> transparent WebM.
# Use it in a `green` layout with media_start=0 and the SAME start/end. Keep punch-ins off during that window.
# Usage: cutout.sh <aroll.mp4> <start_s> <dur_s> <out.webm>
# First run downloads the model (~170 MB); about 0.8 frames/s at 1080p (CoreML on an M2), so keep segments short (2-6 s).
set -euo pipefail
src="$1"; ss="$2"; t="$3"; out="$4"
tmp="$(mktemp -d)/seg.mp4"
ffmpeg -v error -y -i "$src" -ss "$ss" -t "$t" -an -c:v libx264 -crf 14 -preset fast -pix_fmt yuv420p -g 30 "$tmp"
mkdir -p "$(dirname "$out")"
npx --yes hyperframes remove-background "$tmp" -o "$out" --quality best
ffprobe -v error -show_entries format=duration:stream=codec_name,pix_fmt -of compact=p=0 "$out"
