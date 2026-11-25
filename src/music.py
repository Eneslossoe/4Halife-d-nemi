"""Prosedurel fon muzigi: Hicaz makaminda ud, ney, kanun, davul/darbuka, koro, yaylilar."""
import numpy as np

import synth as Y
from synth import SR, pan, place, scale_f

D2, D3, D4, D5 = Y.D4 / 4, Y.D4 / 2, Y.D4, Y.D4 * 2

# 8'lik vuruslarla usul kaliplari  (D=dum, T=tek, K=hafif tek, B=buyuk davul, J=zil, .=bos)
PAT = {
    "duyek": "DT.TD.T.",
    "duyek2": "D.KTD.TK",
    "march": "B.T.D.T.",
    "battle": "BKTKBTBKBKTKBTTT",
    "battle_pre": "B...B...B.B.B...",
    "triumph": "B.T.BTT.B.T.BTTK",
    "soft": "D...K...",
    "outro": "DTKTD.TK",
}

MOODS = {
    "intro": dict(bpm=76, pat="battle_pre", drone=True, brass=True, ney=0.5, choir=True, wet=0.35),
    "desert": dict(bpm=92, pat="duyek", oud=True, ney=0.8, drone=True, wet=0.3),
    "desert2": dict(bpm=100, pat="duyek2", oud=True, kanun=True, ney=0.5, drone=True, wet=0.28),
    "march": dict(bpm=100, pat="march", oud=True, drone=True, brass=True, ney=0.3, wet=0.28),
    "tension": dict(bpm=64, pat="soft", drone=True, pad_dark=True, ney=0.5, wet=0.45),
    "battle_pre": dict(bpm=84, pat="battle_pre", drone=True, choir=True, brass=True, wet=0.35),
    "battle": dict(bpm=132, pat="battle", drone=True, choir=True, brass=True, ostinato=True, wet=0.28),
    "heartbeat": dict(bpm=72, pat=None, drone=True, heart=True, ney=0.6, wet=0.6),
    "aftermath": dict(bpm=60, pat=None, drone=True, pad_dark=True, ney=1.0, wet=0.55),
    "sad": dict(bpm=66, pat=None, drone=True, pad_dark=True, ney=1.0, kanun=True, wet=0.5),
    "triumph": dict(bpm=96, pat="triumph", drone=True, brass=True, choir=True, oud=True, major=True, wet=0.32),
    "plague": dict(bpm=50, pat=None, drone=True, pad_dark=True, bells=True, ney=0.4, wet=0.6),
    "epic_end": dict(bpm=88, pat="soft", drone=True, pad_major=True, ney=0.9, oud=True, wet=0.4),
    "outro": dict(bpm=104, pat="outro", oud=True, kanun=True, drone=True, ney=0.4, wet=0.28),
}

OUD_RIFFS = [[0, 0, 4, 3, 1, 0, -1, 0], [0, 1, 2, 1, 0, -1, -3, -1], [4, 3, 2, 1, 2, 1, 0, 0],
             [0, None, 0, 1, 2, None, 1, 0]]


def melody_phrase(r, n=5, lo=-1, hi=8):
    deg = int(r.integers(0, 5))
    notes = []
    for i in range(n):
        step = int(r.choice([-2, -1, -1, 1, 1, 2, 0]))
        deg = int(np.clip(deg + step, lo, hi))
        notes.append(deg)
    notes[-1] = int(r.choice([0, 4, 7]))
    return notes


