"""Cizgi film karakterleri: insanlar, atlar, develer, silüetler.

Kanal stiline uygun: buyuk kafa, kocaman yuvarlak gozler, kalin kahverengi kontur.
Yerel koordinat: ayaklar (0,0), yukari negatif y.
"""
import math

import skia

from gfx import (OUT, OUTW, P, capsule, circle, ellipse, fill, lin_grad, mix, poly, rad_grad,
                 rgb, rrect, shade, shape, smooth, stroke, blur_paint)

SKIN_ARAB = "#d9a06e"
SKIN_DARK = "#b97f50"
SKIN_ROMAN = "#efc29a"
SKIN_LIGHT = "#f3cfae"


def rounded(pts, r=10):
    p = poly(pts)
    return p


def round_paint(base, r):
    base.setPathEffect(skia.CornerPathEffect.Make(r))
    return base


def rshape(cv, pts, fc, oc=OUT, w=OUTW, r=12, a=255):
    p = poly(pts)
    if fc is not None:
        cv.drawPath(p, round_paint(fill(fc, a), r))
    if oc is not None:
        cv.drawPath(p, round_paint(stroke(oc, w, a), r))
    return p


# ======================================================================== PRESETLER
def preset(name, **kw):
    base = dict(
        skin=SKIN_ARAB, beard=None, beard_color="#2a1a12", mustache=False,
        head="turban", head_color="#efe6d2", head_color2="#c9b58f", turban_tail=True,
        tunic="#a87a4a", tunic_long=True, belt="#5a3a22", sash=None,
        armor=None, cloak=None, legs="#d9a06e", boots=False, shoe="#5b3a22",
        shield=None, shield_color="#9a6a3a", weapon=None, item=None,
        age="adult", female=False, body=1.0, head_scale=1.0, expr="neutral",
        quiver=False, eyepatch=False, cross=False, hair="#2a1a12", plume="#c0262b",
        banner_color="#1d1b1a",
    )
    P_ = {
        "zeyd": dict(beard="stubble", head="turban", head_color="#f1e9d6", tunic="#b4834f",
                     sash="#b23a2a", weapon="spear", shield="round", age="young"),
        "zeyd_kid": dict(beard=None, head="kufi", head_color="#f3ead8", tunic="#c8a170", body=0.7,
                         head_scale=0.92, age="kid", sash=None),
        "zeyd_old": dict(beard="long", beard_color="#e8e4dc", head="turban", head_color="#f1e9d6",
                         tunic="#8f6a46", age="old", sash="#7a2a20", weapon="staff"),
        "arab_soldier": dict(beard="short", head="turban", head_color="#e9dcc0", tunic="#9c7448",
                             weapon="spear", shield="round"),
        "arab_soldier2": dict(beard="full", head="turban", head_color="#3b3430", tunic="#7f6a52",
                              weapon="sword", shield="round", shield_color="#7d5a35", armor="mail"),
        "arab_archer": dict(beard="short", head="turban", head_color="#d8c49c", tunic="#8a6a40",
                            weapon="bow", quiver=True),
        "father": dict(beard="full", beard_color="#6d6660", head="keffiyeh", head_color="#f2efe8",
                       head_color2="#a8282b", tunic="#7a5a3c", age="old", weapon="staff"),
        "mother": dict(female=True, head="veil", head_color="#3a2f3d", tunic="#4b3b52", beard=None),
        "woman2": dict(female=True, head="veil", head_color="#6b2a2a", tunic="#5a3030", beard=None),
        "woman3": dict(female=True, head="veil", head_color="#2f3f55", tunic="#3b4a5e", beard=None),
        "elder": dict(beard="long", beard_color="#e5e0d8", head="keffiyeh", head_color="#f2efe8",
                      head_color2="#2a2a2a", tunic="#6b5038", age="old"),
        "messenger": dict(beard="short", head="turban", head_color="#22201e", tunic="#5e4a36",
                          weapon="banner", banner_color="#1d1b1a"),
        "ghassanid": dict(beard="full", head="keffiyeh", head_color="#e8e2d6", head_color2="#3a3a3a",
                          tunic="#6f4a3a", weapon="spear", shield="round", cross=True),
        "roman": dict(skin=SKIN_ROMAN, beard="short", beard_color="#4a3020", head="byz_helmet",
                      tunic="#b02a2a", tunic_long=False, armor="lamellar", cloak="#8c1f22",
                      legs="#6b5a4a", boots=True, weapon="spear", shield="byz", shield_color="#b3262a"),
        "roman_archer": dict(skin=SKIN_ROMAN, beard="stubble", head="byz_helmet", plume="#1f4f8a",
                             tunic="#2f5e8f", tunic_long=False, armor="lamellar", legs="#5a4a3a",
                             boots=True, weapon="bow", quiver=True),
        "armenian_archer": dict(skin=SKIN_ROMAN, beard="full", beard_color="#1e1410", head="byz_helmet",
                                plume="#2f6b3a", tunic="#3d6b45", tunic_long=False, armor="mail",
                                legs="#4a3a2a", boots=True, weapon="bow", quiver=True),
        "vahan": dict(skin=SKIN_ROMAN, beard="full", beard_color="#1e1410", head="byz_helmet",
                      plume="#e0b030", tunic="#6a1e5a", tunic_long=False, armor="lamellar",
                      cloak="#4b1450", legs="#4a3a2a", boots=True, weapon="sword"),
        "heraclius": dict(skin=SKIN_ROMAN, beard="long", beard_color="#8a7a6a", head="crown",
                          tunic="#5b1d6e", tunic_long=True, cloak="#7b2a8e", belt="#d9a83a",
                          age="old", legs="#5b1d6e", boots=True),
        "patriarch": dict(skin=SKIN_ROMAN, beard="long", beard_color="#efece6", head="mitre",
                          head_color="#1a1a1a", tunic="#1c1c1c", tunic_long=True, cloak="#2b2b2b",
                          belt="#d9a83a", age="old", weapon="staff", cross=True),
        "townsman": dict(skin=SKIN_ROMAN, beard="short", head="hair", tunic="#5a7a8a", tunic_long=True,
                         beard_color="#3a2a1a"),
        "townsman2": dict(skin="#e2b088", beard="full", head="cap", head_color="#8a5a2a",
                          tunic="#7a8a4a", tunic_long=True, beard_color="#2a1a12"),
        "jewish_elder": dict(skin="#e2b088", beard="long", beard_color="#cfc9c0", head="cap",
                             head_color="#2e3b6b", tunic="#4a5a7a", age="old"),
        "farmer": dict(skin="#d8a070", beard="short", head="cap", head_color="#c7b08a", tunic="#7d6a45",
                       weapon="hoe"),
        "scribe": dict(beard="full", beard_color="#3a2a1a", head="turban", head_color="#f7f2e6",
                       tunic="#4a6a5a", item="pen"),
        "servant": dict(beard="short", head="turban", head_color="#d5c3a0", tunic="#8b6f4e"),
        "kid": dict(head="hair", tunic="#c9a070", body=0.66, head_scale=0.9, age="kid"),
    }
    d = dict(base)
    d.update(P_.get(name, {}))
    d.update(kw)
    d["name"] = name
    return d


