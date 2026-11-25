"""Sahneler: Giris + Bolum 1-3"""
import math
import random

import skia

import backgrounds as B
import characters as C
import effects as FX
import engine as E
import maps as M
import scenery as S
from gfx import (OUT, W, H, big_number, circle, clamp, ease_in_out, ease_out, ellipse, fill, font, label_tag, lerp,
                 lin_grad, pop, poly, rad_grad, rgb, ribbon, rrect, shade, shape, smooth, speech_bubble, stroke,
                 text, tint, vignette, blur_paint, mix)
from shotkit import bgk, le, lf, lt, nlines, person, talk_on, walk_x, xfade_layers


# =================================================================== GIRIS
def hook_plain(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.16, (960, 540), (1180, 520))
    bgk(cv, "yarmouk_golden", B.yarmouk, "golden")
    # roma ordusu (uzak)
    E.army(cv, t, [(660, 0.16, 820, 2000, 26), (690, 0.19, 800, 2000, 30), (725, 0.23, 780, 2000, 36),
                   (765, 0.27, 760, 2000, 42)], facing=-1, mix=E.ROMAN_MIX, seed=11)
    for k, x in enumerate((900, 1130, 1380, 1620, 1850)):
        S.banner_pole(cv, x, 760, t + k, h_=170, col="#a8182a", size=0.5, cross=True)
    r = random.Random(5)
    for k in range(40):
        x, y = r.uniform(800, 1950), r.uniform(640, 760)
        ph = (t * 1.3 + r.random()) % 1.0
        if ph < 0.18:
            s = math.sin(ph / 0.18 * math.pi)
            cv.drawLine(x - 10 * s, y, x + 10 * s, y, stroke("#fffbe0", 2.5, int(255 * s)))
            cv.drawLine(x, y - 10 * s, x, y + 10 * s, stroke("#fffbe0", 2.5, int(255 * s)))
    FX.ground_dust(cv, 700, 1950, 780, t, a=60)
    # musluman saflari (on plan)
    E.army(cv, t, [(840, 0.42, -60, 760, 70), (900, 0.5, -60, 700, 84)], facing=1, seed=3)
    person(cv, "zeyd", 430, 1130, 1.45, 1, t, expr="worried" if t < lt(p, 2) else "scared",
           look=(0.9, -0.1), arm_b=10, wpn=4)
    cv.restore()
    E.year_stamp(cv, "636", t, 0.4, 1690, 190, 120)
    E.lower_third(cv, "YERMÜK NEHRİ • SURİYE", t, 1.0, 6.5)
    vignette(cv, 150)


def hook_items(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.06)
    bgk(cv, "studio_warm", B.studio)
    a, b = E.line_t(p, 0)
    person(cv, "zeyd", 960, 1080, 1.75, 1, t, expr="worried", look=(0.0, 0.4) if t < a + 1 else (-0.6, 0.0),
           arm_b=8, wpn=6, item=None)
    cv.restore()

    def spear(c):
        c.rotate(35)
        c.drawLine(0, 70, 0, -70, stroke(OUT, 12))
        c.drawLine(0, 70, 0, -70, stroke("#8a5a2e", 7))
        c.drawPath(poly([(-12, -60), (0, -110), (12, -60)]), fill("#c9d0d6"))
        c.drawPath(poly([(-12, -60), (0, -110), (12, -60)]), stroke(OUT, 3))

    def shield(c):
        C.draw_shield(c, C.preset("zeyd"), 0, -10, "round", 1.4)

    def dates(c):
        S.date_pile(c, 0, 30, 1.3)

    E.icon_card(cv, 380, 420, 300, 300, "MIZRAK", spear, t, a + (b - a) * 0.32)
    E.icon_card(cv, 1540, 420, 300, 300, "KALKAN", shield, t, a + (b - a) * 0.55)
    E.icon_card(cv, 1540, 800, 300, 300, "HURMA", dates, t, a + (b - a) * 0.83)
    vignette(cv, 110)