def gen(mood, dur, seed=0):
    cfg = MOODS[mood]
    r = np.random.default_rng(seed)
    n = int(dur * SR)
    out = np.zeros((n + SR * 4, 2))
    beat = 60.0 / cfg["bpm"]
    eighth = beat / 2
    major = cfg.get("major")
    sc = [0, 2, 4, 5, 7, 9, 11] if major else Y.HICAZ

    def f(deg, base=D4):
        return scale_f(deg, base, sc)

    # drone
    if cfg.get("drone"):
        seg = 12.0
        t0 = 0.0
        while t0 < dur:
            d = min(seg + 2, dur - t0 + 2)
            place(out, pan(Y.drone(D2, d, 0.55), -0.2), t0)
            place(out, pan(Y.drone(D2 * 1.5 if not major else D2 * 1.5, d, 0.25), 0.25), t0)
            t0 += seg
    if cfg.get("pad_dark"):
        t0 = 0.0
        k = 0
        chords = [[D3, D3 * 1.5], [D3 * 2 ** (1 / 12), D3 * 2 ** (8 / 12)], [D3, D3 * 2 ** (5 / 12)]]
        while t0 < dur:
            place(out, pan(Y.pad(chords[k % 3], 8.5, 0.6, att=2.0, rel=2.5, bright=900), 0), t0)
            t0 += 8.0
            k += 1
    if cfg.get("pad_major"):
        t0 = 0.0
        k = 0
        st = lambda *ss: [D3 * 2 ** (x / 12) for x in ss]
        chords = [st(0, 4, 7), st(5, 9, 12), st(0, 4, 7), st(7, 11, 14)]
        while t0 < dur:
            place(out, pan(Y.pad(chords[k % 4], 6.5, 0.7, att=1.5, rel=2.0, bright=2400), 0), t0)
            t0 += 6.0
            k += 1
    if cfg.get("choir"):
        t0 = 0.0
        k = 0
        ch = [[D3, D3 * 1.5, D4], [D3 * 2 ** (1 / 12), D3 * 2 ** (8 / 12), D4 * 2 ** (1 / 12)]] if not major else \
            [[D3, D3 * 1.26, D3 * 1.5], [D3 * 4 / 3, D3 * 5 / 3, D4]]
        while t0 < dur:
            place(out, pan(Y.choir(ch[k % 2], beat * 8 + 1.0, 0.55), 0), t0)
            t0 += beat * 8
            k += 1
    # davul
    pat = PAT.get(cfg.get("pat")) if cfg.get("pat") else None
    if pat:
        step = eighth if len(pat) == 8 else beat / 4
        i = 0
        t0 = 0.0
        while t0 < dur:
            c = pat[i % len(pat)]
            v = r.uniform(0.75, 1.0)
            if c == "D":
                place(out, pan(Y.dum(v), -0.1), t0)
            elif c == "T":
                place(out, pan(Y.tek(v * 0.8), 0.2), t0)
            elif c == "K":
                place(out, pan(Y.tek(v * 0.4, 2400), 0.3), t0)
            elif c == "B":
                place(out, pan(Y.big_drum(v), 0), t0)
            elif c == "J":
                place(out, pan(Y.jingle(v), 0.4), t0)
            if c in "DT" and mood in ("desert", "desert2", "outro") and r.random() < 0.3:
                place(out, pan(Y.jingle(0.5), 0.5), t0)
            t0 += step
            i += 1
            if mood in ("battle", "battle_pre", "intro") and i % (len(pat) * 4) == 0:
                for k in range(6):
                    place(out, pan(Y.big_drum(0.5 + k * 0.08, 130, 60, 0.6), 0), t0 - beat + k * beat / 6)
    # ud ostinato
    if cfg.get("oud"):
        t0 = 0.0
        bar = 0
        while t0 < dur:
            riff = OUD_RIFFS[(bar // 2) % len(OUD_RIFFS)]
            for j, dg in enumerate(riff):
                if dg is None:
                    continue
                place(out, pan(Y.oud(f(dg, D3), 1.2, r.uniform(0.6, 0.9)), -0.35), t0 + j * eighth)
            t0 += eighth * 8
            bar += 1
    if cfg.get("kanun"):
        t0 = beat * 4
        while t0 < dur:
            if r.random() < 0.6:
                base = int(r.integers(0, 5))
                for j in range(4):
                    place(out, pan(Y.kanun(f(base + j * 2 % 7, D4), 0.8, 0.5), 0.45), t0 + j * eighth / 2)
            t0 += beat * 4
    if cfg.get("ostinato"):
        t0 = 0.0
        k = 0
        seq = [0, 0, 1, 0, 2, 0, 1, 0]
        while t0 < dur:
            dg = seq[k % 8]
            nn = Y.pad([f(dg, D3)], beat / 2 * 0.9, 0.9, att=0.005, rel=0.05, bright=3000, nh=10)
            place(out, pan(nn, 0.3 if k % 2 else -0.3), t0)
            t0 += beat / 2
            k += 1
    if cfg.get("brass"):
        t0 = beat * 2
        k = 0
        notes = [0, 1, 0, -1] if not major else [0, 2, 4, 2]
        while t0 < dur:
            dg = notes[k % len(notes)]
            place(out, pan(Y.brass(f(dg, D3), beat * 1.5, 0.8), 0.0), t0)
            place(out, pan(Y.brass(f(dg + 4, D3), beat * 1.5, 0.5), 0.1), t0)
            t0 += beat * 8
            k += 1
    if cfg.get("heart"):
        t0 = 0.0
        while t0 < dur:
            place(out, pan(Y.heartbeat(0.9), 0), t0)
            t0 += 0.85
    if cfg.get("bells"):
        t0 = 1.0
        while t0 < dur:
            place(out, pan(Y.bell(146.8, 6.0, 0.7), 0.2), t0)
            t0 += 7.0
    # ney melodisi
    nv = cfg.get("ney", 0)
    if nv:
        t0 = beat * 4 if mood not in ("aftermath", "sad") else 1.0
        while t0 < dur:
            if r.random() < 0.85:
                ph = melody_phrase(r, int(r.integers(3, 6)))
                durs = r.choice([[1, 1, 2, 1, 3], [0.5, 0.5, 1, 2, 2], [2, 1, 1, 4, 2], [1.5, 0.5, 2, 2, 2]])
                tt = t0
                for dg, dd in zip(ph, durs):
                    ln = dd * beat * (1.6 if mood in ("aftermath", "sad", "plague", "heartbeat") else 1.0)
                    place(out, pan(Y.ney(f(dg, D4 if mood not in ("plague",) else D3), ln + 0.2, nv * 0.9), 0.15), tt)
                    tt += ln
                t0 = tt + beat * r.choice([2, 4])
            else:
                t0 += beat * 4
    out = out[:n]
    out = Y.reverb(out, cfg.get("wet", 0.3), seconds=2.8, damp=2.6)
    pk = np.abs(out).max() + 1e-9
    return out / pk * 0.5
