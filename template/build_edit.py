"""pipdrop edit generator: writes index.html + compositions/*.html for one talking-head reel.

Copy this file to <project>/tools/build_edit.py, edit the CONFIG / CHAPTERS / PUNCHES blocks,
then run it from the project root:   python3 tools/build_edit.py

Everything is absolute seconds in the talking-head clip (word times from assets/transcript.json).
Re-running overwrites the generated HTML: make timing changes here, not in Studio.
Hand-authored scenes (the hook title, a custom diagram) are mounted via CONFIG["extra_hosts"] and never overwritten.

Layout kinds (see references/02-layouts.md for when to use each):
  card    one image centred over the face            src, ar, [pos, zoom, cy]
  top     full-width band at the top, face visible   src, [pos]
  full    full-bleed image, voice carries on         src, [pos, zoom, shake]
  vcard   a clip in a card                           src, ar, [media_start]
  vfull   a full-bleed clip                          src, [media_start]
  stack   2-5 photos dropped in one by one           photos=[{src, ar, at, [pos]}], [frame]
  collage a full-frame wall of photos                photos=[src, ...], [cols, at]
  pip     image fills the frame, the speaker drops   src, [corner, video, media_start]
          into a window (picture-in-picture)
  green   speaker cut out over a photo / collage     cutout, bg=[src, ...], [scale, x, y]
  title   serif question at the top                  text, words_at
  words   stacked serif lines, one per spoken word   lines, at
  chart   a line drawn up to a gold point            draw_end, [label]
  bars    a two-bar comparison that changes state    head, bars=[{label, steps=[(t, value, [color])]}]
"""
import html
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H = 1080, 1920

# ---------------------------------------------------------------- project config (edit)
CONFIG = dict(
    duration=None,                      # None = the A-roll's length from ffprobe
    aroll="assets/talkinghead.mp4",     # voice normalised to -15 LUFS (scripts/normalize_voice.sh)
    music="assets/audio/music.m4a",     # baked bed (scripts/music_bed.py) or None
    transcript="assets/transcript.json",
    card_cy=800,       # card centre y: over the eyes/nose (measure with scripts/face_grid.sh)
    caption_top=1420,  # just under the chin, on the collar
    title_top=176,     # under the platform status bar (168 px)
    cam_origin="50% 42%",  # punch-in origin = the face
    face=(540, 806),   # face centre in the frame, used by the pip drop
    accent="#F4C66B",  # the one colour that means "the answer"; used once or twice per film
    extra_hosts=[      # hand-authored scenes: (id, start, duration, z)
        # ("hook-title", 0, 6.0, 20),
    ],
)

CHAPTERS = [
    # ("ch-hook", 2, [
    #     dict(kind="card", src="assets/web/x.jpg", ar=1.0, start=1.52, end=3.72, zoom=(1.9, "41% 47%")),
    # ]),
]

# A-roll punch-ins on the #cam wrapper: (time, scale, mode)  mode: set | to | push
PUNCHES = [
    # (0.96, 1.08, "to"), (2.32, 1.0, "set"),
]

# ---------------------------------------------------------------- engine (rarely edited)
FILLERS = {"uh", "um", "uh,", "um,", "erm"}


def probe_duration(path):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                             capture_output=True, text=True, check=True).stdout.strip()
        return round(float(out) - 0.03, 2)
    except Exception:
        raise SystemExit(f"set CONFIG['duration']: could not probe {path}")


DURATION = CONFIG["duration"] or probe_duration(os.path.join(ROOT, CONFIG["aroll"]))
ACCENT = CONFIG["accent"]


