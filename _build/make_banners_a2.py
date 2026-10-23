"""Alt A2 ana sayfa banner görselleri — A ile aynı yöntem, daha yüksek bant.

A2'de banner masaüstünde 720 px, tablette 600 px, telefonda 440 px (A ve
kurumsal: 519 / 240). Kadraj kuralları make_banners_a.py ile aynı: proje
bütün ve büyük, metin kutusunun altında odak görsel yok, panel görselin kendi
gök tonundan, geçişler şeffaflık rampasıyla. Yükseklik arttığı için
kaynaklardan daha çok gökyüzü / zemin alınır (VS ve VYK'de üst pay geri
geldi); VYK'de Saat Kulesi yine kadraj dışında.

Derecelendirme görseli 1080 px; A2'de büyütülmez. Rakamlar A'daki ölçekte
kalır, bant görselin kendi üst/alt tonundan uzatılır (pad_top, aynalama yok).

Dosyalar (CSS px x2):
    ≥1700      banner-<ad>-a2-d.jpg   yükseklik 1440, konteynere bağlı (K=720)
    1200–1699  banner-<ad>-a2-o.jpg   yükseklik 1440, konteynere bağlı (K=290)
    768–1199   banner-<ad>-a2-t.jpg   1200 yükseklik, sağa yaslı
    ≤767       banner-<ad>-a2-m.jpg   880 yükseklik, sağa yaslı
    banner-colors-a2.json             slayt zemini (gök tonu)

Çalıştırma:  python _build/make_banners_a2.py
"""
import json
import math
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_banners_a as A  # noqa: E402
from make_banners_a import compose, put_logo, pad_top, crop, save, GAP, K_DESK, K_MID  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
OUT = A.OUT
DL = A.DL
H_DESK, H_TAB, H_MOB = 1440, 1200, 880
W_TAB, W_MOB = 2600, 1600


def pad_bottom(im, frac):
    flip = Image.Image.transpose
    return flip(pad_top(flip(im, Image.FLIP_TOP_BOTTOM), frac), Image.FLIP_TOP_BOTTOM)


def _canvas(photo, ch, sx, spec, min_w):
    """Kanvas genişliği: en az min_w; görsel + sağ ayna payı + rampa sığsın."""
    w = photo.width * ch / photo.height
    r = spec.get('right') or {}
    need = sx - spec.get('subject', 0.0) * w + w * (1 + r.get('mirror', 0.0) + 0.02)
    return max(min_w, 2 * math.ceil(need / 2))


def build(name, tx, desk, dspec, main, mspec, mid_gap=GAP, logo=None, logo_kind='ters'):
    logo = logo or {}
    sx = 2 * (K_DESK + tx + GAP)
    cw = _canvas(desk, H_DESK, sx, dspec, 5200)
    big, sky = compose(desk, cw, H_DESK, sx=sx, **dspec)
    big = put_logo(big, name, logo.get('desk'), logo_kind)
    save(big, 'banner-%s-a2-d.jpg' % name, 78)
    sx = 2 * (K_MID + tx + mid_gap)
    cw = _canvas(main, H_DESK, sx, mspec, 3500)
    mid, _ = compose(main, cw, H_DESK, sx=sx, **mspec)
    mid = put_logo(mid, name, logo.get('mid'), logo_kind)
    save(mid, 'banner-%s-a2-o.jpg' % name, 78)
    tspec = dict(mspec, right=None)
    tab, _ = compose(main, W_TAB, H_TAB, **tspec)
    save(tab, 'banner-%s-a2-t.jpg' % name, 80)
    mob, _ = compose(main, W_MOB, H_MOB, **tspec)
    save(mob, 'banner-%s-a2-m.jpg' % name, 80)
    print('   %s: masaüstü %dx%d, ara %dx%d, gök #%02x%02x%02x'
          % (name, big.width, big.height, mid.width, mid.height, *sky))
    return '#%02x%02x%02x' % sky


