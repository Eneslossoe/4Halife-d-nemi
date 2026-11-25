"""Sahne arka planlari (statik kisimlar; engine.bg ile onbellege alinir)."""
import math
import random

import skia

import scenery as S
from gfx import (OUT, W, H, P, blur_paint, circle, ellipse, fill, lin_grad, mix, poly, rad_grad, rgb, rrect, shade,
                 smooth, stroke, tint)

SKIES = {
    "golden": (["#5f8fc4", "#a9c3d6", "#f4d9a0", "#f3b56a"], [0, 0.35, 0.8, 1]),
    "day": (["#4f8fd0", "#8fbfe6", "#d8ecf6"], [0, 0.6, 1]),
    "hot": (["#6fa0d0", "#cfe0e6", "#f7e2b0"], [0, 0.55, 1]),
    "dawn": (["#2a3a6a", "#7a6a9a", "#e8a07a", "#f6d08a"], [0, 0.35, 0.75, 1]),
    "sunset": (["#3a2a5a", "#a8506a", "#f08a4a", "#ffd08a"], [0, 0.4, 0.75, 1]),
    "dusk": (["#1a1f40", "#4a3a6a", "#b0607a", "#f0a070"], [0, 0.45, 0.8, 1]),
    "night": (["#070b1e", "#0f1a3a", "#1d2c55"], [0, 0.6, 1]),
    "storm": (["#a07a4a", "#c89a60", "#e0b878"], [0, 0.5, 1]),
    "plague": (["#1e2a22", "#3a4a3a", "#6a7a5a"], [0, 0.6, 1]),
}

GROUND = {
    "golden": ["#c9a86a", "#b08a50", "#8a6a3a"],
    "day": ["#d6b878", "#c0995a", "#9a7442"],
    "hot": ["#e8c88a", "#d8b070", "#c09050"],
    "dawn": ["#8a7a6a", "#6a5a4a", "#4a3a30"],
    "sunset": ["#b07a4a", "#8a5a34", "#5a3a22"],
    "dusk": ["#6a5050", "#4a3a3a", "#2a2028"],
    "night": ["#2a2a40", "#1e1e30", "#141420"],
    "storm": ["#b8905a", "#a07a48", "#7a5a34"],
    "plague": ["#4a4a3a", "#3a3a2e", "#26261e"],
}


def sky_for(cv, v, horizon=620):
    cols, pos = SKIES[v]
    S.sky(cv, W, H, cols, pos, horizon=horizon)
    if v in ("night",):
        S.stars(cv, W, H, 260, maxy=horizon)
        S.moon(cv, 1500, 170, 46)
    elif v == "dusk":
        S.stars(cv, W, H, 80, maxy=horizon * 0.5)
    elif v == "golden":
        S.sun(cv, 1450, 330, 70, glow="#ffc870", ga=170)
    elif v == "sunset":
        S.sun(cv, 1500, 520, 90, col="#ffe0a0", glow="#ff9a4a", ga=200)
    elif v == "dawn":
        S.sun(cv, 300, 600, 80, col="#ffe8b0", glow="#ffb07a", ga=170)
    elif v in ("day", "hot"):
        S.sun(cv, 1600, 150, 60)
        S.clouds(cv, W, H, 4, seed=2, a=150, ymax=0.25)


def hills(cv, v, base=600):
    g = GROUND[v]
    far = mix(SKIES[v][0][-1], g[0], 0.45)
    S.ridge(cv, W, H, base - 30, 90, 1.0, far, seed=3, rough=0.4)
    S.ridge(cv, W, H, base + 10, 60, 1.6, mix(far, g[0], 0.5), seed=8, rough=0.6)


def ground(cv, v, y0=640, seed=1):
    g = GROUND[v]
    S.ridge(cv, W, H, y0 + 20, 20, 0.6, g[0], seed=seed, top_col=shade(g[0], 1.08), to_y=H)
    cv.drawRect(skia.Rect.MakeLTRB(0, y0 + 140, W, H), lin_grad((0, y0 + 140), (0, H), [g[0], g[1], g[2]]))
    r = random.Random(seed)
    for _ in range(70):
        x, y = r.uniform(0, W), r.uniform(y0 + 40, H)
        s = (y - y0) / (H - y0)
        cv.drawPath(ellipse(x, y, (14 + 30 * s), (3 + 6 * s)), fill(shade(g[1], 0.85), 90))
    for _ in range(18):
        x, y = r.uniform(0, W), r.uniform(y0 + 60, H)
        s = 0.3 + (y - y0) / (H - y0) * 0.9
        S.bush(cv, x, y, s * 0.8, col=mix("#7a7a40", g[1], 0.5))


