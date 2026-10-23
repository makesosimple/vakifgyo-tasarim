# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif B görselleri

B'de görsel tasarımın kendisi: tam ekran slaytlar, tam genişlik bantlar.
Bu yüzden her görsel kaynağın izin verdiği en yüksek çözünürlükte, birden
çok genişlikte (srcset) üretilir; büyütme yapılmaz.

  Yatay  <ad>-<w>.jpg      3:2, genişlikler 3200 / 2400 / 1600 / 1000
  Dikey  <ad>-p-<w>.jpg    3:5, telefon ve dikey tablet için ayrı kesim
  Kart   <ad>-<w>x<h>.jpg  sabit ölçü

Kaynaklar (en yüksek çözünürlüklü render ve fotoğraflar):
  VSancaktepe gün batımı 3000 px · VYeniKonak 5008 px · IFM 2500 px
  Cubes Ankara 3924 px · Bizimtepe Aydos 6720 px · Medyan Kadıköy 5000 px

Çalıştırma:  python _build/make_images_b.py
Çıktı:       src/assets/img/b/
"""
import os
import re
import sys

import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_images as m  # noqa: E402
import make_images_pages as mp  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
OUT = os.path.join(m.ROOT, 'src', 'assets', 'img', 'b')
GYO = os.path.join(m.ROOT, 'src', 'assets', 'img', 'gyo')
WIDTHS = (3200, 2400, 1600, 1000)
P_WIDTHS = (1500, 1000, 720)


def save(im, name, q=80):
    path = os.path.join(OUT, name)
    im.convert('RGB').save(path, 'JPEG', quality=q, subsampling=0 if q >= 88 else 2,
                           optimize=True, progressive=True)
    print('   %-38s %4dx%-4d %5.0f KB' % (name, im.width, im.height, os.path.getsize(path) / 1024))


def sharpen(im, k=1.0):
    return im.filter(ImageFilter.UnsharpMask(radius=0.8 * k, percent=40, threshold=2))


def crop_ratio(im, ratio, fx=0.5, fy=0.5):
    """Kaynaktan, büyütmeden, verilen orana en büyük kesim."""
    w, h = im.size
    if w / h > ratio:
        cw, ch = round(h * ratio), h
    else:
        cw, ch = w, round(w / ratio)
    x = min(max(round(w * fx - cw / 2), 0), w - cw)
    y = min(max(round(h * fy - ch / 2), 0), h - ch)
    return im.crop((x, y, x + cw, y + ch))


def ladder(im, name, widths):
    """Kesimi genişlik basamaklarında kaydeder; kaynaktan büyük basamak
    yerine kaynağın kendi genişliği bir kez yazılır. Üretilen genişlikleri döner."""
    out = []
    for w in widths:
        if w > im.width:
            continue
        h = round(w * im.height / im.width)
        save(sharpen(im.resize((w, h), Image.LANCZOS)), '%s-%d.jpg' % (name, w))
        out.append(w)
    if not out or (im.width < widths[0] and im.width - out[0] > 200):
        save(sharpen(im, 0.6), '%s-%d.jpg' % (name, im.width))
        out.insert(0, im.width)
    return out


def hero(im, name, fx=0.5, fy=0.5, pfx=None, pfy=None):
    """Tam ekran görsel: 3:2 yatay + 3:5 dikey kesim."""
    print('\n[%s] kaynak %dx%d' % (name, im.width, im.height))
    land = ladder(crop_ratio(im, 3 / 2, fx, fy), name, WIDTHS)
    port = ladder(crop_ratio(im, 3 / 5, pfx if pfx is not None else fx,
                             pfy if pfy is not None else fy), name + '-p', P_WIDTHS)
    return land, port


def card(im, name, w, h, fx=0.5, fy=0.5, q=82):
    c = crop_ratio(im, w / h, fx, fy)
    if c.width < w:
        w, h = c.width, round(c.width * h / w)
    save(sharpen(c.resize((w, h), Image.LANCZOS)), '%s-%dx%d.jpg' % (name, w, h), q)


def vyk_wide():
    """VYeniKonak kare (5008); kuleler tam boy kalsın diye 3:2'ye kırpmak
    yerine sola gökyüzü tonunda pürüzsüz uzatılır (A'daki geçiş yöntemi)."""
    sq = m.mat('10.jpeg')
    cw, ch = 3200, 2134
    photo = np.asarray(sq.resize((ch, ch), Image.LANCZOS), dtype=np.float32)
    xp = cw - ch
    # Zemin: fotoğrafın sol şeridinin üst ve alt üçte bir tonları arasında
    # iki duraklı dikey geçiş (satır satır uzatma yok → yatay şerit yok)
    prof = photo[:, : round(ch * 0.04)].mean(1)
    mean = prof.mean(0)
    top = (prof[: ch // 3].mean(0) + mean) / 2
    bot = (prof[-ch // 3:].mean(0) + mean) / 2
    t = mp._smooth((np.arange(ch) - ch * 0.25) / (ch * 0.6))[:, None].astype(np.float32)
    col = top * (1 - t) + bot * t
    out = np.broadcast_to(col[:, None, :], (ch, cw, 3)).copy()
    a = mp._smooth(np.arange(ch) / (ch * 0.10)).astype(np.float32)[None, :, None]
    out[:, xp:] = out[:, xp:] * (1 - a) + photo * a
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)), sq


def logos():
    """Koyu menü zemini için ters (beyaz) logolar; sarı işaret korunur."""
    src = open(os.path.join(GYO, 'vakif-gyo-logo.svg'), encoding='utf-8').read()
    inv = src.replace('#231f20', '#ffffff').replace('#007a40', '#ffffff')
    open(os.path.join(OUT, 'vakif-gyo-logo-ters.svg'), 'w', encoding='utf-8').write(inv)
    vs = open(os.path.join(GYO, 'vs-logo.svg'), encoding='utf-8').read()
    vs_inv = vs.replace('#3d3d3b', '#ffffff').replace('#007a40', '#ffffff')
    open(os.path.join(OUT, 'vs-logo-ters.svg'), 'w', encoding='utf-8').write(vs_inv)
    print('   logolar: vakif-gyo-logo-ters.svg, vs-logo-ters.svg')


def main():
    os.makedirs(OUT, exist_ok=True)
    logos()

    # Tam ekran slaytlar ve bantlar
    hero(m.mat('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg'),
         'vsancaktepe', 0.5, 0.5, pfx=0.66)
    ext, sq = vyk_wide()
    print('\n[vyenikonak] uzatılmış %dx%d' % ext.size)
    ladder(ext, 'vyenikonak', WIDTHS)
    ladder(crop_ratio(sq, 3 / 5, 0.42), 'vyenikonak-p', P_WIDTHS)
    hero(m.mat('12', 'CUBES.jpg'), 'cubes', 0.5, 0.42, pfx=0.36)
    hero(m.mat('IFM', 'C1.jpg'), 'ifm', 0.5, 0.5, pfx=0.48)
    hero(m.mat('12', 'TepeAydos21.jpg'), 'aydos', 0.5, 0.5, pfx=0.5)
    hero(m.mat('13', 'TepeAydos12N1.jpg'), 'aydos-ticari', 0.5, 0.55, pfx=0.45)
    hero(m.mat('13', 'medyan kadıköy render.jpg'), 'medyan', 0.5, 0.5, pfx=0.33)
    hero(m.mat('7.jpg'), 'sektor', 0.5, 0.5, pfx=0.62)

    # Dikey görseller (yatırımcı bloğu): IFM kuleleri
    print('\n[ifm-dikey]')
    for f, n in (('D1.jpg', 'ifm-gece'), ('D2.jpg', 'ifm-gunduz')):
        ladder(crop_ratio(m.mat('IFM', f), 4 / 5, 0.5, 0.45), n, (1600, 1100, 720))

    # Proje dizini — 4:5 dikey önizleme
    print('\n[proje dizini]')
    for name, src, fx, fy in [
        ('vsancaktepe', ('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg'), 0.66, 0.5),
        ('vyenikonak', ('10.jpeg',), 0.40, 0.5),
        ('tablo-adalar', ('12', 'TABLO.jpg'), 0.5, 0.5),
        ('cubes', ('12', 'CUBES.jpg'), 0.36, 0.5),
        ('ifm', ('IFM', 'B1.jpg'), 0.55, 0.5),
        ('aydos', ('12', 'TepeAydos21.jpg'), 0.5, 0.5),
    ]:
        card(m.mat(*src), 'dizin-' + name, 1280, 1600, fx, fy)

    # Haber kartları (kaynaklar küçük; kart ölçüsünde)
    print('\n[haberler]')
    card(m.mat('3', 'web görsel.jpg'), 'haber-yasam-basliyor', 1200, 800, 0.5, 0.45)
    card(m.mat('3', 'vyenikonak2 (2).jpg'), 'haber-vyenikonak-lansman', 1200, 800)
    card(m.mat('IFM', 'F1.jpg'), 'haber-derecelendirme', 1200, 800, 0.5, 0.5)
    card(m.mat('23', 'Vakif_GYO_EFQM_Odul_Web_Haber.jpg'), 'haber-efqm', 1200, 800, 0.5, 0.4)
    card(m.mat('3', 'TSRS -WEB-DUYURU.jpg'), 'haber-tsrs', 1200, 800)

    # VSancaktepe galeri — kaynaklar 1200x800, büyütülmeden
    print('\n[vs galeri]')
    for i, f in enumerate(['002.jpg', '004.jpg', '007.jpg', '005.jpg', '006.jpg', '05.jpg',
                           '09.jpg', '08.jpg'], 1):
        save(sharpen(m.mat('Sancaktepe_merkez', 'Proje Hakkında', f), 0.6),
             'vs-galeri-%d-1200x800.jpg' % i, 84)


if __name__ == '__main__':
    main()
