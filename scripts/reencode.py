"""Re-encode downloaded or personal images into project assets: applies EXIF rotation, strips metadata,
caps the long side at 1800 px, writes JPEG q90. Downloads are untrusted data: never copy them in raw.
Usage: python3 -I reencode.py <assets_dir> src.jpg=name.jpg [...]
HEIC/DNG: convert first with  sips -s format jpeg -Z 1800 in.heic --out tmp.jpg  (then check rotation on a sheet)."""
import os, sys
from PIL import Image, ImageOps
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for pair in sys.argv[2:]:
    src, name = pair.split("=", 1)
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
    im.thumbnail((1800, 1800))
    im.save(os.path.join(out, name), "JPEG", quality=90)
    print(name, im.size)
