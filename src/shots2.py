"""Sahneler: Bolum 4 (Romalilar) + Bolum 5 (Yermuk)"""
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


def day_badge(cv, n, t, x=200, y=170):
    s = pop(t - 0.15, 0.45)
    if s <= 0:
        return
    cv.save()
    cv.translate(x, y)
    cv.scale(s, s)
    cv.rotate(-6)
    cv.drawPath(circle(6, 8, 110), fill((0, 0, 0), 90))
    cv.drawPath(circle(0, 0, 110), rad_grad((-30, -30), 150, ["#f6d27a", "#c98a2a", "#8a5a1a"]))
    cv.drawPath(circle(0, 0, 110), stroke(OUT, 6))
    cv.drawPath(circle(0, 0, 92), stroke("#fff0c0", 3))
    text(cv, f"{n}.", 0, 6, font("slab", 96), "#fff8e0", oc=OUT, ow=5)
    text(cv, "GÜN", 0, 64, font("black", 40), "#2a1a10")
    cv.restore()


# =================================================================== BOLUM 4
def byzantine_name(cv, t, d, p):
    bgk(cv, "palace", B.palace)
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#000000", 70))
    cv.save()
    E.camera(cv, t, d, 1.0, 1.05)
    person(cv, "roman", 960, 1080, 1.55, 1, t, expr="neutral" if t < lt(p, 1) else "happy", look=(0, 0.1),
           arm_b=12, wpn=8)
    cv.restore()
    a0, b0 = E.line_t(p, 0)
    tb = a0 + (b0 - a0) * 0.72
    s = pop(t - tb, 0.4)
    if s > 0:
        cv.save()
        cv.translate(480, 360)
        cv.scale(s, s)
        cv.rotate(-6)
        text(cv, "BİZANS", 0, 0, font("slab", 120), "#e8e0d0", oc=OUT, ow=7, shadow=(5, 8, 0, 140))
        cv.restore()
        a1, b1 = E.line_t(p, 1)
        E.cross_out(cv, 230, 240, 730, 380, t, a1 + (b1 - a1) * 0.2)
        s2 = pop(t - (a1 + (b1 - a1) * 0.55), 0.45)
        if s2 > 0:
            cv.save()
            cv.translate(1450, 330)
            cv.scale(s2, s2)
            ribbon(cv, "ROMALI", 0, 0, 84, rot=-3)
            cv.restore()
        s3 = pop(t - (a1 + (b1 - a1) * 0.85), 0.45)
        if s3 > 0:
            cv.save()
            cv.translate(1450, 520)
            cv.scale(s3, s3)
            label_tag(cv, "ARAPLARA GÖRE: RÛM", 0, 0, 50, rot=3)
            cv.restore()
        sn = clamp((t - (a1 + (b1 - a1) * 0.3)) / 0.4)
        if sn > 0:
            text(cv, "(Bu isim 16. yüzyılda Avrupalı tarihçilerce yaygınlaştırıldı)", 480, 450, font("bold", 28),
                 "#f3e3bf", a=int(255 * sn))
    vignette(cv, 120)


def stat_bar(cv, x, y, w, frac, col, label, t, t0):
    f = ease_out(clamp((t - t0) / 0.8)) * frac
    cv.drawPath(rrect(x, y, w, 34, 17), fill("#3a2a1e", 200))
    if f > 0.02:
        cv.drawPath(rrect(x, y, w * f, 34, 17), fill(col))
    cv.drawPath(rrect(x, y, w, 34, 17), stroke(OUT, 3.5))


def roman_vs_zeyd(cv, t, d, p):
    t1 = lt(p, 1) - 0.2

    def compare(c):
        bgk(c, "studio_warm", B.studio)
        person(c, "zeyd", 360, 1060, 1.35, 1, t, expr="worried", look=(0.8, 0))
        person(c, "roman", 1560, 1060, 1.35, -1, t, seed=2, expr="determined", look=(0.8, 0))
        label_tag(c, "SEN", 360, 260, 52, rot=-4)
        label_tag(c, "ROMALI ASKER", 1560, 250, 52, rot=4)
        rows = [("ZIRH", 0.15, 0.9), ("EĞİTİM", 0.3, 0.92), ("MAAŞ", 0.08, 0.8)]
        for k, (nm, a, b) in enumerate(rows):
            y = 430 + k * 140
            text(c, nm, 960, y - 14, font("black", 44), "#2a1a10")
            stat_bar(c, 640, y, 300, a, "#4a9a4a", nm, t, 0.6 + k * 0.5)
            stat_bar(c, 980, y, 300, b, "#c8302a", nm, t, 0.6 + k * 0.5)

    def charge(c):
        tt = t - t1
        c.save()
        E.shake(c, tt, 7)
        E.camera(c, tt, d - t1, 1.05, 1.0)
        bgk(c, "yarmouk_day", B.yarmouk, "day")
        E.cavalry(c, tt, [(760, 0.28, 1500, 3400, 120)], facing=-1, rider="roman", armored=True, speed=380,
                  color_mix=("#c8c0b0", "#8a8a8a"), seed=4)
        x = lerp(2300, -500, clamp(tt / max(d - t1, 1.0)))
        C.draw_horse(c, x, 1060, 1.35, -1, phase=tt * 11, gallop=1.0, color="#d8d0c4", armored=True,
                     rider=C.preset("roman", shield="byz"), rider_pose=C.pose(expr="shout", arm_b=60, wpn=70))
        FX.dust_cloud(c, x + 300, 1050, tt, 2.2, a=170, seed=2)
        c.restore()
        s = pop(tt - 0.6, 0.45)
        if s > 0:
            c.save()
            c.translate(W / 2, 170)
            c.scale(s, s)
            ribbon(c, "KATAFRAKT: ZIRHLI AĞIR SÜVARİ", 0, 0, 56, color="#5a5a6a")
            c.restore()

    xfade_layers(cv, t, t1, 0.4, compare, charge)
    vignette(cv, 110)


