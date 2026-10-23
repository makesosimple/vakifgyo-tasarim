# -*- coding: utf-8 -*-
"""
Cubes Ankara landing görselleri — tüm konseptler (A, A2, B, B-üst).

Kaynaklar:
  gorseller/12/CUBES.jpg                       kule render'ı (3924 px) — A/A2 banner'ı, film posteri
  gorseller/indirilen/cubes-katalog/           broşür render'ları (katalog PDF'inden), kampanya görseli
  gorseller/cubes proje web site/ + indirilen/cubes-planlar/   20 daire planı (1200 px PNG)
  gorseller/logolar/cubes_ankara_logo.png      logo (cubes-logo.png / cubes-logo-ters.png)

B'nin tam ekran kule görseli (img/b/cubes-*.jpg) make_images_b.py'den gelir.
Çalıştırma:  python _build/make_images_cubes.py
Çıktı:       src/assets/img/gyo/
"""
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_images as m  # noqa: E402
import cubes_data as cd  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
IND = os.path.join(m.ROOT, 'gorseller', 'indirilen')
KAT = os.path.join(IND, 'cubes-katalog')
PLAN_DIRS = [os.path.join(m.MAT, 'cubes proje web site'), os.path.join(IND, 'cubes-planlar')]

GALLERY_SRC = {'kuleler': 'img-p06-263.jpeg', 'sky-cube': 'img-p07-267.jpeg', 'havuz': 'img-p13-237.jpeg',
               'parkur': 'img-p12-234.jpeg', 'avlu': 'img-p14-240.jpeg', 'teras': 'img-p23-54.jpeg',
               'lobi': 'img-p24-60.jpeg', 'ofis-cephe': 'img-p19-200.jpeg'}


def kat(name):
    return Image.open(os.path.join(KAT, name)).convert('RGB')


