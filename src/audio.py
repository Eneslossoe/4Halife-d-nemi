"""Tum ses miksajı: anlatim + fon muzigi + efektler + ortam sesleri -> soundtrack.wav"""
import json
import os

import numpy as np
import soundfile as sf
from scipy.signal import resample_poly

import music
import synth as Y
from synth import SR, pan, place

WORK = os.environ.get("ZK_WORK", "/tmp/claude-0/work")


def load_tl():
    with open(os.path.join(WORK, "timeline.json")) as f:
        return json.load(f)


class Shot:
    def __init__(self, s):
        self.s = s
        self.t0 = s["start"]
        self.d = s["dur"]
        self.L = [(l["start"], l["end"]) for l in s["lines"]]

    def lt(self, i):
        return self.L[min(i, len(self.L) - 1)][0] if self.L else 0.0

    def le(self, i):
        return self.L[min(i, len(self.L) - 1)][1] if self.L else self.d

    def lf(self, i, fr):
        a, b = (self.lt(i), self.le(i))
        return a + (b - a) * fr


# ------------------------------------------------------------------ anlatim
def narration(tl, n):
    out = np.zeros((n, 2))
    for s in tl["shots"]:
        for l in s["lines"]:
            a, sr = sf.read(l["wav"], dtype="float32")
            a = resample_poly(a, 320, 147).astype(np.float64)  # 22050 -> 48000
            a = Y.hp(a, 75)
            # hafif sicaklik + netlik
            a = a + Y.bp(a, 2500, 5000) * 0.25 + Y.lp(a, 250) * 0.15
            # yumusak kompresyon
            env = np.sqrt(Y.lp(a ** 2, 8) + 1e-9)
            g = np.minimum(1.0, (0.12 / (env + 1e-9)) ** 0.35)
            a = a * g
            a = a / (np.abs(a).max() + 1e-9) * 0.82
            if l["voice"] == "q":
                a = a * 0.95
            place(out, np.stack([a, a], axis=1), s["start"] + l["start"])
    # cok hafif oda yankisi
    return Y.reverb(out, 0.06, seconds=0.9, damp=7.0, bright=5000)


def speech_mask(tl, n):
    m = np.zeros(n)
    for s in tl["shots"]:
        for l in s["lines"]:
            a = int((s["start"] + l["start"] - 0.15) * SR)
            b = int((s["start"] + l["end"] + 0.25) * SR)
            m[max(a, 0):min(b, n)] = 1.0
    k = int(0.25 * SR)
    m = np.convolve(m, np.ones(k) / k, mode="same")
    return np.clip(m, 0, 1)


# ------------------------------------------------------------------ muzik
def soundtrack_music(tl, n):
    segs = []
    cur = None
    for s in tl["shots"]:
        m = s["params"].get("music")
        if m and m != cur:
            segs.append([s["start"], m])
            cur = m
    out = np.zeros((n, 2))
    xf = 1.6
    for i, (t0, m) in enumerate(segs):
        t1 = segs[i + 1][0] if i + 1 < len(segs) else n / SR
        dur = t1 - t0 + xf
        y = music.gen(m, dur, seed=100 + i)
        L = len(y)
        e = np.ones(L)
        fi = int(0.6 * SR)
        e[:fi] = np.linspace(0, 1, fi)
        fo = int(xf * SR)
        if i + 1 < len(segs):
            e[-fo:] *= np.linspace(1, 0, fo)
        y = y * e[:, None]
        print(f"  muzik {m:12s} {t0:7.2f}s  {dur:6.1f}s", flush=True)
        place(out, y, t0)
    # son 4 saniyede sonme
    k = int(4 * SR)
    out[-k:] *= np.linspace(1, 0, k)[:, None]
    return out