def heraclius_tired(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 560), (960, 600))
    bgk(cv, "palace", B.palace)
    person(cv, "heraclius", 960, 1000, 1.25, 1, t, expr="tired" if t > t1 else "worried", look=(0, 0.4),
           arm_b=20, arm_a=20)
    if t > t1:
        S.chest(cv, 1450, 1000, 1.2, open_=clamp((t - t1 - 0.5) / 0.6))
        r = random.Random(3)
        for k in range(5):
            ph = (t * 0.6 + k * 0.2) % 1.0
            if t > t1 + 1.0:
                cv.drawPath(circle(1450 + math.sin(t * 3 + k) * 60, 860 - ph * 260, 5), fill("#8a8a7a", 200))
        for k, x in enumerate((300, 520)):
            person(cv, "roman", x, 1020, 0.85, 1, t, seed=k + 3, expr="tired", wpn=-14, arm_b=6)
    cv.restore()
    if t > t1:
        s = pop(t - t1 - 0.2, 0.45)
        cv.save()
        cv.translate(W / 2, 170)
        cv.scale(s, s)
        ribbon(cv, "602 – 628: 26 YIL PERS SAVAŞI", 0, 0, 54, color="#5a1a6a")
        cv.restore()
        a, b = E.line_t(p, 1)
        for k, (s_, fr) in enumerate((("HAZİNE BOŞ", 0.48), ("ASKER YORGUN", 0.66), ("HALK BIKKIN", 0.88))):
            sc = pop(t - (a + (b - a) * fr), 0.35)
            if sc > 0:
                cv.save()
                cv.translate(1500, 330 + k * 90)
                cv.scale(sc, sc)
                label_tag(cv, s_, 0, 0, 40, rot=-3 + k * 3, bg="#ffe0d0")
                cv.restore()
    vignette(cv, 130)


def ghassanids(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.15, (960, 560), (960, 620))
    bgk(cv, "yarmouk_day", B.yarmouk, "day")
    S.banner_pole(cv, 1640, 880, t, 380, col="#7a1a2a", size=0.9, cross=True)
    for k, (x, s) in enumerate(((1250, 1.0), (1480, 1.05), (1720, 1.0))):
        person(cv, "ghassanid", x, 1000 + k * 8, s, -1, t, seed=k, expr="determined", look=(0.7, 0))
    person(cv, "arab_soldier", 260, 1000, 1.0, 1, t, seed=5, expr="surprised", look=(0.8, 0))
    person(cv, "zeyd", 520, 1030, 1.1, 1, t, seed=6, expr="surprised" if t > t1 else "worried", look=(0.8, -0.1))
    cv.restore()
    s = pop(t - 1.4, 0.4)
    if s > 0:
        cv.save()
        cv.translate(1480, 260)
        cv.scale(s, s)
        label_tag(cv, "GASSANİLER", 0, 0, 56, rot=4)
        text(cv, "Hristiyan Araplar • Roma'nın müttefiki", 0, 70, font("xb", 34), "#ffffff", oc=OUT, ow=4)
        cv.restore()
    if t > t1 + 0.5:
        for k in range(3):
            sc = pop(t - t1 - 0.5 - k * 0.2, 0.35)
            if sc > 0:
                cv.save()
                cv.translate(560 + k * 70, 380 - k * 40)
                cv.scale(sc, sc)
                text(cv, "?", 0, 0, font("slab", 100), "#ffd23a", oc=OUT, ow=6)
                cv.restore()
    vignette(cv, 110)


def first_battles(cv, t, d, p):
    v = M.MapView(36.1, 32.6, 5.2)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08, (960, 540), (1000, 560))
    M.draw_map_base(cv, v, "levant_close")
    M.region_label(cv, v, "AKDENİZ", 33.2, 34.0, 50, col="#2a4a5a")
    a0, b0 = E.line_t(p, 0)
    a1, b1 = E.line_t(p, 1)
    M.route(cv, v, [(30.3, 35.4), (31.2, 35.1), M.PLACES["Ecnadeyn"]], t, 0.3, 1.2, col="#1f6a2a", w=10)
    x, y = v.xy(*M.PLACES["Ecnadeyn"])
    M.battle_icon(cv, x, y, t, a0 + (b0 - a0) * 0.3, 1.0, "Ecnadeyn", "634")
    M.route(cv, v, [M.PLACES["Ecnadeyn"], (32.3, 35.9), M.PLACES["Şam"]], t, a0 + (b0 - a0) * 0.55, 1.2,
            col="#1f6a2a", w=10)
    x, y = v.xy(*M.PLACES["Şam"])
    M.battle_icon(cv, x, y, t, a0 + (b0 - a0) * 0.75, 1.0, "Şam", "634")
    x, y = v.xy(*M.PLACES["Fahl"])
    M.battle_icon(cv, x - 10, y, t, a1, 1.0, "Fahl", "635")
    M.place(cv, v, "Kudüs", t, 0.5, dx=-80, dy=10)
    cv.restore()
    vignette(cv, 120)


def heraclius_gathers(cv, t, d, p):
    a1, b1 = E.line_t(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08, (960, 540), (1000, 560))
    bgk(cv, "city_antioch", B.city, "antioch")
    shape(cv, rrect(60, 760, 380, 120, 10), "#bfae8e")
    person(cv, "heraclius", 250, 770, 0.95, 1, t, expr="angry", arm_b=110 + 10 * math.sin(t * 3), arm_a=20,
           talk=talk_on(t, p, [0]), look=(0.8, 0))
    groups = [("ERMENİLER", "armenian_archer", 0.22), ("SLAVLAR", "roman", 0.4), ("GASSANİLER", "ghassanid", 0.6)]
    for k, (lab, nm, fr) in enumerate(groups):
        x0 = 600 + k * 380
        for j in range(5):
            xx = x0 + j * 60 + (t * 30) % 60
            E.blit(cv, E.person_sprite(nm, 1, "determined", 0.42, seed=j % 3), xx,
                   900 + (j % 2) * 30 - abs(math.sin(t * 6 + j)) * 4)
        s = pop(t - (a1 + (b1 - a1) * fr), 0.4)
        if s > 0:
            cv.save()
            cv.translate(x0 + 140, 700)
            cv.scale(s, s)
            label_tag(cv, lab, 0, 0, 42, rot=-3 + k * 2)
            cv.restore()
    E.cavalry(cv, t, [(1060, 0.4, 500, 1900, 260)], facing=1, rider="roman", armored=False, speed=40,
              color_mix=("#7a4a2a", "#e0d8cc", "#3a2a1a"), seed=9)
    s = pop(t - (a1 + (b1 - a1) * 0.8), 0.4)
    if s > 0:
        cv.save()
        cv.translate(1500, 820)
        cv.scale(s, s)
        label_tag(cv, "ROMA SÜVARİLERİ", 0, 0, 42, rot=3)
        cv.restore()
    FX.ground_dust(cv, 400, 1950, 1060, t, a=80)
    cv.restore()
    E.lower_third(cv, "ANTAKYA", t, 0.4, 4.0)
    vignette(cv, 120)


