#!/usr/bin/env bash
# iPhone clips are often HLG/PQ BT.2020. Left as is, HyperFrames promotes the WHOLE render to HDR HEVC.
# This converts a segment to SDR BT.709 H.264 with a keyframe every second (seek-safe).
# Usage: hdr_to_sdr.sh <in.MOV> <out.mp4> <start_s> <dur_s> [extra_vf e.g. "crop=2400:2160:300:0,scale=1200:1080"]
set -euo pipefail
in="$1"; out="$2"; ss="$3"; t="$4"; pre="${5:-scale=1080:1920}"
ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer,color_primaries -of compact=p=0 "$in"
ffmpeg -v error -y -ss "$ss" -t "$t" -i "$in" -an \
  -vf "${pre},fps=30,colorspace=all=bt709:iall=bt2020:itrc=bt2020-10:fast=0:format=yuv420p,eq=contrast=1.04:saturation=1.06" \
  -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -g 30 -movflags +faststart "$out"
ffprobe -v error -select_streams v:0 -show_entries stream=color_transfer,width,height -of compact=p=0 "$out"