DEFAULT_POSE = dict(arm_a=14, arm_b=14, wpn=8, walk=None, bob=0.0, look=(0.35, 0.0), blink=0.0,
                    mouth=0.0, expr=None, lean=0.0, seated=False, hurt=False, tears=False,
                    sweat=False, sick=False, bandage=False, arrow=False, blood=0.0, eyes_closed=False)


def pose(**kw):
    d = dict(DEFAULT_POSE)
    d.update(kw)
    return d


# ======================================================================== YUZ
def draw_face(cv, c, ps, expr):
    skin = c["skin"]
    look = ps["look"]
    blink = ps["blink"]
    old = c["age"] == "old"
    big = expr in ("scared", "surprised")
    er = 19 if not big else 22
    if c["age"] == "kid":
        er += 2
    pr = 8 if not big else 5.5
    eye_y = -6
    for sx in (-1, 1):
        ex = sx * 24
        cv.drawPath(circle(ex, eye_y, er), fill("#ffffff"))
        # gozbebegi
        px = ex + look[0] * (er - pr - 3)
        py = eye_y + look[1] * (er - pr - 3)
        lid = blink
        if expr == "tired":
            lid = max(lid, 0.45)
        if expr in ("angry", "shout", "determined"):
            lid = max(lid, 0.18)
        if ps.get("sick"):
            lid = max(lid, 0.5)
        if expr == "hurt" and sx == -1:
            lid = max(lid, 0.85)
        closed = ps.get("eyes_closed") or lid > 0.92 or (expr == "happy" and ps.get("mouth", 0) > 0.85)
        if not closed:
            cv.drawPath(circle(px, py, pr), fill("#1a120c"))
            cv.drawPath(circle(px - pr * 0.35, py - pr * 0.4, pr * 0.32), fill("#ffffff"))
            if lid > 0.02:
                cv.save()
                cv.clipPath(circle(ex, eye_y, er + 0.5), skia.ClipOp.kIntersect, True)
                cv.drawRect(skia.Rect.MakeLTRB(ex - er - 2, eye_y - er - 2, ex + er + 2,
                                               eye_y - er + 2 * er * lid), fill(shade(skin, 0.92)))
                cv.drawLine(ex - er, eye_y - er + 2 * er * lid, ex + er, eye_y - er + 2 * er * lid,
                            stroke(OUT, 3))
                cv.restore()
            cv.drawPath(circle(ex, eye_y, er), stroke(OUT, 3.6))
        else:
            cv.drawPath(circle(ex, eye_y, er), fill(shade(skin, 0.92)))
            cv.drawPath(circle(ex, eye_y, er), stroke(OUT, 3.0))
            arc = P()
            arc.moveTo(ex - er * 0.8, eye_y + 2)
            arc.quadTo(ex, eye_y + (8 if expr != "happy" else -9), ex + er * 0.8, eye_y + 2)
            cv.drawPath(arc, stroke(OUT, 3.6))
        if ps.get("eyepatch") and sx == -1:
            cv.drawPath(circle(ex, eye_y, er + 2), fill("#1b1410"))
            cv.drawLine(-60, -30, 55, -10, stroke("#1b1410", 5))
    # kaslar
    bc = c["beard_color"] if c.get("beard") else c.get("hair", "#2a1a12")
    if c["female"]:
        bc = "#2a1a12"
    for sx in (-1, 1):
        x0, x1 = sx * 10, sx * 40
        y0 = y1 = -32
        if expr in ("angry", "shout", "determined", "hurt"):
            y0 += 8; y1 -= 4
        elif expr in ("sad", "scared", "worried"):
            y0 -= 8; y1 += 3
        elif expr in ("surprised", "happy"):
            y0 -= 7; y1 -= 7
        if big:
            y0 -= 4; y1 -= 4
        cv.drawLine(x0, y0, x1, y1, stroke(bc if not old else "#cfc8be", 7 if not c["female"] else 5))
    # burun
    cv.drawPath(ellipse(0, 16, 9, 7), fill(shade(skin, 0.85)))
    nose = P()
    nose.moveTo(-8, 18)
    nose.quadTo(0, 25, 8, 18)
    cv.drawPath(nose, stroke(OUT, 3))
    # yanak
    if c["female"] or c["age"] == "kid":
        for sx in (-1, 1):
            cv.drawPath(circle(sx * 38, 18, 9), fill("#e77d6a", 90))
    if old:
        for sx in (-1, 1):
            w = P()
            w.moveTo(sx * 44, -4)
            w.quadTo(sx * 50, 0, sx * 47, 8)
            cv.drawPath(w, stroke(shade(skin, 0.7), 2.4))


def draw_mouth(cv, c, ps, expr):
    m = ps["mouth"]
    my = 38
    if expr in ("shout",) or m > 0.05 or expr in ("surprised",):
        op = max(m, 0.9 if expr == "shout" else 0.0, 0.55 if expr == "surprised" else 0.0)
        wdt = 15 + 6 * op if expr != "shout" else 22
        hgt = 3 + 15 * op
        if expr == "surprised":
            wdt = 10
        path = ellipse(0, my + 2, wdt, hgt)
        cv.drawPath(path, fill("#5a1a14"))
        cv.save()
        cv.clipPath(path, skia.ClipOp.kIntersect, True)
        cv.drawPath(ellipse(0, my + 2 + hgt * 0.8, wdt * 0.7, hgt * 0.6), fill("#d0605a"))
        if expr in ("shout", "angry", "hurt"):
            cv.drawRect(skia.Rect.MakeLTRB(-wdt, my + 2 - hgt, wdt, my + 2 - hgt * 0.55), fill("#ffffff"))
        cv.restore()
        cv.drawPath(path, stroke(OUT, 3.4))
        return
    p = P()
    if expr == "happy":
        p.moveTo(-18, my - 4)
        p.quadTo(0, my + 16, 18, my - 4)
        p.close()
        cv.drawPath(p, fill("#5a1a14"))
        cv.drawPath(p, stroke(OUT, 3.4))
    elif expr in ("sad", "worried", "tired"):
        p.moveTo(-13, my + 6)
        p.quadTo(0, my - 5, 13, my + 6)
        cv.drawPath(p, stroke(OUT, 3.6))
    elif expr == "scared":
        p.moveTo(-14, my + 2)
        for i in range(1, 8):
            p.lineTo(-14 + i * 4, my + (3 if i % 2 else -2))
        cv.drawPath(p, stroke(OUT, 3.4))
    elif expr in ("angry", "determined", "hurt"):
        cv.drawPath(rrect(-15, my - 4, 30, 9, 3), fill("#ffffff"))
        cv.drawPath(rrect(-15, my - 4, 30, 9, 3), stroke(OUT, 3))
        cv.drawLine(-15, my + 0.5, 15, my + 0.5, stroke(OUT, 1.6))
    else:
        p.moveTo(-12, my)
        p.quadTo(0, my + 7, 12, my)
        cv.drawPath(p, stroke(OUT, 3.6))