def retreat_jizya(cv, t, d, p):
    t1, t2, t3 = lt(p, 1), lt(p, 2), lt(p, 3)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.06, (960, 560))
    bgk(cv, "city_hims", B.city, "hims")
    if t < t1:
        for k in range(8):
            x = 1300 - k * 140 - t * 70
            E.blit(cv, E.person_sprite(E.MUSLIM_MIX[k % 5], -1, "sad", 0.5, seed=k % 3), x, 980 + (k % 2) * 20)
        person(cv, "zeyd", 1250 - t * 70, 1050, 1.0, -1, t, expr="sad", walk=t * 8)
    else:
        # sehir kapisi acik, halk disarida
        S.gate(cv, 960, 760, 170, 200, open_=1.0 if t < t3 + 1.5 else 1.0 - clamp((t - t3 - 1.5) / 1.5))

        def ebu(cc):
            C.draw_person(cc, C.preset("arab_soldier", weapon="staff", shield=None, item=None),
                          C.pose(arm_b=50, wpn=-10, arm_a=60), 520, 1030, 1.2, 1)

        C.draw_silhouette(cv, ebu, glow="#ffe2a0", glow_sigma=12)
        for k in range(2):
            bx = lerp(640, 1000 + k * 260, ease_in_out((t - t1 - 0.8 - k * 0.6) / 1.2))
            if t > t1 + 0.8 + k * 0.6:
                shape(cv, smooth([(bx - 30, 900), (bx - 36, 870), (bx - 12, 850), (bx + 12, 850), (bx + 36, 870),
                                  (bx + 30, 900)]), "#a07a40")
                cv.drawLine(bx - 14, 852, bx + 14, 852, stroke("#5a3a22", 5))
        happy = t > t3
        person(cv, "townsman", 1080, 1030, 1.0, -1, t, seed=2, expr="happy" if happy else "surprised",
               arm_b=110 if happy else 30, arm_a=40, look=(0.6, 0))
        person(cv, "jewish_elder", 1340, 1040, 1.0, -1, t, seed=3, expr="happy" if happy else "surprised",
               arm_b=90 if happy else 30, look=(0.6, 0))
        person(cv, "townsman2", 1590, 1030, 0.95, -1, t, seed=4, expr="happy", arm_b=120 if happy else 20)
        label_tag(cv, "EBU UBEYDE", 520, 560, 44, rot=-3)
    cv.restore()
    if t < t1:
        E.lower_third(cv, "HUMUS VE ŞAM BOŞALTILIYOR", t, 0.3, t1 - 0.2)
    if t2 <= t < t3:
        E.quote_card(cv, "Sizi koruyamıyorsak, bu parayı almaya hakkımız yok.", "Ebu Ubeyde bin Cerrah", t, t2,
                     y=330)
    if t > t1 + 1.5 and t < t2:
        s = pop(t - t1 - 1.5, 0.4)
        cv.save()
        cv.translate(W / 2, 170)
        cv.scale(s, s)
        ribbon(cv, "CİZYE GERİ ÖDENİYOR", 0, 0, 56, color="#1f6a2a")
        cv.restore()
    vignette(cv, 110)