# ------------------------------------------------------------------ efektler
def cues(tl):
    """(mutlak zaman, stereo ses, kazanc) listesi"""
    C = []
    rng = np.random.default_rng(7)

    def add(t, x, g=1.0, p=0.0):
        if x.ndim == 1:
            x = pan(x, p)
        C.append((t, x, g))

    def amb(sh, x, g, t0=0.0, t1=None, fade=0.5):
        t1 = sh.d if t1 is None else t1
        L = int((t1 - t0) * SR)
        x = x[:L]
        if len(x) < L:
            x = np.pad(x, ((0, L - len(x)), (0, 0)))
        f = min(int(fade * SR), L // 2)
        e = np.ones(L)
        if f > 0:
            e[:f] = np.linspace(0, 1, f)
            e[-f:] = np.linspace(1, 0, f)
        add(sh.t0 + t0, x * e[:, None], g)

    shots = {s["id"]: Shot(s) for s in tl["shots"]}
    for sid, sh in shots.items():
        fn = sh.s["fn"]
        T = sh.t0
        d = sh.d
        if fn == "chapter":
            add(T, Y.whoosh(0.7, 1.0, 200, 2500, seed=hash(sid) % 999), 0.7)
            add(T + 0.28, Y.impact(0.6), 0.5)
            add(T + 0.05, Y.paper(1.0, 0.7), 0.6)
            continue
    S = shots

    def pops(sh, times, g=0.6, f=600):
        for k, t in enumerate(times):
            add(sh.t0 + t, Y.ui_pop(1.0, f + k * 60), g)

    # ---- giris
    sh = S["s01"]
    amb(sh, Y.wind(sh.d, 1.0, 1), 0.5)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 2, shouts=True, clashes=False, density=0.3), 0.18)
    add(sh.t0 + 0.4, Y.impact(0.7), 0.45)
    sh = S["s02"]
    amb(sh, Y.wind(sh.d, 1.0, 3), 0.3)
    pops(sh, [sh.lf(0, 0.32), sh.lf(0, 0.55), sh.lf(0, 0.83)])
    sh = S["s03"]
    add(sh.t0 + 0.15, Y.impact(0.8), 0.5)
    add(sh.t0 + 0.45, Y.whoosh(0.5, 1.0, 400, 3000, 2), 0.5)
    t2 = sh.lt(1)
    for k in range(int((sh.d - t2) / 0.85)):
        add(sh.t0 + t2 + k * 0.85, Y.heartbeat(1.0), 0.6)
    pops(sh, [t2 + 0.5 + k * 0.18 for k in range(6)], 0.4, 800)
    add(sh.t0 + sh.d - 2.0, Y.riser(2.0), 0.5)
    sh = S["s04"]
    add(sh.t0 + 0.05, Y.impact(1.0), 0.7)
    add(sh.t0 + 0.9, Y.whoosh(0.5, 1.0, 300, 3000, 3), 0.4)
    # ---- bolum 1
    sh = S["s06"]
    amb(sh, Y.wind(sh.d, 1.0, 4), 0.35)
    amb(sh, Y.camel_steps(3.0, 1.0, 1), 0.5, 0.3, 3.3)
    pops(sh, [sh.lf(0, 0.6)])
    sh = S["s07"]
    t2 = sh.lt(1) - 0.4
    amb(sh, Y.wind(sh.d, 1.0, 5), 0.3, 0, t2 + 0.5)
    amb(sh, Y.camel_steps(t2, 1.0, 2), 0.4, 0, t2)
    amb(sh, Y.fire(sh.d - t2, 1.0, 1), 0.6, t2, sh.d)
    sh = S["s08"]
    add(sh.t0 + 1.4, Y.coins(6, 1.0, 1, 0.4), 0.6)
    pops(sh, [1.0, 1.2])
    sh = S["s09"]
    add(sh.t0, Y.paper(1.0, 0.8, 2), 0.6)
    for k in range(5):
        add(sh.t0 + 0.6 + k * 0.7, Y.sword_clash(0.4, k), 0.25, (k % 3 - 1) * 0.5)
    add(sh.t0 + sh.lt(1) + 1.6, Y.ding(1.0), 0.5)
    add(sh.t0 + sh.lt(1) + 2.6, Y.whoosh(0.5, 1.0, 400, 3000, 5), 0.4)
    sh = S["s10"]
    amb(sh, Y.wind(sh.d, 1.0, 6), 0.3)
    amb(sh, Y.camel_steps(3.6, 1.0, 3), 0.6, 0.0, 3.6)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 9, shouts=False, clashes=False), 0.12)
    add(sh.t0 + 0.3, Y.impact(0.5), 0.35)
    add(sh.t0 + sh.lt(1) + 0.3, Y.ui_pop(1.0, 500), 0.5)
    # ---- bolum 2
    sh = S["s12"]
    amb(sh, Y.wind(sh.d, 1.0, 7, bright=600), 0.35)
    amb(sh, Y.camel_steps(sh.d - sh.lt(1), 1.0, 4), 0.4, sh.lt(1), sh.d)
    sh = S["s13"]
    a0, b0 = sh.lt(0), sh.le(0)
    pops(sh, [a0 + (b0 - a0) * 0.3])
    add(sh.t0 + a0 + (b0 - a0) * 0.45, Y.buzz(1.0), 0.4)
    a, b = sh.lt(1), sh.le(1)
    pops(sh, [a + (b - a) * fr for fr in (0.02, 0.36, 0.55, 0.82)] + [sh.lt(2) + 0.1])
    sh = S["s14"]
    pops(sh, [0.3])
    a, b = sh.lt(0), sh.le(0)
    pops(sh, [a + (b - a) * 0.55 + k * 0.16 for k in range(6)], 0.4, 700)
    sh = S["s15"]
    a, b = sh.lt(0), sh.le(0)
    pops(sh, [0.1] + [a + (b - a) * fr - 0.25 for fr in (0.3, 0.45, 0.62, 0.85)])
    sh = S["s16"]
    add(sh.t0 + 0.8, Y.coins(14, 1.0, 2, 0.8), 0.6)
    add(sh.t0 + 0.5, Y.whoosh(0.5, 1.0, 400, 3000, 6), 0.4)
    t1 = sh.lt(1)
    pops(sh, [t1 + 1.2, t1 + 2.4])
    t2 = sh.lt(2)
    pops(sh, [t2 + 0.6 + k * 0.25 for k in range(3)] + [t2 + 1.6], 0.5, 900)
    t3 = sh.lt(3)
    pops(sh, [t3 + 0.5])
    add(sh.t0 + t3 + 1.0, Y.buzz(1.0), 0.4)
    # ---- bolum 3
    sh = S["s18"]
    amb(sh, Y.wind(sh.d, 1.0, 8), 0.3)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 10, shouts=False, clashes=False), 0.1)
    add(sh.t0 + sh.lt(1) - 0.3, Y.paper(1.0, 0.8, 3), 0.7)
    for li, cnt in ((1, 3), (2, 2), (3, 1)):
        a, b = sh.lt(li), sh.le(li)
        pops(sh, [a + (b - a) * (k / cnt) - 0.1 for k in range(cnt)], 0.35, 400)
    add(sh.t0 + sh.lt(4) + 0.3, Y.whoosh(0.5, 1.0, 400, 3000, 7), 0.4)
    sh = S["s19"]
    t2 = sh.lt(1) - 0.2
    amb(sh, Y.wind(sh.d, 1.0, 9, bright=1200), 0.35)
    amb(sh, Y.camel_steps(t2 + 0.6, 1.0, 5), 0.5, 0, t2 + 0.6)
    amb(sh, Y.gallop(t2 + 0.6, 2, 0.5, 3, 0.6), 0.3, 0, t2 + 0.6)
    amb(sh, Y.fire(sh.d - t2, 1.0, 2), 0.6, t2, sh.d)
    sh = S["s20"]
    t2 = sh.lt(1) - 0.3
    add(sh.t0 + 0.3, Y.impact(0.8), 0.5)
    amb(sh, Y.wind(sh.d, 1.0, 10), 0.3, 0, t2 + 0.5)
    add(sh.t0 + 1.0, Y.whoosh(0.5, 1.0, 400, 3000, 8), 0.4)
    add(sh.t0 + t2, Y.paper(1.0, 0.8, 4), 0.6)
    add(sh.t0 + t2 + 0.8, Y.whoosh(3.0, 1.0, 200, 1200, 9), 0.25)
    sh = S["s21"]
    t1, t2 = sh.lt(1) - 0.3, sh.lt(2) - 0.3
    amb(sh, Y.wind(t1 + 0.4, 1.0, 11, bright=1400), 0.55, 0, t1 + 0.4)
    amb(sh, Y.camel_steps(t1, 1.0, 6), 0.4, 0, t1)
    amb(sh, Y.gallop(t1, 3, 0.6, 4, 0.55), 0.3, 0, t1)
    amb(sh, Y.wind(t2 - t1, 1.0, 12), 0.25, t1, t2)
    add(sh.t0 + t1 + 2.0, Y.whoosh(0.5, 1.0, 400, 3000, 10), 0.4)
    amb(sh, Y.crowd_roar(sh.d - t2, 1.0, 11, shouts=True, clashes=False, density=0.5), 0.2, t2, sh.d)
    pops(sh, [t2 + 0.4, t2 + 0.6], 0.5, 900)
    # ---- bolum 4
    sh = S["s23"]
    a0, b0 = sh.lt(0), sh.le(0)
    add(sh.t0 + a0 + (b0 - a0) * 0.72, Y.impact(0.6), 0.4)
    a1, b1 = sh.lt(1), sh.le(1)
    add(sh.t0 + a1 + (b1 - a1) * 0.2, Y.buzz(1.0), 0.45)
    pops(sh, [a1 + (b1 - a1) * 0.55, a1 + (b1 - a1) * 0.85])
    sh = S["s24"]
    pops(sh, [0.6, 1.1, 1.6], 0.4)
    t1 = sh.lt(1) - 0.2
    amb(sh, Y.gallop(sh.d - t1, 10, 1.0, 5, 0.38), 0.9, t1, sh.d)
    add(sh.t0 + t1 + 0.6, Y.impact(0.8), 0.5)
    amb(sh, Y.crowd_roar(sh.d - t1, 1.0, 12, shouts=True, clashes=False, density=0.5), 0.25, t1, sh.d)
    sh = S["s25"]
    t1 = sh.lt(1)
    add(sh.t0 + t1 + 0.5, Y.paper(1.0, 0.5, 5), 0.5)
    pops(sh, [t1 + 0.2] + [sh.lf(1, fr) for fr in (0.48, 0.66, 0.88)], 0.45)
    sh = S["s26"]
    amb(sh, Y.wind(sh.d, 1.0, 13), 0.3)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 13, shouts=False, clashes=False), 0.1)
    pops(sh, [1.4, sh.lt(1) + 0.5, sh.lt(1) + 0.7, sh.lt(1) + 0.9], 0.45)
    sh = S["s27"]
    add(sh.t0, Y.paper(1.0, 0.8, 6), 0.6)
    for k, tt in enumerate((sh.lf(0, 0.3), sh.lf(0, 0.75), sh.lt(1))):
        add(sh.t0 + tt, Y.sword_clash(0.8, 20 + k), 0.45)
        add(sh.t0 + tt, Y.big_drum(0.6), 0.4)
    sh = S["s28"]
    amb(sh, Y.gallop(sh.d, 6, 0.6, 6, 0.5), 0.4)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 14, shouts=True, clashes=False, density=0.4), 0.16)
    pops(sh, [sh.lf(1, fr) for fr in (0.22, 0.4, 0.6, 0.8)], 0.45)
    sh = S["s29"]
    t1, t2, t3 = sh.lt(1), sh.lt(2), sh.lt(3)
    amb(sh, Y.wind(sh.d, 1.0, 14), 0.25)
    amb(sh, Y.camel_steps(t1, 1.0, 7), 0.35, 0, t1)
    add(sh.t0 + t1 + 0.8, Y.coins(8, 1.0, 3, 0.5), 0.6)
    add(sh.t0 + t1 + 1.4, Y.coins(8, 1.0, 4, 0.5), 0.6)
    amb(sh, Y.crowd_roar(sh.d - t3, 1.0, 15, shouts=True, clashes=False, density=0.8), 0.25, t3, sh.d)
    add(sh.t0 + t3 + 3.0, Y.big_drum(0.6, 90, 40, 1.0), 0.6)
    # ---- bolum 5
    sh = S["s31"]
    add(sh.t0, Y.paper(1.0, 0.8, 7), 0.6)
    add(sh.t0 + sh.lt(1), Y.riser(2.5, 0.8), 0.25)
    pops(sh, [sh.lt(2), sh.lt(2) + 0.4], 0.6)
    add(sh.t0 + sh.lt(2), Y.big_drum(0.8), 0.5)
    sh = S["s32"]
    t1 = sh.lt(1) - 0.3
    add(sh.t0 + 0.5, Y.impact(0.5), 0.35)
    pops(sh, [sh.lt(1) + 0.4 + k * 0.04 * 3 for k in range(12)], 0.25, 900)
    add(sh.t0 + sh.lf(1, 0.6), Y.gallop(1.5, 4, 0.7, 7, 0.4)[:, 0], 0.5)
    sh = S["s33"]
    amb(sh, Y.wind(sh.d, 1.0, 15), 0.3)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 16, shouts=False, clashes=False), 0.08)
    add(sh.t0 + sh.lt(1) + 0.5, Y.impact(0.6), 0.4)
    sh = S["s34"]
    t2 = sh.lt(2)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 17, shouts=True, clashes=False, density=0.5), 0.3)
    k = 0
    tc = 0.32 * 0.9
    while tc < min(sh.d, t2 + 0.6):
        if tc > 1.5:
            add(sh.t0 + tc, Y.sword_clash(1.0, 40 + k), 0.55, 0.0)
        tc += 0.9
        k += 1
    add(sh.t0 + t2 + 0.55, Y.impact(1.0), 0.6)
    add(sh.t0 + t2 + 0.6, Y.thunk(1.0, 2), 0.6)
    add(sh.t0 + t2 + 1.0, Y.crowd_roar(2.5, 1.0, 18, shouts=True, clashes=False, density=2.0)[:, 0], 0.4)
    add(sh.t0 + 0.15, Y.big_drum(1.0), 0.5)
    sh = S["s35"]
    add(sh.t0 + 0.15, Y.big_drum(1.0), 0.5)
    amb(sh, Y.gallop(sh.d, 8, 0.8, 8, 0.4), 0.5, 1.0, sh.d)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 19, shouts=True, clashes=True, density=0.7), 0.4)
    sh = S["s36"]
    t1 = sh.lt(1)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 20, shouts=True, clashes=True, density=0.5), 0.3)
    for k in range(6):
        add(sh.t0 + t1 + k * 0.45, Y.shout(r := float(rng.uniform(300, 420)), 0.7, "a", 0.9, k), 0.45,
            (k % 3 - 1) * 0.5)
    for k in range(5):
        add(sh.t0 + t1 + 0.8 + k * 0.5, Y.thunk(0.8, k), 0.4)
    sh = S["s37"]
    add(sh.t0 + 0.15, Y.big_drum(1.0), 0.5)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 21, shouts=True, clashes=True, density=1.6), 0.55)
    sh = S["s38"]
    add(sh.t0 + 0.15, Y.big_drum(1.0), 0.5)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 22, shouts=True, clashes=False, density=0.6), 0.3)
    tt = 0.0
    k = 0
    while tt < sh.d:
        for j in range(6):
            add(sh.t0 + tt + j * 0.12, Y.arrow_whiz(0.8, k * 10 + j), 0.4, float(rng.uniform(-0.8, 0.8)))
        for j in range(5):
            add(sh.t0 + tt + 1.1 + j * 0.08, Y.thunk(0.6, k * 10 + j), 0.35, float(rng.uniform(-0.8, 0.8)))
        tt += 1.6
        k += 1
    add(sh.t0 + 1.0, Y.impact(0.7), 0.4)
    sh = S["s39"]
    t1 = sh.lt(1)
    amb(sh, Y.crowd_roar(t1 + 2.0, 1.0, 23, shouts=True, clashes=False, density=0.6), 0.3, 0, t1 + 2.0)
    for k in range(10):
        add(sh.t0 + t1 + k * 0.1, Y.shout(float(rng.uniform(140, 220)), 1.2, "a", 0.8, 100 + k), 0.35,
            float(rng.uniform(-0.6, 0.6)))
    add(sh.t0 + t1, Y.big_drum(1.0), 0.6)
    amb(sh, Y.wind(sh.d - t1 - 2.0, 1.0, 24), 0.4, t1 + 2.0, sh.d)
    add(sh.t0 + t1 + 2.0, Y.impact(0.7), 0.4)
    sh = S["s40"]
    cr = Y.crowd_roar(sh.d, 1.0, 25, shouts=True, clashes=True, density=1.0)
    cr = np.stack([Y.lp(cr[:, 0], 500), Y.lp(cr[:, 1], 500)], axis=1)
    amb(sh, cr, 0.6)
    n_ = int(sh.d * SR)
    tin = np.sin(2 * np.pi * 4200 * np.arange(n_) / SR) * 0.02
    amb(sh, np.stack([tin, tin], axis=1), 0.6)
    sh = S["s41"]
    t2 = sh.lt(2)
    amb(sh, Y.wind(sh.d, 1.0, 26), 0.35)
    pops(sh, [0.8])
    add(sh.t0 + t2, Y.impact(0.8), 0.5)
    sh = S["s42"]
    add(sh.t0 + 0.1, Y.big_drum(1.0), 0.6)
    amb(sh, Y.gallop(sh.d, 16, 1.0, 9, 0.36), 1.0)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 27, shouts=True, clashes=True, density=1.2), 0.45)
    sh = S["s43"]
    t1 = sh.lt(1) - 0.2
    amb(sh, Y.gallop(t1 + 0.4, 6, 0.8, 10, 0.4), 0.5, 0, t1 + 0.4)
    amb(sh, Y.fire(t1, 1.0, 3), 0.3, 0, t1)
    amb(sh, Y.wind(sh.d, 1.0, 27), 0.25)
    add(sh.t0 + t1, Y.paper(1.0, 0.7, 8), 0.5)
    add(sh.t0 + t1 + 0.5, Y.impact(0.8), 0.5)
    add(sh.t0 + t1 + 1.0, Y.whoosh(0.5, 1.0, 400, 3000, 11), 0.4)
    sh = S["s44"]
    t1 = sh.lt(1)
    amb(sh, Y.wind(sh.d, 1.0, 28, bright=2500), 1.0)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 29, shouts=True, clashes=True, density=0.8), 0.35)
    for k in range(8):
        y = Y.shout(float(rng.uniform(250, 400)), 1.0, "a", 0.7, 200 + k)
        nn = len(y)
        y = y * np.linspace(1, 0.1, nn)
        add(sh.t0 + t1 + 1.5 + k * 0.4, y, 0.35, float(rng.uniform(-0.5, 0.8)))
    sh = S["s45"]
    amb(sh, Y.wind(sh.d, 1.0, 30, bright=700), 0.5)
    amb(sh, Y.fire(sh.d, 0.6, 4), 0.2)
    for k in range(4):
        add(sh.t0 + 0.8 + k * 1.6, Y.caw(1.0, k), 0.5, float(rng.uniform(-0.7, 0.7)))
    # ---- bolum 6
    sh = S["s47"]
    a, b = sh.lt(0), sh.le(0)
    pops(sh, [0.2, a + (b - a) * 0.25, a + (b - a) * 0.7], 0.5)
    for k in range(12):
        add(sh.t0 + a + (b - a) * 0.25 + k * 0.11, Y.tek(0.3, 3000), 0.3)
    sh = S["s48"]
    t1 = sh.lt(1)
    amb(sh, Y.wind(sh.d, 1.0, 31), 0.25)
    pops(sh, [sh.lf(1, fr) for fr in (0.1, 0.3, 0.5)])
    add(sh.t0 + sh.lf(1, 0.5), Y.coins(30, 1.0, 5, 2.5), 0.6)
    sh = S["s49"]
    amb(sh, Y.sea_waves(sh.d, 1.0, 1), 0.6)
    amb(sh, Y.wind(sh.d, 1.0, 32), 0.2)
    add(sh.t0 + sh.lt(2), Y.impact(0.6), 0.35)
    sh = S["s50"]
    amb(sh, Y.crowd_roar(sh.d, 1.0, 33, shouts=False, clashes=False), 0.1)
    amb(sh, Y.wind(sh.d, 1.0, 33), 0.2)
    add(sh.t0 + sh.lt(1) - 0.3, Y.ui_pop(1.0, 500), 0.5)
    sh = S["s51"]
    amb(sh, Y.camel_steps(sh.d, 1.0, 8), 0.5)
    amb(sh, Y.wind(sh.d, 1.0, 34), 0.3)
    t1 = sh.lt(1)
    for k in range(int((sh.d - t1) / 2.4) + 1):
        add(sh.t0 + t1 + k * 2.4, Y.ding(0.6), 0.3)
    sh = S["s52"]
    amb(sh, Y.camel_steps(sh.d, 1.0, 9), 0.45)
    amb(sh, Y.crowd_roar(sh.d, 1.0, 35, shouts=False, clashes=False), 0.12)
    add(sh.t0 + sh.lt(1) + 0.5, Y.ui_pop(1.0, 500), 0.5)
    sh = S["s53"]
    add(sh.t0, Y.paper(1.0, 0.8, 9), 0.6)
    for fr in (0.45, 0.6, 0.75):
        add(sh.t0 + sh.lf(0, fr), Y.ding(1.0), 0.35)
    add(sh.t0 + sh.lt(1) - 0.2, Y.bell(220, 5.0, 0.6), 0.35)
    add(sh.t0 + sh.lt(2), Y.impact(0.6), 0.35)
    # ---- bolum 7
    sh = S["s55"]
    amb(sh, Y.wind(sh.d, 1.0, 36, bright=500), 0.5)
    add(sh.t0 + 0.5, Y.bell(110, 6.0, 0.8), 0.45)
    add(sh.t0 + sh.lt(1) + 0.2, Y.impact(0.6), 0.4)
    sh = S["s56"]
    amb(sh, Y.wind(sh.d, 1.0, 37), 0.35)
    add(sh.t0 + sh.lt(1), Y.impact(0.5), 0.3)
    add(sh.t0 + sh.lt(3), Y.impact(0.6), 0.35)
    sh = S["s57"]
    amb(sh, Y.wind(sh.d, 1.0, 38, bright=500), 0.45)
    for k in range(14):
        add(sh.t0 + 0.4 + k * 0.11, Y.tek(0.3, 2600), 0.25)
    add(sh.t0 + 3.5, Y.bell(98, 6.0, 0.7), 0.35)
    sh = S["s58"]
    rec = sh.lf(0, 0.62)
    add(sh.t0 + rec, Y.ding(1.0), 0.4)
    add(sh.t0 + rec, Y.riser(0.8, 0.6)[::-1].copy(), 0.0)
    # ---- bolum 8
    sh = S["s60"]
    t1 = sh.lt(1)
    amb(sh, Y.scribble(sh.d, 1.0, 1), 0.5, 1.0, sh.d)
    add(sh.t0 + sh.lf(1, 0.75), Y.coins(10, 1.0, 6, 0.6), 0.6)
    pops(sh, [1.0, sh.lf(1, 0.8)])
    sh = S["s61"]
    amb(sh, Y.wind(sh.d, 0.6, 39), 0.25)
    pops(sh, [sh.lf(0, 0.45), sh.lt(1) + 0.2])
    add(sh.t0 + sh.lf(0, 0.7), Y.buzz(1.0), 0.35)
    add(sh.t0 + sh.lt(1) + 0.6, Y.ding(1.0), 0.4)
    sh = S["s62"]
    pops(sh, [sh.lt(0) + 0.1, sh.lf(0, 0.55), sh.lt(1) + 0.2], 0.55)
    sh = S["s63"]
    amb(sh, Y.sea_waves(sh.d, 1.0, 2), 0.45)
    add(sh.t0 + 0.4, Y.impact(0.6), 0.4)
    pops(sh, [2.5])
    sh = S["s64"]
    t1 = sh.lt(1) - 0.3
    amb(sh, Y.wind(sh.d, 1.0, 40), 0.3)
    add(sh.t0 + t1, Y.riser(1.2, 0.6), 0.25)
    add(sh.t0 + t1 + 0.3, Y.impact(1.0), 0.55)
    pops(sh, [t1 + 2.5])
    sh = S["s65"]
    pops(sh, [sh.lf(0, fr) for fr in (0.0, 0.35, 0.7)], 0.5)
    sh = S["s66"]
    a, b = sh.lt(0), sh.le(0)
    pops(sh, [0.3] + [a + (b - a) * fr for fr in (0.22, 0.42, 0.72)], 0.55)
    t1 = sh.lt(1)
    add(sh.t0 + t1 + 0.1, Y.impact(0.6), 0.35)
    add(sh.t0 + t1 + 1.0, Y.ui_pop(1.0, 500), 0.5)
    add(sh.t0 + t1 + 3.2, Y.tek(1.0, 3500), 0.5)
    add(sh.t0 + t1 + 3.25, Y.ding(1.0), 0.45)
    # bolum kartlari
    for sid, sh in S.items():
        if sh.s["fn"] == "chapter":
            add(sh.t0, Y.whoosh(0.7, 1.0, 200, 2500, int(sid[1:])), 0.6)
            add(sh.t0 + 0.28, Y.impact(0.6), 0.45)
            add(sh.t0 + 0.05, Y.paper(1.0, 0.7, int(sid[1:])), 0.5)
    return C


def build():
    tl = load_tl()
    total = tl["total"]
    n = int((total + 0.5) * SR)
    print("anlatim...", flush=True)
    nar = narration(tl, n)
    print("muzik...", flush=True)
    mus = soundtrack_music(tl, n)
    mask = speech_mask(tl, n)
    mus *= (1.0 - 0.62 * mask)[:, None]
    print("efektler...", flush=True)
    fx = np.zeros((n, 2))
    for t, x, g in cues(tl):
        place(fx, x, t, g)
    fxm = (1.0 - 0.35 * mask)[:, None]
    mix = nar * 1.0 + mus * 0.55 + fx * 0.55 * fxm
    # yumusak limitleyici
    pk = np.abs(mix).max()
    print("tepe:", round(float(pk), 3))
    mix = np.tanh(mix * 1.1) / np.tanh(1.1)
    sf.write(os.path.join(WORK, "soundtrack.wav"), mix.astype(np.float32), SR, subtype="FLOAT")
    sf.write(os.path.join(WORK, "stem_narration.wav"), nar.astype(np.float32), SR, subtype="FLOAT")
    print("yazildi:", os.path.join(WORK, "soundtrack.wav"), round(n / SR, 2), "sn")


if __name__ == "__main__":
    build()
