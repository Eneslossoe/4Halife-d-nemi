"""Kare kare render + ffmpeg ile kodlama (paralel).

Kullanim:
  python3 render.py stills s01:2.0 s05:1.0 ...      -> test kareleri (PNG)
  python3 render.py video [--workers 4] [--only s01,s02]
"""
import json
import math
import os
import subprocess
import sys
import time
from multiprocessing import Process

import numpy as np
import skia

from gfx import W, H, FPS

WORK = os.environ.get("ZK_WORK", "/tmp/claude-0/work")
OUTDIR = os.path.join(WORK, "render")
os.makedirs(OUTDIR, exist_ok=True)


def load_fns():
    import shots1
    import shots2
    import shots3
    fns = {}
    for mod in (shots1, shots2, shots3):
        for k in dir(mod):
            v = getattr(mod, k)
            if callable(v) and not k.startswith("_"):
                fns.setdefault(k, v)
    return fns


def load_timeline():
    with open(os.path.join(WORK, "timeline.json")) as f:
        return json.load(f)


def shot_params(shot):
    p = dict(shot["params"])
    p["_lines"] = [(l["start"], l["end"]) for l in shot["lines"]]
    p["_dur"] = shot["dur"]
    p["_id"] = shot["id"]
    return p


def render_frame(cv, fns, shot, t):
    cv.clear(skia.ColorBLACK)
    p = shot_params(shot)
    fn = fns[shot["fn"]]
    cv.save()
    fn(cv, t, shot["dur"], p)
    cv.restore()
    # sahne basi/sonu cok kisa kararma (kesmeleri yumusatir)
    fi = t / 0.12
    if fi < 1 and shot["fn"] not in ("chapter", "title_card"):
        cv.drawRect(skia.Rect.MakeWH(W, H), skia.Paint(Color=skia.Color(0, 0, 0, int(255 * (1 - fi) * 0.6))))


def stills(args):
    fns = load_fns()
    tl = load_timeline()
    byid = {s["id"]: s for s in tl["shots"]}
    arr = np.zeros((H, W, 4), np.uint8)
    surf = skia.Surface(arr, colorType=skia.kRGBA_8888_ColorType)
    cv = surf.getCanvas()
    outs = []
    for a in args:
        sid, tt = a.split(":")
        shot = byid[sid]
        tt = float(tt)
        if tt < 0:
            tt = shot["dur"] + tt
        t0 = time.time()
        render_frame(cv, fns, shot, tt)
        path = os.path.join(OUTDIR, f"still_{sid}_{tt:.1f}.png")
        surf.makeImageSnapshot().save(path, skia.kPNG)
        outs.append(path)
        print(path, f"{(time.time() - t0) * 1000:.0f} ms", flush=True)
    return outs


def worker(wid, frames, shots, seg_path):
    fns = load_fns()
    arr = np.zeros((H, W, 4), np.uint8)
    surf = skia.Surface(arr, colorType=skia.kRGBA_8888_ColorType)
    cv = surf.getCanvas()
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r",
           str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-pix_fmt", "yuv420p",
           "-threads", "2", seg_path]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    n = 0
    for (si, t) in frames:
        render_frame(cv, fns, shots[si], t)
        pr.stdin.write(arr.tobytes())
        n += 1
        if n % 300 == 0:
            el = time.time() - t0
            print(f"[w{wid}] {n}/{len(frames)} kare, {n / el:.1f} fps", flush=True)
    pr.stdin.close()
    pr.wait()
    print(f"[w{wid}] bitti {n} kare {time.time() - t0:.0f}s", flush=True)


def video(workers=4, only=None):
    tl = load_timeline()
    shots = tl["shots"]
    frames = []
    for si, s in enumerate(shots):
        if only and s["id"] not in only:
            continue
        f0 = round(s["start"] * FPS)
        f1 = round((s["start"] + s["dur"]) * FPS)
        for f in range(f0, f1):
            frames.append((si, (f - f0) / FPS))
    n = len(frames)
    chunk = math.ceil(n / workers)
    procs, segs = [], []
    for w in range(workers):
        part = frames[w * chunk:(w + 1) * chunk]
        if not part:
            continue
        seg = os.path.join(OUTDIR, f"seg_{w}.mp4")
        segs.append(seg)
        pr = Process(target=worker, args=(w, part, shots, seg))
        pr.start()
        procs.append(pr)
    for pr in procs:
        pr.join()
    lst = os.path.join(OUTDIR, "segs.txt")
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    out = os.path.join(OUTDIR, "video_noaudio.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", out],
                   check=True)
    print("video:", out, n, "kare")


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        stills(sys.argv[2:])
    elif sys.argv[1] == "video":
        w = 4
        only = None
        a = sys.argv[2:]
        if "--workers" in a:
            w = int(a[a.index("--workers") + 1])
        if "--only" in a:
            only = set(a[a.index("--only") + 1].split(","))
        video(w, only)