# =================================================================== YERMUK TAKTIK HARITASI
def tactical(cv, t, state):
    """state: dict(roman=0..1, muslim=0..1, units36=t0, reserve=t0, bridge=t0, escape=t0)"""
    cv.drawRect(skia.Rect.MakeWH(W, H), rad_grad((960, 540), 1200, ["#ecd8a8", "#d8bb80", "#a8844a"]))
    r = random.Random(2)
    for _ in range(90):
        cv.drawPath(circle(r.uniform(0, W), r.uniform(0, H), r.uniform(4, 16)), fill("#8a6a3a", 22))
    # tepeler
    for (x, y) in ((1500, 180), (1650, 260), (1380, 120), (300, 130)):
        cv.drawPath(poly([(x - 60, y + 30), (x, y - 30), (x + 60, y + 30)]), fill("#b89a62"))
        cv.drawPath(poly([(x - 60, y + 30), (x, y - 30), (x + 60, y + 30)]), stroke("#6a4a22", 3))
    # Rakkad vadisi (bati)
    wadi = [(380, -20), (420, 200), (360, 420), (430, 640), (380, 860), (420, 1100)]
    pth = smooth(wadi, closed=False)
    cv.drawPath(pth, stroke("#4a3018", 70))
    cv.drawPath(pth, stroke("#2a1a0c", 40))
    # yermuk nehri (guney)
    riv = smooth([(380, 960), (800, 1000), (1200, 960), (1600, 1010), (1960, 980)], closed=False)
    cv.drawPath(riv, stroke("#4a3018", 60))
    cv.drawPath(riv, stroke("#5a8ab0", 22))
    text(cv, "RAKKAD VADİSİ", 300, 560, font("xb", 30), "#3a2010", oc="#f3e3bf", ow=4)
    text(cv, "YERMÜK NEHRİ", 1500, 1060, font("xb", 32), "#1a3a5a", oc="#f3e3bf", ow=4)
    # kopru
    bx, by = 405, 520
    shape(cv, rrect(bx - 60, by - 14, 120, 28, 6), "#c8b090", w=3)
    text(cv, "KÖPRÜ", bx + 120, by + 10, font("black", 28), "#3a2010", oc="#f3e3bf", ow=4)
    if state.get("bridge") is not None and t > state["bridge"]:
        s = pop(t - state["bridge"], 0.35)
        cv.save()
        cv.translate(bx, by)
        cv.scale(s, s)
        cv.drawPath(circle(0, 0, 46), fill("#1f7a3a", 220))
        cv.drawPath(circle(0, 0, 46), stroke(OUT, 4))
        cv.drawLine(-22, -22, 22, 22, stroke("#ffffff", 9))
        cv.drawLine(-22, 22, 22, -22, stroke("#ffffff", 9))
        cv.restore()
    # birlikler
    ro = state.get("roman", 1.0)
    rr = random.Random(5)
    n_ro = int(28 * ro)
    for k in range(n_ro):
        col, row = k % 4, k // 4
        x = 640 + col * 70 + rr.uniform(-8, 8)
        y = 200 + row * 92 + rr.uniform(-6, 6)
        cv.drawPath(rrect(x - 26, y - 34, 52, 68, 6), fill("#b02a2a"))
        cv.drawPath(rrect(x - 26, y - 34, 52, 68, 6), stroke(OUT, 3))
    mu = state.get("muslim", 1.0)
    u36 = state.get("units36")
    if u36 is not None:
        for k in range(36):
            s = pop(t - u36 - k * 0.04, 0.3)
            if s <= 0:
                continue
            x = 1180 + (k % 3) * 56
            y = 180 + (k // 3) * 64
            cv.save()
            cv.translate(x, y)
            cv.scale(s, s)
            cv.drawPath(rrect(-22, -24, 44, 48, 5), fill("#1f7a3a"))
            cv.drawPath(rrect(-22, -24, 44, 48, 5), stroke(OUT, 3))
            cv.restore()
    else:
        for k in range(int(8 * mu)):
            x = 1200 + (k % 2) * 80
            y = 220 + (k // 2) * 160
            cv.drawPath(rrect(x - 30, y - 60, 60, 120, 6), fill("#1f7a3a"))
            cv.drawPath(rrect(x - 30, y - 60, 60, 120, 6), stroke(OUT, 3))
    if state.get("reserve") is not None and t > state["reserve"]:
        s = pop(t - state["reserve"], 0.4)
        cv.save()
        cv.translate(1500, 560)
        cv.scale(s, s)
        cv.drawPath(rrect(-80, -60, 160, 120, 12), fill("#2a5a9a"))
        cv.drawPath(rrect(-80, -60, 160, 120, 12), stroke(OUT, 4))
        text(cv, "SÜVARİ", 0, 12, font("black", 34), "#ffffff")
        cv.restore()
        text(cv, "HIZLI YEDEK KUVVET", 1500, 680, font("xb", 30), "#1a2a5a", oc="#f3e3bf", ow=4,
             a=int(255 * clamp((t - state["reserve"] - 0.3) / 0.3)))
    if state.get("escape") is not None:
        M_route_xy(cv, [(700, 540), (560, 540), (440, 520)], t, state["escape"], 1.0, "#b02a2a")


def M_route_xy(cv, pts, t, t0, dur, col):
    f = clamp((t - t0) / dur)
    if f <= 0:
        return
    path = poly(pts, closed=False)
    meas = skia.PathMeasure(path, False)
    L = meas.getLength()
    seg = skia.Path()
    meas.getSegment(0, L * f, seg, True)
    cv.drawPath(seg, stroke(OUT, 18))
    cv.drawPath(seg, stroke(col, 11))


def yarmouk_map(cv, t, d, p):
    t1, t2 = lt(p, 1), lt(p, 2)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.06)
    ro = 0.35 + 0.65 * ease_out(clamp((t - t1) / 2.5))
    tactical(cv, t, dict(roman=ro if t > t1 else 0.35, muslim=1.0))
    cv.restore()
    s = pop(t - 0.4, 0.4)
    if s > 0:
        cv.save()
        cv.translate(W / 2, 80)
        cv.scale(s, s)
        ribbon(cv, "YERMÜK SAVAŞ ALANI", 0, 0, 48, color="#6a3a1a")
        cv.restore()
    if t > t2:
        for k, (lab, num, col, x) in enumerate((("MÜSLÜMANLAR", "~30.000", "#1f7a3a", 1330),
                                                 ("ROMALILAR", "~100.000?", "#b02a2a", 760))):
            sc = pop(t - t2 - k * 0.4, 0.4)
            if sc > 0:
                cv.save()
                cv.translate(x, 880)
                cv.scale(sc, sc)
                cv.drawPath(rrect(-210, -70, 420, 150, 20), fill("#fbf3df"))
                cv.drawPath(rrect(-210, -70, 420, 150, 20), stroke(col, 6))
                text(cv, lab, 0, -18, font("black", 36), col)
                text(cv, num, 0, 54, font("slab", 62), "#2a1a10")
                cv.restore()
        text(cv, "* Sayılar kaynaklara göre değişir, tahminidir.", W / 2, 1050, font("bold", 26), "#3a2010",
             a=int(255 * clamp((t - t2 - 0.8) / 0.4)))
    vignette(cv, 110)


def halid_command(cv, t, d, p):
    t1 = lt(p, 1) - 0.3

    def leaders(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.08)
        bgk(c, "yarmouk_golden", B.yarmouk, "golden")
        E.army(c, t, [(760, 0.3, -40, 1960, 48)], facing=1, seed=31)

        def ebu(cc):
            C.draw_person(cc, C.preset("arab_soldier", weapon="staff", shield=None),
                          C.pose(arm_b=20, wpn=-6), 620, 1040, 1.3, 1)

        def halid(cc):
            C.draw_horse(cc, 1330, 1060, 1.1, -1, phase=0.5, gallop=0.2, color="#3a2a1a",
                         rider=C.preset("arab_soldier2", weapon="sword", shield=None),
                         rider_pose=C.pose(arm_b=120, wpn=140))

        C.draw_silhouette(c, ebu, glow="#ffe2a0")
        C.draw_silhouette(c, halid, glow="#ffe2a0")
        c.restore()
        a0, b0 = E.line_t(p, 0)
        s1 = pop(t - 0.5, 0.4)
        if s1 > 0:
            c.save()
            c.translate(560, 300)
            c.scale(s1, s1)
            label_tag(c, "EBU UBEYDE", 0, 0, 44, rot=-3)
            text(c, "Başkomutan", 0, 62, font("xb", 32), "#ffffff", oc=OUT, ow=4)
            c.restore()
        s2 = pop(t - (a0 + (b0 - a0) * 0.6), 0.4)
        if s2 > 0:
            c.save()
            c.translate(1340, 300)
            c.scale(s2, s2)
            label_tag(c, "HALİD BİN VELİD", 0, 0, 44, rot=3)
            text(c, "Sahada komuta", 0, 62, font("xb", 32), "#ffffff", oc=OUT, ow=4)
            c.restore()

    def tac(c):
        a1, b1 = E.line_t(p, 1)
        tactical(c, t, dict(roman=1.0, units36=a1 + 0.4, reserve=a1 + (b1 - a1) * 0.6))
        s = pop(t - a1 - 0.6, 0.4)
        if s > 0:
            c.save()
            c.translate(1250, 80)
            c.scale(s, s)
            ribbon(c, "36 BİRLİK", 0, 0, 46, color="#1f7a3a")
            c.restore()

    xfade_layers(cv, t, t1, 0.5, leaders, tac)
    vignette(cv, 110)


def camp_women(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 560), (700, 600))
    bgk(cv, "muslim_camp", B.muslim_camp, "golden")
    for k, (nm, x, s) in enumerate((("mother", 300, 0.85), ("woman2", 520, 0.85), ("woman3", 1500, 0.8),
                                    ("woman2", 1700, 0.8))):
        person(cv, nm, x, 930 + (k % 2) * 20, s, 1 if x < 960 else -1, t, seed=k, expr="determined", look=(0.5, 0))
    for k, x in enumerate((420, 640, 1600)):
        person(cv, "kid", x + math.sin(t * 2 + k) * 20, 960, 0.6, 1, t, seed=k + 5, expr="happy")
    facing = -1 if t < t1 + 0.3 else 1
    person(cv, "zeyd", 1060, 1090, 1.3, facing, t, expr="sad" if t < t1 else "determined",
           look=(0.7, 0) if facing == -1 else (0.8, 0))
    cv.restore()
    if t > t1 + 0.5:
        s = pop(t - t1 - 0.5, 0.45)
        cv.save()
        cv.translate(W / 2, 170)
        cv.scale(s, s)
        ribbon(cv, "GERİ KAÇACAK YER YOK", 0, 0, 58)
        cv.restore()
    vignette(cv, 120)


