"""Search Wikimedia Commons files. Prints title | size | licence for each hit.
Usage: python3 -I wm_search.py "Rodin Thinker" "Hokusai Great Wave" [--audio]
Paintings before 1900 are public domain; check the licence column anyway."""
import json, sys, time, urllib.parse, urllib.request
UA = {"User-Agent": "pipdrop-editing-style/1.0 (video research; github.com/nopefallacy/pipdrop-editing-style)"}
audio = "--audio" in sys.argv
for q in [a for a in sys.argv[1:] if a != "--audio"]:
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "generator": "search", "gsrsearch": q, "gsrnamespace": 6, "gsrlimit": 10,
        "prop": "imageinfo", "iiprop": "size|mediatype|extmetadata", "iiextmetadatafilter": "LicenseShortName"})
    d = json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30))
    print("==", q)
    for p in sorted(d.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 0)):
        ii = p.get("imageinfo", [{}])[0]
        if audio != (ii.get("mediatype") == "AUDIO"):
            continue
        lic = ii.get("extmetadata", {}).get("LicenseShortName", {}).get("value", "?")
        print(f"  {p['title']} | {ii.get('width')}x{ii.get('height')} | {lic}")
    time.sleep(1.5)  # Commons rate-limits bursts (HTTP 429)
