"""Download URLs: python3 -I fetch.py <out_dir> name.jpg=https://... [...]
Unsplash: https://images.unsplash.com/<photo-id>?w=1800&q=85 (free licence, no watermark)."""
import os, sys, urllib.request
UA = {"User-Agent": "Mozilla/5.0 (pipdrop-editing-style)"}
out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for pair in sys.argv[2:]:
    name, url = pair.split("=", 1)
    try:
        data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        open(os.path.join(out, name), "wb").write(data)
        print("ok", name, len(data))
    except Exception as e:
        print("FAIL", name, e)