def duel_pose(t, period=0.9, seed=0):
    ph = (t / period + seed * 0.37) % 1.0
    if ph < 0.35:
        a = lerp(150, 60, ph / 0.35)
    else:
        a = lerp(60, 150, (ph - 0.35) / 0.65)
    return a


def day1_duels(cv, t, d, p):
    t2 = lt(p, 2)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.12, (960, 560), (960, 620))
    bgk(cv, "yarmouk_golden", B.yarmouk, "golden")
    E.army(cv, t, [(760, 0.3, -60, 560, 44), (820, 0.38, -60, 500, 56)], facing=1, seed=41)
    E.army(cv, t, [(760, 0.3, 1360, 1980, 44), (820, 0.38, 1420, 1980, 56)], facing=-1, mix=E.ROMAN_MIX, seed=42)
    fall = clamp((t - (t2 + 0.6)) / 0.6)
    a1 = duel_pose(t, 0.9, 0)
    a2 = duel_pose(t, 0.9, 0.5)
    approach = ease_out(clamp(t / 2.0))
    x1 = lerp(560, 820, approach)
    x2 = lerp(1360, 1100, approach)
    person(cv, "arab_soldier2", x1, 1010, 1.05, 1, t, expr="shout", arm_b=a1 if fall < 1 else 140, wpn=a1 + 20,
           look=(0.8, 0))
    if fall < 1:
        person(cv, "roman", x2, 1010, 1.05, -1, t, seed=3, expr="angry" if fall == 0 else "hurt", arm_b=a2,
               wpn=a2 + 20, weapon="sword", lean=-fall * 80, look=(0.8, 0))
    else:
        cv.save()
        cv.translate(x2 + 120, 1000)
        cv.rotate(-90)
        person(cv, "roman", 0, 0, 1.05, -1, t, seed=3, expr="hurt", weapon="sword", eyes_closed=True, breathe=False)
        cv.restore()
        FX.blood_pool(cv, x2 + 80, 1010, 1.4)
    # carpisma kivilcimlari
    period = 0.9
    for k in range(int(t / period) + 1):
        tc = k * period + 0.32 * period
        if t > 1.5 and fall == 0:
            FX.sparks(cv, (x1 + x2) / 2, 770, t, tc, 1.0, seed=k)
    if t2 > 0:
        FX.blood_splat(cv, x2 - 20, 820, t, t2 + 0.6, 1.2, seed=3)
        FX.impact_star(cv, x2 - 20, 820, t, t2 + 0.55, 1.4)
    cv.restore()
    day_badge(cv, 1, t)
    vignette(cv, 120)