# ------------------------------------------------------------------ YERMUK OVASI
def yarmouk(cv, v="golden"):
    sky_for(cv, v)
    hills(cv, v, 590)
    g = GROUND[v]
    # nehir
    p = P()
    p.moveTo(0, 640)
    p.cubicTo(500, 610, 1100, 660, 1920, 625)
    p.lineTo(1920, 640)
    p.cubicTo(1100, 676, 500, 626, 0, 656)
    p.close()
    cv.drawPath(p, fill(mix("#6a9ab0", SKIES[v][0][-2], 0.4)))
    ground(cv, v, 650, seed=4)
    r = random.Random(9)
    for _ in range(6):
        S.rock(cv, r.uniform(0, W), r.uniform(800, 1060), r.uniform(0.5, 1.0), col=shade(g[1], 0.9))


# ------------------------------------------------------------------ BEDEVI KAMPI
def camp(cv, v="day"):
    sky_for(cv, v, horizon=640)
    g = GROUND["hot" if v == "day" else v]
    S.ridge(cv, W, H, 600, 70, 1.0, mix(SKIES[v][0][-1], g[0], 0.6), seed=21)
    S.ridge(cv, W, H, 650, 50, 1.4, mix(SKIES[v][0][-1], g[0], 0.8), seed=22)
    S.ridge(cv, W, H, 700, 30, 0.8, g[0], seed=23, top_col=shade(g[0], 1.08), to_y=H)
    cv.drawRect(skia.Rect.MakeLTRB(0, 760, W, H), lin_grad((0, 760), (0, H), [g[0], g[2]]))
    S.sand_ripples(cv, W, H, 760, shade(g[1], 0.8), n=50)
    S.palm(cv, 1700, 720, 0.9, lean=6, seed=1)
    S.palm(cv, 1820, 740, 0.75, lean=-4, seed=2)
    S.palm(cv, 120, 730, 0.8, lean=-6, seed=3)
    S.bedouin_tent(cv, 380, 760, 0.9, col="#2e2622" if v == "day" else "#1a1616")
    S.bedouin_tent(cv, 1350, 745, 0.75, col="#3a302a" if v == "day" else "#1e1a18")
    S.bedouin_tent(cv, 900, 720, 0.55, col="#2e2622" if v == "day" else "#1a1616")
    # cit
    for k in range(9):
        x = 1000 + k * 40
        cv.drawLine(x, 800, x, 860, stroke("#6a4a2a", 6))
    cv.drawLine(1000, 815, 1320, 815, stroke("#8a6a40", 4))
    cv.drawLine(1000, 840, 1320, 840, stroke("#8a6a40", 4))
    if v == "night":
        tint(cv, "#0a1030", 90)


def desert(cv, v="hot"):
    sky_for(cv, v, horizon=620)
    g = GROUND[v]
    far = mix(SKIES[v][0][-1], g[0], 0.5)
    S.ridge(cv, W, H, 590, 80, 0.8, far, seed=31)
    S.ridge(cv, W, H, 650, 90, 1.1, mix(far, g[0], 0.6), seed=32, top_col=shade(g[0], 1.1), to_y=800)
    S.ridge(cv, W, H, 760, 70, 1.4, g[0], seed=33, top_col=shade(g[0], 1.12), to_y=H)
    cv.drawRect(skia.Rect.MakeLTRB(0, 880, W, H), lin_grad((0, 860), (0, H), [rgb(g[1], 0), rgb(g[1], 255)]))
    S.sand_ripples(cv, W, H, 800, shade(g[1], 0.8), n=40, seed=12)
    S.rock(cv, 1600, 980, 0.9, col=shade(g[2], 1.0))
    S.rock(cv, 260, 1010, 0.7, col=shade(g[2], 1.05))


def studio(cv, col="#f0d9a8", col2="#c89a58"):
    cv.drawRect(skia.Rect.MakeWH(W, H), rad_grad((W / 2, H * 0.45), 1300, [shade(col, 1.08), col, col2]))
    r = random.Random(4)
    for _ in range(26):
        x, y = r.uniform(0, W), r.uniform(0, H)
        rr = r.uniform(60, 200)
        cv.drawPath(circle(x, y, rr), fill("#ffffff", 14))
    # alt zemin
    cv.drawPath(ellipse(W / 2, 1010, 820, 70), fill(shade(col2, 0.8), 120))


