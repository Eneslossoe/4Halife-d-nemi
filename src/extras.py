"""Kucuk resim (thumbnail), altyazi (SRT) ve YouTube aciklamasi uretir."""
import json
import math
import os
import sys

import numpy as np
import skia

import backgrounds as B
import characters as C
import effects as FX
import engine as E
import scenery as S
from gfx import (OUT, W, H, big_number, label_tag, lin_grad, poly, rgb, ribbon, stroke, vignette, fill, rad_grad)
from script import CHAPTERS, TITLE

WORK = os.environ.get("ZK_WORK", "/tmp/claude-0/work")
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTD = os.path.join(ROOT, "output")


def thumbnail(path):
    s = skia.Surface(W, H)
    cv = s.getCanvas()
    left = poly([(0, 0), (1010, 0), (900, H), (0, H)])
    right = poly([(1010, 0), (W, 0), (W, H), (900, H)])
    cv.save()
    cv.clipPath(left, skia.ClipOp.kIntersect, True)
    E.draw_bg(cv, "yarmouk_day", lambda c: B.yarmouk(c, "day"))
    cv.drawRect(skia.Rect.MakeWH(W, H), fill("#3a4a6a", 70))
    E.army(cv, 0, [(760, 0.3, -40, 1000, 46)], facing=1, seed=3)
    FX.arrow_volley(cv, 0.7, 1500, 300, 300, 700, n=30, dur=1.4, seed=2, s=0.8, spread=500)
    C.draw_person(cv, C.preset("zeyd", weapon="sword"), C.pose(expr="scared", look=(0.7, -0.3), arm_b=100, wpn=120,
                                                               arm_a=30), 440, 1250, 2.05, 1)
    cv.restore()
    cv.save()
    cv.clipPath(right, skia.ClipOp.kIntersect, True)
    cv.drawRect(skia.Rect.MakeWH(W, H), lin_grad((0, 0), (0, H), ["#ffcf6a", "#f3a640", "#c66a20"]))
    for k in range(16):
        a = math.radians(-90 + (k - 8) * 11)
        cv.drawPath(poly([(1460, 760), (1460 + math.cos(a) * 1400 + 50, 760 + math.sin(a) * 1400),
                          (1460 + math.cos(a) * 1400 - 50, 760 + math.sin(a) * 1400)]), fill("#fff2b0", 50))
    S.ridge(cv, W, H, 900, 50, 1.0, "#a8642a", seed=4)
    for k, x in enumerate((1180, 1760)):
        C.draw_person(cv, C.preset("roman"), C.pose(expr="angry", look=(-0.6, 0)), x, 1000, 1.0, -1)
    C.draw_person(cv, C.preset("heraclius"), C.pose(expr="angry", look=(-0.7, 0), arm_b=100, arm_a=20),
                  1480, 1250, 2.0, -1)
    cv.restore()
    zig = [(1010, -20), (950, 300), (995, 330), (900, 700), (945, 720), (860, 1100)]
    cv.drawPath(poly(zig, closed=False), stroke("#ffffff", 26))
    cv.drawPath(poly(zig, closed=False), stroke("#ffe680", 11))
    cv.save()
    cv.translate(W / 2, 250)
    big_number(cv, "636", 0, 0, 250, rot=-2)
    cv.restore()
    ribbon(cv, "HALİFE ASKERİ OLSAYDIN?", W / 2, 350, 74, rot=-2.5)
    label_tag(cv, "BEDEVİ", 220, 1000, 64, rot=-6)
    label_tag(cv, "HERAKLEİOS", 1700, 1000, 64, rot=5)
    vignette(cv, 90)
    img = s.makeImageSnapshot()
    small = skia.Surface(1280, 720)
    small.getCanvas().drawImageRect(img, skia.Rect.MakeWH(1280, 720),
                                    skia.SamplingOptions(skia.CubicResampler.Mitchell()))
    small.makeImageSnapshot().save(path, skia.kJPEG, 92)
    img.save(path.replace(".jpg", "_1080p.png"), skia.kPNG)


def fmt(t):
    h = int(t // 3600)
    m = int(t % 3600 // 60)
    s = t % 60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int((s - int(s)) * 1000):03d}"


def srt(path):
    tl = json.load(open(os.path.join(WORK, "timeline.json")))
    idx = 1
    out = []
    for sh in tl["shots"]:
        for l in sh["lines"]:
            txt = l["sub"]
            a, b = sh["start"] + l["start"], sh["start"] + l["end"]
            # uzun cumleleri parcala
            words = txt.split()
            chunks, cur = [], ""
            for w in words:
                if len(cur) + len(w) + 1 > 80 and cur:
                    chunks.append(cur)
                    cur = w
                else:
                    cur = (cur + " " + w).strip()
            if cur:
                chunks.append(cur)
            total = sum(len(c) for c in chunks)
            t = a
            for c in chunks:
                d = (b - a) * len(c) / total
                # iki satira bol
                if len(c) > 42:
                    ws = c.split()
                    best = min(range(1, len(ws)), key=lambda k: abs(len(" ".join(ws[:k])) - len(c) / 2))
                    c = " ".join(ws[:best]) + "\n" + " ".join(ws[best:])
                if l["voice"] == "q":
                    c = "“" + c + "”" if "\n" not in c else "“" + c.replace("\n", "\n") + "”"
                out.append(f"{idx}\n{fmt(t)} --> {fmt(t + d)}\n{c}\n")
                idx += 1
                t += d
    open(path, "w", encoding="utf-8").write("\n".join(out))


def description(path):
    tl = json.load(open(os.path.join(WORK, "timeline.json")))
    lines = [TITLE, "", "Yıl 636. Yermük Nehri'nin kıyısında, dünyanın en güçlü ordusunun karşısındasın. "
             "Halife Ebu Bekir ve Halife Ömer döneminde Romalılara (Bizans) karşı savaşan sıradan bir Arap askeri "
             "olsaydın hayatın nasıl olurdu? Çölde geçen çocukluktan orduya katılmaya, ganimet paylarından "
             "Yermük'ün altı gününe, Kudüs'ün teslimi, Amvas vebası ve Divan'a kadar bir askerin hikâyesi.", "",
             "⏱ BÖLÜMLER"]
    for sh in tl["shots"]:
        if sh["id"] in CHAPTERS:
            t = sh["start"]
            lines.append(f"{int(t // 60):d}:{int(t % 60):02d} {CHAPTERS[sh['id']]}")
    lines += ["", "📚 Not: Sayılar ve bazı olaylar (kum fırtınası, Herakleios'un vedası vb.) farklı kaynaklarda farklı "
              "anlatılır; videoda 'rivayete göre' diye belirtilmiştir. Halife ve sahabeler saygı gereği yüzsüz "
              "siluet olarak gösterilmiştir.", "",
              "🎙 Bu videonun tüm görselleri, animasyonları, müziği, efektleri ve seslendirmesi kodla üretilmiştir.",
              "", "#ZamanKırığı #Yermük #Halife #İslamTarihi #Bizans #Tarih #Olsaydın", "",
              "ETİKETLER: yermük savaşı, halife ömer, halid bin velid, ebu ubeyde, bizans, roma, herakleios, "
              "arap fetihleri, islam tarihi, 636, kudüs'ün fethi, amvas vebası, divan, olsaydın, zaman kırığı"]
    open(path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    os.makedirs(OUTD, exist_ok=True)
    thumbnail(os.path.join(OUTD, "kucuk_resim.jpg"))
    srt(os.path.join(OUTD, "altyazi_tr.srt"))
    description(os.path.join(OUTD, "youtube_aciklama.txt"))
    print("ok")
