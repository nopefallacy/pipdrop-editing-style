"""Labelled contact sheet(s) of a folder of images, EXIF-rotated, 48 per sheet.
Usage: python3 -I contact_sheet.py <image_dir> <out_prefix>   ->  <out_prefix>_0.jpg, _1.jpg ...
Look at every sheet before choosing: rotation, faces, watermarks, who is who."""
import os, sys
from PIL import Image, ImageDraw, ImageOps
src, out = sys.argv[1], sys.argv[2]
files = sorted(f for f in os.listdir(src) if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")))
cols, cell, per = 8, 220, 48
for p in range(0, len(files), per):
    chunk = files[p:p + per]
    rows = (len(chunk) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + 16)), "white")
    d = ImageDraw.Draw(sheet)
    for i, f in enumerate(chunk):
        try:
            im = ImageOps.exif_transpose(Image.open(os.path.join(src, f))).convert("RGB")
        except Exception:
            continue
        im.thumbnail((cell - 6, cell - 6))
        x, y = (i % cols) * cell, (i // cols) * (cell + 16)
        sheet.paste(im, (x + 3 + (cell - 6 - im.width) // 2, y + 3 + (cell - 6 - im.height) // 2))
        d.text((x + 3, y + cell), f"{p + i}:{f[:28]}", fill="black")
    sheet.save(f"{out}_{p // per}.jpg", quality=85)
    print(f"{out}_{p // per}.jpg")