def main():
    m = A.m
    colors = {}

    print('\n[A2] VSancaktepe Merkez')
    sun = m.mat('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg')
    # A'ya göre üstte daha çok gökyüzü (0.02), altta yol payı korunur
    vsz = [(0.0, 0.33, 0.35), (0.33, 0.80, 0.07), (0.80, 1.0, 0.22)]
    # 720 px bantta tüm proje 1920 ekranda metnin sağına sığmıyor: kesim sol
    # bloğun sağ kısmından (x 0.33) başlar ve fotoğraf metnin hemen sağına oturur.
    # Geçiş her satırda aynı uzunlukta şeffaf rampa (fotoğraf genişliğinin %22'si):
    # sol blok zemine karışır, orta ve sağ blok net. Panel: gök satırları
    # fotoğraftan, ufkun altı fotoğrafın zemin tonuna iner (ground).
    vmain = crop(sun, 0.33, 0.97, 0.02, 0.92)
    vspec = dict(subject=0.0, clean=((0.0, 0.34),), ground=0.8, fade=0.3,
                 left=dict(mirror=0.0, zones=[(0.0, 1.0, 0.22)]),
                 right=dict(mirror=0.0, zones=[(0.0, 1.0, 0.25)]))
    colors['vsancaktepe'] = build(
        'vsancaktepe', 508, vmain, vspec, vmain, vspec,
        logo=dict(desk=(0.03, 0.07, 0.10), mid=(0.03, 0.07, 0.10)))

    print('\n[A2] VYeniKonak (katalog render: iki kule)')
    vyk = Image.open(os.path.join(DL, 'vyk-katalog', 'vyk-saat-kulesi-kuleler-3548x1777.png')).convert('RGB')
    # A: y 0.27–0.99; A2: kulelerin üstünde daha çok gökyüzü (0.12)
    kule = crop(vyk, 0.50, 1.0, 0.12, 0.99)
    kspec = dict(subject=0.20, clean=((0.0, 0.69),),
                 left=dict(mirror=0.10, zones=[(0.0, 0.10, 0.35), (0.10, 0.86, 0.30), (0.86, 1.0, 0.30)]),
                 right=dict(mirror=0.10, zones=[(0.0, 1.0, 0.40)]))
    colors['vyenikonak'] = build('vyenikonak', 449, kule, kspec, kule, kspec,
                                 logo=dict(desk=(0.66, 0.20, 0.10), mid=(0.66, 0.20, 0.10)))

    print('\n[A2] Tablo Adalar (broşür genel görünüm)')
    tablo = Image.open(os.path.join(DL, 'tablo-genel-gorunum.png')).convert('RGB')
    colors['tablo-adalar'] = build(
        'tablo-adalar', 422,
        crop(tablo, 0.0, 1.0, 0.0, 0.97),
        dict(subject=0.15, clean=((0.0, 0.60),),
             left=dict(mirror=0.10, zones=[(0.0, 0.05, 0.35), (0.05, 1.0, 0.25)]),
             right=dict(mirror=0.08, zones=[(0.0, 0.33, 0.35), (0.33, 0.86, 0.20), (0.86, 1.0, 0.30)])),
        crop(tablo, 0.08, 0.92, 0.0, 0.97),
        dict(subject=0.083, clean=((0.0, 0.60),),
             left=dict(mirror=0.08, zones=[(0.0, 0.05, 0.30), (0.05, 1.0, 0.16)]),
             right=dict(mirror=0.05, zones=[(0.0, 0.33, 0.30), (0.33, 0.86, 0.10), (0.86, 1.0, 0.20)])),
        logo=dict(desk=(0.52, 0.13, 0.12), mid=(0.52, 0.13, 0.11)), logo_kind='renkli')

    print('\n[A2] Kurumsal Yönetim Derecelendirme (haber görseli, 9,48)')
    der = m.mat('3', 'DERECELENDİRME (1).jpg')
    # A'daki kesim ve ölçek (kaynak 1,49x); bant 1440'a üst ve alttan kendi
    # tonuyla uzar: rakamlar dikeyde ortada, büyütme A'dakinden fazla değil.
    extra = (1440 / 1040 - 1) / 2
    mbase = pad_top(crop(der, 0.0, 0.66, 0.53, 1.0), 0.13 / 0.47)
    mid = pad_bottom(pad_top(mbase, extra), extra / (1 + extra))
    # masaüstünde de ara kesim: defne dalı 1920 ekranın kenarında kesik kalıyordu
    dspec = dict(subject=0.12, clean=((0.0, 0.62), (0.84, 1.0)), strip=0.04,
                 left=dict(mirror=0.0, zones=[(0.0, 0.32, 0.35), (0.32, 0.62, 0.10), (0.62, 1.0, 0.32)]),
                 right=dict(mirror=0.0, zones=[(0.0, 0.32, 0.30), (0.32, 0.62, 0.04), (0.62, 1.0, 0.15)]))
    colors['derecelendirme'] = build('derecelendirme', 700, mid, dspec, mid, dspec,
        mid_gap=12)

    with open(os.path.join(OUT, 'banner-colors-a2.json'), 'w', encoding='utf-8') as f:
        json.dump(colors, f, indent=1)
    print('\n   banner-colors-a2.json:', colors)


if __name__ == '__main__':
    main()