def day2_dawn(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.shake(cv, t, 4 if t > 1.5 else 0)
    E.camera(cv, t, d, 1.0, 1.1, (960, 560))
    bgk(cv, "yarmouk_dawn", B.yarmouk, "dawn")
    charge = ease_in_out(clamp(t / (d * 0.9)))
    E.army(cv, t, [(780, 0.3, 1100, 2100, 46), (850, 0.4, 1150, 2200, 58), (940, 0.52, 1250, 2300, 74)],
           facing=-1, mix=E.ROMAN_MIX, seed=51, charge=lerp(0, 700, charge), expr="shout")
    FX.ground_dust(cv, 900, 1950, 960, t, a=110)
    if t > t1:
        ft = t - t1
        r = random.Random(3)
        for k in range(9):
            x = 1000 - ft * r.uniform(110, 170) + k * 70
            E.blit(cv, E.person_sprite(E.MUSLIM_MIX[k % 5], -1, "scared", 0.5 + (k % 3) * 0.05, seed=k % 3),
                   x, 930 + (k % 3) * 40 - abs(math.sin(t * 9 + k)) * 10)
    else:
        E.army(cv, t, [(900, 0.45, -60, 700, 70)], facing=1, seed=52, expr="surprised")
    cv.restore()
    day_badge(cv, 2, t)
    if t > t1 + 0.4:
        s = pop(t - t1 - 0.4, 0.4)
        cv.save()
        cv.translate(W / 2, 160)
        cv.scale(s, s)
        ribbon(cv, "SAĞ KANAT DAĞILIYOR!", 0, 0, 56)
        cv.restore()
    vignette(cv, 130)


def women_push(cv, t, d, p):
    t1 = lt(p, 1)
    a1, b1 = E.line_t(p, 1)
    turn = a1 + (b1 - a1) * 0.62
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08, (960, 560))
    bgk(cv, "muslim_camp_dawn", B.muslim_camp, "dawn")
    # kadinlar (sol), direklerle
    for k, (nm, x) in enumerate((("woman2", 260), ("mother", 470), ("woman3", 680))):
        shout = t > t1
        person(cv, nm, x, 1020 + (k % 2) * 16, 1.05, 1, t, seed=k, expr="shout" if shout else "determined",
               weapon="pole", arm_b=lerp(14, 70, clamp((t - t1) / 0.5)) + 10 * math.sin(t * 6 + k),
               wpn=lerp(0, 50, clamp((t - t1) / 0.5)), look=(0.8, 0))
    # kacan erkekler
    for k in range(4):
        base = 1250 + k * 170
        if t < turn:
            x = base - min(t, turn) * 120
            f = -1
            ex = "scared"
        else:
            x = base - turn * 120 + (t - turn) * 220
            f = 1
            ex = "determined"
        stopped = (t1 + 1.0 < t < turn)
        if stopped:
            x = base - (t1 + 1.0) * 120
            ex = "sad"
        person(cv, E.MUSLIM_MIX[k], x, 1010 + (k % 2) * 30, 0.95, f, t, seed=k + 3, expr=ex,
               walk=None if stopped else t * 12 + k, look=(0.8, 0))
    # tas atma
    if t > t1:
        for k in range(3):
            tt = (t - t1 - k * 0.5) % 1.5
            if t - t1 > k * 0.5 and tt < 0.8:
                sx, sy = 700 + k * 40, 760
                x = sx + tt * 700
                y = sy - math.sin(tt / 0.8 * math.pi) * 160 + tt * 120
                cv.drawPath(circle(x, y, 13), fill("#8a7a6a"))
                cv.drawPath(circle(x, y, 13), stroke(OUT, 3))
    cv.restore()
    if t > t1 + 0.4:
        s = pop(t - t1 - 0.4, 0.4)
        cv.save()
        cv.translate(W / 2, 160)
        cv.scale(s, s)
        ribbon(cv, "YERMÜK'ÜN KADINLARI", 0, 0, 56, color="#6a2a6a")
        cv.restore()
    vignette(cv, 120)


def melee(cv, t, cx, cy, s, seed, roman_win=False):
    r = random.Random(seed)
    for k in range(3):
        x = cx + (k - 1) * 260 * s
        y = cy + r.uniform(-20, 20) * s
        a1 = duel_pose(t, r.uniform(0.7, 1.0), r.random())
        a2 = duel_pose(t, r.uniform(0.7, 1.0), r.random())
        E_m = E.MUSLIM_MIX[r.randrange(5)]
        E_r = E.ROMAN_MIX[r.randrange(5)]
        person(cv, E_m, x - 70 * s, y, 0.8 * s, 1, t, seed=k, expr="shout", arm_b=a1, wpn=a1 + 20, weapon="sword")
        person(cv, E_r, x + 70 * s, y, 0.8 * s, -1, t, seed=k + 9, expr="angry", arm_b=a2, wpn=a2 + 20)
        FX.sparks(cv, x, y - 230 * s, t % 0.9, 0.3, s * 0.8, seed=k + seed)


def day3_chaos(cv, t, d, p):
    cv.save()
    E.shake(cv, t, 6)
    E.camera(cv, t, d, 1.05, 1.15, (960, 560))
    bgk(cv, "yarmouk_day", B.yarmouk, "day")
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#d8b080", 80))
    melee(cv, t, 500, 860, 0.7, 3)
    melee(cv, t, 1450, 870, 0.75, 7)
    FX.dust_cloud(cv, 960, 960, t, 3.0, a=150, seed=4, n=12)
    melee(cv, t, 950, 1080, 1.0, 11)
    for k in range(4):
        FX.blood_splat(cv, 400 + k * 380, 800, t % 1.6, 0.2 + k * 0.3, 0.9, seed=k)
    cv.restore()
    FX.ground_dust(cv, 0, 1920, 1080, t, a=100, density=14)
    day_badge(cv, 3, t)
    vignette(cv, 150)


