"""Recurring-device example: the iceberg ("what people see" above the water, the real why at the bottom).

Lifted from a finished pipdrop edit. Three visits of one scene file each (ice-a, ice-b, ice-c), mounted as extra hosts:
  ice-a  tip + "to be recognized, / to be seen"; on "is so that I can help more people" the camera pans below the waterline
         and "to help people / who are stuck" writes in
  ice-b  "going more deep into my thoughts": the camera descends into the dark, a plumb line draws down to a faint "?"
  ice-c  "That's the whole goal": zoom out to the whole iceberg, the deepest label lands in gold ("my mom")
Needs assets/web/iceberg.jpg: a real above-and-below-water iceberg photo (Wikimedia Commons:
"File:Iceberg in the Arctic with its underside exposed, brightened underwater.jpg").
World coordinates: photo top 520 / waterline ~799 / underwater tip ~1271; labels at 330, 1395 and 1740; camera = stage translateY + scale.
Paste these helpers into tools/build_edit.py, call build_ice() for each visit, write compositions/<id>.html,
and add (id, start, duration, 10) to CONFIG["extra_hosts"].
"""
from build_edit import W, H, fmt, words_spans, scene_file  # noqa: E402  (when pasted, these already exist)

ICE_CSS = """
    #root { background: #01080c; overflow: hidden; }
    .stage { position: absolute; left: 0; top: 0; width: 1080px; height: 3100px; transform-origin: 50% 0%; }
    .sky { position: absolute; left: -1200px; top: 0; width: 3480px; height: 800px;
           background: linear-gradient(180deg, #2b4361 0%, #4d6687 45%, #7088a8 82%, #93a6bf 100%); }
    .deep { position: absolute; left: -1200px; top: 800px; width: 3480px; height: 2300px;
            background: linear-gradient(180deg, #0d2a3b 0%, #04161f 22%, #01090d 45%, #000507 100%); }
    .photo { position: absolute; left: -210px; top: 520px; width: 1500px; height: 844px;
             -webkit-mask-image: linear-gradient(90deg, transparent 0%, #000 7%, #000 93%, transparent 100%),
                                 linear-gradient(180deg, transparent 0%, #000 9%, #000 86%, transparent 100%);
             -webkit-mask-composite: source-in;
             mask-image: linear-gradient(90deg, transparent 0%, #000 7%, #000 93%, transparent 100%),
                         linear-gradient(180deg, transparent 0%, #000 9%, #000 86%, transparent 100%);
             mask-composite: intersect; }
    .lbl { position: absolute; left: 0; width: 1080px; text-align: center;
           font-family: "EB Garamond", serif; font-style: italic; font-weight: 500; color: #FFF6E3;
           text-shadow: 0 3px 16px rgba(0, 0, 0, 0.6), 0 1px 3px rgba(0, 0, 0, 0.6); }
    .l1 { top: 330px; font-size: 70px; line-height: 1.1; }
    .l2 { top: 1395px; font-size: 66px; line-height: 1.12; }
    .l3 { top: 1740px; font-size: 118px; line-height: 1; color: #F4C66B; }
    .q  { top: 1740px; font-size: 104px; line-height: 1; color: rgba(255, 246, 227, 0.6); }
    .line { position: absolute; left: 539px; width: 2px; background: rgba(255, 246, 227, 0.55); transform-origin: 50% 0%; }
    .seg1 { top: 1290px; height: 90px; }
    .seg2 { top: 1570px; height: 160px; background: linear-gradient(180deg, rgba(255, 246, 227, 0.55), rgba(244, 198, 107, 0.85)); }
    .w { display: inline-block; }
"""


