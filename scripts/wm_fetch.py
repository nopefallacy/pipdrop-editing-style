"""Download Wikimedia Commons files by exact title, 1800 px wide (originals for audio).
Usage: python3 -I wm_fetch.py <out_dir> "name.jpg=File:Exact Title.jpg" ...
Backs off on HTTP 429."""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
UA = {"User-Agent": "pipdrop-editing-style/1.0 (video research; github.com/nopefallacy/pipdrop-editing-style)"}

def get(url):
    for attempt in range(6):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=180).read()
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(8 * (attempt + 1))
                continue
            raise
        except (TimeoutError, OSError):  # big originals on a slow link: retry
            time.sleep(4 * (attempt + 1))
            continue
    raise RuntimeError("rate limited: " + url)

out = sys.argv[1]
os.makedirs(out, exist_ok=True)
for spec in sys.argv[2:]:
    name, title = spec.split("=", 1)
    if os.path.exists(os.path.join(out, name)):
        print("have", name); continue
    q = urllib.parse.urlencode({"action": "query", "format": "json", "titles": title, "prop": "imageinfo",
                                "iiprop": "url|size|mediatype", "iiurlwidth": 1800})
    p = list(json.loads(get("https://commons.wikimedia.org/w/api.php?" + q))["query"]["pages"].values())[0]
    if "imageinfo" not in p:
        print("MISSING", title); continue
    ii = p["imageinfo"][0]
    src = ii["url"] if ii.get("mediatype") == "AUDIO" else (ii.get("thumburl") or ii["url"])
    data = get(src)
    open(os.path.join(out, name), "wb").write(data)
    print("ok", name, ii.get("width"), ii.get("height"), len(data))
    time.sleep(4)