def hook_question(cv, t, d, p):
    t2 = lt(p, 1)
    zf = ease_in_out((t - t2) / 0.8) if t > t2 else 0.0
    z = 1.0 + 0.55 * zf
    cv.save()
    cv.translate(W / 2, H / 2)
    cv.scale(z, z)
    cv.translate(-lerp(960, 640, zf), -lerp(540, 620, zf))
    # sol: col mavisi, sag: saray
    left = poly([(0, 0), (1060, 0), (860, H), (0, H)])
    right = poly([(1060, 0), (W, 0), (W, H), (860, H)])
    cv.save()
    cv.clipPath(left, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect.MakeWH(W, H), lin_grad((0, 0), (0, H), ["#3a6aa0", "#9ac0d8", "#f0d8a0"]))
    S.ridge(cv, W, H, 840, 60, 1.0, "#d8b070", seed=3)
    person(cv, "zeyd", 470, 1120, 1.55, 1, t, expr="scared" if t > t2 else "determined", look=(0.6, -0.2), wpn=-6,
           arm_b=12)
    cv.restore()
    cv.save()
    cv.clipPath(right, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect.MakeWH(W, H), lin_grad((0, 0), (0, H), ["#2a1040", "#6a2a70", "#d9a040"]))
    for k in range(12):
        a_ = math.radians(-90 + (k - 6) * 12)
        cv.drawPath(poly([(1450, 700), (1450 + math.cos(a_) * 1200 + 40, 700 + math.sin(a_) * 1200),
                          (1450 + math.cos(a_) * 1200 - 40, 700 + math.sin(a_) * 1200)]), fill("#f6d870", 30))
    person(cv, "heraclius", 1460, 1120, 1.55, -1, t, expr="angry", look=(0.5, 0), arm_b=40, arm_a=20)
    cv.restore()
    # simsek ayirac
    zig = [(1060, -20), (1000, 300), (1040, 330), (950, 700), (990, 720), (860, 1100)]
    cv.drawPath(poly(zig, closed=False), stroke("#ffffff", 22))
    cv.drawPath(poly(zig, closed=False), stroke("#ffe680", 9))
    label_tag(cv, "BEDEVİ", 250, 980, 46, rot=-5)
    label_tag(cv, "HERAKLEİOS", 1660, 980, 46, rot=4)
    cv.restore()
    # baslik
    a = 1.0 - clamp((t - t2) / 0.4)
    if a > 0:
        cv.save()
        s = pop(t - 0.15, 0.5)
        cv.translate(W / 2, 200)
        cv.scale(s, s)
        big_number(cv, "636", 0, 0, 190)
        cv.restore()
        s2 = pop(t - 0.45, 0.5)
        cv.save()
        cv.translate(W / 2, 300)
        cv.scale(s2, s2)
        ribbon(cv, "HALİFE ASKERİ OLSAYDIN?", 0, 0, 60, rot=-2)
        cv.restore()
    if t > t2:
        r = random.Random(2)
        for k in range(6):
            s = pop(t - t2 - 0.5 - k * 0.18, 0.4)
            if s > 0:
                x, y = 900 + r.uniform(-500, 600), 250 + r.uniform(-120, 200)
                cv.save()
                cv.translate(x, y)
                cv.scale(s, s)
                cv.rotate(r.uniform(-20, 20))
                text(cv, "?", 0, 0, font("slab", r.uniform(90, 160)), "#ffd23a", oc=OUT, ow=7, shadow=(4, 6, 0, 120))
                cv.restore()
        hb = 0.5 + 0.5 * math.sin((t - t2) * 7.5)
        cv.drawRect(skia.Rect.MakeWH(W, H), rad_grad((W / 2, H / 2), 1200, [rgb("#ff0000", 0), rgb("#ff0000", 0),
                                                                        rgb("#a00000", int(110 * hb))],
                                                     [0, 0.6, 1]))
    vignette(cv, 120)


def hourglass(cv, x, y, s=1.0, t=0.0):
    cv.save()
    cv.translate(x, y)
    cv.scale(s, s)
    cv.drawPath(circle(0, 0, 150), fill("#1a120c"))
    cv.drawPath(circle(0, 0, 150), stroke("#d9a83a", 8))
    cv.drawPath(circle(0, 0, 136), stroke("#d9a83a", 2))
    for sy in (-1, 1):
        cv.drawPath(rrect(-70, sy * 100 - 10, 140, 20, 6), fill("#c9963a"))
        cv.drawPath(rrect(-70, sy * 100 - 10, 140, 20, 6), stroke(OUT, 3))
    glass = P_glass()
    cv.drawPath(glass, fill("#fff6e0", 60))
    cv.drawPath(glass, stroke("#f0d090", 4))
    f = (t * 0.15) % 1.0
    top = poly([(-44 * (1 - f) - 4, -88 + f * 70), (44 * (1 - f) + 4, -88 + f * 70), (4, -14), (-4, -14)])
    cv.drawPath(top, fill("#e8b040"))
    cv.drawPath(poly([(-50, 88), (50, 88), (12 + f * 30, 88 - 30 - f * 30), (-12 - f * 30, 88 - 30 - f * 30)]),
                fill("#e8b040"))
    cv.drawLine(0, -14, 0, 88, stroke("#e8b040", 3))
    for sx in (-1, 1):
        cv.drawLine(sx * 62, -92, sx * 62, 92, stroke("#c9963a", 8))
    cv.restore()


def P_glass():
    p = skia.Path()
    p.moveTo(-52, -90)
    p.lineTo(52, -90)
    p.cubicTo(52, -40, 8, -20, 8, 0)
    p.cubicTo(8, 20, 52, 40, 52, 90)
    p.lineTo(-52, 90)
    p.cubicTo(-52, 40, -8, 20, -8, 0)
    p.cubicTo(-8, -20, -52, -40, -52, -90)
    p.close()
    return p


def title_card(cv, t, d, p):
    cv.drawRect(skia.Rect.MakeWH(W, H), rad_grad((W / 2, H * 0.4), 1300, ["#3a2414", "#1e130b", "#0a0604"]))
    FX.light_rays(cv, W / 2, -100, t, n=12, a=40, length=1300, spread=80)
    FX.embers(cv, t, 40)
    s = pop(t - 0.1, 0.6)
    cv.save()
    cv.translate(W / 2, 290)
    cv.scale(s, s)
    hourglass(cv, 0, 0, 1.0, t)
    cv.restore()
    a = int(255 * clamp((t - 0.5) / 0.5))
    text(cv, "ZAMAN KIRIĞI", W / 2, 540, font("deco", 70), "#e9c46a", a=a, shadow=(3, 5, 6, 160))
    s2 = pop(t - 0.9, 0.55)
    if s2 > 0:
        cv.save()
        cv.translate(W / 2, 690)
        cv.scale(s2, s2)
        ribbon(cv, "HALİFE DÖNEMİNDE ARAP ASKERİ OLSAYDIN?", 0, 0, 62, rot=-1.5, maxw=1750)
        cv.restore()
    a3 = int(255 * clamp((t - 1.5) / 0.5))
    text(cv, "Romalılara Karşı  •  634 – 638", W / 2, 840, font("xb", 48), "#f3e3bf", a=a3)
    FX.flash(cv, t, 0.05, 0.35, "#fff2c0", 180)
    fo = clamp((t - (d - 0.5)) / 0.5)
    if fo > 0:
        cv.drawRect(skia.Rect.MakeWH(W, H), fill("#000000", int(255 * fo)))