def palace(cv):
    cv.drawRect(skia.Rect.MakeWH(W, H), lin_grad((0, 0), (0, H), ["#2a1438", "#4a2050", "#2a1028"]))
    # kemerler
    for k in range(5):
        x = 140 + k * 410
        a = P()
        a.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 130, 160, 260, 600), 130, 130))
        cv.drawPath(a, fill("#5a2a6a"))
        cv.drawPath(a, stroke("#d9a83a", 6))
        cv.save()
        cv.clipPath(a, skia.ClipOp.kIntersect, True)
        for yy in range(160, 760, 30):
            for xx in range(x - 130, x + 130, 30):
                cv.drawPath(rrect(xx + 2, yy + 2, 26, 26, 3), fill("#e0b040" if (xx + yy) % 60 == 0 else "#6a3a7a",
                                                                    60))
        cv.restore()
    for k in range(6):
        S.column(cv, -65 + k * 410, 820, 680, col="#d8c8b0")
    cv.drawRect(skia.Rect.MakeLTRB(0, 820, W, H), lin_grad((0, 820), (0, H), ["#6a4a3a", "#3a2a22"]))
    for k in range(0, W, 120):
        cv.drawPath(poly([(k, 820), (k + 60, 860), (k + 120, 820)]), fill("#8a6a4a", 120))
    # kirmizi hali
    cv.drawPath(poly([(840, 820), (1080, 820), (1300, H), (620, H)]), fill("#8a1a22"))
    cv.drawPath(poly([(860, 820), (1060, 820), (1270, H), (650, H)]), stroke("#d9a83a", 4))
    # taht
    shape_throne(cv, 960, 820)


def shape_throne(cv, x, y):
    from gfx import shape
    shape(cv, rrect(x - 130, y - 420, 260, 330, 40), "#d9a83a", w=5)
    shape(cv, rrect(x - 100, y - 390, 200, 290, 30), "#7a1a4a", w=4)
    shape(cv, rrect(x - 160, y - 140, 320, 120, 16), "#d9a83a", w=5)
    shape(cv, rrect(x - 190, y - 30, 380, 30, 8), "#a8782a", w=4)
    cv.drawPath(circle(x, y - 330, 40), fill("#f6d870", 120))


def city(cv, kind="antioch", v="day"):
    sky_for(cv, v, horizon=700)
    S.ridge(cv, W, H, 560, 110, 0.9, mix(SKIES[v][0][-1], "#9a8a6a", 0.6), seed=41)
    col = {"antioch": "#cdbb98", "hims": "#d0b48a", "damascus": "#d6c09a", "jerusalem": "#e0d0a8"}[kind]
    S.city_skyline(cv, -40, W + 60, 640, seed=5, roman=True, scale=0.8, col=shade(col, 0.92))
    S.stone_wall(cv, -20, W + 20, 760, 150, col=col)
    for x in (160, 620, 1300, 1760):
        S.tower(cv, x, 760, 140, 230, col=shade(col, 0.95))
    S.gate(cv, 960, 760, 170, 200, 0.0)
    cv.drawRect(skia.Rect.MakeLTRB(0, 760, W, H), lin_grad((0, 760), (0, H), ["#c8a870", "#8a6a3a"]))
    if kind == "jerusalem":
        for x in (80, 330, 1550, 1850):
            S.olive(cv, x, 900, 0.9)
    if v == "night":
        tint(cv, "#0a1030", 100)


def muslim_camp(cv, v="golden"):
    sky_for(cv, v)
    hills(cv, v, 600)
    ground(cv, v, 650, seed=6)
    for k, (x, y, s) in enumerate(((180, 720, 0.6), (520, 700, 0.5), (1450, 705, 0.5), (1760, 725, 0.62),
                                   (980, 690, 0.42))):
        S.army_tent(cv, x, y, s, col="#efe6d2", stripe="#6a4a2a" if k % 2 else "#2a2a2a")
    for k, (x, y, s) in enumerate(((330, 800, 0.7), (1640, 810, 0.7))):
        S.bedouin_tent(cv, x, y, s)


