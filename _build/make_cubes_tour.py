# -*- coding: utf-8 -*-
"""Cubes Ankara Sanal Tur görseli — turun örnek daire "salon" panoramasından.

Kaynak: gorseller/indirilen/cubes-sanal-tur/salon-[frblud].jpg (3DVista küp
yüzleri, 2560 px; bkz. KAYNAK.txt). Küpten düz (perspektif) ve geniş bant
için silindirik kadraj üretilir; tur arayüzü görselde yer almaz.

  cubes-sanal-tur-2220x926 / 1110x463   A ve B bandı (masaüstü)
  cubes-sanal-tur-686x926 / 343x463     mobil
  cubes-sanal-tur-a2-3840x1200 / 1920x600   A2 geniş bant
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'gorseller', 'indirilen', 'cubes-sanal-tur')
OUT = os.path.join(ROOT, 'src', 'assets', 'img', 'gyo')
F = {k: np.asarray(Image.open(os.path.join(SRC, 'salon-%s.jpg' % k))) for k in 'frblud'}
N = F['f'].shape[0]


def _sample(out, face, m, u, v):
    px = np.clip(((u + 1) / 2 * (N - 1)).round().astype(int), 0, N - 1)
    py = np.clip(((v + 1) / 2 * (N - 1)).round().astype(int), 0, N - 1)
    out[m] = F[face][py[m], px[m]]


def _project(out, X, Y, Z):
    ax, ay, az = np.abs(X), np.abs(Y), np.abs(Z)
    hz = ay < np.maximum(ax, az)
    _sample(out, 'u', ~hz & (Y > 0), X / ay, Z / ay)
    _sample(out, 'd', ~hz & (Y < 0), X / ay, -Z / ay)
    _sample(out, 'f', hz & (az >= ax) & (Z > 0), X / az, -Y / az)
    _sample(out, 'b', hz & (az >= ax) & (Z < 0), -X / az, -Y / az)
    _sample(out, 'r', hz & (ax > az) & (X > 0), -Z / ax, -Y / ax)
    _sample(out, 'l', hz & (ax > az) & (X < 0), Z / ax, -Y / ax)
    return Image.fromarray(out)


def render(yaw, pitch, hfov, w, h):
    """Düz perspektif."""
    t = np.tan(np.radians(hfov / 2))
    X, Y = np.meshgrid(np.linspace(-t, t, w), np.linspace(t * h / w, -t * h / w, h))
    Z = np.ones_like(X)
    p = np.radians(pitch)
    Y, Z = Y * np.cos(p) + Z * np.sin(p), -Y * np.sin(p) + Z * np.cos(p)
    a = np.radians(yaw)
    X, Z = X * np.cos(a) + Z * np.sin(a), -X * np.sin(a) + Z * np.cos(a)
    return _project(np.zeros((h, w, 3), np.uint8), X, Y, Z)


def render_wide(yaw, pitch, hfov, w, h):
    """Silindirik izdüşüm: geniş kadrajda kenarlar esnemez, dikeyler düz."""
    th = np.radians(np.linspace(-hfov / 2, hfov / 2, w)) + np.radians(yaw)
    vt = (h / w) * np.radians(hfov)
    ys = np.tan(np.linspace(vt / 2, -vt / 2, h))
    TH, Y = np.meshgrid(th, ys)
    X, Z = np.sin(TH), np.cos(TH)
    p = np.radians(pitch)
    Y, Z = Y * np.cos(p) + Z * np.sin(p), -Y * np.sin(p) + Z * np.cos(p)
    return _project(np.zeros((h, w, 3), np.uint8), X, Y, Z)


def save(im, name, q):
    im.save(os.path.join(OUT, name), quality=q, optimize=True, progressive=True)
    print(name, im.size)


def main():
    # Masaüstü bandı: solda tablo/lamba (metin alanı sakin), ortada pencere ve kanepe
    desk = render(-8, -4, 112, 2220, 926)
    save(desk, 'cubes-sanal-tur-2220x926.jpg', 84)
    save(desk.resize((1110, 463), Image.LANCZOS), 'cubes-sanal-tur-1110x463.jpg', 88)
    # Mobil: pencereye bakış
    mob = render(4, -6, 68, 686, 926)
    save(mob, 'cubes-sanal-tur-686x926.jpg', 84)
    save(mob.resize((343, 463), Image.LANCZOS), 'cubes-sanal-tur-343x463.jpg', 88)
    # A2 geniş bant
    wide = render_wide(-6, -4, 140, 3840, 1200)
    save(wide, 'cubes-sanal-tur-a2-3840x1200.jpg', 82)
    save(wide.resize((1920, 600), Image.LANCZOS), 'cubes-sanal-tur-a2-1920x600.jpg', 86)


if __name__ == '__main__':
    main()