def chapter(cv, t, d, p):
    E.chapter_card(cv, t, d, p["num"], p["title"], p.get("sub"))
    fo = clamp((t - (d - 0.35)) / 0.35)
    if fo > 0:
        cv.drawRect(skia.Rect.MakeWH(W, H), fill("#000000", int(200 * fo)))


# =================================================================== BOLUM 1
def camp_intro(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.12, 1.0, (900, 600), (960, 540))
    bgk(cv, "camp_day", B.camp, "day")
    C.draw_camel(cv, 1250, 860, 0.62, -1, phase=t * 3, walk=0.0)
    C.draw_camel(cv, 1500, 900, 0.7, 1, phase=t * 3 + 1, walk=0.0, load=True)
    person(cv, "mother", 300, 880, 0.75, 1, t, seed=2, expr="happy")
    person(cv, "father", 520, 900, 0.8, 1, t, seed=3, expr="neutral", wpn=-6)
    # cocuklar kosuyor
    kx = 700 + math.sin(t * 1.2) * 120
    person(cv, "zeyd_kid", kx, 930, 0.7, 1 if math.cos(t * 1.2) > 0 else -1, t, seed=4, expr="happy",
           walk=t * 12, arm_a=40, arm_b=40)
    x, mv = walk_x(t, 0.3, 3.0, -150, 960)
    person(cv, "zeyd", x, 1010, 1.05, 1, t, seed=1, expr="happy", walk=t * 9 if mv else None,
           look=(0.5, 0) if mv else (-0.2, 0.1), arm_b=10, wpn=4)
    a, b = E.line_t(p, 0)
    if t > a + (b - a) * 0.6:
        s = pop(t - (a + (b - a) * 0.6), 0.4)
        cv.save()
        cv.translate(x, 580)
        cv.scale(s, s)
        label_tag(cv, "ZEYD", 0, 0, 60, rot=-4)
        cv.restore()
    cv.restore()
    E.lower_third(cv, "HİCAZ, ARAP YARIMADASI", t, lt(p, 1), le(p, 1) + 0.3)
    vignette(cv, 110)


def daily_life(cv, t, d, p):
    t2 = lt(p, 1) - 0.4

    def day(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.1, (960, 540), (1000, 560))
        bgk(c, "camp_day", B.camp, "day")
        # deve sagma + suru
        for k in range(3):
            xx = (1200 + k * 260 + t * 40) % 2300 - 200
            C.draw_camel(c, xx, 820 + k * 20, 0.5, 1, phase=t * 4 + k, walk=1.0)
        C.draw_camel(c, 820, 1000, 0.85, 1, phase=0, walk=0.0)
        person(c, "zeyd", 640, 1040, 1.0, 1, t, expr="happy", arm_b=50, wpn=0, look=(0.6, 0.3))
        shape(c, smooth([(700, 960), (690, 1010), (740, 1020), (760, 965)]), "#9a6a3a")
        c.drawPath(ellipse(726, 964, 30, 8), fill("#f6f2e6"))
        c.restore()
        S.sun(c, lerp(200, 1600, t / max(t2, 1)), 150 + 40 * math.sin(t), 0)

    def night(c):
        c.save()
        E.camera(c, t, d, 1.05, 1.0, (960, 600), (960, 540))
        bgk(c, "camp_night", B.camp, "night")
        c.drawRect(skia.Rect.MakeWH(W, H), rad_grad((960, 900), 900, [rgb("#ff9a3a", 60), rgb("#ff9a3a", 0)]))
        person(c, "elder", 600, 980, 0.95, 1, t, expr="happy" if (t * 0.5) % 2 > 1 else "neutral",
               talk=talk_on(t, p, [1]), arm_b=40 + 20 * math.sin(t * 2), look=(0.6, 0))
        S.campfire(c, 960, 960, t, 1.0)
        person(c, "zeyd_kid", 1240, 990, 0.75, -1, t, seed=3, expr="happy", look=(0.6, -0.2))
        person(c, "zeyd", 1430, 1010, 0.92, -1, t, seed=4, expr="happy", look=(0.7, 0), arm_b=10, wpn=-10)
        person(c, "mother", 1650, 990, 0.82, -1, t, seed=5, expr="happy")
        c.restore()
        speech_bubble(c, "Bir zamanlar, çölün en hızlı atlısı...", 760, 520, 650, 700, maxw=520, size=38,
                      a=int(255 * clamp((t - t2 - 0.8) / 0.4)))
        FX.embers(c, t, 18, col="#ffa040")

    xfade_layers(cv, t, t2, 0.6, day, night)
    vignette(cv, 120)


