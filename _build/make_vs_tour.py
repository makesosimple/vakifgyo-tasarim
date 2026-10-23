"""VSancaktepe Sanal Tur görseli — turun kendi "Salon" panoramasından.

Kaynak: gorseller/indirilen/vs-sanal-tur/salon-[frblud].jpg (3DVista küp
yüzleri, 4608 px; bkz. KAYNAK.txt). Küpten düz perspektif kadraj üretilir;
tur arayüzü (menü, yön işaretleri) görselde yer almaz.
"""
import os
import numpy as np
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'gorseller', 'indirilen', 'vs-sanal-tur')
OUT = os.path.join(ROOT, 'src', 'assets', 'img', 'gyo')
F = {k: np.asarray(Image.open(os.path.join(SRC, 'salon-%s.jpg' % k))) for k in 'frblud'}
N = F['f'].shape[0]


def _sample(out, face, m, u, v):
    px = np.clip(((u + 1) / 2 * (N - 1)).round().astype(int), 0, N - 1)
    py = np.clip(((v + 1) / 2 * (N - 1)).round().astype(int), 0, N - 1)
    out[m] = F[face][py[m], px[m]]


def render(yaw, pitch, hfov, w, h):
    t = np.tan(np.radians(hfov / 2))
    X, Y = np.meshgrid(np.linspace(-t, t, w), np.linspace(t * h / w, -t * h / w, h))
    Z = np.ones_like(X)
    p = np.radians(pitch)
    Y, Z = Y * np.cos(p) + Z * np.sin(p), -Y * np.sin(p) + Z * np.cos(p)
    a = np.radians(yaw)
    X, Z = X * np.cos(a) + Z * np.sin(a), -X * np.sin(a) + Z * np.cos(a)
    out = np.zeros((h, w, 3), np.uint8)
    ax, ay, az = np.abs(X), np.abs(Y), np.abs(Z)
    hz = ay < np.maximum(ax, az)
    _sample(out, 'u', ~hz & (Y > 0), X / ay, Z / ay)
    _sample(out, 'd', ~hz & (Y < 0), X / ay, -Z / ay)
    _sample(out, 'f', hz & (az >= ax) & (Z > 0), X / az, -Y / az)
    _sample(out, 'b', hz & (az >= ax) & (Z < 0), -X / az, -Y / az)
    _sample(out, 'r', hz & (ax > az) & (X > 0), -Z / ax, -Y / ax)
    _sample(out, 'l', hz & (ax > az) & (X < 0), Z / ax, -Y / ax)
    return Image.fromarray(out)


def save(im, name, q):
    im.save(os.path.join(OUT, name), quality=q, optimize=True, progressive=True)
    print(name, im.size)


def main():
    # Masaüstü (.private-banking 1110x463): sol taraf duvar/perde — metin alanı sakin
    desk = render(22, -6, 118, 2220, 926)
    save(desk, 'vs-sanal-tur-2220x926.jpg', 84)
    save(desk.resize((1110, 463), Image.LANCZOS), 'vs-sanal-tur-1110x463.jpg', 88)
    # Mobil (343x463): salon boyunca bakış
    mob = render(45, -8, 72, 686, 926)
    save(mob, 'vs-sanal-tur-686x926.jpg', 84)
    save(mob.resize((343, 463), Image.LANCZOS), 'vs-sanal-tur-343x463.jpg', 88)


if __name__ == '__main__':
    main()
