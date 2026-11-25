"""Parsomen tarzinda tarihi haritalar (kara/deniz maskesi: global_land_mask)."""
import math
import os

import numpy as np
import skia
from global_land_mask import globe
from scipy import ndimage

from gfx import (OUT, W, H, ROOT, circle, ease_in_out, ease_out, fill, font, label_tag, lin_grad, poly, pop,
                 rad_grad, rgb, rrect, shade, smooth, stroke, text, clamp, blur_paint)

CACHE = os.path.join("/tmp", "zk_mapcache")
os.makedirs(CACHE, exist_ok=True)
MS = 1.6  # harita goruntusu ekranin 1.6 kati cozunurlukte
COSL = math.cos(math.radians(31))

PLACES = {
    "Medine": (24.47, 39.61), "Mekke": (21.42, 39.83), "Şam": (33.51, 36.29), "Kudüs": (31.78, 35.23),
    "Humus": (34.73, 36.72), "Antakya": (36.20, 36.16), "Yermük": (32.80, 35.95), "Ecnadeyn": (31.68, 34.98),
    "Fahl": (32.45, 35.62), "Amvas": (31.84, 34.99), "Tebük": (28.38, 36.57), "Hîre": (31.90, 44.40),
    "Ayn et-Temr": (32.57, 43.49), "Tedmür": (34.55, 38.27), "Busra": (32.52, 36.48),
    "Konstantinopolis": (41.01, 28.98), "Medain": (33.09, 44.58), "İskenderiye": (31.20, 29.92),
    "Fustat": (30.00, 31.23), "Gazze": (31.50, 34.47), "Halep": (36.20, 37.16), "Kayseri": (38.72, 35.48),
    "Kufe": (32.03, 44.40), "Basra": (30.50, 47.80), "Taif": (21.27, 40.42), "Yemen": (15.35, 44.20),
}

RIVERS = {
    "Fırat": [(39.0, 38.6), (37.6, 38.3), (36.6, 38.2), (35.95, 39.0), (35.33, 40.14), (34.45, 40.92), (34.13, 42.37),
              (33.42, 43.30), (32.5, 44.4), (31.05, 46.25), (31.0, 47.43), (30.5, 47.8), (29.95, 48.55)],
    "Dicle": [(38.0, 40.2), (37.1, 42.2), (36.34, 43.13), (34.6, 43.68), (34.2, 43.87), (33.3, 44.4), (33.09, 44.58),
              (32.5, 45.8), (31.84, 47.15), (31.0, 47.43)],
    "Nil": [(22.0, 31.4), (24.1, 32.9), (25.7, 32.6), (27.2, 31.2), (29.0, 31.1), (30.05, 31.25), (30.6, 31.0),
            (31.45, 30.35)],
    "Ürdün": [(33.2, 35.62), (32.8, 35.58), (32.3, 35.56), (31.85, 35.55)],
}


class MapView:
    def __init__(self, lon_c, lat_c, span_lat):
        self.lon_c, self.lat_c, self.span = lon_c, lat_c, span_lat
        self.h_deg = span_lat
        self.w_deg = span_lat * (W / H) / COSL

    def xy(self, lat, lon):
        x = (lon - self.lon_c) / self.w_deg * W + W / 2
        y = (self.lat_c - lat) / self.h_deg * H + H / 2
        return x, y