def draw_beard_back(cv, c):
    pass


def draw_beard(cv, c, ps):
    b = c.get("beard")
    if not b:
        return
    bc = c["beard_color"]
    skin = c["skin"]
    if b == "stubble":
        p = smooth([(-56, 12), (-40, 44), (0, 62), (40, 44), (56, 12), (30, 30), (0, 34), (-30, 30)])
        cv.drawPath(p, fill(mix(skin, bc, 0.35), 170))
        return
    ext = {"short": 70, "full": 86, "long": 128}[b]
    pts = [(-61, -6), (-60, 26), (-44, 56), (-18, ext - 6), (0, ext), (18, ext - 6), (44, 56), (60, 26),
           (61, -6), (50, 18), (30, 30), (0, 28), (-30, 30), (-50, 18)]
    if b == "long":
        pts = [(-61, -6), (-60, 30), (-46, 70), (-22, 110), (0, ext), (22, 110), (46, 70), (60, 30),
               (61, -6), (50, 18), (30, 30), (0, 28), (-30, 30), (-50, 18)]
    p = smooth(pts, tension=0.45)
    cv.drawPath(p, fill(bc))
    cv.drawPath(p, stroke(OUT, 3.6))
    # dokular
    for i in range(-2, 3):
        l = P()
        l.moveTo(i * 15, 46)
        l.quadTo(i * 17, ext - 22, i * 12, ext - 12)
        cv.drawPath(l, stroke(shade(bc, 0.75 if sum(shade(bc, 1)) > 150 else 1.4), 2.2))
    # biyik
    m = smooth([(-26, 30), (-12, 22), (0, 25), (12, 22), (26, 30), (12, 30), (0, 31), (-12, 30)])
    cv.drawPath(m, fill(shade(bc, 0.9)))
    cv.drawPath(m, stroke(OUT, 2.6))