def day4_arrows(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.06, (960, 560))
    bgk(cv, "yarmouk_day", B.yarmouk, "day")
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#8a3a2a", 40))
    # ermeni okcular
    for k in range(9):
        x = 1300 + (k % 3) * 200 + (k // 3) * 60
        y = 820 + (k // 3) * 70
        pull = (t * 1.2 + k * 0.3) % 1.0
        person(cv, "armenian_archer", x, y, 0.55, -1, t, seed=k, expr="angry", arm_b=90, wpn=90 + pull * 6,
               arm_a=70, look=(0.8, 0))
    # musluman saf, kalkanlar yukarda
    for k in range(7):
        x = 120 + k * 140
        person(cv, E.MUSLIM_MIX[k % 5], x, 960 + (k % 2) * 30, 0.75, 1, t, seed=k + 5, expr="scared",
               arm_a=150, look=(0.6, -0.8))
    FX.arrow_volley(cv, t, 1500, 640, 500, 860, n=60, dur=1.4, seed=1, s=0.7, spread=500, loop=1.6)
    cv.restore()
    day_badge(cv, 4, t)
    s = pop(t - 1.0, 0.45)
    if s > 0:
        cv.save()
        cv.translate(W / 2 + 120, 160)
        cv.scale(s, s)
        ribbon(cv, "GÖZLERİN KAYBEDİLDİĞİ GÜN", 0, 0, 56, color="#8a1010")
        cv.restore()
    if t > t1 + 0.6:
        f = ease_out(clamp((t - t1 - 0.6) / 0.5))
        cv.save()
        cv.translate(lerp(-400, 0, f), 0)
        cv.drawPath(rrect(80, 330, 520, 620, 30), lin_grad((0, 330), (0, 950), ["#8fb8d8", "#e8d0a0"]))
        cv.drawPath(rrect(80, 330, 520, 620, 30), stroke("#d9a83a", 6))
        cv.save()
        cv.clipPath(rrect(80, 330, 520, 620, 30), skia.ClipOp.kIntersect, True)
        person(cv, "arab_soldier", 340, 960, 1.7, 1, t, expr="determined", eyepatch=True, look=(0.6, 0))
        cv.restore()
        cv.restore()
    vignette(cv, 140)


def ikrima(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 560))
    bgk(cv, "yarmouk_sunset", B.yarmouk, "sunset")
    if t < t1 + 2.0:
        ch = ease_in(clamp((t - t1) / 2.0))

        def men(cc):
            for row in range(3):
                for k in range(14):
                    x = 60 + k * 82 + row * 30 + ch * 1500
                    y = 820 + row * 60
                    C.draw_person(cc, C.preset(E.MUSLIM_MIX[(k + row) % 5]),
                                  C.pose(arm_b=60 + 30 * math.sin(t * 5 + k), wpn=60, walk=t * 12 + k if ch > 0 else None),
                                  x, y, 0.42 + row * 0.06, 1)
            C.draw_person(cc, C.preset("arab_soldier2", weapon="sword"), C.pose(arm_b=150, wpn=160,
                                                                                    walk=t * 12 if ch > 0 else None),
                          1200 + ch * 1500, 1040, 1.1, 1)

        C.draw_silhouette(cv, men, glow="#ffb070", glow_sigma=10, glow_a=200)
        FX.dust_cloud(cv, 1700, 960, t, 3.0, col="#c86a4a", a=160, seed=8)
    else:
        f = clamp((t - t1 - 2.0) / 1.0)
        r = random.Random(4)
        for k in range(14):
            x = r.uniform(100, 1800)
            y = r.uniform(880, 1060)
            cv.save()
            cv.translate(x, y)
            cv.rotate(r.uniform(-30, 30))
            cv.drawLine(0, 0, 0, -160, stroke(OUT, 8))
            cv.drawLine(0, 0, 0, -160, stroke("#8a5a2e", 4))
            cv.restore()
            if k % 3 == 0:
                C.draw_shield(cv, C.preset("zeyd"), x + 40, y + 10, "round", 0.6)
        cv.drawRect(skia.Rect.MakeWH(W, H), fill("#3a0a0a", int(90 * f)))
    cv.restore()
    s = pop(t - 0.6, 0.4)
    if s > 0 and t < t1 + 2.0:
        cv.save()
        cv.translate(W / 2, 160)
        cv.scale(s, s)
        ribbon(cv, "İKRİME BİN EBU CEHİL • 400 YİĞİT", 0, 0, 52, color="#7a1a10")
        cv.restore()
    vignette(cv, 150)


def ease_in(x):
    x = clamp(x)
    return x * x * x


def zeyd_wounded(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.12, (960, 560), (960, 520))
    bgk(cv, "yarmouk_day", B.yarmouk, "day")
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#3a2a1a", 120))
    FX.dust_cloud(cv, 500, 900, t, 3.0, a=120, seed=2)
    FX.dust_cloud(cv, 1500, 900, t, 3.0, a=120, seed=5)
    sway = math.sin(t * 1.3) * 3
    person(cv, "zeyd", 960, 1130, 1.9, 1, t, expr="hurt", arrow=True, blood=1.0, shield=None, lean=sway,
           look=(0.3, 0.1), arm_b=10, wpn=-4)
    for k, (x, y, a) in enumerate(((620, 1040, 30), (720, 1060, -50), (1300, 1050, 110))):
        cv.save()
        cv.translate(x, y)
        cv.rotate(a)
        p_ = skia.Path()
        p_.moveTo(0, 0)
        p_.arcTo(skia.Rect.MakeLTRB(-50, -50, 50, 50), 0, 110, False)
        p_.close()
        shape(cv, p_, "#8a5a2a")
        cv.restore()
    cv.restore()
    hb = (t * 1.25) % 1.0
    pulse = math.exp(-hb * 8) + 0.6 * math.exp(-max(0, hb - 0.18) * 8) * (hb > 0.18)
    cv.drawRect(skia.Rect.MakeWH(W, H), rad_grad((W / 2, H / 2), 1150, [rgb("#ff0000", 0), rgb("#ff0000", 0),
                                                                    rgb("#8a0000", int(170 * pulse))], [0, 0.5, 1]))
    vignette(cv, 170)


def day5_truce(cv, t, d, p):
    t2 = lt(p, 2)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08)
    bgk(cv, "yarmouk_golden", B.yarmouk, "golden")
    person(cv, "vahan", 1450, 1030, 1.15, -1, t, expr="worried", talk=talk_on(t, p, [0]), look=(0.8, 0), arm_b=60,
           wpn=40)
    person(cv, "roman", 1700, 1010, 0.95, -1, t, seed=2, weapon="banner", banner_color="#f4f1ea", shield=None,
           arm_b=20, wpn=0)

    def halid(cc):
        C.draw_horse(cc, 520, 1060, 1.15, 1, phase=0.4, gallop=0.15, color="#3a2a1a",
                     rider=C.preset("arab_soldier2", weapon="sword", shield=None),
                     rider_pose=C.pose(arm_b=40, wpn=20))

    C.draw_silhouette(cv, halid, glow="#ffe2a0")
    cv.restore()
    label_tag(cv, "VAHAN", 1450, 520, 46, rot=3)
    label_tag(cv, "HALİD", 560, 420, 46, rot=-3)
    if t < t2:
        day_badge(cv, 5, t)
    s = pop(t - 0.8, 0.4)
    if s > 0 and t < t2:
        cv.save()
        cv.translate(1300, 300)
        cv.scale(s, s)
        speech_bubble(cv, "Ateşkes yapalım!", 0, 0, 120, 140, size=44)
        cv.restore()
    if t >= t2:
        E.quote_card(cv, "Bu işi bir an önce bitirmek için acelemiz var!", "Halid bin Velid", t, t2, y=360, size=50)
    vignette(cv, 120)


