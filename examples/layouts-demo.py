"""Every layout in 26 seconds: paste over the CONFIG / CHAPTERS / PUNCHES block of template/build_edit.py.

Tested on a real 9:16 take (face measured: eyes ~870, chin ~1350): hook title (two-line variant), a 3-photo stack,
a 6-photo collage wall, a PIP drop into the top-right corner, a green-screen cutout over a collage, a two-bar flip and a card.
The cutout came from: scripts/cutout.sh assets/talkinghead.mp4 17.5 2.5 assets/cutout/green-1.webm
"""

CONFIG = dict(
    duration=None,
    aroll="assets/talkinghead.mp4",
    music="assets/audio/music.m4a",
    transcript="assets/transcript.json",
    card_cy=800,
    caption_top=1460,
    title_top=176,
    cam_origin="50% 42%",
    face=(540, 870),
    accent="#F4C66B",
    extra_hosts=[("hook-title", 0, 4.4, 20)],
)

W_ = "assets/web/"
CHAPTERS = [
    ("ch-a", 2, [
        dict(kind="stack", start=4.6, end=9.4, photos=[
            dict(src=W_ + "judas.jpg", ar=1.0, at=4.6),
            dict(src=W_ + "trust-baby.jpg", ar=1.5, at=5.9),
            dict(src=W_ + "broken-glass.jpg", ar=0.75, at=7.4),
        ]),
        dict(kind="collage", start=9.6, end=12.6, photos=[W_ + f for f in
             ["monk.jpg", "daedalus.jpg", "sisyphus.jpg", "icarus-fall.jpg", "janus.jpg", "atlas.jpg"]]),
    ]),
    ("ch-b", 3, [
        dict(kind="pip", src=W_ + "monk.jpg", start=13.0, end=17.2, corner="tr", pos="34% 50%"),
        dict(kind="green", cutout="assets/cutout/green-1.webm", start=17.5, end=20.0,
             bg=[W_ + f for f in ["adam.jpg", "kintsugi.jpg", "compass.jpg", "judas.jpg", "sisyphus.jpg", "daedalus.jpg"]]),
    ]),
    ("ch-c", 2, [
        dict(kind="bars", start=20.4, end=24.2, head="who I trusted",
             bars=[dict(label="him", steps=[(20.8, 0.95)]),
                   dict(label="me", color="#8C8478", steps=[(21.8, 0.12), (23.0, 1.0, "#F4C66B")])]),
        dict(kind="card", src=W_ + "kintsugi.jpg", ar=1.0, start=24.5, end=26.0),
    ]),
]

PUNCHES = [
    (26.0, 1.06, "set"), (28.0, 1.0, "set"),
]