def ravine_bg(cv, v="night"):
    sky_for(cv, v, horizon=560)
    g = GROUND[v]
    S.ridge(cv, W, H, 520, 70, 1.0, mix(SKIES[v][0][-1], g[1], 0.5), seed=51)
    # uzak yamac
    S.ridge(cv, W, H, 600, 40, 1.0, g[0], seed=52)
    # vadi (orta)
    gap = poly([(560, 640), (700, 760), (660, 1080), (1260, 1080), (1220, 760), (1360, 640)])
    cv.drawPath(gap, lin_grad((0, 640), (0, H), ["#3a2818", "#0e0806"]))
    # yamac kenarlari
    left = poly([(0, 640), (560, 640), (700, 760), (660, H), (0, H)])
    right = poly([(1920, 640), (1360, 640), (1220, 760), (1260, H), (1920, H)])
    for pth in (left, right):
        cv.drawPath(pth, lin_grad((0, 640), (0, H), [g[0], g[2]]))
        cv.drawPath(pth, stroke(OUT, 4))
    for k in range(10):
        y = 690 + k * 40
        cv.drawLine(560 + k * 10, y, 640 + k * 6, y + 20, stroke(shade(g[2], 0.7), 3))
        cv.drawLine(1360 - k * 10, y, 1280 - k * 6, y + 20, stroke(shade(g[2], 0.7), 3))
    # kopru
    br = P()
    br.moveTo(540, 650)
    br.lineTo(1380, 650)
    br.lineTo(1380, 690)
    br.quadTo(960, 610, 540, 690)
    br.close()
    cv.drawPath(br, fill("#8a7a62"))
    cv.drawPath(br, stroke(OUT, 4))
    for x in range(560, 1380, 46):
        cv.drawLine(x, 650, x, 640, stroke("#6a5a42", 8))
    if v == "night":
        tint(cv, "#0a1030", 80)


def coast(cv):
    sky_for(cv, "sunset", horizon=640)
    S.sea(cv, W, 600, H, 0.0, col="#3a5a7a")
    # suriye kiyisi uzakta
    p = poly([(1100, 620), (1300, 560), (1500, 540), (1700, 520), (1920, 500), (1920, 640), (1100, 640)])
    cv.drawPath(p, fill("#6a4a5a"))
    p2 = poly([(1300, 620), (1450, 590), (1700, 570), (1920, 560), (1920, 640), (1300, 640)])
    cv.drawPath(p2, fill("#8a5a5a"))


def church(cv):
    sky_for(cv, "golden", horizon=700)
    S.ridge(cv, W, H, 560, 90, 0.8, "#c8b08a", seed=61)
    S.city_skyline(cv, -50, W + 50, 700, seed=8, roman=True, scale=0.7, col="#ddcca8")
    # kutsal kabir kilisesi
    from gfx import shape
    x = 960
    shape(cv, rrect(x - 420, 400, 840, 420, 6), "#e8dcc0", w=5)
    rot = P()
    rot.moveTo(x - 230, 400)
    rot.cubicTo(x - 230, 120, x + 230, 120, x + 230, 400)
    rot.close()
    shape(cv, rot, "#b8a888", w=5)
    cv.drawLine(x, 190, x, 120, stroke("#d9a83a", 8))
    cv.drawLine(x - 24, 145, x + 24, 145, stroke("#d9a83a", 8))
    for k in range(5):
        S.column(cv, x - 300 + k * 150, 820, 300, col="#f0e6d0")
    for k in range(4):
        a = P()
        a.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 255 + k * 150, 600, 90, 220), 45, 45))
        shape(cv, a, "#3a2a1e", w=3)
    cv.drawRect(skia.Rect.MakeLTRB(0, 820, W, H), lin_grad((0, 820), (0, H), ["#d8c09a", "#a8885a"]))
    for k in range(6):
        cv.drawRect(skia.Rect.MakeLTRB(x - 460 - k * 20, 820 + k * 22, x + 460 + k * 20, 842 + k * 22),
                    fill(shade("#e0d0b0", 1 - k * 0.04)))
        cv.drawLine(x - 460 - k * 20, 842 + k * 22, x + 460 + k * 20, 842 + k * 22, stroke(OUT, 2))


def plague_town(cv):
    sky_for(cv, "plague", horizon=700)
    S.ridge(cv, W, H, 580, 80, 0.9, "#3a4a3a", seed=71)
    S.city_skyline(cv, -40, W + 40, 760, seed=13, roman=True, scale=1.0, col="#8a8a70")
    cv.drawRect(skia.Rect.MakeLTRB(0, 760, W, H), lin_grad((0, 760), (0, H), ["#5a5a44", "#2a2a20"]))
    tint(cv, "#2a4a2a", 60)


