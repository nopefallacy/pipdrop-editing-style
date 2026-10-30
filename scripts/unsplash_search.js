// Run in the browser (built-in browser pane, javascript tool) on any https://unsplash.com page.
// The JSON search API needs auth, but the server-rendered search pages do not.
// Returns, per query, [alt text, photo id] for free (non-Unsplash+) photos.
// Download with: https://images.unsplash.com/<photo-id>?w=1800&q=85  (preview first with ?w=500&q=70)
const qs = ["burnt-matches", "kintsugi", "person-in-maze"]; // slug form: words joined by "-"
const out = {};
for (const q of qs) {
  const h = await (await fetch("/s/photos/" + q)).text();
  const doc = new DOMParser().parseFromString(h, "text/html");
  out[q] = [...doc.querySelectorAll("figure")]
    .filter((f) => !f.innerText.includes("Unsplash+"))
    .map((f) => { const i = f.querySelector("img[srcset]"); return i ? [(i.alt || "").slice(0, 60), (i.getAttribute("src") || "").split("?")[0].replace("https://images.unsplash.com/", "")] : null; })
    .filter((x) => x && x[1].startsWith("photo"))
    .slice(0, 8);
}
JSON.stringify(out);