def well_vs_gold(cv, t, d, p):
    bgk(cv, "studio_sand", B.studio, "#efd6a0", "#b8884a")
    tilt = ease_out(clamp((t - 1.4) / 1.2)) * 14
    cx, cy = 960, 430
    shape(cv, rrect(cx - 16, cy, 32, 520, 8), "#8a6a3a")
    shape(cv, rrect(cx - 120, cy + 500, 240, 40, 10), "#6a4a2a")
    cv.save()
    cv.translate(cx, cy)
    cv.rotate(-tilt)
    shape(cv, rrect(-430, -12, 860, 24, 10), "#a07a40")
    cv.restore()
    for sx in (-1, 1):
        r = math.radians(-tilt)
        px = cx + sx * 410 * math.cos(r)
        py = cy + sx * 410 * math.sin(r)
        cv.drawLine(px, py, px - 120, py + 200, stroke("#5a3a22", 4))
        cv.drawLine(px, py, px + 120, py + 200, stroke("#5a3a22", 4))
        shape(cv, smooth([(px - 150, py + 200), (px + 150, py + 200), (px + 110, py + 240), (px - 110, py + 240)]),
              "#c9a060")
        if sx < 0:
            S.waterskin(cv, px, py + 196, 1.2)
            label_tag(cv, "SU", px, py + 300, 50, rot=-3, bg="#cfe8ff")
        else:
            for k in range(7):
                S.coin(cv, px - 70 + (k % 4) * 46 + (k // 4) * 22, py + 186 - (k // 4) * 28, 24)
            label_tag(cv, "ALTIN", px, py + 300, 50, rot=3, bg="#fff0b0")
    person(cv, "zeyd", 220, 1080, 1.0, 1, t, expr="happy" if t > 2.2 else "neutral", look=(0.8, -0.3), arm_b=10)
    vignette(cv, 100)


def unity_map(cv, t, d, p):
    v = M.MapView(42.0, 25.0, 20)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08, (960, 540), (900, 520))
    M.draw_map_base(cv, v, "arabia")
    M.region_label(cv, v, "ARAP YARIMADASI", 20.0, 47.0, 54)
    r = random.Random(7)
    tribes = [(r.uniform(18, 31), r.uniform(37, 50)) for _ in range(26)]
    cols = ["#b03a2a", "#2a6ab0", "#3a8a3a", "#a07a2a", "#7a3a8a", "#2a8a8a"]
    t2 = lt(p, 1) + 1.6
    med = v.xy(*M.PLACES["Medine"])
    f = ease_in_out((t - t2) / 2.2)
    for k, (la, lo) in enumerate(tribes):
        x, y = v.xy(la, lo)
        x2, y2 = lerp(x, med[0], f * 0.55), lerp(y, med[1], f * 0.55)
        s = pop(t - 0.2 - k * 0.05, 0.35)
        if s <= 0:
            continue
        col = mix(cols[k % len(cols)], "#1f7a3a", f)
        cv.save()
        cv.translate(x2, y2)
        cv.scale(s, s)
        shape(cv, poly([(-22, 12), (0, -18), (22, 12)]), col, w=3)
        cv.restore()
    if f < 0.3:
        for k in range(8):
            a, b = tribes[k * 3 % 26], tribes[(k * 3 + 1) % 26]
            x = (v.xy(*a)[0] + v.xy(*b)[0]) / 2
            y = (v.xy(*a)[1] + v.xy(*b)[1]) / 2
            ph = (t * 0.8 + k * 0.3) % 2.0
            if ph < 0.6:
                M.battle_icon(cv, x, y, ph, 0.0, 0.6)
    M.place(cv, v, "Medine", t, t2 - 0.3, size=44, star=True)
    M.place(cv, v, "Mekke", t, t2, size=34)
    cv.restore()
    if t > t2 + 1.0:
        cv.save()
        s = pop(t - t2 - 1.0, 0.45)
        cv.translate(W / 2, 140)
        cv.scale(s, s)
        ribbon(cv, "TEK DEVLET • TEK HALİFE", 0, 0, 54, color="#1f7a3a")
        cv.restore()
    vignette(cv, 120)


def messengers(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 540), (1000, 560))
    bgk(cv, "camp_day", B.camp, "day")
    for k, (x, s) in enumerate(((260, 0.8), (420, 0.85), (560, 0.78), (700, 0.82))):
        person(cv, ["arab_soldier", "father", "elder", "arab_archer"][k], x, 960, s, 1, t, seed=k,
               expr="surprised" if t > 2 else "neutral", look=(0.8, 0))
    person(cv, "zeyd", 880, 1010, 0.95, 1, t, seed=9, expr="happy" if t > lt(p, 1) else "surprised", look=(0.8, -0.2),
           arm_b=20 if t < lt(p, 1) else 120, wpn=40)
    x, mv = walk_x(t, 0.0, 3.2, 2200, 1450)
    C.draw_camel(cv, x, 980, 0.8, -1, phase=t * 4, walk=1.0 if mv else 0.0,
                 rider=C.preset("messenger"), rider_pose=C.pose(expr="shout" if t > lt(p, 1) else "neutral",
                                                                wpn=10, arm_b=20,
                                                                mouth=talk_on(t, p, [1])))
    x2, mv2 = walk_x(t, 0.4, 3.6, 2500, 1780)
    C.draw_camel(cv, x2, 950, 0.7, -1, phase=t * 4 + 1, walk=1.0 if mv2 else 0.0,
                 rider=C.preset("messenger", head_color="#efe6d2", weapon="spear"))
    cv.restore()
    E.year_stamp(cv, "633", t, 0.3, 1700, 170, 110)
    if t > lt(p, 1) + 0.3:
        speech_bubble(cv, "ŞAM'A SEFER VAR! ROMALILARA KARŞI!", 1300, 330, 1420, 520, maxw=520, size=42)
    vignette(cv, 110)


