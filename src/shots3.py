"""Sahneler: Bolum 6 (Zaferden sonra), 7 (Veba), 8 (Bir askerin sonu) + kapanis"""
import math
import random

import skia

import backgrounds as B
import characters as C
import effects as FX
import engine as E
import scenery as S
from gfx import (OUT, W, H, big_number, circle, clamp, ease_in_out, ease_out, ellipse, fill, font, label_tag, lerp,
                 lin_grad, pop, poly, rad_grad, rgb, ribbon, rrect, shade, shape, smooth, speech_bubble, stroke,
                 text, tint, vignette, blur_paint, mix)
from shotkit import bgk, le, lf, lt, nlines, person, talk_on, walk_x, xfade_layers
from shots1 import hourglass


def ribbon_top(cv, s, t, t0, color="#c8202a", y=160, size=56):
    sc = pop(t - t0, 0.45)
    if sc <= 0:
        return
    cv.save()
    cv.translate(W / 2, y)
    cv.scale(sc, sc)
    ribbon(cv, s, 0, 0, size, color=color)
    cv.restore()


def omar_figure(cv, x, y, s, f, t, walk=None, seated=False, rope_to=None):
    """Halife Omer: saygi geregi yuzsuz, isikli siluet"""
    def fig(cc):
        C.draw_person(cc, C.preset("arab_soldier", weapon="staff" if not seated else None, shield=None,
                                   head_color="#f1e9d6", tunic="#8a6a46"),
                      C.pose(walk=walk, seated=seated, arm_b=30 if rope_to else 14, wpn=-8), x, y, s, f)
    C.draw_silhouette(cv, fig, glow="#ffe6a8", glow_sigma=14, glow_a=230)