def extend_sides(im, w, h, fx=0.5):
    """Dikey özneli görseli geniş banda yerleştirir: görsel yüksekliğe
    ölçeklenir, iki yan görselin satır ortalamasından türeyen pürüzsüz
    gök/zemin geçişiyle dolar (kuleler kırpılmaz, şerit/çizgi yok)."""
    s = h / im.height
    im = im.resize((round(im.width * s), h), Image.LANCZOS)
    if im.width >= w:
        return m.cover(im, w, h, (fx, 0.5))
    x = round((w - im.width) * fx)
    a = np.asarray(im, dtype=np.float32)
    rows = a.mean(axis=1)                                   # (h, 3) satır ortalaması
    k = max(3, h // 12)
    ker = np.ones(k) / k
    rows = np.stack([np.convolve(np.pad(rows[:, c], (k // 2, k - 1 - k // 2), mode='edge'), ker, mode='valid')
                     for c in range(3)], axis=1)
    canvas = Image.fromarray(np.clip(np.broadcast_to(rows[:, None, :], (h, w, 3)), 0, 255).astype(np.uint8))
    fade = round(im.width * 0.22)
    ramp = [min(255, round(i * 255 / fade)) for i in range(im.width)]
    ramp = [min(p, q) for p, q in zip(ramp, ramp[::-1])]
    mask = Image.frombytes('L', (im.width, 1), bytes(ramp)).resize((im.width, h))
    canvas.paste(im, (x, 0), mask)
    return canvas


def build_banners():
    print('\n[A] banner — kuleler, Yeni Yaşam Tarzı (havuz), Yeni Çalışma Alanı (ofis)')
    towers = m.mat('12', 'CUBES.jpg')
    pool = kat('img-p13-237.jpeg')
    office = kat('img-p19-200.jpeg')
    for key, w, h in m.BANNER_SIZES + [('1536x480', 1536, 480)]:
        m.save(m.sharpen(extend_sides(towers, w, h, 0.5)), 'banner-cubes-%s.jpg' % key)
    m.save(m.sharpen(m.cover(towers, 828, 480, (0.58, 0.45))), 'banner-cubes-828x480.jpg')
    for name, src, anc, phone_x in (('yasam', pool, (0.5, 0.5), 0.6), ('calisma', office, (0.5, 0.45), 0.55)):
        m.save(m.sharpen(m.cover(src, 1512, 520, anc)), 'cubes-banner-%s-1512x520.jpg' % name)
        m.save(m.sharpen(m.cover(src, 1536, 480, anc)), 'cubes-banner-%s-1536x480.jpg' % name)
        m.save(m.sharpen(m.cover(src, 828, 480, (phone_x, anc[1]))), 'cubes-banner-%s-828x480.jpg' % name)
    print('\n[A2] banner')
    m.save(extend_sides(towers, 2880, 1440, 0.5), 'cubes-a2-havasi-d.jpg', 80)
    m.save(m.cover(towers, 1600, 1200, (0.55, 0.45)), 'cubes-a2-havasi-m.jpg', 82)
    for name, src, anc, phone_x in (('yasam', pool, (0.5, 0.5), 0.6), ('calisma', office, (0.5, 0.45), 0.55)):
        m.save(m.cover(src, 1200, 600, anc), 'cubes-a2-%s-d.jpg' % name, 88)
        m.save(m.cover(src, 1067, 800, (phone_x, anc[1])), 'cubes-a2-%s-m.jpg' % name, 88)


def plan_1200(path, w=1200, pad=0.02):
    """Saydam zeminli plan PNG'si: boş kenarlar kırpılır, beyaz zemin, kendi oranında."""
    im = Image.open(path).convert('RGBA')
    a = np.asarray(im)[..., 3]
    ys, xs = np.where(a > 8)
    x0, y0, x1, y1 = max(xs.min() - 12, 0), max(ys.min() - 12, 0), min(xs.max() + 13, im.width), min(ys.max() + 13, im.height)
    im = im.crop((x0, y0, x1, y1))
    h = round(w * im.height / im.width)
    bw, bh = round(w * (1 - 2 * pad)), round(h * (1 - 2 * pad))
    s = min(bw / im.width, bh / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    canvas.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas.convert('RGB')


def build_plans():
    print('\n[planlar] 20 daire tipi')
    for key, name in zip(cd.PLAN_KEYS, cd.PLAN_IMAGES):
        for d in PLAN_DIRS:
            p = os.path.join(d, name + '.png')
            if os.path.exists(p):
                m.save(m.sharpen(plan_1200(p)), 'cubes-plan-%s-1200.jpg' % key, 88)
                break
        else:
            raise SystemExit('plan yok: ' + name)


def build_gallery():
    print('\n[galeri] katalog render\'ları')
    for i, (key, _alt) in enumerate(cd.GALLERY, 1):
        im = kat(GALLERY_SRC[key])
        m.save(m.sharpen(m.cover(im, 1200, 800)), 'cubes-galeri-%d-1200x800.jpg' % i)
        m.save(m.sharpen(m.cover(im, 960, 640)), 'cubes-galeri-%d-960x640.jpg' % i)


def build_misc():
    print('\n[diğer] bloklar, kampanya, film posteri')
    import fitz
    doc = fitz.open(os.path.join(IND, 'cubes-katalog', 'cubes.catalog.pdf')) if os.path.exists(
        os.path.join(IND, 'cubes-katalog', 'cubes.catalog.pdf')) else None
    if doc:
        pg = doc[4]   # A Blok Rezidans / B Blok Ofis şeması
        pm = pg.get_pixmap(matrix=fitz.Matrix(1600 / pg.rect.width, 1600 / pg.rect.width))
        im = Image.frombytes('RGB', (pm.width, pm.height), pm.samples)
        m.save(m.cover(im, 1600, 800), 'cubes-bloklar-1600x800.jpg', 86)
    else:
        print('   katalog PDF yok (gorseller/indirilen/cubes-katalog/cubes.catalog.pdf); bloklar atlandı')
    # Kampanya bandı: ofis bloğu render'ı (kampanya ofis/home ofis için); sitedeki kampanya görseli yazılı kompozit
    m.save(m.sharpen(m.cover(kat('img-p19-200.jpeg'), 1078, 944, (0.42, 0.5))), 'cubes-kampanya-1078x944.jpg')
    m.save(m.sharpen(m.cover(kat('img-p06-263.jpeg'), 1280, 720, (0.5, 0.5))), 'cubes-film-1280x720.jpg')


if __name__ == '__main__':
    build_banners()
    build_plans()
    build_gallery()
    build_misc()