# =================================================================== BOLUM 2
def farewell(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.08, 1.0, (900, 560), (960, 540))
    bgk(cv, "camp_dusk", B.camp, "dusk")
    t2 = lt(p, 1)
    wave = 80 + 40 * math.sin(t * 8) if t > t2 + 0.5 else 14
    person(cv, "father", 420, 1000, 1.05, 1, t, expr="sad", tears=True, arm_b=wave, wpn=-8, look=(0.6, 0))
    person(cv, "mother", 640, 1010, 1.0, 1, t, seed=2, expr="sad", tears=t > 1.0, arm_b=wave * 0.9,
           arm_a=20 + 6 * math.sin(t * 14), look=(0.6, 0))
    for k, name in enumerate(("arab_soldier", "arab_archer")):
        x, mv = walk_x(t, t2 + 0.2, d + 0.5, 1250 + k * 220, 2300 + k * 200)
        person(cv, name, x, 980, 0.9, 1, t, seed=6 + k, expr="happy", walk=t * 9 + k if mv else None)
    x, mv = walk_x(t, t2 + 0.5, d + 0.3, 1000, 2000)
    person(cv, "zeyd", x, 1040, 1.1, -1 if not mv else 1, t, seed=1, expr="determined", walk=t * 9 if mv else None,
           look=(0.5, 0) if mv else (0.6, 0.0))
    cv.restore()
    vignette(cv, 140)


def equipment(cv, t, d, p):
    bgk(cv, "studio_warm", B.studio)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.05)
    person(cv, "zeyd", 960, 1060, 1.6, 1, t, expr="determined" if t > lt(p, 1) else "neutral",
           look=(-0.4, 0.1), arm_b=12, wpn=8)
    cv.restore()
    a0, b0 = E.line_t(p, 0)

    def uni(c):
        shape(c, poly([(-60, -70), (-100, -40), (-80, -10), (-55, -25), (-55, 70), (55, 70), (55, -25), (80, -10),
                       (100, -40), (60, -70), (20, -60), (-20, -60)]), "#3a6aa0")
        E.cross_out(c, -90, -80, 90, 80, t, a0 + (b0 - a0) * 0.45)

    if t < lt(p, 1) - 0.2:
        E.icon_card(cv, 1520, 420, 340, 320, "ÜNİFORMA YOK", uni, t, a0 + (b0 - a0) * 0.3)
    a, b = E.line_t(p, 1)

    def sword(c):
        c.rotate(40)
        C.draw_weapon(c, {}, 0, 50, 0, "sword")

    def spear(c):
        c.rotate(35)
        c.drawLine(0, 80, 0, -70, stroke(OUT, 12))
        c.drawLine(0, 80, 0, -70, stroke("#8a5a2e", 7))
        c.drawPath(poly([(-12, -60), (0, -110), (12, -60)]), fill("#c9d0d6"))
        c.drawPath(poly([(-12, -60), (0, -110), (12, -60)]), stroke(OUT, 3))

    def shield(c):
        C.draw_shield(c, C.preset("zeyd"), 0, -10, "round", 1.4)

    def bow(c):
        S.bow_item(c, -10, -10, 0.8)
        for k in range(3):
            FX.arrow(c, 40 + k * 14, -50 + k * 30, -60, 0.8)

    def turban(c):
        c.save()
        c.scale(1.3, 1.3)
        C.draw_head_front(c, C.preset("zeyd"), {})
        c.restore()

    if t >= lt(p, 1) - 0.2:
        E.icon_card(cv, 330, 330, 280, 280, "KILIÇ", sword, t, a + (b - a) * 0.02)
        E.icon_card(cv, 330, 700, 280, 280, "MIZRAK", spear, t, a + (b - a) * 0.36)
        E.icon_card(cv, 1590, 330, 280, 280, "KALKAN", shield, t, a + (b - a) * 0.55)
        E.icon_card(cv, 1590, 700, 280, 280, "YAY VE OK", bow, t, a + (b - a) * 0.82)
    if nlines(p) > 2:
        a2, b2 = E.line_t(p, 2)
        E.icon_card(cv, 960, 190, 300, 250, "SARIK", turban, t, a2 + 0.1)
    vignette(cv, 100)