def room(cv, warm=True):
    cv.drawRect(skia.Rect.MakeWH(W, H), lin_grad((0, 0), (0, H), ["#a8805a", "#8a6440", "#5a4028"]))
    r = random.Random(3)
    for _ in range(40):
        x, y = r.uniform(0, W), r.uniform(0, 760)
        cv.drawPath(ellipse(x, y, r.uniform(40, 120), r.uniform(10, 30)), fill("#6a4a2a", 30))
    # pencere
    a = P()
    a.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(1380, 180, 260, 380), 130, 130))
    cv.drawPath(a, lin_grad((0, 180), (0, 560), ["#bfe0ff", "#fff0c8"]))
    cv.drawPath(a, stroke(OUT, 6))
    cv.drawLine(1510, 180, 1510, 560, stroke("#5a3a22", 10))
    cv.drawLine(1380, 360, 1640, 360, stroke("#5a3a22", 10))
    # nis + kandil
    n = P()
    n.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(260, 260, 160, 220), 80, 80))
    cv.drawPath(n, fill("#4a3018"))
    cv.drawPath(n, stroke(OUT, 4))
    cv.drawPath(ellipse(340, 450, 40, 16), fill("#c9a040"))
    cv.drawPath(circle(340, 420, 60), fill("#ffd070", 60))
    cv.drawPath(circle(340, 425, 10), fill("#fff3b0"))
    # zemin + hali
    cv.drawRect(skia.Rect.MakeLTRB(0, 760, W, H), lin_grad((0, 760), (0, H), ["#7a5a3a", "#4a3220"]))
    cv.drawLine(0, 760, W, 760, stroke(OUT, 5))
    rug = poly([(420, 820), (1500, 820), (1640, 1040), (280, 1040)])
    cv.drawPath(rug, fill("#8a1a22"))
    cv.drawPath(rug, stroke("#d9a83a", 6))
    cv.drawPath(poly([(520, 850), (1400, 850), (1500, 1010), (420, 1010)]), stroke("#d9a83a", 3))


def fields(cv):
    sky_for(cv, "day", horizon=600)
    S.ridge(cv, W, H, 540, 90, 0.9, "#9ab07a", seed=81)
    S.city_skyline(cv, 1250, 1900, 600, seed=21, roman=True, scale=0.5, col="#d8c8a0")
    for k in range(7):
        y0 = 600 + k * 70
        col = ["#a8b860", "#c8b860", "#98a850", "#d0c070", "#90a048", "#c0b060", "#a0a850"][k]
        cv.drawRect(skia.Rect.MakeLTRB(0, y0, W, y0 + 72), fill(col))
        for x in range(-40, W, 36):
            cv.drawLine(x, y0 + 8, x + 20, y0 + 60, stroke(shade(col, 0.82), 3))
    for x in (120, 520, 1500, 1820):
        S.olive(cv, x, 640, 0.8)


def constantinople(cv):
    sky_for(cv, "golden", horizon=700)
    S.sea(cv, 700, 640, H, 0.0, col="#3a6a8a")
    S.city_skyline(cv, 700, W + 50, 600, seed=17, roman=True, scale=0.75, col="#d8c8a8")
    # teodosius surlari
    S.stone_wall(cv, 640, W + 20, 760, 210, col="#c8b090")
    for x in (760, 1060, 1360, 1660, 1900):
        S.tower(cv, x, 760, 150, 300, col="#bfa888")
    cv.drawRect(skia.Rect.MakeLTRB(600, 760, W, H), lin_grad((0, 760), (0, H), ["#a89060", "#6a5030"]))
    cv.drawRect(skia.Rect.MakeLTRB(0, 860, 700, H), lin_grad((0, 860), (0, H), ["#b09868", "#7a6040"]))


