"""Alt A2 blok görselleri — A'daki kaynaklardan, esnetilmiş bileşen ölçülerine.

Kural: kaynak çözünürlüğünün üstüne büyütme yok (1x yoğunlukta en az 1,0).
Kaynağı küçük olanlarda (VSancaktepe "Proje Hakkında" görselleri 1200x800)
A2 kadrajı kaynağın kendi boyunda üretilir.

    one-cikan-a2-1536x1024.jpg      öne çıkan proje (ekran kenarına taşan sütun)
    surdurulebilirlik-a2-1200x650   sürdürülebilirlik bandının sağ yarısı
    proje-<ad>-a2-720x540.jpg       proje kartları (4:3, A'da 1,73)
    30-yil-a2-1920x560 / 3840x1120  tam genişlik 30. yıl bandı
    vs-sanal-tur-a2-1920x600 / 3840x1200  tam genişlik sanal tur bandı
    vs-a2-<slayt>-d / -m            VSancaktepe sayfası banner'ı (720 / 440 px)

Çalıştırma:  python _build/make_images_a2.py
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_images as m  # noqa: E402
import make_images_pages as mp  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
DL = os.path.join(m.ROOT, 'gorseller', 'indirilen')


def save(im, name, q=84):
    m.save(m.sharpen(im) if im.width <= 2000 else im, name, q)


def smooth(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * (3 - 2 * t)


def band_30(src, w, h, photo=0.60, anchor=(0.5, 0.55)):
    """Tam genişlik koyu bant: fotoğraf sağda (genişliğin `photo` oranı), solu
    fotoğrafın kendi sol kenar tonundan koyulaşan zemin; geçiş şeffaf rampa."""
    pw = round(w * photo)
    ph = m.cover(src, pw, h, anchor)
    a = np.asarray(ph, dtype=np.float32)
    # sol zemin: kenar şeridinin parlaklığı (renksiz, koyulaştırılmış) — ışık
    # lekeleri taşınmasın diye renk alınmaz; uzaklaştıkça tek koyu tona iner
    lum = a[:, : max(4, pw // 40)].mean((1, 2))
    lum = np.convolve(np.pad(lum, h // 8, mode='edge'), np.ones(h // 4 + 1) / (h // 4 + 1), 'same')[h // 8: h // 8 + h]
    tone = np.array([0.92, 0.95, 1.12], np.float32)               # hafif lacivert (gece fotoğrafı)
    edge = (lum[:, None] * 0.35)[:, None, :] * tone[None, None, :]
    xs = np.arange(w, dtype=np.float32)
    x0 = w - pw
    dark = smooth((x0 - xs) / (w * 0.30))[None, :, None]
    base = edge * (1 - dark) + np.array([8, 9, 14], np.float32) * dark
    base = np.broadcast_to(base, (h, w, 3)).copy()
    layer = base.copy()
    layer[:, x0:] = a
    k = smooth((xs - x0) / (w * 0.12))[None, :, None]
    out = base * (1 - k) + layer * k
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def tour_wide(w, h, yaw, pitch, hfov):
    """Silindirik izdüşüm: geniş kadrajda kenarlar esnemez, dikeyler düz."""
    import make_vs_tour as t
    th = np.radians(np.linspace(-hfov / 2, hfov / 2, w)) + np.radians(yaw)
    vt = np.tan(np.radians(hfov / 2)) * 0 + (h / w) * np.radians(hfov)   # dikey açıklık (radyan)
    ys = np.tan(np.linspace(vt / 2, -vt / 2, h))
    TH, Y = np.meshgrid(th, ys)
    X, Z = np.sin(TH), np.cos(TH)
    p = np.radians(pitch)
    Y, Z = Y * np.cos(p) + Z * np.sin(p), -Y * np.sin(p) + Z * np.cos(p)
    out = np.zeros((h, w, 3), np.uint8)
    ax, ay, az = np.abs(X), np.abs(Y), np.abs(Z)
    hz = ay < np.maximum(ax, az)
    s = t._sample
    s(out, 'u', ~hz & (Y > 0), X / ay, Z / ay)
    s(out, 'd', ~hz & (Y < 0), X / ay, -Z / ay)
    s(out, 'f', hz & (az >= ax) & (Z > 0), X / az, -Y / az)
    s(out, 'b', hz & (az >= ax) & (Z < 0), -X / az, -Y / az)
    s(out, 'r', hz & (ax > az) & (X > 0), -Z / ax, -Y / ax)
    s(out, 'l', hz & (ax > az) & (X < 0), Z / ax, -Y / ax)
    return Image.fromarray(out)


def main():
    yasam = m.mat('3', 'web görsel.jpg')
    hava = m.mat('Sancaktepe_merkez', 'Proje Hakkında', '08.jpg')
    sokak = m.mat('Sancaktepe_merkez', 'Proje Hakkında', '05.jpg')
    vyk = m.mat('10.jpeg')
    tablo = Image.open(os.path.join(DL, 'tablo-genel-gorunum.png')).convert('RGB')
    cubes = m.mat('12', 'CUBES.jpg')
    ifm = m.mat('IFM', 'C1.jpg')
    sun = m.mat('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg')

    print('\n[A2] öne çıkan, sürdürülebilirlik, proje kartları')
    save(yasam, 'one-cikan-a2-1536x1024.jpg')   # tam kare: 1,2–1,6 oranlarda az kırpılır
    save(m.cover(hava, 1200, 650, (0.62, 0.55)), 'surdurulebilirlik-a2-1200x650.jpg', 86)
    for name, im, anc in [('vsancaktepe-merkez', sokak, (0.5, 0.55)),
                          ('vyenikonak', vyk, (0.5, 0.42)),
                          ('tablo-adalar', tablo, (0.45, 0.5)),
                          ('cubes-ankara', cubes, (0.40, 0.5))]:
        save(m.cover(im, 720, 540, anc), 'proje-%s-a2-720x540.jpg' % name)

    print('\n[A2] 30. yıl bandı (tam genişlik)')
    big = band_30(ifm, 3840, 1120)
    save(big, '30-yil-a2-3840x1120.jpg', 80)
    save(big.resize((1920, 560), Image.LANCZOS), '30-yil-a2-1920x560.jpg', 86)

    print('\n[A2] sanal tur bandı (tam genişlik, silindirik)')
    tw = tour_wide(3840, 1200, 10, -4, 185)
    save(tw, 'vs-sanal-tur-a2-3840x1200.jpg', 80)
    save(tw.resize((1920, 600), Image.LANCZOS), 'vs-sanal-tur-a2-1920x600.jpg', 86)

    print('\n[A2] VSancaktepe sayfa banner\'ı')
    save(m.cover(sun, 2880, 1440, (0.5, 0.5)), 'vs-a2-vsancaktepe-d.jpg', 80)
    save(m.cover(sun, 1600, 1200, (0.62, 0.5)), 'vs-a2-vsancaktepe-m.jpg', 82)
    for name, src, anc, phone_x in mp.VS_SLIDES:
        im = mp.vs(*src)
        save(m.cover(im, 1200, 600, anc), 'vs-a2-%s-d.jpg' % name, 88)
        save(m.cover(im, 1067, 800, (phone_x, anc[1])), 'vs-a2-%s-m.jpg' % name, 88)


if __name__ == '__main__':
    main()