def _render_raster(view, key):
    path = os.path.join(CACHE, key + ".png")
    if os.path.exists(path):
        return skia.Image.open(path)
    pw, ph = int(W * MS), int(H * MS)
    lons = view.lon_c + (np.arange(pw) / pw - 0.5) * view.w_deg
    lats = view.lat_c - (np.arange(ph) / ph - 0.5) * view.h_deg
    LO, LA = np.meshgrid(lons, lats)
    land = globe.is_land(LA, LO).astype(np.float32)
    sm = ndimage.gaussian_filter(land, 2.0) > 0.5
    # cok kucuk adaciklari temizle
    lab, n = ndimage.label(sm)
    if n > 0:
        sizes = ndimage.sum(sm, lab, range(1, n + 1))
        keep = np.zeros(n + 1, bool)
        keep[1:] = sizes > 60
        sm = keep[lab]
    dist_in = ndimage.distance_transform_edt(sm)
    dist_out = ndimage.distance_transform_edt(~sm)
    rng = np.random.default_rng(3)
    noise = ndimage.gaussian_filter(rng.standard_normal((ph, pw)).astype(np.float32), 3) * 6
    img = np.zeros((ph, pw, 3), np.float32)
    sea = np.array([126, 166, 170], np.float32)
    sea_deep = np.array([96, 136, 146], np.float32)
    landc = np.array([234, 214, 168], np.float32)
    landd = np.array([196, 160, 104], np.float32)
    fsea = np.clip(dist_out / 260, 0, 1)[..., None]
    img[:] = sea * (1 - fsea) + sea_deep * fsea
    # kiyi cizgileri (dalga konturleri)
    rings = ((dist_out % 22) < 2.2) & (dist_out < 90) & (dist_out > 6)
    img[rings] = img[rings] * 0.86
    fl = np.clip(dist_in / 40, 0, 1)[..., None]
    lc = landd * (1 - fl) + landc * fl
    img = np.where(sm[..., None], lc, img)
    img += noise[..., None]
    coast = (dist_out > 0) & (dist_out < 3.2)
    img[coast] = np.array([92, 62, 36])
    # parsomen lekeleri
    big = ndimage.gaussian_filter(rng.standard_normal((ph // 8, pw // 8)).astype(np.float32), 6)
    big = np.kron(big, np.ones((8, 8), np.float32))[:ph, :pw]
    img *= (1 + big[..., None] * 0.6)
    yy, xx = np.mgrid[0:ph, 0:pw]
    vig = 1 - 0.35 * (((xx / pw - 0.5) * 1.6) ** 2 + ((yy / ph - 0.5) * 1.6) ** 2)
    img *= vig[..., None]
    img = np.clip(img, 0, 255).astype(np.uint8)
    rgba = np.concatenate([img, np.full((ph, pw, 1), 255, np.uint8)], axis=2)
    im = skia.Image.fromarray(np.ascontiguousarray(rgba), colorType=skia.kRGBA_8888_ColorType)
    im.save(path, skia.kPNG)
    return skia.Image.open(path)


_imgs = {}


def map_image(view, key):
    if key not in _imgs:
        _imgs[key] = _render_raster(view, key)
    return _imgs[key]


def draw_map_base(cv, view, key, rivers=True, rivers_a=255):
    img = map_image(view, key)
    cv.drawImageRect(img, skia.Rect.MakeWH(W, H), skia.SamplingOptions(skia.FilterMode.kLinear,
                                                                       skia.MipmapMode.kNone))
    if rivers:
        for name, pts in RIVERS.items():
            xy = [view.xy(a, b) for a, b in pts]
            p = smooth(xy, closed=False)
            cv.drawPath(p, stroke("#4f7f96", 5.5, rivers_a))
            cv.drawPath(p, stroke("#86b4c4", 2.5, rivers_a))


def place(cv, view, name, t=1.0, t0=0.0, size=34, dot="#b01818", dx=0, dy=-26, star=False, label=None):
    s = pop(t - t0, 0.35)
    if s <= 0:
        return
    lat, lon = PLACES[name]
    x, y = view.xy(lat, lon)
    cv.save()
    cv.translate(x, y)
    cv.scale(s, s)
    if star:
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            r = 22 if k % 2 == 0 else 9
            pts.append((math.cos(a) * r, math.sin(a) * r))
        cv.drawPath(poly(pts), fill("#f6c64a"))
        cv.drawPath(poly(pts), stroke(OUT, 3))
    else:
        cv.drawPath(circle(0, 0, 10), fill(dot))
        cv.drawPath(circle(0, 0, 10), stroke(OUT, 3))
    f = font("black", size)
    text(cv, label or name, dx, dy, f, "#2a1a10", oc="#f6ead0", ow=5)
    cv.restore()


def region_label(cv, view, s, lat, lon, size=44, col="#6a3a1a", a=255, rot=0, spacing=True):
    x, y = view.xy(lat, lon)
    cv.save()
    cv.translate(x, y)
    cv.rotate(rot)
    f = font("deco", size)
    text(cv, s, 0, 0, f, col, a=a, oc="#f3e3bf", ow=3)
    cv.restore()


def route(cv, view, pts, t, t0, dur, col="#b01818", w=10, dashed=True, head=True, a=255):
    """pts: [(lat,lon)] animasyonlu ok"""
    f = clamp((t - t0) / dur)
    if f <= 0:
        return
    xy = [view.xy(a_, b_) for a_, b_ in pts]
    path = smooth(xy, closed=False) if len(xy) > 2 else poly(xy, closed=False)
    meas = skia.PathMeasure(path, False)
    L = meas.getLength()
    seg = skia.Path()
    meas.getSegment(0, L * ease_in_out(f), seg, True)
    p_out = stroke(OUT, w + 6, a)
    p_in = stroke(col, w, a)
    if dashed:
        p_in.setPathEffect(skia.DashPathEffect.Make([w * 2.4, w * 1.4], 0))
    cv.drawPath(seg, p_out)
    cv.drawPath(seg, p_in)
    if head and f > 0.02:
        pos, tan = meas.getPosTan(L * ease_in_out(f))
        ang = math.atan2(tan.y(), tan.x())
        hx, hy = pos.x(), pos.y()
        tri = poly([(hx + math.cos(ang) * 30, hy + math.sin(ang) * 30),
                    (hx + math.cos(ang + 2.4) * 24, hy + math.sin(ang + 2.4) * 24),
                    (hx + math.cos(ang - 2.4) * 24, hy + math.sin(ang - 2.4) * 24)])
        cv.drawPath(tri, fill(col, a))
        cv.drawPath(tri, stroke(OUT, 3.5, a))


def battle_icon(cv, x, y, t, t0, s=1.0, label=None, year=None):
    sc = pop(t - t0, 0.4)
    if sc <= 0:
        return
    cv.save()
    cv.translate(x, y)
    cv.scale(sc * s, sc * s)
    cv.drawPath(circle(0, 0, 40), fill("#fbf3df"))
    cv.drawPath(circle(0, 0, 40), stroke(OUT, 4))
    for sg in (-1, 1):
        cv.save()
        cv.rotate(sg * 45)
        cv.drawPath(rrect(-5, -30, 10, 46, 3), fill("#c9d0d6"))
        cv.drawPath(rrect(-5, -30, 10, 46, 3), stroke(OUT, 2.5))
        cv.drawPath(rrect(-14, 12, 28, 7, 3), fill("#c9a040"))
        cv.drawPath(rrect(-4, 18, 8, 12, 3), fill("#6a4424"))
        cv.restore()
    if label:
        text(cv, label, 0, 78, font("black", 36), "#2a1a10", oc="#f6ead0", ow=5)
    if year:
        text(cv, year, 0, 116, font("slab", 32), "#a01818", oc="#f6ead0", ow=5)
    cv.restore()


def mountains(cv, view, lat, lon, n=5, s=1.0, seed=0):
    import random
    r = random.Random(seed)
    x0, y0 = view.xy(lat, lon)
    for k in range(n):
        x = x0 + r.uniform(-90, 90) * s
        y = y0 + r.uniform(-30, 30) * s
        hh = r.uniform(30, 50) * s
        p = poly([(x - hh * 0.9, y), (x, y - hh), (x + hh * 0.9, y)])
        cv.drawPath(p, fill("#b89a6a"))
        cv.drawPath(poly([(x, y - hh), (x + hh * 0.9, y), (x + hh * 0.2, y)]), fill("#9a7a4a"))
        cv.drawPath(p, stroke("#5a3a1a", 2.5))