def turbe(cv):
    sky_for(cv, "dusk", horizon=700)
    S.ridge(cv, W, H, 640, 50, 0.8, "#4a3a5a", seed=91)
    from gfx import shape
    x = 960
    # serviler
    for cx in (520, 1400, 300, 1640):
        shape(cv, smooth([(cx, 760), (cx - 40, 600), (cx - 20, 380), (cx, 300), (cx + 20, 380), (cx + 40, 600)]),
              "#1e3a2a", w=4)
    shape(cv, poly([(x - 220, 760), (x - 220, 520), (x - 170, 470), (x + 170, 470), (x + 220, 520), (x + 220, 760)]),
          "#efe6d6", w=5)
    d = P()
    d.moveTo(x - 170, 470)
    d.cubicTo(x - 170, 250, x + 170, 250, x + 170, 470)
    d.close()
    shape(cv, d, "#6a8aa0", w=5)
    cv.drawLine(x, 305, x, 230, stroke("#d9a83a", 7))
    cv.drawPath(circle(x, 222, 14), stroke("#d9a83a", 6))
    for k in range(3):
        a = P()
        a.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - 150 + k * 110, 560, 80, 150), 40, 40))
        shape(cv, a, "#3a5a4a", w=3)
    cv.drawRect(skia.Rect.MakeLTRB(0, 760, W, H), lin_grad((0, 760), (0, H), ["#5a4a50", "#2a2028"]))


def snow(cv):
    S.sky(cv, W, H, ["#8aa8c8", "#c8d8e8", "#eef2f6"], horizon=700)
    for k, (base, amp, col) in enumerate(((520, 260, "#9aaac0"), (640, 200, "#b8c6d6"), (760, 120, "#e6eef4"))):
        pts = S.ridge(cv, W, H, base, amp, 0.7 + k * 0.3, col, seed=101 + k, rough=0.8)
    r = random.Random(4)
    for _ in range(120):
        cv.drawPath(circle(r.uniform(0, W), r.uniform(0, H), r.uniform(2, 5)), fill("#ffffff", 200))


def egypt(cv):
    sky_for(cv, "hot", horizon=650)
    from gfx import shape
    for (x, s) in ((1200, 1.0), (1500, 0.75), (900, 0.55)):
        shape(cv, poly([(x - 300 * s, 660), (x, 660 - 360 * s), (x + 300 * s, 660)]), "#e0c080", w=4)
        cv.drawPath(poly([(x, 660 - 360 * s), (x + 300 * s, 660), (x + 40 * s, 660)]), fill("#c0a060"))
    cv.drawRect(skia.Rect.MakeLTRB(0, 660, W, H), lin_grad((0, 660), (0, H), ["#e8c88a", "#c09050"]))
    p = P()
    p.moveTo(0, 760)
    p.cubicTo(600, 720, 1200, 800, 1920, 740)
    p.lineTo(1920, 790)
    p.cubicTo(1200, 850, 600, 770, 0, 810)
    p.close()
    cv.drawPath(p, fill("#4a8ab0"))
    S.palm(cv, 200, 760, 0.8, seed=5)
    S.palm(cv, 1780, 750, 0.7, seed=6)


def cliff(cv, v="storm"):
    """yandan gorunum: solda plato, sagda ucurum ve derin vadi"""
    sky_for(cv, v, horizon=640)
    g = GROUND[v]
    S.ridge(cv, W, H, 560, 60, 1.0, mix(SKIES[v][0][-1], g[1], 0.5), seed=57)
    # karsi yamac
    far = poly([(1480, 700), (1560, 690), (1920, 680), (1920, H), (1540, H), (1500, 900)])
    cv.drawPath(far, lin_grad((0, 680), (0, H), [shade(g[1], 0.9), shade(g[2], 0.6)]))
    cv.drawPath(far, stroke(OUT, 4))
    # ucurum boslugu
    cv.drawRect(skia.Rect.MakeLTRB(1100, 700, 1560, H), lin_grad((0, 700), (0, H), ["#5a3a22", "#120a06"]))
    # yakin plato
    near = poly([(0, 790), (600, 780), (1150, 790), (1180, 860), (1150, 940), (1220, 1010), (1190, H), (0, H)])
    cv.drawPath(near, lin_grad((0, 780), (0, H), [g[0], g[2]]))
    cv.drawPath(near, stroke(OUT, 4))
    for k in range(8):
        y = 820 + k * 32
        cv.drawLine(1150 + (k % 2) * 20, y, 1190, y + 18, stroke(shade(g[2], 0.6), 3))
    r = random.Random(3)
    for _ in range(20):
        x, y = r.uniform(0, 1100), r.uniform(800, H)
        cv.drawPath(ellipse(x, y, r.uniform(14, 40), r.uniform(4, 8)), fill(shade(g[1], 0.85), 100))