def ice_body(p, show):
    def lbl(cls, idx, text, extra=""):
        return f'      <div id="{p}-l{idx}" class="lbl {cls}"{extra}>{words_spans(text, f"{p}-l{idx}")}</div>'
    parts = [
        f'    <div id="{p}-stage" class="stage">',
        '      <div class="sky"></div>',
        '      <div class="deep"></div>',
        f'      <img id="{p}-photo" class="photo" src="assets/web/iceberg.jpg" alt="" />',
        f'      <div id="{p}-seg1" class="line seg1"></div>',
        f'      <div id="{p}-seg2" class="line seg2"></div>',
        f'      <div id="{p}-l1" class="lbl l1">{words_spans("to be recognized,", p + "-l1a")}<br />{words_spans("to be seen", p + "-l1b")}</div>',
        f'      <div id="{p}-l2" class="lbl l2">{words_spans("to help people", p + "-l2a")}<br />{words_spans("who are stuck", p + "-l2b")}</div>',
    ]
    if "q" in show:
        parts.append(f'      <div id="{p}-q" class="lbl q">?</div>')
    if "l3" in show:
        parts.append(lbl("l3", 3, "my mom"))
    parts.append("    </div>")
    return "\n".join(parts)


def word_ids(p, key, text):
    return [f"#{p}-{key}-w{i}" for i in range(len(text.split()))]


def reveal(ids, t, step=0.067):
    return "\n".join(
        f'    tl.fromTo("{i}", {{ opacity: 0, filter: "blur(6px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.13, ease: "power2.out" }}, {fmt(t + n * step)});'
        for n, i in enumerate(ids))


def shown(ids):
    return "\n".join(f'    tl.set("{i}", {{ opacity: 1 }}, 0);' for i in ids)


def hidden(ids):
    return "\n".join(f'    tl.set("{i}", {{ opacity: 0 }}, 0);' for i in ids)


def build_ice(cid, s, e):
    p = cid.replace("-", "")
    hide = []
    d = round(e - s, 3)
    l1 = word_ids(p, "l1a", "to be recognized,") + word_ids(p, "l1b", "to be seen")
    l2 = word_ids(p, "l2a", "to help people") + word_ids(p, "l2b", "who are stuck")
    l3 = word_ids(p, "l3", "my mom")
    js = []
    if cid == "ice-a":
        show = set()
        hide += l1 + l2
        js += [f'    gsap.set("#{p}-seg2", {{ scaleY: 0 }});',
               f'    tl.fromTo("#{p}-stage", {{ y: 0, scale: 1.06 }}, {{ y: 0, scale: 1.0, duration: 5.3, ease: "sine.out" }}, 0);',
               reveal(l1[:3], 52.20 - s), reveal(l1[3:], 54.62 - s),
               f'    tl.to("#{p}-stage", {{ y: -560, duration: 0.95, ease: "power3.inOut" }}, {fmt(55.62 - s)});',
               f'    tl.fromTo("#{p}-seg1", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.5, ease: "power2.out" }}, {fmt(56.30 - s)});',
               reveal(l2, 56.80 - s, 0.06)]
    elif cid == "ice-b":
        show = {"q"}
        hide += [f"#{p}-q"]
        js += [
               f'    tl.fromTo("#{p}-stage", {{ y: -560 }}, {{ y: -820, duration: 2.6, ease: "power2.inOut" }}, 0.05);',
               f'    tl.fromTo("#{p}-seg2", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 2.3, ease: "power1.inOut" }}, 0.35);',
               f'    tl.fromTo("#{p}-q", {{ opacity: 0, filter: "blur(8px)" }}, {{ opacity: 1, filter: "blur(0px)", duration: 0.4, ease: "power2.out" }}, 2.3);']
    else:
        show = {"l3"}
        hide += l3
        js += [
               f'    tl.fromTo("#{p}-stage", {{ y: -820, scale: 1 }}, {{ y: -48, scale: 0.72, duration: 1.1, ease: "power3.inOut" }}, 0);',
               reveal(l3, 1.15, 0.1)]
    js = [j for j in js if j]
    css = ICE_CSS + (f"    {', '.join(hide)} {{ opacity: 0; }}\n" if hide else "")
    return scene_file(cid, css, ice_body(p, show), "\n".join(js))


