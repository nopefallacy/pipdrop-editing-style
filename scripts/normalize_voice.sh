#!/usr/bin/env bash
# Two-pass loudness normalisation of a talking-head take to -15 LUFS (-1.5 dBTP), video stream copied.
# Usage: normalize_voice.sh <in.mp4> <out.mp4>
set -euo pipefail
in="$1"; out="$2"
read -r I TP LRA TH OFF < <(ffmpeg -nostats -hide_banner -i "$in" -vn -af loudnorm=I=-15:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 \
  | python3 -c 'import sys,json,re; d=json.loads(re.search(r"\{[^{}]*\}", sys.stdin.read(), re.S).group(0)); print(d["input_i"], d["input_tp"], d["input_lra"], d["input_thresh"], d["target_offset"])')
echo "measured: I=${I} LUFS TP=${TP}"
ffmpeg -v error -y -i "$in" -map 0:v -map 0:a -c:v copy \
  -af "highpass=f=70,loudnorm=I=-15:TP=-1.5:LRA=11:measured_I=${I}:measured_TP=${TP}:measured_LRA=${LRA}:measured_thresh=${TH}:offset=${OFF}:linear=true" \
  -ar 48000 -c:a aac -b:a 256k -movflags +faststart "$out"
ffmpeg -nostats -i "$out" -vn -af ebur128=peak=true -f null - 2>&1 | grep -A14 Summary | grep -E "I:|Peak:"