def day6_cavalry(cv, t, d, p):
    cv.save()
    E.shake(cv, t, 8)
    E.camera(cv, t, d, 1.0, 1.1)
    bgk(cv, "yarmouk_golden", B.yarmouk, "golden")
    E.cavalry(cv, t, [(760, 0.3, 1200, 2400, 140)], facing=1, rider="roman", armored=True, speed=260,
              color_mix=("#c8c0b0", "#8a8a8a"), seed=3)
    E.cavalry(cv, t, [(840, 0.42, -1600, 600, 170), (960, 0.58, -1700, 500, 230)], facing=1, rider="arab_soldier",
              speed=520, seed=7)
    FX.ground_dust(cv, 0, 1950, 1000, t, a=130, density=16)
    x = lerp(-500, 2300, clamp(t / d))
    C.draw_horse(cv, x, 1100, 1.4, 1, phase=t * 11, gallop=1.0, color="#e8e0d4",
                 rider=C.preset("zeyd", head_color="#f4efe2"), rider_pose=C.pose(expr="shout", arm_b=70, wpn=70))
    cv.restore()
    day_badge(cv, 6, t)
    FX.speed_lines(cv, t, W / 2, H / 2, a=60)
    vignette(cv, 130)


def bridge_night(cv, t, d, p):
    t1 = lt(p, 1) - 0.2

    def night(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.1, (960, 600))
        bgk(c, "ravine_night", B.ravine_bg, "night")
        n = 8
        for k in range(n):
            x = (k * 120 + t * 160) % 1400 + 360
            C.draw_horse(c, x, 650, 0.24, 1, phase=t * 9 + k, gallop=1.0, color="#3a2a1a",
                         rider=C.preset("arab_soldier"), rider_pose=C.pose(expr="shout", arm_b=90, wpn=70))
            fx, fy = x - 12, 540
            c.drawPath(circle(fx, fy, 22), blur_paint("#ffb040", 10, 200))
        for k in range(3):
            x = 1400 + k * 90 + (t * 100)
            person(c, "roman", x, 660, 0.24, 1, t, seed=k, expr="scared", walk=t * 12)
        c.restore()
        s = pop(t - 0.5, 0.4)
        if s > 0:
            c.save()
            c.translate(W / 2, 170)
            c.scale(s, s)
            ribbon(c, "DIRAR BİN EZVER • 500 SÜVARİ", 0, 0, 52, color="#1f3a6a")
            c.restore()

    def tac(c):
        tactical(c, t, dict(roman=1.0, muslim=1.0, bridge=t1 + 0.5, escape=t1 + 0.3))
        s = pop(t - t1 - 1.0, 0.4)
        if s > 0:
            c.save()
            c.translate(W / 2, 90)
            c.scale(s, s)
            ribbon(c, "KAÇIŞ YOLU KAPANDI", 0, 0, 52)
            c.restore()

    xfade_layers(cv, t, t1, 0.5, night, tac)
    vignette(cv, 140)


def sandstorm_ravine(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.shake(cv, t, 5)
    E.camera(cv, t, d, 1.0, 1.08, (960, 600), (1060, 640))
    bgk(cv, "cliff_storm", B.cliff, "storm")
    r = random.Random(7)
    push = ease_in_out(clamp((t - t1) / 3.6)) if t > t1 else 0.0
    for k in range(14):
        row = k % 2
        x0 = 560 + (k // 2) * 85 + row * 40
        y0 = 800 + row * 40
        delay = 0.0
        x = x0 + push * 720
        tt = (t - t1 - 3.6 * ((1150 - x0) / 720) - 0.2) if t > t1 else -1
        sc = 0.55 + row * 0.07
        if x < 1160 or tt < 0:
            x = min(x, 1150)
            person(cv, E.ROMAN_MIX[k % 5], x, y0, sc, -1, t, seed=k, expr="scared", look=(-0.6, -0.2),
                   arm_a=40 + 50 * push, walk=t * 10 + k if 0 < push < 1 else None)
        else:
            fy = y0 + 900 * tt * tt
            if fy < 1400:
                cv.save()
                cv.translate(x + tt * 120, fy - 120 * sc)
                cv.rotate(tt * 220)
                person(cv, E.ROMAN_MIX[k % 5], 0, 120 * sc, sc, -1, t, seed=k, expr="scared", arm_a=150, arm_b=150,
                       look=(0, -0.8))
                cv.restore()
    E.army(cv, t, [(860, 0.62, -260, 380, 110), (950, 0.72, -300, 300, 130)], facing=1, seed=61, expr="shout",
           charge=push * 340, march=0.0)
    cv.restore()
    FX.sandstorm(cv, t, 0.65, direction=1)
    if t > t1 + 0.4:
        s = pop(t - t1 - 0.4, 0.4)
        cv.save()
        cv.translate(W / 2, 150)
        cv.scale(s, s)
        ribbon(cv, "UÇURUMUN KENARINDA", 0, 0, 54, color="#7a3a10")
        cv.restore()
    vignette(cv, 150)


def silent_evening(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.15, 1.0, (960, 620), (960, 540))
    bgk(cv, "yarmouk_sunset", B.yarmouk, "sunset")
    r = random.Random(3)
    for k in range(22):
        x = r.uniform(0, W)
        y = r.uniform(780, 1060)
        s = 0.5 + (y - 780) / 300
        cv.save()
        cv.translate(x, y)
        cv.rotate(r.uniform(-35, 35))
        cv.drawLine(0, 0, 0, -170 * s, stroke(OUT, 8 * s))
        cv.drawLine(0, 0, 0, -170 * s, stroke("#6a4a2a", 4 * s))
        cv.restore()
        if k % 4 == 0:
            C.draw_shield(cv, C.preset("roman", shield_color="#7a2020"), x + 30, y, "byz", 0.5 * s)
    for k, x in enumerate((300, 1650)):
        cv.drawPath(smooth([(x - 30, 800), (x - 60 + math.sin(t + k) * 20, 500), (x + math.sin(t * 0.7 + k) * 40, 200),
                            (x + 40, 500), (x + 30, 800)]), blur_paint("#3a2a2a", 30, 120))
    person(cv, "zeyd", 960, 1020, 1.0, 1, t, expr="sad", bandage=True, shield=None, look=(0.2, 0.3), wpn=-14)
    for k in range(5):
        a = t * 0.6 + k * 1.3
        bx = 960 + math.cos(a) * (300 + k * 40)
        by = 260 + math.sin(a) * 60
        wing = math.sin(t * 8 + k) * 10
        cv.drawPath(poly([(bx - 22, by - wing), (bx, by + 4), (bx + 22, by - wing)], closed=False), stroke(OUT, 4))
    cv.restore()
    vignette(cv, 160)