# ======================================================================== BAS
def draw_head_back(cv, c, ps):
    h = c["head"]
    hc = c["head_color"]
    if h == "turban" and c.get("turban_tail", True):
        tail = smooth([(-46, -20), (-66, 14), (-70, 70), (-60, 100), (-50, 66), (-50, 20)], closed=True)
        shape(cv, tail, shade(hc, 0.88))
    elif h == "keffiyeh":
        back = smooth([(-70, -50), (-30, -88), (30, -88), (70, -50), (84, 40), (100, 118), (-100, 118),
                       (-84, 40)], tension=0.5)
        shape(cv, back, hc)
        # desen
        cv.save()
        cv.clipPath(back, skia.ClipOp.kIntersect, True)
        c2 = c["head_color2"]
        for yy in range(-90, 130, 18):
            cv.drawLine(-110, yy, 110, yy + 30, stroke(c2, 2.2, 150))
            cv.drawLine(-110, yy + 30, 110, yy, stroke(c2, 2.2, 150))
        cv.restore()
        shape(cv, back, None)
    elif h == "veil":
        back = smooth([(-74, -40), (-40, -86), (40, -86), (74, -40), (84, 40), (96, 122), (-96, 122),
                       (-84, 40)], tension=0.5)
        shape(cv, back, hc)
    elif h == "byz_helmet":
        av = smooth([(-66, -10), (-74, 60), (-50, 92), (50, 92), (74, 60), (66, -10)], closed=True)
        shape(cv, av, "#8d949c")
        cv.save()
        cv.clipPath(av, skia.ClipOp.kIntersect, True)
        for yy in range(-10, 100, 9):
            for xx in range(-80, 80, 9):
                cv.drawPath(circle(xx + (yy // 9 % 2) * 4.5, yy, 3.6), stroke("#5f666e", 1.6))
        cv.restore()
        shape(cv, av, None)
    elif h == "crown":
        # sac arkada
        hair = smooth([(-62, -20), (-70, 30), (-60, 70), (60, 70), (70, 30), (62, -20)], closed=True)
        shape(cv, hair, c["beard_color"])


def draw_head_front(cv, c, ps):
    h = c["head"]
    hc = c["head_color"]
    if h == "turban":
        main = smooth([(-64, -12), (-72, -42), (-56, -76), (-20, -92), (20, -92), (56, -76), (72, -42),
                       (64, -12), (32, -24), (0, -26), (-32, -24)], tension=0.5)
        shape(cv, main, hc)
        cv.save()
        cv.clipPath(main, skia.ClipOp.kIntersect, True)
        for k, (y0, y1) in enumerate([(-34, -62), (-50, -80), (-22, -46)]):
            f = P()
            f.moveTo(-74, y0 + 12)
            f.quadTo(0, y1, 74, y0 + 4 * (k + 1))
            cv.drawPath(f, stroke(shade(hc, 0.78), 3.2))
        cv.drawPath(ellipse(20, -60, 40, 14), fill(shade(hc, 1.12), 120))
        cv.restore()
        shape(cv, main, None)
    elif h == "kufi":
        cap = smooth([(-58, -20), (-56, -60), (0, -78), (56, -60), (58, -20), (0, -30)], tension=0.5)
        shape(cv, cap, hc)
        for x in range(-40, 50, 16):
            cv.drawPath(circle(x, -46, 3), fill(shade(hc, 0.75)))
    elif h == "keffiyeh":
        front = smooth([(-66, -16), (-70, -50), (-40, -84), (40, -84), (70, -50), (66, -16), (30, -30),
                        (0, -32), (-30, -30)], tension=0.5)
        shape(cv, front, hc)
        cv.save()
        cv.clipPath(front, skia.ClipOp.kIntersect, True)
        c2 = c["head_color2"]
        for yy in range(-100, 0, 16):
            cv.drawLine(-80, yy, 80, yy + 24, stroke(c2, 2.0, 150))
            cv.drawLine(-80, yy + 24, 80, yy, stroke(c2, 2.0, 150))
        cv.restore()
        shape(cv, front, None)
        # agal
        cv.drawPath(ellipse(0, -60, 62, 14), stroke("#141210", 9))
        cv.drawPath(ellipse(0, -48, 66, 13), stroke("#141210", 8))
    elif h == "veil":
        outer = ellipse(0, -8, 76, 84)
        inner = ellipse(0, 8, 52, 58)
        frame = skia.Op(outer, inner, skia.PathOp.kDifference_PathOp)
        clipb = P()
        clipb.addRect(skia.Rect.MakeLTRB(-120, -120, 120, 60))
        frame = skia.Op(frame, clipb, skia.PathOp.kIntersect_PathOp)
        shape(cv, frame, hc)
        cv.drawLine(-46, -36, 46, -36, stroke(shade(hc, 1.3), 4, 150))
    elif h == "byz_helmet":
        # tepe sorgucu
        pl = smooth([(-8, -92), (-30, -120), (-70, -126), (-96, -104), (-80, -112), (-50, -108),
                     (-20, -96)], tension=0.5)
        shape(cv, pl, c.get("plume", "#c0262b"))
        dome = P()
        dome.moveTo(-66, -14)
        dome.cubicTo(-70, -70, -40, -100, 0, -102)
        dome.cubicTo(40, -100, 70, -70, 66, -14)
        dome.quadTo(0, -30, -66, -14)
        dome.close()
        cv.drawPath(dome, lin_grad((-60, -100), (60, -10), ["#e6eaee", "#a9b1b9", "#6f7780"]))
        cv.drawPath(dome, stroke(OUT, OUTW))
        for x in (-30, 0, 30):
            cv.drawLine(x, -97 + abs(x) * 0.3, x * 1.1, -24, stroke("#c9a040", 6))
        band = P()
        band.moveTo(-66, -14)
        band.quadTo(0, -32, 66, -14)
        cv.drawPath(band, stroke("#c9a040", 10))
        cv.drawPath(band, stroke(OUT, 2.4))
        for sx in (-1, 1):
            cheek = rrect(sx * 64 - 11, -18, 22, 56, 10)
            shape(cv, cheek, "#a9b1b9", w=3)
        cv.drawPath(circle(0, -102, 7), fill("#c9a040"))
        cv.drawPath(circle(0, -102, 7), stroke(OUT, 2.5))
    elif h == "crown":
        cap = smooth([(-54, -40), (-48, -80), (0, -96), (48, -80), (54, -40)], closed=True)
        shape(cv, cap, "#6a1f7a")
        band = rrect(-62, -54, 124, 30, 8)
        cv.drawPath(band, lin_grad((0, -54), (0, -24), ["#fff0a0", "#e0a92e", "#a8701a"]))
        cv.drawPath(band, stroke(OUT, 3.5))
        for i, x in enumerate(range(-44, 50, 22)):
            cv.drawPath(circle(x, -39, 6), fill("#c0262b" if i % 2 else "#2a6ad0"))
            cv.drawPath(circle(x, -39, 6), stroke(OUT, 2))
        cv.drawLine(0, -96, 0, -132, stroke("#e0a92e", 7))
        cv.drawLine(-14, -118, 14, -118, stroke("#e0a92e", 7))
        cv.drawLine(0, -96, 0, -132, stroke(OUT, 1.5))
        for sx in (-1, 1):
            for k in range(5):
                cv.drawPath(circle(sx * 62, -20 + k * 12, 5), fill("#fbf6ea"))
                cv.drawPath(circle(sx * 62, -20 + k * 12, 5), stroke(OUT, 1.6))
    elif h == "mitre":
        m = smooth([(-48, -26), (-46, -80), (0, -98), (46, -80), (48, -26)], closed=True)
        shape(cv, m, "#1c1c1c")
        cv.drawLine(0, -92, 0, -40, stroke("#d9a83a", 4))
        cv.drawLine(-14, -70, 14, -70, stroke("#d9a83a", 4))
    elif h == "hair":
        hr = smooth([(-62, -6), (-64, -50), (-30, -78), (20, -80), (60, -52), (62, -8), (40, -40),
                     (0, -46), (-36, -40)], tension=0.5)
        shape(cv, hr, c.get("hair", "#2a1a12") if c["age"] != "old" else "#cfc8be")
    elif h == "cap":
        cap = smooth([(-60, -24), (-58, -64), (0, -84), (58, -64), (60, -24), (0, -34)], tension=0.5)
        shape(cv, cap, hc)


def draw_head(cv, c, ps, expr):
    s = c.get("head_scale", 1.0)
    cv.save()
    cv.scale(s, s)
    draw_head_back(cv, c, ps)
    skin = c["skin"]
    if ps.get("sick"):
        skin = mix(skin, "#a8b48a", 0.45)
    # kulaklar
    if c["head"] not in ("veil", "keffiyeh", "byz_helmet"):
        for sx in (-1, 1):
            shape(cv, circle(sx * 60, 4, 12), shade(skin, 0.95), w=3.2)
    head = ellipse(0, 0, 60, 64)
    cv.drawPath(head, fill(skin))
    cv.save()
    cv.clipPath(head, skia.ClipOp.kIntersect, True)
    cv.drawPath(ellipse(28, 18, 50, 60), fill(shade(skin, 0.9), 120))
    cv.restore()
    cv.drawPath(head, stroke(OUT, OUTW))
    cc = dict(c)
    cc["skin"] = skin
    draw_beard(cv, cc, ps)
    draw_face(cv, cc, ps, expr)
    draw_mouth(cv, cc, ps, expr)
    if ps.get("sweat") or ps.get("sick"):
        for (x, y) in ((52, -40), (-56, -20)):
            d = smooth([(x, y - 12), (x + 6, y + 2), (x, y + 8), (x - 6, y + 2)])
            shape(cv, d, "#9fd4ff", w=2)
    if ps.get("tears"):
        for sx in (-1, 1):
            d = smooth([(sx * 26, 14), (sx * 31, 30), (sx * 26, 36), (sx * 21, 30)])
            shape(cv, d, "#8fd0ff", w=2)
    draw_head_front(cv, c, ps)
    if ps.get("bandage"):
        b = rrect(-64, -40, 128, 20, 8)
        shape(cv, b, "#f3eee2", w=3)
        cv.drawPath(circle(-30, -30, 7), fill("#b0201a", 200))
    cv.restore()


# ======================================================================== SILAHLAR
def draw_weapon(cv, c, hx, hy, ang, kind):
    r = math.radians(ang)
    dx, dy = math.sin(r), -math.cos(r)
    nx, ny = -dy, dx
    if kind in ("spear", "staff", "pole", "banner", "hoe", "torch"):
        top = 200 if kind != "staff" else 120
        if kind == "pole":
            top = 170
        bot = -90 if kind != "staff" else -150
        x0, y0 = hx + dx * bot, hy + dy * bot
        x1, y1 = hx + dx * top, hy + dy * top
        capsule(cv, x0, y0, x1, y1, 7, "#8a5a2e", ow=3)
        if kind == "spear":
            tip = poly([(x1 - nx * 9, y1 - ny * 9), (x1 + dx * 48, y1 + dy * 48), (x1 + nx * 9, y1 + ny * 9),
                        (x1 - dx * 6, y1 - dy * 6)])
            cv.drawPath(tip, lin_grad((x1 - nx * 9, y1), (x1 + nx * 9, y1), ["#f2f4f6", "#9aa3ab"]))
            cv.drawPath(tip, stroke(OUT, 3))
        elif kind == "banner":
            bc = c.get("banner_color", "#1d1b1a")
            fl = [(x1, y1), (x1 + nx * 110 + dx * -10, y1 + ny * 110 + dy * -10),
                  (x1 + nx * 96 - dx * 40, y1 + ny * 96 - dy * 40),
                  (x1 + nx * 112 - dx * 76, y1 + ny * 112 - dy * 76), (x1 - dx * 74, y1 - dy * 74)]
            shape(cv, smooth(fl, tension=0.3), bc)
            if c.get("cross"):
                cx_, cy_ = x1 + nx * 50 - dx * 36, y1 + ny * 50 - dy * 36
                cv.drawLine(cx_ - 14, cy_, cx_ + 14, cy_, stroke("#f0c040", 6))
                cv.drawLine(cx_, cy_ - 18, cx_, cy_ + 18, stroke("#f0c040", 6))
        elif kind == "hoe":
            cv.drawLine(x1, y1, x1 + nx * 34 - dx * 10, y1 + ny * 34 - dy * 10, stroke("#8f969c", 10))
        elif kind == "torch":
            cv.drawPath(circle(x1, y1 - 6, 16), blur_paint("#ffb020", 6))
            cv.drawPath(circle(x1, y1 - 4, 9), fill("#fff0a0"))
        elif kind == "staff" and c.get("cross"):
            cv.drawLine(x1 - 14, y1 + 14, x1 + 14, y1 + 14, stroke("#d9a83a", 6))
            cv.drawLine(x1, y1, x1, y1 + 30, stroke("#d9a83a", 6))
    elif kind == "sword":
        x0, y0 = hx + dx * 14, hy + dy * 14
        x1, y1 = hx + dx * 128, hy + dy * 128
        blade = poly([(x0 - nx * 7, y0 - ny * 7), (x1 - nx * 5, y1 - ny * 5), (x1 + dx * 14, y1 + dy * 14),
                      (x1 + nx * 5, y1 + ny * 5), (x0 + nx * 7, y0 + ny * 7)])
        cv.drawPath(blade, lin_grad((x0 - nx * 7, y0 - ny * 7), (x0 + nx * 7, y0 + ny * 7),
                                    ["#ffffff", "#b9c2ca", "#7d868e"]))
        cv.drawPath(blade, stroke(OUT, 3))
        cv.drawLine(hx + dx * 10 - nx * 20, hy + dy * 10 - ny * 20, hx + dx * 10 + nx * 20,
                    hy + dy * 10 + ny * 20, stroke("#c9a040", 8))
        cv.drawPath(circle(hx - dx * 16, hy - dy * 16, 7), fill("#c9a040"))
        cv.drawPath(circle(hx - dx * 16, hy - dy * 16, 7), stroke(OUT, 2.5))
    elif kind == "bow":
        p = P()
        p.moveTo(hx + dx * 90 - nx * 6, hy + dy * 90 - ny * 6)
        p.quadTo(hx + nx * 40, hy + ny * 40, hx - dx * 90 - nx * 6, hy - dy * 90 - ny * 6)
        cv.drawPath(p, stroke(OUT, 10))
        cv.drawPath(p, stroke("#7a4a22", 6))
        cv.drawLine(hx + dx * 90 - nx * 6, hy + dy * 90 - ny * 6, hx - dx * 90 - nx * 6,
                    hy - dy * 90 - ny * 6, stroke("#efe6d0", 2))


def draw_shield(cv, c, x, y, kind, scale=1.0):
    cv.save()
    cv.translate(x, y)
    cv.scale(scale, scale)
    sc = c.get("shield_color", "#9a6a3a")
    if kind == "round":
        cv.drawPath(circle(3, 5, 48), fill((0, 0, 0), 60))
        cv.drawPath(circle(0, 0, 48), rad_grad((-14, -16), 60, [shade(sc, 1.25), sc, shade(sc, 0.75)]))
        cv.drawPath(circle(0, 0, 48), stroke(OUT, OUTW))
        p = stroke(shade(sc, 0.55), 2.4)
        p.setPathEffect(skia.DashPathEffect.Make([7, 6], 0))
        cv.drawPath(circle(0, 0, 40), p)
        cv.drawPath(circle(0, 0, 12), fill("#b8bfc5"))
        cv.drawPath(circle(0, 0, 12), stroke(OUT, 3))
        if c.get("cross"):
            cv.drawLine(0, -30, 0, 30, stroke("#e8d8a8", 6))
            cv.drawLine(-22, -8, 22, -8, stroke("#e8d8a8", 6))
    elif kind == "byz":
        e = ellipse(0, 0, 44, 66)
        cv.drawPath(ellipse(4, 6, 44, 66), fill((0, 0, 0), 60))
        cv.drawPath(e, rad_grad((-12, -20), 80, [shade(sc, 1.25), sc, shade(sc, 0.7)]))
        cv.drawPath(ellipse(0, 0, 38, 60), stroke("#e2b842", 5))
        cv.drawPath(e, stroke(OUT, OUTW))
        # chi-rho benzeri yildiz
        for a in (0, 60, 120):
            r = math.radians(a)
            cv.drawLine(-math.sin(r) * 34, -math.cos(r) * 50, math.sin(r) * 34, math.cos(r) * 50,
                        stroke("#e2b842", 5))
        cv.drawPath(circle(0, 0, 10), fill("#e2b842"))
        cv.drawPath(circle(0, 0, 10), stroke(OUT, 2.6))
    cv.restore()


# ======================================================================== GOVDE
def draw_person(cv, c, ps=None, x=0, y=0, scale=1.0, facing=1):
    if ps is None:
        ps = DEFAULT_POSE
    expr = ps.get("expr") or c.get("expr", "neutral")
    b = c.get("body", 1.0)
    cv.save()
    cv.translate(x, y)
    cv.scale(scale * facing, scale)
    seated = ps.get("seated")
    walk = ps.get("walk")
    bob = ps.get("bob", 0.0)
    if walk is not None:
        bob += -abs(math.sin(walk)) * 6
    cv.translate(0, bob)
    if ps.get("lean"):
        cv.rotate(ps["lean"])
    sy = -150 * b
    hip = -58 * b
    hem = -24 if c["tunic_long"] else hip + 18
    if seated:
        hem = hip + 6
    tunic = c["tunic"]
    skin = c["skin"]

    # pelerin
    if c.get("cloak"):
        cl = [(-38, sy + 2), (-66, hem + 8 if not seated else hip + 10), (66, hem + 8 if not seated else hip + 10),
              (38, sy + 2)]
        rshape(cv, cl, c["cloak"], r=16)
    # sadak
    if c.get("quiver"):
        cv.save()
        cv.translate(-22, sy + 30)
        cv.rotate(-28)
        shape(cv, rrect(-14, -70, 28, 100, 8), "#6b4424", w=3.4)
        for k in range(3):
            cv.drawLine(-8 + k * 8, -70, -8 + k * 8, -92, stroke("#d8d0c0", 4))
            cv.drawPath(poly([(-8 + k * 8, -92), (-13 + k * 8, -104), (-3 + k * 8, -104)]), fill("#b03030"))
        cv.restore()

    # bacaklar
    if not seated:
        for sx, ph in ((-1, 0.0), (1, math.pi)):
            ang = 0.0
            if walk is not None:
                ang = math.sin(walk + ph) * 26
            r = math.radians(ang)
            hx, hy = sx * 17, hip
            L = -hip - 8
            fx, fy = hx + math.sin(r) * L, hy + math.cos(r) * L
            leg_c = c["legs"] if not c["boots"] else c["legs"]
            capsule(cv, hx, hy, fx, fy, 24 * min(1, b + 0.15), leg_c, ow=3.6)
            if c["boots"]:
                capsule(cv, hx + (fx - hx) * 0.55, hy + (fy - hy) * 0.55, fx, fy, 26, "#4a3020", ow=3.6)
            foot = ellipse(fx + 9, fy + 2, 19, 9)
            shape(cv, foot, c["shoe"] if not c["boots"] else "#3a2416", w=3.4)
            if not c["boots"] and c["tunic_long"]:
                cv.drawLine(fx - 8, fy - 8, fx + 10, fy - 4, stroke(c["shoe"], 3))
    # govde
    shw = 40 if not c["female"] else 36
    hw = 54 if c["tunic_long"] else 50
    body_pts = [(-shw + 4, sy), (-shw - 6, sy + 22), (-hw + 6, hip), (-hw, hem), (hw, hem), (hw - 6, hip),
                (shw + 6, sy + 22), (shw - 4, sy)]
    bp = poly(body_pts)
    cv.drawPath(bp, round_paint(fill(tunic), 14))
    cv.save()
    cv.clipPath(bp, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect.MakeLTRB(18, sy - 10, 70, 10), fill(shade(tunic, 0.82)))
    arm = c.get("armor")
    if arm == "mail":
        cv.drawRect(skia.Rect.MakeLTRB(-70, sy - 10, 70, hip + 14), fill("#8d949c"))
        for yy in range(int(sy - 4), int(hip + 14), 9):
            for xx in range(-64, 66, 10):
                cv.drawPath(circle(xx + ((yy // 9) % 2) * 5, yy, 4.2), stroke("#5f666e", 1.7))
        cv.drawRect(skia.Rect.MakeLTRB(18, sy - 10, 70, hip + 14), fill((0, 0, 0), 40))
    elif arm == "lamellar":
        cv.drawRect(skia.Rect.MakeLTRB(-70, sy - 10, 70, hip + 12), fill("#a6aeb6"))
        row = 0
        for yy in range(int(sy + 4), int(hip + 12), 12):
            for xx in range(-66, 70, 9):
                cv.drawPath(rrect(xx + (row % 2) * 4.5, yy, 8, 11, 2), stroke("#5f666e", 1.5))
            row += 1
        cv.drawRect(skia.Rect.MakeLTRB(18, sy - 10, 70, hip + 12), fill((0, 0, 0), 40))
        cv.drawLine(-60, hip + 12, 60, hip + 12, stroke("#c9a040", 5))
        # pteruges
        for xx in range(-44, 50, 12):
            cv.drawPath(rrect(xx - 5, hip + 14, 10, 24, 3), fill("#7a4a2a"))
            cv.drawPath(rrect(xx - 5, hip + 14, 10, 24, 3), stroke(OUT, 1.6))
    if c["name"] == "heraclius":
        cv.drawRect(skia.Rect.MakeLTRB(-12, sy, 12, hem), fill("#e0a92e"))
        cv.drawPath(rrect(-50, sy + 20, 36, 36, 4), fill("#e0a92e"))
    cv.restore()
    cv.drawPath(bp, round_paint(stroke(OUT, OUTW), 14))
    # kemer
    if not arm or arm == "mail":
        cv.drawPath(rrect(-hw + 4, hip - 10, (hw - 4) * 2, 14, 5), fill(c["belt"]))
        cv.drawPath(rrect(-hw + 4, hip - 10, (hw - 4) * 2, 14, 5), stroke(OUT, 3))
        if c.get("sash"):
            sp = smooth([(-hw + 6, hip - 12), (hw - 6, hip - 12), (hw - 4, hip + 4), (-hw + 4, hip + 4)])
            shape(cv, sp, c["sash"], w=3)
            tail = smooth([(10, hip), (24, hip + 30), (14, hip + 34), (4, hip + 4)])
            shape(cv, tail, shade(c["sash"], 0.85), w=3)
    # oturuyorsa: bacak
    if seated:
        capsule(cv, 10, hip + 4, 38, hip + 46, 26, c["legs"] if c["boots"] else tunic, ow=3.6)
        capsule(cv, 38, hip + 46, 32, hip + 92, 22, c["legs"] if c["boots"] else skin, ow=3.6)
        shape(cv, ellipse(44, hip + 96, 18, 9), "#3a2416", w=3.2)

    # kollar
    sl = tunic if not c.get("armor") else (tunic if c["armor"] != "lamellar" else c["tunic"])
    shoulder_y = sy + 14
    L = 74 * max(0.75, b)

    def arm_end(sx, ang):
        r = math.radians(ang)
        return sx * (shw + 2) + sx * math.sin(r) * L, shoulder_y + math.cos(r) * L

    ax, ay = arm_end(-1, ps["arm_a"])
    bx, by = arm_end(1, ps["arm_b"])
    # kol A (sol)
    capsule(cv, -(shw + 2), shoulder_y, ax, ay, 22, sl, ow=3.6)
    cv.drawPath(circle(ax, ay, 12), fill(skin))
    cv.drawPath(circle(ax, ay, 12), stroke(OUT, 3.4))
    if c.get("shield"):
        draw_shield(cv, c, ax + 8, ay - 8, c["shield"], 1.0)

    # kafa
    head_cy = sy - 62 * c.get("head_scale", 1.0)
    cv.save()
    cv.translate(0, head_cy)
    if ps.get("head_tilt"):
        cv.rotate(ps["head_tilt"])
    draw_head(cv, c, ps, expr)
    cv.restore()

    # yaralar
    if ps.get("arrow"):
        cv.drawPath(circle(-24, sy + 18, 10), fill("#a01818", 220))
        cv.drawLine(-24, sy + 18, -70, sy - 40, stroke(OUT, 7))
        cv.drawLine(-24, sy + 18, -70, sy - 40, stroke("#7a5030", 4))
        for k in (-1, 1):
            cv.drawLine(-64, sy - 32, -64 + k * 10, sy - 50, stroke("#e8e0d0", 5))
    if ps.get("blood", 0) > 0:
        bl = ps["blood"]
        for (bx_, by_, r_) in ((14, sy + 40, 12), (-10, sy + 70, 9), (30, hip - 20, 7)):
            cv.drawPath(circle(bx_, by_, r_ * bl), fill("#9a1010", 210))

    # kol B (sag) + silah
    if c.get("weapon"):
        draw_weapon(cv, c, bx, by, ps.get("wpn", 8), c["weapon"])
    capsule(cv, shw + 2, shoulder_y, bx, by, 22, sl, ow=3.6)
    if c.get("item"):
        draw_item(cv, c["item"], bx, by)
    cv.drawPath(circle(bx, by, 12), fill(skin))
    cv.drawPath(circle(bx, by, 12), stroke(OUT, 3.4))
    cv.restore()


def draw_item(cv, item, x, y):
    if item == "pen":
        cv.drawLine(x, y, x + 30, y - 40, stroke(OUT, 5))
        cv.drawLine(x, y, x + 30, y - 40, stroke("#e8dcc0", 3))
    elif item == "dates":
        for k in range(3):
            shape(cv, ellipse(x - 10 + k * 10, y - 14, 7, 11), "#6a2e12", w=2)
    elif item == "coin":
        shape(cv, circle(x, y - 14, 13), "#e8c050", w=3)
    elif item == "waterskin":
        shape(cv, smooth([(x - 6, y - 4), (x - 30, y + 20), (x - 22, y + 56), (x + 18, y + 56), (x + 26, y + 22),
                          (x + 6, y - 4)]), "#8a5a30")
    elif item == "rope":
        cv.drawLine(x, y, x + 140, y - 30, stroke("#a07840", 4))


# ======================================================================== AT
def draw_horse(cv, x, y, scale=1.0, facing=1, phase=0.0, gallop=0.0, color="#7a4a2a", armored=False,
               mane="#2a1a10", rider=None, rider_pose=None, run_speed=1.0):
    cv.save()
    cv.translate(x, y)
    cv.scale(scale * facing, scale)
    bobv = -abs(math.sin(phase)) * 10 * gallop
    cv.translate(0, bobv)
    # bacaklar (arkadakiler)
    legs = [(-70, 0.0, True), (68, math.pi * 0.6, True), (-56, math.pi, False), (82, math.pi * 1.6, False)]

    def leg(lx, ph, back):
        a1 = math.sin(phase + ph) * 34 * gallop
        a2 = (math.cos(phase + ph) * 0.5 + 0.5) * 50 * gallop
        r1 = math.radians(a1)
        kx, ky = lx + math.sin(r1) * 62, -130 + math.cos(r1) * 62
        r2 = math.radians(a1 - a2 if lx > 0 else a1 + a2 * 0.4)
        fx, fy = kx + math.sin(r2) * 62, ky + math.cos(r2) * 62
        cc = shade(color, 0.78) if back else color
        capsule(cv, lx, -140, kx, ky, 20, cc, ow=3.6)
        capsule(cv, kx, ky, fx, fy, 15, cc, ow=3.6)
        shape(cv, rrect(fx - 11, fy - 6, 22, 12, 3), "#2a1a10", w=3)

    for lx, ph, back in legs[:2]:
        leg(lx, ph + math.pi * 0.5, True)
    # kuyruk
    sw = math.sin(phase * 0.5) * 10
    tail = smooth([(-104, -175), (-140, -160 + sw), (-160, -100 + sw), (-146, -96 + sw), (-122, -140),
                   (-100, -160)], tension=0.5)
    shape(cv, tail, mane)
    # govde
    body = smooth([(-110, -170), (-80, -196), (0, -200), (70, -196), (108, -170), (110, -132), (60, -112),
                   (-60, -112), (-112, -134)], tension=0.5)
    shape(cv, body, color)
    cv.save()
    cv.clipPath(body, skia.ClipOp.kIntersect, True)
    cv.drawPath(ellipse(0, -110, 130, 30), fill(shade(color, 0.8), 150))
    cv.drawPath(ellipse(-20, -190, 70, 14), fill(shade(color, 1.18), 110))
    cv.restore()
    shape(cv, body, None)
    # boyun + bas
    neck = smooth([(70, -190), (110, -246), (132, -290), (162, -296), (176, -270), (130, -200), (104, -160)],
                  tension=0.5)
    shape(cv, neck, color)
    headp = smooth([(124, -298), (154, -320), (230, -262), (236, -236), (216, -224), (150, -244)], tension=0.4)
    shape(cv, headp, color)
    shape(cv, ellipse(226, -238, 13, 11), shade(color, 0.8), w=3)
    cv.drawPath(circle(230, -240, 3), fill(OUT))
    shape(cv, poly([(136, -306), (140, -336), (156, -310)]), color, w=3)
    cv.drawPath(circle(160, -280, 7), fill("#ffffff"))
    cv.drawPath(circle(162, -280, 4), fill("#1a120c"))
    cv.drawPath(circle(160, -280, 7), stroke(OUT, 2.4))
    mn = smooth([(132, -300), (100, -260), (76, -206), (64, -196), (84, -246), (112, -290)], tension=0.5)
    shape(cv, mn, mane)
    if armored:
        for pth in (body, neck):
            cv.save()
            cv.clipPath(pth, skia.ClipOp.kIntersect, True)
            cv.drawRect(skia.Rect.MakeLTRB(-130, -320, 200, -100), fill("#9aa2aa"))
            for yy in range(-320, -100, 11):
                for xx in range(-130, 200, 12):
                    o = ((yy // 11) % 2) * 6
                    arc = P()
                    arc.moveTo(xx + o - 6, yy)
                    arc.quadTo(xx + o, yy + 12, xx + o + 6, yy)
                    cv.drawPath(arc, stroke("#5f666e", 1.8))
            cv.restore()
            shape(cv, pth, None)
        shape(cv, poly([(150, -300), (204, -258), (196, -246), (146, -276)]), "#c2c9d0", w=3)
    # eyer
    shape(cv, smooth([(-40, -198), (30, -200), (34, -176), (-44, -174)]), "#8a2222" if not armored else "#6a1a1a",
          w=3)
    # rider
    if rider is not None:
        rp = dict(rider_pose or DEFAULT_POSE)
        rp["seated"] = True
        draw_person(cv, rider, rp, x=-4, y=-160, scale=0.8, facing=1)
    for lx, ph, back in legs[2:]:
        leg(lx, ph + math.pi * 0.5, False)
    cv.restore()


# ======================================================================== DEVE
def draw_camel(cv, x, y, scale=1.0, facing=1, phase=0.0, walk=0.0, color="#c99a5e", load=False, rider=None,
               rider_pose=None, kneel=False):
    cv.save()
    cv.translate(x, y)
    cv.scale(scale * facing, scale)
    cv.translate(0, -abs(math.sin(phase)) * 6 * walk)
    if kneel:
        cv.translate(0, 100)

    def leg(lx, ph, back):
        a = math.sin(phase + ph) * 24 * walk
        r = math.radians(a)
        L1, L2 = 82, 84
        kx, ky = lx + math.sin(r) * L1, -170 + math.cos(r) * L1
        r2 = math.radians(a - abs(math.sin(phase + ph)) * 18 * walk)
        fx, fy = kx + math.sin(r2) * L2, ky + math.cos(r2) * L2
        if kneel:
            kx, ky, fx, fy = lx + 20, -110, lx - 30, -100
        cc = shade(color, 0.8) if back else color
        capsule(cv, lx, -180, kx, ky, 18, cc, ow=3.6)
        cv.drawPath(circle(kx, ky, 11), fill(cc))
        cv.drawPath(circle(kx, ky, 11), stroke(OUT, 3))
        capsule(cv, kx, ky, fx, fy, 14, cc, ow=3.6)
        shape(cv, ellipse(fx + 4, fy - 2, 15, 7), shade(color, 0.6), w=3)

    leg(-78, math.pi, True)
    leg(88, 0, True)
    tail = smooth([(-118, -230), (-134, -200), (-128, -168), (-120, -200)])
    shape(cv, tail, shade(color, 0.85), w=3)
    body = smooth([(-124, -220), (-100, -262), (-46, -320), (-10, -326), (30, -296), (90, -262), (126, -236),
                   (124, -196), (90, -176), (-90, -176), (-124, -192)], tension=0.5)
    shape(cv, body, color)
    cv.save()
    cv.clipPath(body, skia.ClipOp.kIntersect, True)
    cv.drawPath(ellipse(0, -176, 140, 30), fill(shade(color, 0.82), 150))
    cv.drawPath(ellipse(-20, -310, 40, 14), fill(shade(color, 1.15), 120))
    cv.restore()
    shape(cv, body, None)
    neck = smooth([(100, -250), (150, -240), (176, -276), (190, -330), (214, -340), (206, -300), (186, -240),
                   (150, -206), (112, -206)], tension=0.5)
    shape(cv, neck, color)
    headp = smooth([(190, -344), (220, -356), (262, -340), (270, -320), (250, -308), (204, -316)], tension=0.45)
    shape(cv, headp, color)
    lip = smooth([(252, -318), (272, -318), (270, -306), (250, -304)])
    shape(cv, lip, shade(color, 0.85), w=3)
    shape(cv, ellipse(204, -352, 7, 12), color, w=3)
    cv.drawPath(circle(226, -338, 8), fill("#ffffff"))
    cv.drawPath(circle(229, -337, 4), fill("#1a120c"))
    cv.drawPath(circle(226, -338, 8), stroke(OUT, 2.4))
    cv.drawLine(216, -347, 236, -345, stroke(OUT, 3.4))
    if load:
        shape(cv, rrect(-70, -300, 64, 70, 10), "#8a3a2a", w=3.4)
        shape(cv, rrect(10, -292, 60, 60, 10), "#5a6a3a", w=3.4)
        cv.drawLine(-80, -268, 80, -262, stroke("#d8c090", 5))
    else:
        shape(cv, smooth([(-60, -316), (40, -300), (44, -276), (-64, -290)]), "#a8282b", w=3)
        for k in range(5):
            cv.drawLine(-50 + k * 22, -286, -52 + k * 22, -270, stroke("#e8c050", 4))
    if rider is not None:
        rp = dict(rider_pose or DEFAULT_POSE)
        rp["seated"] = True
        draw_person(cv, rider, rp, x=-10, y=-284, scale=0.8, facing=1)
    leg(-62, 0, False)
    leg(104, math.pi, False)
    cv.restore()


# ======================================================================== SILUET
def silhouette_begin(cv, glow="#ffd27a", glow_a=200, dark="#17110c"):
    """Sahabe/halife gibi tarihi sahsiyetler yuzsuz siluetle gosterilir."""
    p = skia.Paint()
    p.setColorFilter(skia.ColorFilters.Blend(rgb(dark), skia.BlendMode.kSrcIn))
    cv.saveLayer(None, p)


def silhouette_end(cv):
    cv.restore()


def draw_silhouette(cv, drawfn, glow="#ffd88a", glow_sigma=14, glow_a=220, dark="#1a130e"):
    # parlama
    gp = skia.Paint()
    gp.setColorFilter(skia.ColorFilters.Blend(rgb(glow, glow_a), skia.BlendMode.kSrcIn))
    gp.setImageFilter(skia.ImageFilters.Blur(glow_sigma, glow_sigma))
    cv.saveLayer(None, gp)
    drawfn(cv)
    cv.restore()
    p = skia.Paint()
    p.setColorFilter(skia.ColorFilters.Blend(rgb(dark), skia.BlendMode.kSrcIn))
    cv.saveLayer(None, p)
    drawfn(cv)
    cv.restore()