def armor_price(cv, t, d, p):
    bgk(cv, "studio_cool", B.studio, "#e6dcc6", "#a8987a")
    s = pop(t - 0.3, 0.45)
    cv.save()
    cv.translate(420, 620)
    cv.scale(s * 1.6, s * 1.6)
    S.mail_shirt(cv, 0, 60, 1.0)
    cv.restore()
    label_tag(cv, "ZİNCİR ZIRH", 420, 820, 50)
    text(cv, "=", 760, 640, font("slab", 140), "#2a1a10")
    a, b = E.line_t(p, 0)
    for k in range(6):
        s = pop(t - (a + (b - a) * 0.55) - k * 0.16, 0.35)
        if s <= 0:
            continue
        cv.save()
        cv.translate(980 + (k % 3) * 260, 540 + (k // 3) * 300)
        cv.scale(s * 0.5, s * 0.5)
        C.draw_camel(cv, 0, 200, 1.0, 1, phase=0, walk=0.0)
        cv.restore()
    person(cv, "zeyd", 1720, 1120, 1.1, -1, t, expr="surprised" if t > a + (b - a) * 0.6 else "neutral",
           look=(0.8, 0))
    vignette(cv, 100)


def rations(cv, t, d, p):
    bgk(cv, "studio_warm", B.studio)
    a, b = E.line_t(p, 0)
    items = [("HURMA", lambda c: S.date_pile(c, 0, 40, 1.4), 0.3),
             ("ARPA UNU", lambda c: S.flour_sack(c, 0, 70, 1.2), 0.45),
             ("KURU ET", lambda c: S.meat(c, 10, 60, 1.3), 0.62),
             ("SU KIRBASI", lambda c: S.waterskin(c, 0, 40, 1.1), 0.85)]
    for k, (name, fn, fr) in enumerate(items):
        E.icon_card(cv, 300 + k * 440, 560, 360, 400, name, fn, t, a + (b - a) * fr - 0.25)
    s = pop(t - 0.1, 0.4)
    cv.save()
    cv.translate(W / 2, 200)
    cv.scale(s, s)
    ribbon(cv, "ASKERİN AZIĞI", 0, 0, 56, color="#8a5a1a")
    cv.restore()
    vignette(cv, 100)


def loot_shares(cv, t, d, p):
    bgk(cv, "studio_warm", B.studio)
    t1, t2, t3 = lt(p, 1), lt(p, 2), lt(p, 3)
    if t < t1 - 0.1:
        s = pop(t - 0.2, 0.5)
        cv.save()
        cv.translate(960, 760)
        cv.scale(s * 1.6, s * 1.6)
        S.chest(cv, 0, 0, 1.0, open_=clamp((t - 0.8) / 0.6))
        for k in range(10):
            S.coin(cv, -60 + (k % 5) * 30, -120 - (k // 5) * 22 - 10 * math.sin(t * 3 + k), 16)
        cv.restore()
        sr = pop(t - 0.5, 0.45)
        cv.save()
        cv.translate(W / 2, 220)
        cv.scale(sr, sr)
        ribbon(cv, "GANİMET", 0, 0, 80, color="#b8861a")
        cv.restore()
    elif t < t2 - 0.1:
        cx, cy, R = 760, 560, 300
        f = ease_out(clamp((t - t1) / 1.0))
        for k in range(5):
            a0 = -90 + k * 72
            sweep = 72 * f
            pth = skia.Path()
            pth.moveTo(cx, cy)
            pth.arcTo(skia.Rect.MakeLTRB(cx - R, cy - R, cx + R, cy + R), a0, sweep, False)
            pth.close()
            col = "#e8b030" if k == 0 else ["#5a8a4a", "#6a9a5a", "#4a7a3a", "#7aa86a"][k - 1]
            off = 30 if k == 0 else 0
            cv.save()
            am = math.radians(a0 + 36)
            cv.translate(math.cos(am) * off * f, math.sin(am) * off * f)
            shape(cv, pth, col, w=5)
            cv.restore()
        sc = pop(t - t1 - 1.2, 0.4)
        if sc > 0:
            cv.save()
            cv.translate(1430, 380)
            cv.scale(sc, sc)
            S.chest(cv, 0, 60, 1.0)
            label_tag(cv, "BEYTÜLMAL • 1/5", 0, 140, 44, bg="#fff0b0")
            cv.restore()
        sc2 = pop(t - t1 - 2.4, 0.4)
        if sc2 > 0:
            cv.save()
            cv.translate(1430, 760)
            cv.scale(sc2, sc2)
            for k in range(4):
                E.blit(cv, E.person_sprite(E.MUSLIM_MIX[k], 1, "happy", 0.4, seed=k), -120 + k * 80, 60)
            label_tag(cv, "ASKERLER • 4/5", 0, 120, 44, bg="#d8f0c0")
            cv.restore()
    elif t < t3 - 0.1:
        tt = t - t2
        E.blit(cv, E.horse_sprite("arab_soldier", 1, 0.62, "#7a4a2a", False, 0.0, 0.0, "happy"), 560, 900)
        E.blit(cv, E.person_sprite("arab_soldier", 1, "neutral", 0.85, seed=1), 1400, 920)
        for k in range(3):
            s = pop(tt - 0.6 - k * 0.25, 0.35)
            if s > 0:
                cv.save()
                cv.translate(420 + k * 110, 330)
                cv.scale(s, s)
                S.coin(cv, 0, 0, 44)
                cv.restore()
        s = pop(tt - 1.6, 0.35)
        if s > 0:
            cv.save()
            cv.translate(1400, 330)
            cv.scale(s, s)
            S.coin(cv, 0, 0, 44)
            cv.restore()
        label_tag(cv, "ATLI: 3 PAY", 540, 1000, 52, bg="#fff0b0")
        label_tag(cv, "YAYA: 1 PAY", 1400, 1000, 52, rot=3)
    else:
        tt = t - t3
        cv.save()
        E.camera(cv, tt, d - t3, 1.0, 1.1, (960, 600))
        person(cv, "zeyd", 960, 1090, 1.55, 1, t, expr="sad", look=(0.2, -0.6), arm_b=70, wpn=0, weapon=None,
               item="coin")
        cv.restore()

        def horse(c):
            C.draw_horse(c, -40, 120, 0.55, 1, 0, 0)
            E.cross_out(c, -110, -110, 110, 110, t, t3 + 1.0)

        E.icon_card(cv, 1520, 420, 320, 320, "AT YOK", horse, t, t3 + 0.5)
    vignette(cv, 100)


# =================================================================== BOLUM 3
ORDERS = [
    ["Hıyanet etmeyin", "Ganimetten çalmayın", "Ölülere işkence etmeyin"],
    ["Çocuk, kadın ve yaşlıya dokunmayın", "Ağaç kesmeyin, hurmalık yakmayın"],
    ["Rahipleri kendi hallerine bırakın"],
]


def orders(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.06)
    bgk(cv, "desert_hot", B.desert, "hot")
    E.army(cv, t, [(780, 0.32, -40, 1250, 52), (850, 0.4, -40, 1250, 62), (940, 0.5, -60, 1200, 76),
                   (1050, 0.62, -60, 1150, 92)], facing=1, seed=21)
    S.rock(cv, 1520, 860, 1.6, col="#b89a6a")
    person(cv, "messenger", 1520, 790, 0.95, -1, t, expr="determined", talk=talk_on(t, p, [0]), arm_b=60, wpn=-20,
           weapon=None, arm_a=60, look=(0.5, 0.2))
    S.scroll_shape(cv, 1440, 640, 90, 120, 1.0)
    cv.restore()
    # emir parsomeni
    t1 = lt(p, 1) - 0.3
    t4 = lt(p, 4) if nlines(p) > 4 else d
    if t1 < t < t4 + 0.2:
        op = ease_out(clamp((t - t1) / 0.5))
        cl = 1 - ease_out(clamp((t - t4) / 0.4))
        o = op * cl
        cv.drawRect(skia.Rect.MakeWH(W, H), fill("#000000", int(110 * o)))
        S.scroll_shape(cv, 960, 540, 1100, 760 * o + 1, 1.0)
        if o > 0.9:
            text(cv, "HALİFE'NİN EMİRLERİ", 960, 250, font("deco", 50), "#5a1a10")
            row = 0
            for li, items in enumerate(ORDERS):
                a, b = E.line_t(p, li + 1)
                for k, it in enumerate(items):
                    tt = a + (b - a) * (k / len(items)) - 0.1
                    al = clamp((t - tt) / 0.3)
                    y = 340 + row * 82
                    if al > 0:
                        cx, cy = 500, y - 14
                        cv.drawLine(cx - 16, cy - 16, cx + 16, cy + 16, stroke("#b01818", 8, int(255 * al)))
                        cv.drawLine(cx - 16, cy + 16, cx + 16, cy - 16, stroke("#b01818", 8, int(255 * al)))
                        text(cv, it, 545, y, font("xb", 46), "#2a1a10", align="left", a=int(255 * al))
                    row += 1
    if nlines(p) > 4 and t > t4:
        a = clamp((t - t4 - 0.3) / 0.4)
        cv.save()
        cv.drawRect(skia.Rect.MakeWH(W, H), fill("#000000", int(60 * a)))
        cv.restore()
        sc = pop(t - t4 - 0.3, 0.45)
        if sc > 0:
            cv.save()
            cv.translate(W / 2, 200)
            cv.scale(sc, sc)
            ribbon(cv, "DÖNEMİNE GÖRE SIRA DIŞI", 0, 0, 54, color="#1f6a8a")
            cv.restore()
    vignette(cv, 110)


def march(cv, t, d, p):
    t2 = lt(p, 1) - 0.2

    def day(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.06)
        bgk(c, "desert_hot", B.desert, "hot")
        # yuruyen kol
        r = random.Random(4)
        for k in range(22):
            x = (k * 120 + t * 60) % 2800 - 400
            y = 760 + (k % 2) * 16
            if k % 5 == 2:
                C.draw_camel(c, x, y + 10, 0.36, 1, phase=t * 4 + k, walk=1.0, load=True)
            else:
                E.blit(c, E.person_sprite(E.MUSLIM_MIX[k % 5], 1, "tired", 0.36, seed=k % 3),
                       x, y - abs(math.sin(t * 6 + k)) * 3)
        person(c, "zeyd", 760, 1080, 1.25, 1, t, expr="tired", sweat=True, walk=t * 7, look=(0.6, 0.1))
        person(c, "arab_soldier", 1180, 1060, 1.1, 1, t, seed=3, expr="tired", sweat=True, walk=t * 7 + 1)
        c.restore()
        FX.heat_shimmer_overlay(c, t, 600, 800, a=26)
        c.drawRect(skia.Rect.MakeWH(W, H), fill("#ffb040", 30))

    def night(c):
        c.save()
        E.camera(c, t, d, 1.05, 1.0)
        bgk(c, "desert_night", B.desert, "night")
        c.drawRect(skia.Rect.MakeWH(W, H), rad_grad((960, 950), 800, [rgb("#ff9a3a", 70), rgb("#ff9a3a", 0)]))
        S.campfire(c, 960, 950, t, 0.9)
        sh = math.sin(t * 40) * 2.5
        person(c, "zeyd", 640 + sh, 1030, 1.05, 1, t, expr="scared", look=(0.5, 0.2), arm_a=40, arm_b=40,
               weapon=None, shield=None, cloak="#6a5a4a")
        person(c, "arab_soldier", 1280 - sh, 1020, 1.0, -1, t, seed=2, expr="worried", arm_a=40, arm_b=40,
               weapon=None, shield=None, cloak="#5a4a3a")
        c.restore()
        r = random.Random(1)
        for k in range(30):
            x = (r.uniform(0, W) + t * 40) % W
            y = r.uniform(0, H)
            c.drawPath(circle(x, y, 2), fill("#cfe4ff", 120))

    xfade_layers(cv, t, t2, 0.7, day, night)
    E.lower_third(cv, "MEDİNE → ŞAM", t, 0.4, 5.0)
    vignette(cv, 130)


def halid_map(cv, t, d, p):
    t2 = lt(p, 1) - 0.3

    def halid(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.08, (960, 560))
        bgk(c, "desert_dusk", B.desert, "dusk")
        FX.light_rays(c, 960, 380, t, n=14, a=55, length=1200, spread=360, base_ang=0)

        def h(cc):
            C.draw_horse(cc, 960, 1000, 1.45, 1, phase=1.2, gallop=0.6, color="#3a2a1a",
                         rider=C.preset("arab_soldier2", weapon="sword", shield=None),
                         rider_pose=C.pose(arm_b=150, wpn=170))

        C.draw_silhouette(c, h, glow="#ffd88a", glow_sigma=16)
        FX.ground_dust(c, 400, 1500, 1000, t, col="#c89a70", a=90)
        c.restore()
        s = pop(t - 1.0, 0.4)
        if s > 0:
            c.save()
            c.translate(W / 2, 150)
            c.scale(s, s)
            ribbon(c, "HALİD BİN VELİD", 0, 0, 64, color="#1f5a2a")
            c.restore()
            text(c, "\"Allah'ın Kılıcı\"", W / 2, 250, font("xb", 44), "#ffe6b0", oc=OUT, ow=4,
                 a=int(255 * clamp((t - 1.6) / 0.4)))

    def mp(c):
        v = M.MapView(40.5, 32.5, 11)
        c.save()
        E.camera(c, t - t2, d - t2, 1.0, 1.05)
        M.draw_map_base(c, v, "syria_iraq")
        M.region_label(c, v, "SURİYE", 35.5, 37.3, 50)
        M.region_label(c, v, "IRAK", 31.0, 45.4, 50)
        M.region_label(c, v, "SASANİLER", 34.5, 45.8, 40, col="#7a2a2a")
        M.route(c, v, [M.PLACES["Hîre"], M.PLACES["Ayn et-Temr"], (32.3, 41.0), (33.3, 38.9), M.PLACES["Tedmür"],
                       M.PLACES["Şam"]], t, t2 + 0.8, 3.2, col="#1f6a2a", w=12)
        M.place(c, v, "Hîre", t, t2 + 0.2, dx=0, dy=40)
        M.place(c, v, "Şam", t, t2 + 0.4, dx=-40)
        M.place(c, v, "Tedmür", t, t2 + 0.6)
        c.restore()

    xfade_layers(cv, t, t2, 0.6, halid, mp)
    vignette(cv, 120)


def desert_crossing(cv, t, d, p):
    t1, t2 = lt(p, 1) - 0.3, lt(p, 2) - 0.3

    def cross(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.05)
        bgk(c, "desert_hot2", B.desert, "hot")
        S.sun(c, 960, 560, 260, col="#fff2c0", glow="#ffb050", ga=220)

        def caravan(cc):
            for k in range(9):
                x = (k * 260 + t * 70) % 2600 - 350
                if k % 3 == 0:
                    C.draw_camel(cc, x, 820, 0.55, 1, phase=t * 4 + k, walk=1.0)
                else:
                    C.draw_horse(cc, x, 820, 0.5, 1, phase=t * 6 + k, gallop=0.4,
                                 rider=C.preset("arab_soldier"))
        C.draw_silhouette(c, caravan, glow="#ffcf7a", glow_sigma=6, glow_a=120, dark="#2a1a10")
        c.restore()
        FX.heat_shimmer_overlay(c, t, 650, 860, a=40)
        E.lower_third(c, "SEMAVE ÇÖLÜ • SUSUZ GEÇİŞ", t, 0.5, t1)

    def drink(c):
        c.save()
        E.camera(c, t - t1, 6, 1.0, 1.08)
        bgk(c, "desert_hot", B.desert, "hot")
        shape(c, rrect(700, 880, 520, 70, 14), "#8a7a62")
        c.drawPath(rrect(716, 890, 488, 30, 10), fill("#5aa0c8"))
        for k, x in enumerate((640, 1260)):
            C.draw_camel(c, x, 1000 + k * 10, 0.85, 1 if k == 0 else -1, phase=0, walk=0.0)
        for k in range(4):
            dy = (t * 60 + k * 30) % 90
            c.drawPath(circle(900 + k * 50, 900 - dy * 0.2, 4), fill("#bfe4ff", 200))
        person(c, "arab_soldier", 960, 1060, 0.9, 1, t, expr="happy", item="waterskin", weapon=None, arm_b=40)
        c.restore()
        sc = pop(t - t1 - 2.0, 0.4)
        if sc > 0:
            c.save()
            c.translate(W / 2, 170)
            c.scale(sc, sc)
            ribbon(c, "YÜRÜYEN SU DEPOLARI", 0, 0, 56, color="#1f5a8a")
            c.restore()

    def romans(c):
        c.save()
        E.camera(c, t - t2, 4, 1.0, 1.1, (960, 500))
        bgk(c, "city_damascus", B.city, "damascus")
        for k, x in enumerate((380, 600, 1300, 1540)):
            person(c, "roman", x, 640, 0.6, 1 if k < 2 else -1, t, seed=k, expr="scared", look=(0, -0.3))
        FX.dust_cloud(c, 960, 760, t, 2.0, col="#d8b88a", a=150, seed=3)
        c.restore()
        for k, (x, y) in enumerate(((380, 380), (1540, 380))):
            s = pop(t - t2 - 0.4 - k * 0.2, 0.35)
            if s > 0:
                c.save()
                c.translate(x, y)
                c.scale(s, s)
                text(c, "!?", 0, 0, font("slab", 110), "#ffd23a", oc=OUT, ow=7)
                c.restore()

    if t < t2:
        xfade_layers(cv, t, t1, 0.5, cross, drink)
    else:
        xfade_layers(cv, t, t2, 0.5, drink, romans)
    vignette(cv, 120)