# =================================================================== BOLUM 6
def casualties(cv, t, d, p):
    bgk(cv, "studio_dark", B.studio, "#cdb894", "#6a5a44")
    a, b = E.line_t(p, 0)
    ribbon_top(cv, "ZAFERİN BEDELİ", t, 0.2, color="#5a3a1a")
    for k, (x, col, title, fr) in enumerate(((560, "#1f7a3a", "MÜSLÜMANLAR", 0.25), (1360, "#b02a2a", "ROMALILAR", 0.7))):
        sc = pop(t - (a + (b - a) * fr), 0.45)
        if sc <= 0:
            continue
        cv.save()
        cv.translate(x, 600)
        cv.scale(sc, sc)
        cv.drawPath(rrect(-320, -260, 640, 520, 30), fill("#fbf3df"))
        cv.drawPath(rrect(-320, -260, 640, 520, 30), stroke(col, 8))
        text(cv, title, 0, -180, font("black", 48), col)
        if k == 0:
            n = int(3000 * ease_out(clamp((t - (a + (b - a) * fr)) / 1.4)))
            text(cv, f"~{n:,}".replace(",", "."), 0, -40, font("slab", 110), "#2a1a10")
            text(cv, "şehit", 0, 30, font("xb", 44), "#3a2a1a")
            for j in range(12):
                S.grave(cv, -250 + (j % 6) * 100, 150 + (j // 6) * 70, 0.5)
        else:
            text(cv, "ON BİNLERCE", 0, -50, font("slab", 76), "#2a1a10")
            text(cv, "ölü", 0, 20, font("xb", 44), "#3a2a1a")
            for j in range(12):
                C.draw_shield(cv, C.preset("roman", shield_color="#7a2020"), -250 + (j % 6) * 100,
                              150 + (j // 6) * 70, "byz", 0.42)
        cv.restore()
    vignette(cv, 120)


def zeyd_loot(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08)
    bgk(cv, "yarmouk_golden", B.yarmouk, "golden")
    happy = t > t1 + 1.0
    person(cv, "zeyd", 960, 1080, 1.5, 1, t, expr="happy" if happy else "tired", bandage=True, shield=None,
           weapon=None if t > t1 else "spear", arm_b=90 if happy else 14, arm_a=90 if happy else 14,
           look=(0.0, -0.4) if happy else (0.3, 0.2))
    cv.restore()
    if t > t1:
        a, b = E.line_t(p, 1)
        E.icon_card(cv, 330, 420, 320, 320, "ROMA ZIRHI", lambda c: S.mail_shirt(c, 0, 70, 1.0), t, a + (b - a) * 0.1)
        E.icon_card(cv, 1590, 420, 320, 320, "KILIÇ", lambda c: (c.rotate(40), C.draw_weapon(c, {}, 0, 50, 0, "sword")),
                    t, a + (b - a) * 0.3)

        def coins(c):
            for j in range(6):
                S.coin(c, -60 + (j % 3) * 60, 10 - (j // 3) * 40, 26, col="#d8dce0")

        E.icon_card(cv, 1590, 800, 320, 300, "GÜMÜŞ SİKKE", coins, t, a + (b - a) * 0.5)
        if t > a + (b - a) * 0.5:
            r = random.Random(9)
            for j in range(24):
                ph = (t * 0.8 + r.random()) % 1.0
                x = 960 + r.uniform(-300, 300)
                y = -40 + ph * 900
                S.coin(cv, x, y, 18, col="#d8dce0")
    vignette(cv, 110)


def heraclius_farewell(cv, t, d, p):
    t2 = lt(p, 2)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.12, (900, 560), (800, 600))
    bgk(cv, "coast", B.coast)
    S.sea(cv, W, 640, H, t, col="#3a5a7a")
    S.ship(cv, 760, 900, 1.6, t)
    bob = math.sin(t * 1.5) * 6
    person(cv, "heraclius", 680, 860 + bob, 0.85, 1, t, expr="sad", tears=t > t2, look=(0.9, -0.1), arm_b=40,
           arm_a=10)
    cv.restore()
    E.lower_third(cv, "HERAKLEİOS SURİYE'Yİ TERK EDİYOR", t, 0.4, lt(p, 1) + 1.0)
    if t >= t2:
        E.quote_card(cv, "Elveda Suriye! Düşmana ne güzel bir ülke bırakıyorum.", "İmparator Herakleios (rivayet)",
                     t, t2, y=330, size=50)
    vignette(cv, 140)


def jerusalem_siege(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 540), (1000, 500))
    bgk(cv, "city_jerusalem", B.city, "jerusalem")
    person(cv, "patriarch", 1000, 620, 0.62, -1, t, expr="determined", talk=talk_on(t, p, [1]), arm_b=60, wpn=0,
           look=(0.4, 0.3))
    E.army(cv, t, [(900, 0.4, -40, 760, 60), (980, 0.5, -60, 700, 76), (900, 0.4, 1240, 1960, 60),
                   (990, 0.5, 1260, 1980, 76)], facing=1, seed=71)
    cv.restore()
    E.lower_third(cv, "KUDÜS • 637", t, 0.4, 4.5)
    if t > t1 - 0.3:
        speech_bubble(cv, "Anahtarları yalnızca Halife'ye teslim ederim!", 1250, 300, 1060, 450, maxw=560, size=42)
    vignette(cv, 120)


def camel_with(cv, x, y, s, f, t, walking, rider_omar, other_walk_dx=180):
    phase = t * 4
    C.draw_camel(cv, x, y, s, f, phase=phase, walk=1.0 if walking else 0.0,
                 rider=None if rider_omar else C.preset("servant"),
                 rider_pose=C.pose(expr="worried" if not rider_omar else "neutral"))
    if rider_omar:
        bob = -abs(math.sin(phase)) * 6 * (1.0 if walking else 0.0) * s
        omar_figure(cv, x + f * (-10) * s, y + bob + (-284) * s, 0.8 * s, f, t, seated=True)
        # hizmetkar yurur
        person(cv, "servant", x + f * 280 * s, y, 0.95 * s, f, t, walk=t * 8 if walking else None, expr="happy")
        cv.drawLine(x + f * (280 * s - 50 * s), y - 140 * s, x + f * 250 * s, y - 330 * s, stroke("#a07840", 4))
    else:
        omar_figure(cv, x + f * 300 * s, y, 1.0 * s, f, t, walk=t * 8 if walking else None, rope_to=True)
        cv.drawLine(x + f * (300 * s + 50 * s), y - 150 * s, x + f * 250 * s, y - 330 * s, stroke("#a07840", 5))


def omar_journey(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.05)
    bgk(cv, "desert_hot", B.desert, "hot")
    x = lerp(200, 1300, t / d)
    swap_every = 2.4
    omar_rides = (t > t1) and (int((t - t1) / swap_every) % 2 == 0)
    camel_with(cv, x, 1000, 0.95, 1, t, True, omar_rides)
    cv.restore()
    for k in range(int(max(0, t - t1) / swap_every) + 1):
        if t > t1:
            FX.flash(cv, t, t1 + k * swap_every, 0.2, "#fff6d0", 120)
    s = pop(t - 0.6, 0.4)
    if s > 0:
        cv.save()
        cv.translate(W / 2, 150)
        cv.scale(s, s)
        ribbon(cv, "HALİFE ÖMER • BİR DEVE, BİR HİZMETKÂR", 0, 0, 50, color="#1f6a2a")
        cv.restore()
    if t > t1 + 0.3:
        label_tag(cv, "SIRAYLA BİNİYORLAR", 1500, 330, 44, rot=4)
    vignette(cv, 110)


def omar_arrives(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.12, (960, 560), (1000, 600))
    bgk(cv, "city_jerusalem", B.city, "jerusalem")
    S.gate(cv, 960, 760, 170, 200, open_=1.0)
    E.army(cv, t, [(880, 0.42, -40, 520, 64)], facing=1, seed=81, expr="surprised")
    for k, nm in enumerate(("townsman", "patriarch", "jewish_elder", "townsman2")):
        person(cv, nm, 1350 + k * 140, 900 + (k % 2) * 20, 0.6, -1, t, seed=k, expr="surprised", look=(0.6, 0))
    x = lerp(380, 820, clamp(t / d))
    camel_with(cv, x, 1000, 0.85, 1, t, True, False)
    person(cv, "zeyd", 180, 1120, 1.35, 1, t, expr="surprised" if t > t1 else "neutral", look=(0.8, -0.1))
    cv.restore()
    if t > t1 + 0.5:
        label_tag(cv, "HALİFE YAYA, HİZMETKÂR DEVEDE", 1200, 300, 46, rot=-3)
    vignette(cv, 120)


def church(cv, t, d, p):
    t1, t2 = lt(p, 1), lt(p, 2)
    if t < t1 - 0.2:
        bgk(cv, "studio_parch", B.studio, "#f1dfb4", "#b89060")
        S.scroll_shape(cv, 960, 560, 1000, 720 * ease_out(clamp(t / 0.6)) + 1)
        if t > 0.5:
            text(cv, "AHİTNAME", 960, 320, font("deco", 64), "#5a1a10")
            a, b = E.line_t(p, 0)
            for k, (s_, fr) in enumerate((("Canlarının güvencesi", 0.45), ("Mallarının güvencesi", 0.6),
                                           ("Kiliselerinin güvencesi", 0.75))):
                tt = a + (b - a) * fr
                al = clamp((t - tt) / 0.3)
                if al > 0:
                    E.check_mark(cv, 560, 440 + k * 110 - 14, 0.9, t, tt)
                    text(cv, s_, 620, 440 + k * 110, font("xb", 52), "#2a1a10", align="left", a=int(255 * al))
        vignette(cv, 100)
        return
    cv.save()
    E.camera(cv, t - t1, d - t1, 1.0, 1.1, (960, 600))
    bgk(cv, "church", B.church)
    person(cv, "patriarch", 1180, 840, 0.95, -1, t, expr="happy", arm_b=80, wpn=-10, look=(0.7, 0))
    omar_figure(cv, 760, 1040, 1.15, -1, t)
    cv.restore()
    if t >= t2:
        E.quote_card(cv, "Burada namaz kılarsam, ileride Müslümanlar burayı camiye çevirmek isteyebilir.",
                     "Halife Ömer (rivayet)", t, t2, y=330, size=46)
    else:
        speech_bubble(cv, "Buyurun, burada kılabilirsiniz.", 1400, 420, 1220, 560, maxw=480, size=40)
    vignette(cv, 120)


# =================================================================== BOLUM 7
def lying(cv, name, x, y, s, t, seed=0, **kw):
    cv.save()
    cv.translate(x, y)
    cv.rotate(-90)
    person(cv, name, 0, 0, s, 1, t, seed=seed, breathe=False, **kw)
    cv.restore()


def plague(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 560))
    bgk(cv, "plague_town", B.plague_town)
    shape(cv, rrect(330, 900, 560, 50, 10), "#6a5a44")
    lying(cv, "arab_soldier", 440, 890, 0.95, t, expr="tired", sick=True, shield=None, weapon=None)
    lying(cv, "townsman", 1120, 960, 0.9, t, seed=2, expr="tired", sick=True)
    person(cv, "mother", 1550, 1000, 0.9, -1, t, expr="sad", tears=True, look=(0.5, 0.6))
    cv.restore()
    FX.plague_miasma(cv, t, a=60 + 20 * math.sin(t))
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#1a3a1a", 50))
    if t > t1:
        E.year_stamp(cv, "638", t, t1 + 0.2, 1700, 180, 110)
        E.lower_third(cv, "AMVAS VEBASI", t, t1 + 0.4, d)
    vignette(cv, 170)


def omar_qadar(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08)
    bgk(cv, "desert_dusk", B.desert, "dusk")
    omar_figure(cv, 640, 1030, 1.25, 1, t)

    def ebu(cc):
        C.draw_person(cc, C.preset("arab_soldier", weapon="staff", shield=None), C.pose(arm_b=40, wpn=-10),
                      1280, 1030, 1.25, -1)

    C.draw_silhouette(cv, ebu, glow="#ffe2a0")
    cv.restore()
    label_tag(cv, "HALİFE ÖMER", 640, 420, 44, rot=-3)
    label_tag(cv, "EBU UBEYDE", 1280, 420, 44, rot=3)
    t1, t3 = lt(p, 1), lt(p, 3)
    if t1 <= t < lt(p, 2):
        E.quote_card(cv, "Allah'ın kaderinden mi kaçıyorsun?", "Ebu Ubeyde", t, t1, y=300, size=52)
    if t >= t3:
        E.quote_card(cv, "Evet. Allah'ın kaderinden, yine Allah'ın kaderine kaçıyoruz.", "Halife Ömer", t, t3, y=300,
                     size=52)
    vignette(cv, 140)


def plague_toll(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (960, 600))
    bgk(cv, "plague_town", B.plague_town)
    r = random.Random(4)
    for k in range(30):
        x = r.uniform(40, 1880)
        y = 820 + (k % 6) * 45 + r.uniform(-10, 10)
        S.grave(cv, x, y, 0.5 + (y - 820) / 400, col="#7a7a64")
    person(cv, "zeyd", 1450, 1080, 1.2, -1, t, expr="sad", tears=t > t1, shield=None, look=(0.4, 0.6), wpn=-16)
    cv.restore()
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#1a2a1a", 60))
    a, b = E.line_t(p, 0)
    sc = pop(t - 0.4, 0.45)
    if sc > 0:
        cv.save()
        cv.translate(600, 330)
        cv.scale(sc, sc)
        n = int(25000 * ease_out(clamp((t - 0.4) / 1.6)))
        big_number(cv, f"{n:,}".replace(",", "."), 0, 0, 130)
        text(cv, "kişi hayatını kaybetti", 0, 70, font("xb", 44), "#ffffff", oc=OUT, ow=4)
        cv.restore()
    if t > a + (b - a) * 0.55:
        s2 = pop(t - (a + (b - a) * 0.55), 0.4)
        cv.save()
        cv.translate(600, 560)
        cv.scale(s2, s2)
        label_tag(cv, "EBU UBEYDE BİN CERRAH (ö. 639)", 0, 0, 40, bg="#e8e4dc")
        cv.restore()
    vignette(cv, 170)


def zeyd_sick(cv, t, d, p):
    a, b = E.line_t(p, 0)
    rec = a + (b - a) * 0.62
    cv.save()
    E.camera(cv, t, d, 1.08, 1.0, (960, 640))
    bgk(cv, "room", B.room)
    if t > rec:
        FX.light_rays(cv, 1510, 300, t, n=8, a=int(70 * clamp((t - rec) / 0.6)), length=1000, spread=40, base_ang=125)
    shape(cv, rrect(560, 930, 800, 70, 20), "#e8dcc0")
    if t < rec:
        lying(cv, "zeyd", 700, 920, 1.0, t, expr="tired", sick=True, sweat=True, shield=None, weapon=None,
              eyes_closed=(t % 3) < 1.5)
        person(cv, "mother", 1420, 1000, 1.0, -1, t, expr="sad", look=(0.6, 0.5))
    else:
        person(cv, "zeyd", 960, 1000, 1.2, 1, t, expr="happy", shield=None, weapon=None, arm_a=120, arm_b=120,
               look=(0.3, -0.4))
        person(cv, "mother", 1420, 1000, 1.0, -1, t, expr="happy", tears=True, look=(0.6, 0))
    cv.restore()
    vignette(cv, 130)


# =================================================================== BOLUM 8
def divan(cv, t, d, p):
    t1 = lt(p, 1)
    a, b = E.line_t(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.06)
    bgk(cv, "room", B.room)
    shape(cv, rrect(380, 820, 560, 40, 8), "#6a4424")
    for x in (420, 880):
        shape(cv, rrect(x - 10, 860, 20, 140, 6), "#5a3a1e")
    person(cv, "scribe", 520, 1010, 1.1, 1, t, expr="neutral", arm_b=70 + 8 * math.sin(t * 9), wpn=30,
           look=(0.6, 0.4))
    S.book(cv, 700, 800, 260, 120)
    person(cv, "zeyd", 1300, 1020, 1.15, -1, t, expr="happy" if t > a + (b - a) * 0.55 else "neutral",
           shield=None, weapon=None, item="coin" if t > a + (b - a) * 0.75 else None,
           arm_b=60 if t > a + (b - a) * 0.75 else 14, look=(0.6, 0.2))
    cv.restore()
    ribbon_top(cv, "DİVAN: ASKERLERİN KAYIT DEFTERİ", t, 1.0, color="#1f5a6a", size=50)
    if t > t1:
        f = ease_out(clamp((t - t1) / 0.5)) * 0.8
        cv.save()
        cv.translate(1560, 420)
        cv.scale(f, f)
        cv.drawPath(rrect(-260, -230, 520, 460, 16), fill("#f4e8c8"))
        cv.drawPath(rrect(-260, -230, 520, 460, 16), stroke(OUT, 5))
        names = ["Abdullah b. Amr", "Halid b. Said", "Ubeyd b. Rafi", "Kays b. Hubeyre", "ZEYD"]
        for k, nm in enumerate(names):
            tt = t1 + 0.4 + k * 0.5
            n = int(len(nm) * clamp((t - tt) / 0.6))
            if n > 0:
                text(cv, nm[:n], -210, -150 + k * 80, font("xb" if nm != "ZEYD" else "black", 40 if nm != "ZEYD" else 52),
                     "#2a1a10" if nm != "ZEYD" else "#a01818", align="left")
        cv.restore()
        sc = pop(t - (a + (b - a) * 0.8), 0.4)
        if sc > 0:
            cv.save()
            cv.translate(1640, 760)
            cv.scale(sc, sc)
            label_tag(cv, "ATÂ = YILLIK MAAŞ", 0, 0, 44, bg="#fff0b0")
            cv.restore()
    vignette(cv, 120)


def land_rule(cv, t, d, p):
    t1 = lt(p, 1)
    cv.save()
    E.camera(cv, t, d, 1.0, 1.08)
    bgk(cv, "fields", B.fields)
    for k, x in enumerate((420, 760, 1120)):
        sw = math.sin(t * 4 + k) * 30
        person(cv, "farmer", x, 900 + k * 40, 0.8, 1 if k % 2 else -1, t, seed=k, expr="happy", arm_b=60 + sw,
               wpn=80 + sw)
    E.army(cv, t, [(660, 0.24, 1250, 1900, 50)], facing=-1, seed=91, march=20)
    cv.restore()

    def soldier_farm(c):
        E.blit(c, E.person_sprite("arab_soldier", 1, "happy", 0.5, seed=1), -20, 110)
        c.drawLine(40, 60, 90, -60, stroke("#8a5a2e", 8))
        E.cross_out(c, -110, -110, 110, 110, t, lf(p, 0, 0.7))

    def farmer_ok(c):
        E.blit(c, E.person_sprite("farmer", 1, "happy", 0.5, seed=1), 0, 110)
        E.check_mark(c, 70, -60, 1.0, t, t1 + 0.6)

    E.icon_card(cv, 1550, 380, 320, 320, "ASKER ÇİFTÇİ OLAMAZ", soldier_farm, t, lf(p, 0, 0.45), tsize=30)
    if t > t1:
        E.icon_card(cv, 1550, 760, 320, 320, "TOPRAK YERLİ HALKTA", farmer_ok, t, t1 + 0.2, tsize=30)
    vignette(cv, 110)


def panel(cv, x, y, w, h, t, t0, key, fn, draw_actors, title):
    s = pop(t - t0, 0.45)
    if s <= 0:
        return
    cv.save()
    cv.translate(x, y)
    cv.scale(s, s)
    cv.rotate((1 - s) * 6)
    cv.drawPath(rrect(-w / 2 + 8, -h / 2 + 10, w, h, 24), fill((0, 0, 0), 90))
    clip = rrect(-w / 2, -h / 2, w, h, 24)
    cv.save()
    cv.clipPath(clip, skia.ClipOp.kIntersect, True)
    cv.translate(-w / 2, -h / 2)
    cv.scale(w / W * 1.25, w / W * 1.25)
    cv.translate(-W * 0.1, -H * 0.12)
    bgk(cv, key, fn)
    draw_actors(cv)
    cv.restore()
    cv.drawPath(clip, stroke("#fbf3df", 10))
    cv.drawPath(clip, stroke(OUT, 4))
    label_tag(cv, title, 0, h / 2 + 10, 40)
    cv.restore()


def future_paths(cv, t, d, p):
    bgk(cv, "studio_warm", B.studio)
    t1 = lt(p, 1)
    a, b = E.line_t(p, 0)

    def sham(c):
        person(c, "zeyd", 820, 1000, 1.3, 1, t, expr="happy", shield=None, weapon=None, look=(0.7, 0))
        person(c, "woman3", 1160, 1000, 1.25, -1, t, seed=2, expr="happy", look=(0.7, 0))
        for k in range(4):
            y = 400 + math.sin(t * 2 + k) * 20
            shape(c, smooth([(1000 + k * 30 - 40, y), (1000 + k * 30, y + 40), (1000 + k * 30 + 40, y),
                             (1000 + k * 30, y - 20)]), "#e04050", w=3)

    def egy(c):
        for k in range(4):
            E.blit(c, E.person_sprite(E.MUSLIM_MIX[k], 1, "determined", 0.8, seed=k), 600 + k * 200, 1000)

    def ana(c):
        sh = math.sin(t * 40) * 3
        person(c, "zeyd", 960 + sh, 1000, 1.3, 1, t, expr="scared", cloak="#6a5a4a", arm_a=40, arm_b=40,
               look=(0.3, -0.3))

    panel(cv, 330, 500, 560, 420, t, a + 0.1, "city_damascus", lambda c: B.city(c, "damascus"), sham, "ŞAM: AİLE")
    panel(cv, 960, 500, 560, 420, t, a + (b - a) * 0.55, "egypt", B.egypt, egy, "MISIR SEFERİ")
    panel(cv, 1590, 500, 560, 420, t, t1 + 0.2, "snow", B.snow, ana, "ANADOLU AKINLARI")
    vignette(cv, 100)


def constantinople(cv, t, d, p):
    cv.save()
    E.camera(cv, t, d, 1.0, 1.1, (900, 560), (1000, 580))
    bgk(cv, "constantinople", B.constantinople)
    S.sea(cv, 640, 640, H, t, col="#3a6a8a")
    S.ship(cv, 300, 820, 0.8, t)
    S.ship(cv, 560, 760, 0.5, t + 1)

    def eyyub(cc):
        C.draw_person(cc, C.preset("elder", weapon="staff"), C.pose(arm_b=20, wpn=-6), 1050, 1040, 1.15, 1)

    C.draw_silhouette(cv, eyyub, glow="#ffe2a0")
    person(cv, "zeyd_old", 1380, 1050, 1.15, -1, t, expr="happy", look=(0.7, 0))
    cv.restore()
    E.year_stamp(cv, "669", t, 0.4, 1700, 180, 110)
    E.lower_third(cv, "KONSTANTİNOPOLİS SURLARI", t, 0.8, d)
    sc = pop(t - 2.5, 0.4)
    if sc > 0:
        cv.save()
        cv.translate(1050, 440)
        cv.scale(sc, sc)
        label_tag(cv, "EBU EYYUB EL-ENSARİ", 0, 0, 40, rot=-3)
        cv.restore()
    vignette(cv, 120)


def eyup(cv, t, d, p):
    t1 = lt(p, 1) - 0.3

    def grave_scene(c):
        c.save()
        E.camera(c, t, d, 1.0, 1.06)
        bgk(c, "constantinople", B.constantinople)
        c.drawRect(skia.Rect.MakeWH(W, H), fill("#2a1a3a", 90))
        S.grave(c, 1100, 990, 1.6, col="#cfc8b8")
        person(c, "zeyd_old", 1450, 1040, 1.1, -1, t, expr="sad", tears=True, look=(0.6, 0.5))
        c.restore()

    def turbe(c):
        c.save()
        E.camera(c, t - t1, d - t1, 1.0, 1.1, (960, 540))
        bgk(c, "turbe", B.turbe)
        S.banner_pole(c, 1500, 900, t, 420, col="#b0101a", size=1.0)
        cx, cy = 1500 + 70, 900 - 420 + 4 + 45
        c.drawPath(circle(cx - 6, cy, 22), fill("#f6f2ea"))
        c.drawPath(circle(cx + 2, cy, 18), fill("#b0101a"))
        c.restore()
        E.year_stamp(c, "1453", t, t1 + 0.3, 1600, 180, 120)
        E.lower_third(c, "EYÜP SULTAN • İSTANBUL", t, t1 + 0.8, d)
        sc = pop(t - (t1 + 2.5), 0.4)
        if sc > 0:
            c.save()
            c.translate(560, 330)
            c.scale(sc, sc)
            label_tag(c, "KABRİ AKŞEMSEDDİN BULDU", 0, 0, 40, rot=-3)
            c.restore()

    xfade_layers(cv, t, t1, 0.8, grave_scene, turbe)
    vignette(cv, 130)


def recap(cv, t, d, p):
    bgk(cv, "studio_warm", B.studio)
    a, b = E.line_t(p, 0)
    cv.drawLine(200, 900, 1720, 900, stroke(OUT, 14))
    cv.drawLine(200, 900, 1720 * min(1, 0.12 + t / 3), 900, stroke("#d9a83a", 8))
    items = [("zeyd_kid", "HİCAZ'DA ÇOCUK", "610'lar", 380, 0.0), ("zeyd", "YERMÜK'TE ASKER", "636", 960, 0.35),
             ("zeyd_old", "SURLARDA İHTİYAR", "669", 1540, 0.7)]
    for nm, lab, yr, x, fr in items:
        s = pop(t - (a + (b - a) * fr), 0.45)
        if s <= 0:
            continue
        cv.save()
        cv.translate(x, 880)
        cv.scale(s, s)
        person(cv, nm, 0, 0, 1.05 if nm != "zeyd_kid" else 1.2, 1, t, expr="happy", look=(0.2, 0))
        cv.restore()
        if s > 0.5:
            label_tag(cv, lab, x, 960, 38, rot=0)
            text(cv, yr, x, 1050, font("slab", 46), "#5a1a10")
    vignette(cv, 100)


def outro(cv, t, d, p):
    t1 = lt(p, 1)
    cv.drawRect(skia.Rect.MakeWH(W, H), rad_grad((W / 2, H * 0.4), 1300, ["#3a2414", "#1e130b", "#0a0604"]))
    FX.embers(cv, t, 30)
    a, b = E.line_t(p, 0)
    if t < t1 + 0.2:
        opts = [("A", "ATLI SÜVARİ", 0.22), ("B", "OKÇU", 0.42), ("C", "CESUR KADIN", 0.72)]
        for k, (letter, lab, fr) in enumerate(opts):
            x = 400 + k * 560
            s = pop(t - (a + (b - a) * fr), 0.45)
            if s <= 0:
                continue
            cv.save()
            cv.translate(x, 560)
            cv.scale(s, s)
            cv.drawPath(rrect(-230, -330, 460, 660, 30), fill("#f4e6c4"))
            cv.drawPath(rrect(-230, -330, 460, 660, 30), stroke("#d9a83a", 8))
            cv.save()
            cv.clipPath(rrect(-230, -330, 460, 660, 30), skia.ClipOp.kIntersect, True)
            if k == 0:
                C.draw_horse(cv, -20, 230, 0.85, 1, phase=t * 9, gallop=0.6, rider=C.preset("arab_soldier"),
                             rider_pose=C.pose(expr="shout", arm_b=60, wpn=60))
            elif k == 1:
                person(cv, "arab_archer", 0, 240, 1.15, 1, t, expr="determined", arm_b=90, wpn=90, arm_a=70)
            else:
                person(cv, "woman2", 0, 240, 1.15, 1, t, expr="shout", weapon="pole", arm_b=60, wpn=40)
            cv.restore()
            cv.drawPath(circle(-180, -280, 46), fill("#c8202a"))
            cv.drawPath(circle(-180, -280, 46), stroke(OUT, 4))
            text(cv, letter, -180, -262, font("slab", 52), "#ffffff")
            label_tag(cv, lab, 0, 300, 40)
            cv.restore()
        sc = pop(t - 0.3, 0.45)
        if sc > 0:
            cv.save()
            cv.translate(W / 2, 110)
            cv.scale(sc, sc)
            ribbon(cv, "SEN HANGİSİ OLURDUN?", 0, 0, 58)
            cv.restore()
    else:
        tt = t - t1
        s = pop(tt - 0.1, 0.6)
        cv.save()
        cv.translate(W / 2, 330)
        cv.scale(s * 0.9, s * 0.9)
        hourglass(cv, 0, 0, 1.0, t)
        cv.restore()
        text(cv, "ZAMAN KIRIĞI", W / 2, 560, font("deco", 76), "#e9c46a", a=int(255 * clamp(tt / 0.5)),
             shadow=(3, 5, 6, 160))
        text(cv, "Yorumlarda buluşalım!", W / 2, 640, font("xb", 46), "#f3e3bf", a=int(255 * clamp((tt - 0.4) / 0.5)))
        bs = pop(tt - 1.0, 0.5)
        if bs > 0:
            clicked = tt > 3.2
            cv.save()
            cv.translate(W / 2, 800)
            cv.scale(bs * (0.94 if 3.0 < tt < 3.3 else 1.0), bs * (0.94 if 3.0 < tt < 3.3 else 1.0))
            col = "#cc0000" if not clicked else "#5a5a5a"
            cv.drawPath(rrect(-260, -60, 520, 120, 60), fill(col))
            cv.drawPath(rrect(-260, -60, 520, 120, 60), stroke("#ffffff", 4))
            text(cv, "ABONE OL" if not clicked else "ABONE OLUNDU", 35, 18, font("black", 52 if not clicked else 42),
                 "#ffffff")
            # zil
            cv.drawPath(smooth([(-225, 20), (-221, -10), (-205, -26), (-189, -10), (-185, 20)]), fill("#ffffff"))
            cv.drawPath(circle(-205, 28, 6), fill("#ffffff"))
            cv.restore()
            # imlec
            cx = lerp(1500, W / 2 + 160, ease_in_out((tt - 1.6) / 1.2))
            cy = lerp(1000, 830, ease_in_out((tt - 1.6) / 1.2))
            if tt > 1.4:
                pth = poly([(cx, cy), (cx, cy + 56), (cx + 14, cy + 42), (cx + 26, cy + 66), (cx + 36, cy + 60),
                            (cx + 24, cy + 38), (cx + 44, cy + 38)])
                cv.drawPath(pth, fill("#ffffff"))
                cv.drawPath(pth, stroke("#000000", 3))
            if clicked:
                FX.impact_star(cv, W / 2 + 160, 830, t, t1 + 3.2, 1.0)
        fo = clamp((t - (d - 0.8)) / 0.8)
        if fo > 0:
            cv.drawRect(skia.Rect.MakeWH(W, H), fill("#000000", int(255 * fo)))
