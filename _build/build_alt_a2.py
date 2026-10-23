# -*- coding: utf-8 -*-
"""Vakıf GYO — Alternatif A2 sayfa üreteci.

A ile aynı içerik ve kurumsal bileşenler; bileşenler esnetilir: daha yüksek
ana banner (make_banners_a2.py), tam genişlik bantlar, Vakıf GYO yeşili
(#007a40) üçüncü renk olarak ölçülü. Farklar 06-a2.css ve A2 kadrajlarında;
markup A ile aynı üreteçlerden gelir (GYO_VARIANT=a2).

Çalıştırma:  python _build/build_alt_a2.py
Çıktı:       src/alt-a2/*.html
"""
import os
import sys

os.environ['GYO_VARIANT'] = 'a2'
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import re  # noqa: E402

import build_alt_a as b  # noqa: E402
import build_alt_a_pages as pages  # noqa: E402

G = '../assets/img/gyo/'
# A görseli → A2 kadrajı (make_images_a2.py). Tam genişlik bantlar ve büyüyen
# bloklar için; mobil kadrajlar A ile aynı kalır.
SWAP = [
    (G + '30-yil-1110x463.jpg 1x, ' + G + '30-yil-2220x926.jpg 2x',
     G + '30-yil-a2-1920x560.jpg 1x, ' + G + '30-yil-a2-3840x1120.jpg 2x'),
    (G + '30-yil-1110x463.jpg"', G + '30-yil-a2-1920x560.jpg"'),
    (G + 'vs-sanal-tur-1110x463.jpg 1x, ' + G + 'vs-sanal-tur-2220x926.jpg 2x',
     G + 'vs-sanal-tur-a2-1920x600.jpg 1x, ' + G + 'vs-sanal-tur-a2-3840x1200.jpg 2x'),
    (G + 'vs-sanal-tur-1110x463.jpg"', G + 'vs-sanal-tur-a2-1920x600.jpg"'),
    (G + 'cubes-sanal-tur-1110x463.jpg 1x, ' + G + 'cubes-sanal-tur-2220x926.jpg 2x',
     G + 'cubes-sanal-tur-a2-1920x600.jpg 1x, ' + G + 'cubes-sanal-tur-a2-3840x1200.jpg 2x'),
    (G + 'cubes-sanal-tur-1110x463.jpg"', G + 'cubes-sanal-tur-a2-1920x600.jpg"'),
    ('one-cikan-yasam-basliyor-1078x944.jpg', 'one-cikan-a2-1536x1024.jpg'),
    ('width="539" height="472"', 'width="768" height="512"'),
    ('surdurulebilirlik-2280x926.jpg', 'surdurulebilirlik-a2-1200x650.jpg'),
    # mobil: A'daki üstten beyaza açılan kadraj yerine aynı A2 görseli (bant zemini yeşil)
    ('surdurulebilirlik-750x870.jpg', 'surdurulebilirlik-a2-1200x650.jpg'),
    ('width="355" height="205" class="img-fluid"', 'width="360" height="270" class="img-fluid"'),
]
RE_SWAP = [
    (r'(proje-[a-z-]+)-710x410\.jpg', r'\1-a2-720x540.jpg'),
    (r'banner-vsancaktepe-(?:3024x1040|2400x828)\.jpg', 'vs-a2-vsancaktepe-d.jpg'),
    (r'banner-vsancaktepe-(?:1536x480|828x480)\.jpg', 'vs-a2-vsancaktepe-m.jpg'),
    (r'vs-banner-(dogallik|uyum)-1512x520\.jpg', r'vs-a2-\1-d.jpg'),
    (r'vs-banner-(dogallik|uyum)-(?:1536x480|828x480)\.jpg', r'vs-a2-\1-m.jpg'),
    (r'banner-cubes-(?:3024x1040|2400x828)\.jpg', 'cubes-a2-havasi-d.jpg'),
    (r'banner-cubes-(?:1536x480|828x480)\.jpg', 'cubes-a2-havasi-m.jpg'),
    (r'cubes-banner-(yasam|calisma)-1512x520\.jpg', r'cubes-a2-\1-d.jpg'),
    (r'cubes-banner-(yasam|calisma)-(?:1536x480|828x480)\.jpg', r'cubes-a2-\1-m.jpg'),
]


def a2_filter(html):
    for old, new in SWAP:
        html = html.replace(old, new)
    for pat, rep in RE_SWAP:
        html = re.sub(pat, rep, html)
    return html


b.PAGE_FILTER = a2_filter

if __name__ == '__main__':
    b.main()
    pages.main()
