# Zaman Kırığı — Halife Döneminde Romalılara Karşı Savaşan Bir Arap Askeri Olsaydın?

Bu depo, "Zaman Kırığı" kanalı için hazırlanan videonun **tamamen kodla üretilmiş** kaynaklarını içerir:
görseller, animasyonlar, haritalar, müzik, ses efektleri ve seslendirme. Hiçbir hazır görsel/ses dosyası,
stok içerik veya ElevenLabs kullanılmamıştır.

## Çıktılar (`output/`)

| Dosya | Açıklama |
|---|---|
| `halife_askeri_olsaydin_github.mp4` | 1920×1080, 30 fps, 12:27 final video (GitHub 100 MB sınırı için sıkıştırılmış kopya; tam kalite sürüm sohbette ayrıca iletildi) |
| `reels_halife_askeri.mp4` | 1080×1920 dikey Reels/Shorts, 54 sn, büyük altyazılı |
| `kucuk_resim.jpg` | 1280×720 YouTube küçük resmi (kanal stilinde) |
| `kucuk_resim_1080p.png` | Küçük resmin yüksek çözünürlüklü hâli |
| `altyazi_tr.srt` | Türkçe altyazı (YouTube'a yüklenebilir) |
| `youtube_aciklama.txt` | Başlık, açıklama, bölüm zaman damgaları, etiketler |

## Nasıl üretildi?

- **Seslendirme:** Açık kaynak, yerel çalışan [Piper](https://github.com/rhasspy/piper) Türkçe sesleri
  (`tr_TR-dfki-medium` anlatıcı, `tr_TR-fahrettin-medium` alıntılar). `src/tts.py`
- **Çizimler:** `skia-python` ile vektörel çizim. Karakterler (`src/characters.py`), dekor (`src/scenery.py`),
  arka planlar (`src/backgrounds.py`), efektler (`src/effects.py`).
- **Haritalar:** `global-land-mask` kara/deniz verisiyle parşömen stili haritalar. `src/maps.py`
- **Müzik:** Hicaz makamında ud, ney, kanun, davul/darbuka, koro ve yaylılar numpy ile sentezlendi.
  `src/synth.py`, `src/music.py`
- **Efektler:** Kılıç, ok yağmuru, at nalı, kalabalık, rüzgâr, kum fırtınası, ateş, deniz, çan vb.
  hepsi matematiksel olarak sentezlendi. `src/audio.py`
- **Sahneler:** 66 sahne, `src/shots1.py`, `src/shots2.py`, `src/shots3.py`; senaryo `src/script.py`.

Hassasiyet notu: Halife Ömer, Halid bin Velid, Ebu Ubeyde gibi sahabeler saygı gereği **yüzsüz, ışıklı siluet**
olarak gösterilmiştir.

## Yeniden üretmek

```bash
pip install skia-python piper-tts soundfile scipy numpy global-land-mask
# Piper Türkçe ses modelleri: $ZK_WORK/models/vits-piper-tr_TR-{dfki,fahrettin}-medium/
cd src
python3 tts.py                 # seslendirme + timeline.json
python3 audio.py               # müzik + efekt + miksaj -> soundtrack.wav
python3 render.py video        # sahne sahne render -> video_noaudio.mp4
python3 extras.py              # küçük resim, altyazı, açıklama
```

Tek bir sahneyi yeniden çizmek: `python3 render.py video --only s34` ; test karesi: `python3 render.py stills s34:3.0`
