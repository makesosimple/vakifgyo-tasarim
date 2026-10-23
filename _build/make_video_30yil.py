# -*- coding: utf-8 -*-
"""
30. yıl reklam filminden (gorseller/5.mp4) ana banner videosu — Alternatif B, video versiyonu.

Filmin yazısız sahneleri art arda kesilir; köşedeki VB / 30 rozeti (sol alt,
y ≥ 945) kadraj dışında kalacak biçimde kırpılır. Ses yok, döngü.

  src/assets/video/b-30yil-1600x900.mp4   masaüstü (16:9)
  src/assets/video/b-30yil-608x1080.mp4   telefon / dikey ekran (9:16, merkez kesim)
  src/assets/img/b/b-30yil-poster-*.jpg   poster (ilk kare)

Sahne sınırları kesme tespitiyle bulundu; her sahnenin başından/sonundan
iki kare pay bırakılır (geçiş karesi görünmesin).
Çalıştırma:  python _build/make_video_30yil.py   (imageio-ffmpeg gerekir)
"""
import os
import subprocess

import imageio_ffmpeg

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'gorseller', 'gorseller', '5.mp4')
VID = os.path.join(ROOT, 'src', 'assets', 'video')
IMG = os.path.join(ROOT, 'src', 'assets', 'img', 'b')
FF = imageio_ffmpeg.get_ffmpeg_exe()

# (başlangıç, bitiş) saniye — yazısız sahneler, film sırasından bağımsız kurgu
SHOTS = [
    (22.40, 23.30),   # VSancaktepe Merkez, drone (sonrası bir sonraki sahneyle bindirmeli)
    (25.52, 26.28),   # Tablo Adalar, havuz ve fıskiyeler
    (13.36, 14.16),   # iki mühendis, yakın
    (14.32, 14.84),   # plan üzerinde eller
    (15.24, 16.00),   # ekip, şantiyede yürüyüş
    (16.16, 17.00),   # iskele
    (20.80, 22.24),   # kıvılcımlar
    (28.88, 29.60),   # gülümseyen çocuk
    (33.60, 35.00),   # ağaç gövdesi
    (37.68, 39.16),   # çimende el sallayan çocuk
]

CROP_D = 'crop=1671:940:124:0,scale=1600:900:flags=lanczos'    # alt 140 px (rozet) dışarıda
CROP_M = 'crop=608:1080:656:0'                                 # merkez dikey; rozet x<280, dışarıda


def build(crop, out, crf):
    parts, labels = [], []
    for i, (a, b) in enumerate(SHOTS):
        parts.append('[0:v]trim=start=%.2f:end=%.2f,setpts=PTS-STARTPTS,%s,setsar=1[v%d]' % (a, b, crop, i))
        labels.append('[v%d]' % i)
    fc = ';'.join(parts) + ';' + ''.join(labels) + 'concat=n=%d:v=1:a=0,fps=25,format=yuv420p[out]' % len(SHOTS)
    cmd = [FF, '-y', '-loglevel', 'error', '-i', SRC, '-filter_complex', fc, '-map', '[out]', '-an',
           '-c:v', 'libx264', '-preset', 'slow', '-crf', str(crf), '-profile:v', 'high',
           '-movflags', '+faststart', out]
    subprocess.run(cmd, check=True)
    print('%-40s %6.0f KB' % (os.path.basename(out), os.path.getsize(out) / 1024))


def poster(video, out):
    subprocess.run([FF, '-y', '-loglevel', 'error', '-i', video, '-frames:v', '1', '-q:v', '3', out], check=True)
    print('%-40s %6.0f KB' % (os.path.basename(out), os.path.getsize(out) / 1024))


if __name__ == '__main__':
    os.makedirs(VID, exist_ok=True)
    d = os.path.join(VID, 'b-30yil-1600x900.mp4')
    m = os.path.join(VID, 'b-30yil-608x1080.mp4')
    build(CROP_D, d, 24)
    build(CROP_M, m, 25)
    poster(d, os.path.join(IMG, 'b-30yil-poster-1600x900.jpg'))
    poster(m, os.path.join(IMG, 'b-30yil-poster-608x1080.jpg'))