def fmt(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def card_rect(ar, cy=None):
    cy = CONFIG["card_cy"] if cy is None else cy
    if ar < 0.9:
        w = 700
        h = min(round(w / ar), 930)
    elif ar <= 1.2:
        w = 820
        h = round(w / ar)
    else:
        w = 920
        h = round(w / ar)
    return (W - w) // 2, cy - h // 2, w, h


def words_spans(text, prefix):
    return " ".join(f'<span id="{prefix}-w{i}" class="w">{html.escape(w)}</span>' for i, w in enumerate(text.split()))


def scene_file(cid, style, body, script):
    return f"""<template>
  <style>
    #root {{
      position: absolute;
      inset: 0;
    }}
{style}
  </style>
  <div id="root" data-composition-id="{cid}" data-width="{W}" data-height="{H}">
{body}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{script}
    window.__timelines["{cid}"] = tl;
  </script>
</template>
"""


CSS = f"""
    .ov {{ position: absolute; inset: 0; pointer-events: none; }}
    .card {{ position: absolute; overflow: hidden; border-radius: 4px; background: #0d0d0d;
            box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45); opacity: 0; }}
    .card img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .vbox {{ position: absolute; opacity: 0; }}
    .vbox video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover;
                  border-radius: 4px; box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45); }}
    .top {{ position: absolute; left: 0; top: 0; width: 1080px; height: 640px; overflow: hidden; background: #0d0d0d; }}
    .top img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .full {{ position: absolute; inset: 0; overflow: hidden; background: #000; opacity: 0; }}
    .full img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .fullv {{ position: absolute; inset: 0; opacity: 0; }}
    .fullv video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    .snap {{ position: absolute; overflow: hidden; background: #f3eee4; opacity: 0;
            box-shadow: 0 18px 44px rgba(0, 0, 0, 0.5); }}
    .snap.framed {{ padding: 12px 12px 12px 12px; }}
    .snap img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .wall {{ position: absolute; inset: 0; background: #0b0a09; overflow: hidden; }}
    .wall .cell {{ position: absolute; overflow: hidden; opacity: 0; }}
    .wall .cell img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
    .pipwin {{ position: absolute; inset: 0; }}
    .pipwin .lens {{ position: absolute; inset: 0; }}
    .pipwin video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    .pipring {{ position: absolute; border: 6px solid rgba(255, 246, 227, 0.92); border-radius: 30px;
               box-shadow: 0 18px 50px rgba(0, 0, 0, 0.5); opacity: 0; }}
    .cut {{ position: absolute; inset: 0; }}
    .cut video {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
    .scrim {{ position: absolute; left: 0; top: 0; width: 1080px; height: 640px;
             background: linear-gradient(180deg, rgba(0, 0, 0, 0.55) 0%, rgba(0, 0, 0, 0.22) 55%, rgba(0, 0, 0, 0) 100%); }}
    .title {{ position: absolute; left: 60px; top: {CONFIG["title_top"]}px; width: 960px; text-align: center;
             font-family: "EB Garamond", serif; font-style: italic; font-weight: 500; font-size: 92px;
             line-height: 1.05; letter-spacing: -0.01em; color: #FFF6E3; text-wrap: balance;
             text-shadow: 0 3px 18px rgba(0, 0, 0, 0.6), 0 1px 3px rgba(0, 0, 0, 0.5); }}
    .stack {{ position: absolute; left: 0; top: {CONFIG["title_top"]}px; width: 1080px; text-align: center;
             font-family: "EB Garamond", serif; font-style: italic; font-weight: 500; font-size: 104px;
             line-height: 1.08; color: #FFF6E3;
             text-shadow: 0 3px 18px rgba(0, 0, 0, 0.6), 0 1px 3px rgba(0, 0, 0, 0.5); }}
    .stack div {{ display: block; }}
    .w {{ display: inline-block; }}
    .chart {{ position: absolute; overflow: hidden; border-radius: 4px; background: #15120f; opacity: 0;
             box-shadow: 0 24px 60px rgba(0, 0, 0, 0.45); }}
    .chart .lab {{ position: absolute; left: 56px; top: 40px; font-family: "EB Garamond", serif; font-style: italic;
                  font-size: 60px; color: #FFF6E3; }}
    .chart svg {{ position: absolute; left: 0; top: 0; }}
    .veil {{ position: absolute; inset: 0; background: rgba(12, 10, 8, 0.86); opacity: 0; }}
    .bhead {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center;
             font-family: "EB Garamond", serif; font-style: italic; font-weight: 500; font-size: 66px;
             color: rgba(255, 246, 227, 0.78); opacity: 0; }}
    .blbl {{ position: absolute; left: 90px; font-family: "EB Garamond", serif; font-style: italic; font-weight: 500;
            font-size: 92px; line-height: 1; color: #FFF6E3; opacity: 0; }}
    .btrack {{ position: absolute; left: 90px; width: 900px; height: 96px; border-radius: 6px;
              background: rgba(255, 246, 227, 0.08); opacity: 0; }}
    .bbar {{ position: absolute; left: 0; top: 0; width: 900px; height: 96px; border-radius: 6px;
            transform-origin: 0% 50%; }}
"""

# scattered drop positions for a stack, relative to (540, card_cy): (dx, dy, rotation)
STACK_SLOTS = {
    1: [(0, 0, -2)],
    2: [(-150, -110, -4), (150, 130, 3.5)],
    3: [(-190, -200, -5), (180, -40, 4), (-50, 200, -2)],
    4: [(-200, -230, -5), (190, -170, 4), (-180, 170, 3), (190, 230, -4)],
    5: [(-200, -230, -5), (190, -170, 4), (-180, 170, 3), (190, 230, -4), (0, 0, 1.5)],
}
STACK_W = {1: 700, 2: 560, 3: 500, 4: 460, 5: 420}


def zoom_js(pid, it, d, s):
    if "zoom" in it:
        z, origin = it["zoom"]
        return (f'    tl.fromTo("#{pid}-img", {{ scale: {z}, transformOrigin: "{origin}" }}, '
                f'{{ scale: {round(z * 1.045, 3)}, duration: {fmt(d)}, ease: "none" }}, {fmt(s)});')
    push = 1.07 if it["kind"] == "full" else 1.045
    return f'    tl.fromTo("#{pid}-img", {{ scale: 1 }}, {{ scale: {push}, duration: {fmt(d)}, ease: "none" }}, {fmt(s)});'


def wall_cells(n, cols=None):
    """Grid that fills 1080x1920 with n photos (6 px gutters)."""
    cols = cols or (2 if n <= 4 else 3)
    rows = -(-n // cols)
    g = 6
    cw = (W - g * (cols + 1)) / cols
    ch = (H - g * (rows + 1)) / rows
    cells = []
    for i in range(n):
        r, c = divmod(i, cols)
        cells.append((round(g + c * (cw + g)), round(g + r * (ch + g)), round(cw), round(ch)))
    return cells


def build_wall(pid, photos, s, at=None, cols=None):
    """A collage wall; cells cascade in from `at` (local seconds)."""
    at = s if at is None else at
    cells = wall_cells(len(photos), cols)
    body = [f'      <div id="{pid}-wall" class="wall">']
    js = []
    for j, (src, (x, y, w, h)) in enumerate(zip(photos, cells)):
        body.append(f'        <div id="{pid}-c{j}" class="cell" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px">'
                    f'<img src="{src}" alt="" /></div>')
        js.append(f'    tl.fromTo("#{pid}-c{j}", {{ opacity: 0, scale: 1.08 }}, {{ opacity: 1, scale: 1, duration: 0.3, ease: "power3.out" }}, {fmt(at + j * 0.06)});')
    body.append("      </div>")
    return body, js


def build_chapter(cid, items):
    c0 = min(it["start"] for it in items)
    c1 = max(it["end"] for it in items)
    body, js = [], []
    for i, it in enumerate(items):
        k = it["kind"]
        s = round(it["start"] - c0, 3)
        d = round(it["end"] - it["start"], 3)
        e = s + d
        pid = f"{cid.replace('ch-', '')}-{i + 1}"
        pos = it.get("pos", "50% 50%")
        clip_open = f'    <div id="{pid}" class="clip ov" data-start="{fmt(s)}" data-duration="{fmt(d)}" data-track-index="{i}">'
        if k == "card":
            x, y, w, h = card_rect(it["ar"], it.get("cy"))
            body.append(f'''{clip_open}
      <div id="{pid}-box" class="card" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px">
        <img id="{pid}-img" src="{it['src']}" alt="" style="object-position: {pos}" />
      </div>
    </div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ opacity: 0, scale: 1.035 }}, {{ opacity: 1, duration: 0.1, ease: "none" }}, {fmt(s)});
    tl.fromTo("#{pid}-box", {{ scale: 1.035 }}, {{ scale: 1, duration: 0.35, ease: "power3.out", immediateRender: false }}, {fmt(s)});
{zoom_js(pid, it, d, s)}
    tl.to("#{pid}-box", {{ opacity: 0, duration: 0.08, ease: "power1.in" }}, {fmt(e - 0.09)});''')
        elif k == "top":
            body.append(f'''{clip_open}
      <div id="{pid}-box" class="top">
        <img id="{pid}-img" src="{it['src']}" alt="" style="object-position: {pos}" />
      </div>
    </div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ clipPath: "inset(0% 0% 100% 0%)" }}, {{ clipPath: "inset(0% 0% 0% 0%)", duration: 0.3, ease: "power3.out" }}, {fmt(s)});
    tl.fromTo("#{pid}-img", {{ scale: 1.06 }}, {{ scale: 1.0, duration: {fmt(d)}, ease: "none" }}, {fmt(s)});
    tl.to("#{pid}-box", {{ clipPath: "inset(0% 0% 100% 0%)", duration: 0.2, ease: "power2.in" }}, {fmt(e - 0.21)});''')
        elif k == "full":
            body.append(f'''{clip_open}
      <div id="{pid}-box" class="full">
        <img id="{pid}-img" src="{it['src']}" alt="" style="object-position: {pos}" />
      </div>
    </div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.15, ease: "power2.out" }}, {fmt(s)});
{zoom_js(pid, it, d, s)}
    tl.to("#{pid}-box", {{ opacity: 0, duration: 0.1, ease: "power1.in" }}, {fmt(e - 0.11)});''')
            if "shake" in it:
                t0 = it["shake"] - c0
                for j, a in enumerate([16, -14, 12, -10, 8, -6, 4, -2, 0]):
                    js.append(f'    tl.to("#{pid}-box", {{ x: {a}, y: {-a // 2}, duration: 0.055, ease: "sine.inOut" }}, {fmt(t0 + j * 0.055)});')
        elif k == "vcard":
            x, y, w, h = card_rect(it["ar"], it.get("cy"))
            body.append(f'''    <div id="{pid}-box" class="vbox" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px">
      <video id="{pid}" class="clip" src="{it['src']}" muted playsinline data-start="{fmt(s)}" data-duration="{fmt(d)}" data-media-start="{fmt(it.get('media_start', 0))}" data-track-index="{i}"></video>
    </div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ opacity: 0, scale: 1.035 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {fmt(s)});''')
        elif k == "vfull":
            body.append(f'''    <div id="{pid}-box" class="fullv">
      <video id="{pid}" class="clip" src="{it['src']}" muted playsinline data-start="{fmt(s)}" data-duration="{fmt(d)}" data-media-start="{fmt(it.get('media_start', 0))}" data-track-index="{i}"></video>
    </div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.18, ease: "power2.out" }}, {fmt(s)});''')
        elif k == "stack":
            photos = it["photos"]
            n = len(photos)
            w = STACK_W[min(n, 5)]
            framed = it.get("frame", True)
            body.append(clip_open)
            for j, ph in enumerate(photos):
                dx, dy, rot = STACK_SLOTS[min(n, 5)][j]
                ar = ph.get("ar", 1.0)
                h = min(round(w / ar), round(w * 1.3))
                x = 540 + dx - w // 2
                y = CONFIG["card_cy"] + dy - h // 2
                body.append(f'''      <div id="{pid}-p{j}" class="snap{' framed' if framed else ''}" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px">
        <img src="{ph['src']}" alt="" style="object-position: {ph.get('pos', '50% 50%')}" />
      </div>''')
                at = round(ph["at"] - c0, 3)
                js.append(f'    tl.fromTo("#{pid}-p{j}", {{ opacity: 0, scale: 1.12, rotation: {rot * 1.8:.1f}, y: -30 }}, '
                          f'{{ opacity: 1, scale: 1, rotation: {rot}, y: 0, duration: 0.32, ease: "power3.out" }}, {fmt(at)});')
            body.append("    </div>")
            js.append(f'    tl.to("#{pid} .snap", {{ opacity: 0, duration: 0.12, ease: "power1.in" }}, {fmt(e - 0.13)});')
        elif k == "collage":
            wb, wj = build_wall(pid, it["photos"], s, round(it.get("at", it["start"]) - c0, 3), it.get("cols"))
            body.append(clip_open)
            body += wb
            body.append("    </div>")
            js += wj
            js.append(f'    tl.fromTo("#{pid}-wall", {{ scale: 1 }}, {{ scale: 1.05, duration: {fmt(d)}, ease: "none" }}, {fmt(s)});')
            js.append(f'    tl.to("#{pid}-wall", {{ opacity: 0, duration: 0.15, ease: "power1.in" }}, {fmt(e - 0.16)});')
        elif k == "pip":
            # the frame fills with an image while the speaker shrinks into a window: the "PIP drop"
            corner = it.get("corner", "tr")
            ww, wh = 400, 520
            L = {"tl": 50, "bl": 50, "tr": W - 50 - ww, "br": W - 50 - ww}[corner]
            T = {"tl": 210, "tr": 210, "bl": 840, "br": 840}[corner]
            fx, fy = CONFIG["face"]
            sc = 0.46
            dx, dy = L + ww / 2 - fx, T + wh / 2 - fy
            ins = f"inset({T}px {W - L - ww}px {H - T - wh}px {L}px round 30px)"
            if it.get("video"):
                bg_html = (f'''    <div id="{pid}-box" class="fullv">
      <video id="{pid}-bgv" class="clip" src="{it["src"]}" muted playsinline data-start="{fmt(s)}" data-duration="{fmt(d)}" data-media-start="{fmt(it.get("bg_media_start", 0))}" data-track-index="{i}"></video>
    </div>''')
            else:
                bg_html = (f'''{clip_open}
      <div id="{pid}-box" class="full">
        <img id="{pid}-img" src="{it["src"]}" alt="" style="object-position: {pos}" />
      </div>
    </div>''')
            body.append(f'''{bg_html}
    <div id="{pid}-win" class="pipwin" style="clip-path: inset(0px 0px 0px 0px round 0px)">
      <div id="{pid}-lens" class="lens" style="transform-origin: {fx}px {fy}px">
        <video id="{pid}-me" class="clip" src="{CONFIG['aroll']}" muted playsinline data-start="{fmt(s)}" data-duration="{fmt(d)}" data-media-start="{fmt(it['start'])}" data-track-index="{i + 20}"></video>
      </div>
    </div>
    <div id="{pid}-ring" class="pipring" style="left: {L - 3}px; top: {T - 3}px; width: {ww + 6}px; height: {wh + 6}px"></div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05 }}, {fmt(s)});
    tl.fromTo("#{pid}-win", {{ clipPath: "inset(0px 0px 0px 0px round 0px)" }}, {{ clipPath: "{ins}", duration: 0.55, ease: "power3.inOut" }}, {fmt(s)});
    tl.fromTo("#{pid}-lens", {{ scale: 1, x: 0, y: 0 }}, {{ scale: {sc}, x: {dx:.0f}, y: {dy:.0f}, duration: 0.55, ease: "power3.inOut" }}, {fmt(s)});
    tl.fromTo("#{pid}-ring", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {fmt(s + 0.45)});''')
            if not it.get("video"):
                js.append(f'    tl.fromTo("#{pid}-img", {{ scale: 1.08 }}, {{ scale: 1.0, duration: {fmt(d)}, ease: "none" }}, {fmt(s)});')
            js.append(f'''    tl.to("#{pid}-ring", {{ opacity: 0, duration: 0.12 }}, {fmt(e - 0.55)});
    tl.to("#{pid}-win", {{ clipPath: "inset(0px 0px 0px 0px round 0px)", duration: 0.45, ease: "power3.inOut" }}, {fmt(e - 0.47)});
    tl.to("#{pid}-lens", {{ scale: 1, x: 0, y: 0, duration: 0.45, ease: "power3.inOut" }}, {fmt(e - 0.47)});''')
            if it.get("video"):  # an untimed box around a timed video: close it when the clip ends
                js.append(f'    tl.set("#{pid}-box", {{ opacity: 0 }}, {fmt(e)});')
        elif k == "green":
            # the room disappears behind the speaker: a photo (or collage) slides in under a cutout of them
            bg = it["bg"]
            body.append(clip_open)
            if len(bg) == 1:
                body.append(f'''      <div id="{pid}-box" class="full" style="opacity: 1"><img id="{pid}-img" src="{bg[0]}" alt="" style="object-position: {pos}" /></div>''')
                js.append(f'    tl.fromTo("#{pid}-box", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {fmt(s)});')
                js.append(f'    tl.fromTo("#{pid}-img", {{ scale: 1.1 }}, {{ scale: 1.0, duration: {fmt(d)}, ease: "none" }}, {fmt(s)});')
            else:
                wb, wj = build_wall(pid, bg, s, s, it.get("cols"))
                body += wb
                js += wj
            sc, gx, gy = it.get("scale", 1.0), it.get("x", 0), it.get("y", 0)
            # the cutout is a timed video, so it sits OUTSIDE the timed background clip (never time both)
            body.append(f'''    </div>
    <div id="{pid}-cut" class="cut" data-layout-allow-occlusion style="transform-origin: 50% 100%">
      <video id="{pid}-cv" class="clip" src="{it['cutout']}" muted playsinline data-start="{fmt(s)}" data-duration="{fmt(d)}" data-media-start="{fmt(it.get('media_start', 0))}" data-track-index="{i + 20}"></video>
    </div>''')
            if sc != 1.0 or gx or gy:
                js.append(f'    tl.fromTo("#{pid}-cut", {{ scale: 1, x: 0, y: 0 }}, {{ scale: {sc}, x: {gx}, y: {gy}, duration: 0.5, ease: "power3.inOut" }}, {fmt(s)});')
            js.append(f'    tl.to("#{pid} .wall, #{pid}-box", {{ opacity: 0, duration: 0.2, ease: "power1.in" }}, {fmt(e - 0.21)});')
        elif k == "title":
            body.append(f'''{clip_open}
      <div id="{pid}-scrim" class="scrim"></div>
      <div id="{pid}-text" class="title">{words_spans(it['text'], pid)}</div>
    </div>''')
            js.append(f'    tl.fromTo("#{pid}-scrim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {fmt(s)});')
            for j, wt in enumerate(it["words_at"]):
                js.append(f'    tl.fromTo("#{pid}-w{j}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power2.out" }}, {fmt(wt - c0)});')
            if it["end"] < DURATION - 0.01:
                js.append(f'    tl.to("#{pid}-text, #{pid}-scrim", {{ opacity: 0, filter: "blur(6px)", duration: 0.2, ease: "power2.in" }}, {fmt(e - 0.22)});')
        elif k == "words":
            lines = "\n".join(f'        <div id="{pid}-w{j}">{html.escape(t)}</div>' for j, t in enumerate(it["lines"]))
            body.append(f'''{clip_open}
      <div id="{pid}-scrim" class="scrim"></div>
      <div id="{pid}-text" class="stack">
{lines}
      </div>
    </div>''')
            js.append(f'    tl.fromTo("#{pid}-scrim", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.3, ease: "power2.out" }}, {fmt(s)});')
            for j, wt in enumerate(it["at"]):
                js.append(f'    tl.fromTo("#{pid}-w{j}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.15, ease: "power2.out" }}, {fmt(wt - c0)});')
            js.append(f'    tl.to("#{pid}-text, #{pid}-scrim", {{ opacity: 0, filter: "blur(6px)", duration: 0.2, ease: "power2.in" }}, {fmt(e - 0.22)});')
        elif k == "chart":
            x, y, w, h = card_rect(1.45, it.get("cy"))
            pts = [(70, 520), (190, 500), (300, 470), (400, 430), (500, 390), (600, 320), (690, 250), (770, 150), (850, 110)]
            path = "M " + " L ".join(f"{px} {py}" for px, py in pts)
            body.append(f'''{clip_open}
      <div id="{pid}-box" class="chart" style="left: {x}px; top: {y}px; width: {w}px; height: {h}px">
        <div class="lab">{html.escape(it.get("label", "results"))}</div>
        <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">
          <line x1="70" y1="560" x2="{w - 50}" y2="560" stroke="rgba(255,246,227,0.25)" stroke-width="2" />
          <path id="{pid}-line" d="{path}" fill="none" stroke="#FFF6E3" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"
                stroke-dasharray="1200" stroke-dashoffset="1200" />
          <circle id="{pid}-dot" cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="14" fill="{ACCENT}" opacity="0" />
        </svg>
      </div>
    </div>''')
            js.append(f'''    tl.fromTo("#{pid}-box", {{ opacity: 0, scale: 1.035 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "power3.out" }}, {fmt(s)});
    tl.fromTo("#{pid}-line", {{ strokeDashoffset: 1200 }}, {{ strokeDashoffset: 0, duration: {fmt(it["draw_end"] - it["start"] - 0.2)}, ease: "power1.inOut" }}, {fmt(s + 0.2)});
    tl.fromTo("#{pid}-dot", {{ opacity: 0, scale: 0.4, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)" }}, {fmt(it["draw_end"] - c0)});
    tl.to("#{pid}-box", {{ opacity: 0, duration: 0.08, ease: "power1.in" }}, {fmt(e - 0.09)});''')
        elif k == "bars":
            body.append(clip_open)
            body.append(f'      <div id="{pid}-veil" class="veil"></div>')
            body.append(f'      <div id="{pid}-head" class="bhead">{html.escape(it["head"])}</div>')
            js.append(f'    tl.fromTo("#{pid}-veil", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, {fmt(s)});')
            js.append(f'    tl.fromTo("#{pid}-head", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.2 }}, {fmt(s + 0.1)});')
            for j, b in enumerate(it["bars"]):
                top = 520 + j * 320
                body.append(f'      <div id="{pid}-l{j}" class="blbl" style="top: {top}px">{html.escape(b["label"])}</div>')
                body.append(f'      <div id="{pid}-t{j}" class="btrack" style="top: {top + 120}px"><div id="{pid}-b{j}" class="bbar" style="background: {b.get("color", "#E9DFCC")}"></div></div>')
                js.append(f'    tl.fromTo("#{pid}-l{j}, #{pid}-t{j}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {fmt(s + 0.15)});')
                prev = b.get("from", 0.0)
                js.append(f'    tl.fromTo("#{pid}-b{j}", {{ scaleX: {prev} }}, {{ scaleX: {prev}, duration: 0.01 }}, {fmt(s)});')
                for step in b["steps"]:
                    t, v = step[0], step[1]
                    extra = f', backgroundColor: "{step[2]}"' if len(step) > 2 else ""
                    js.append(f'    tl.to("#{pid}-b{j}", {{ scaleX: {v}{extra}, duration: 1.0, ease: "power2.inOut" }}, {fmt(t - c0)});')
                    if len(step) > 2 and step[2] == ACCENT:
                        js.append(f'    tl.to("#{pid}-l{j}", {{ color: "{ACCENT}", duration: 0.5 }}, {fmt(t - c0 + 0.3)});')
            body.append("    </div>")
            js.append(f'    tl.to("#{pid} > *", {{ opacity: 0, duration: 0.15, ease: "power1.in" }}, {fmt(e - 0.16)});')
        else:
            raise SystemExit(f"unknown kind {k!r} in {cid}")
    return c0, c1, scene_file(cid, CSS, "\n".join(body), "\n".join(js))


# ---------------------------------------------------------------- captions
def caption_groups(words):
    ws = [w for w in words if w["text"].lower() not in FILLERS]
    groups, cur = [], []
    for i, w in enumerate(ws):
        cur.append(w)
        nxt = ws[i + 1] if i + 1 < len(ws) else None
        txt = w["text"]
        brk = (
            nxt is None
            or len(cur) >= 5
            or txt.endswith((".", "?", "!"))
            or (txt.endswith(",") and len(cur) >= 2)
            or (nxt["start"] - w["end"] >= 0.15 and len(cur) >= 2)
            or sum(len(x["text"]) + 1 for x in cur) >= 26
        )
        if brk:
            groups.append(cur)
            cur = []
    out = []
    for gi, g in enumerate(groups):
        s = max(g[0]["start"], 0.15) if gi == 0 else g[0]["start"]
        nxt_s = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else DURATION
        e = min(g[-1]["end"] + 0.25, nxt_s)
        if nxt_s - g[-1]["end"] < 0.6:
            e = nxt_s
        e = min(e, DURATION - 0.02)
        text = " ".join(re.sub(r"[.,;:]+$", "", x["text"]) for x in g)
        out.append((round(s, 3), round(e, 3), text))
    return out


def build_captions(groups):
    body = "\n".join(
        f'    <div id="cap-{i}" class="cap"><span>{html.escape(t)}</span></div>' for i, (_, _, t) in enumerate(groups))
    data = json.dumps([[f"#cap-{i}", s, e] for i, (s, e, _) in enumerate(groups)])
    style = f"""
    #root {{ pointer-events: none; }}
    .cap {{ position: absolute; left: 0; top: {CONFIG["caption_top"]}px; width: 1080px; display: flex; justify-content: center;
           opacity: 0; visibility: hidden; }}
    .cap span {{ max-width: 880px; text-align: center; font-family: "Open Sans", sans-serif; font-weight: 600;
                font-size: 50px; line-height: 1.22; color: #FFF4DC;
                text-shadow: 0 2px 4px rgba(0, 0, 0, 0.65), 0 0 18px rgba(0, 0, 0, 0.4); }}
"""
    script = f"""    const groups = {data};
    groups.forEach(([sel, s, e]) => {{
      tl.set(sel, {{ visibility: "visible" }}, s);
      tl.fromTo(sel, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.06, ease: "none" }}, s);
      tl.set(sel, {{ opacity: 0, visibility: "hidden" }}, e);
    }});"""
    return scene_file("captions", style, body, script)


# ---------------------------------------------------------------- root
def build_index(hosts):
    host_html = []
    for cid, s, e, track, kind, z in hosts:
        host_html.append(
            f'      <div id="{cid}" data-composition-id="{cid}" data-composition-src="compositions/{cid}.html" '
            f'data-start="{fmt(s)}" data-duration="{fmt(round(e - s, 3))}" data-track-index="{track}" '
            f'data-track-kind="{kind}" data-width="{W}" data-height="{H}" '
            f'style="position: absolute; inset: 0; z-index: {z}"></div>')
    cam = []
    for t, sc, mode in PUNCHES:
        if mode == "set":
            cam.append(f'      tl.set("#cam", {{ scale: {sc} }}, {fmt(t)});')
        elif mode == "to":
            cam.append(f'      tl.to("#cam", {{ scale: {sc}, duration: 0.3, ease: "power3.out" }}, {fmt(t)});')
        else:
            cam.append(f'      tl.to("#cam", {{ scale: {sc}, duration: 3.2, ease: "sine.inOut" }}, {fmt(t)});')
    music = ""
    if CONFIG["music"]:
        music = (f'      <audio id="music" class="clip" src="{CONFIG["music"]}" data-start="0" data-duration="{fmt(DURATION)}"\n'
                 f'        data-volume="1" data-track-index="1"></audio>\n')
    return f"""<!doctype html>
<html lang="en" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      body {{ font-family: "Open Sans", sans-serif; }}
      #cam {{ position: absolute; inset: 0; transform-origin: {CONFIG["cam_origin"]}; overflow: hidden; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{fmt(DURATION)}" data-width="{W}" data-height="{H}">
      <div id="cam">
        <video id="a-roll" class="clip" src="{CONFIG["aroll"]}" playsinline data-has-audio="true"
          data-start="0" data-duration="{fmt(DURATION)}" data-track-index="0"
          style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover"></video>
      </div>
{music}{chr(10).join(host_html)}
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
      tl.set("#cam", {{ scale: 1 }}, 0);
{chr(10).join(cam)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def main():
    os.makedirs(os.path.join(ROOT, "compositions"), exist_ok=True)
    hosts, shots = [], []
    for n, (cid, track, items) in enumerate(CHAPTERS):
        c0, c1, src = build_chapter(cid, items)
        open(os.path.join(ROOT, "compositions", f"{cid}.html"), "w").write(src)
        hosts.append((cid, c0, c1, track, "graphics", 10))
        for it in items:
            what = it.get("src") or it.get("text") or it.get("head") or it.get("cutout") \
                or " / ".join(it.get("lines", [])) or ", ".join(p if isinstance(p, str) else p["src"] for p in it.get("photos", [])) or it["kind"]
            shots.append((it["start"], it["end"], it["kind"], what))
    for cid, s, dur, z in CONFIG["extra_hosts"]:
        hosts.append((cid, s, s + dur, 5, "graphics", z))
        shots.append((s, s + dur, "hand-authored", f"compositions/{cid}.html"))
    words = json.load(open(os.path.join(ROOT, CONFIG["transcript"])))
    groups = caption_groups(words)
    open(os.path.join(ROOT, "compositions", "captions.html"), "w").write(build_captions(groups))
    hosts.append(("captions", 0, DURATION, 6, "captions", 50))
    hosts.sort(key=lambda h: (h[4] == "captions", h[1]))
    open(os.path.join(ROOT, "index.html"), "w").write(build_index(hosts))
    with open(os.path.join(ROOT, "SHOTS.md"), "w") as f:
        f.write("# Shot list (generated by tools/build_edit.py)\n\n| start | end | layout | visual |\n|---|---|---|---|\n")
        for s, e, k, what in sorted(shots):
            f.write(f"| {s:.2f} | {e:.2f} | {k} | {what} |\n")
        f.write(f"\n{len(groups)} caption groups. Duration {DURATION} s.\n")
    print(f"wrote {len(hosts)} hosts, {len(groups)} caption groups, {len(shots)} overlays, {DURATION} s")


if __name__ == "__main__":
    main()
