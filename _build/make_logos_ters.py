# -*- coding: utf-8 -*-
"""
Proje logolarının ters (beyaz yazılı) versiyonları — banner görselleri üzerine
yerleştirmek için. Kaynak: gorseller/gorseller/logolar/*.pdf (müşteri).
Yazı rengi beyaz olur; sarı V işareti ve Tablo Adalar'ın ada renkleri korunur.

Çıktı:
  src/assets/img/gyo/logo-<ad>-ters.svg / -renkli.svg   (web'de kullanılabilir vektör)
  gorseller/indirilen/logolar-ters/logo-<ad>-ters.png / -renkli.png  (banner'a
                                     gömmek için; şeffaf, kenara kırpılmış)
Çalıştırma:  python _build/make_logos_ters.py
"""
import os
import re

import fitz
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'gorseller', 'gorseller', 'logolar')
SVG_OUT = os.path.join(ROOT, 'src', 'assets', 'img', 'gyo')
PNG_OUT = os.path.join(ROOT, 'gorseller', 'indirilen', 'logolar-ters')

LOGOS = {
    # ad: (pdf, {eski renk: yeni renk})
    'vsancaktepe': ('SancaktepeMerkezLogo.pdf', {'#3d3d3b': '#ffffff', '#007a40': '#ffffff'}),
    'vyenikonak': ('VB_YeniKonak_Logo.pdf', {'#353939': '#ffffff'}),
    'tablo-adalar': ('tablo_adalar_logo.pdf', {'#222e44': '#ffffff'}),
}


def main():
    from playwright.sync_api import sync_playwright
    os.makedirs(PNG_OUT, exist_ok=True)
    with sync_playwright() as p:
        br = p.chromium.launch(channel='chrome')
        jobs = [(n, pdf, swap, 'ters') for n, (pdf, swap) in LOGOS.items()]
        jobs += [(n, pdf, {}, 'renkli') for n, (pdf, swap) in LOGOS.items()]
        for name, pdf, swap, kind in jobs:
            page = fitz.open(os.path.join(SRC, pdf))[0]
            svg = page.get_svg_image(text_as_path=True)
            for a, b in swap.items():
                svg = svg.replace('"%s"' % a, '"%s"' % b)
            svg_path = os.path.join(SVG_OUT, 'logo-%s-%s.svg' % (name, kind))
            open(svg_path, 'w', encoding='utf-8').write(svg)
            # 4x raster, şeffaf zemin, kenara kırp
            w, h = page.rect.width * 4, page.rect.height * 4
            pg = br.new_page(viewport={'width': int(w), 'height': int(h)})
            body = svg[svg.index('<svg'):]
            pg.set_content('<html><head><style>html,body{margin:0;background:transparent}'
                           'svg{display:block;width:%dpx;height:%dpx}</style></head><body>%s</body></html>'
                           % (w, h, body))
            tmp = os.path.join(PNG_OUT, '_tmp.png')
            pg.screenshot(path=tmp, omit_background=True)
            pg.close()
            im = Image.open(tmp).convert('RGBA')
            os.remove(tmp)
            bb = im.getbbox()
            im = im.crop(bb)
            # SVG'yi de logonun kendi sınırına kırp (PDF sayfası geniş boşluk içeriyor)
            x0, y0, x1, y1 = (v / 4.0 for v in bb)
            pad = 0.5
            vb = '%.2f %.2f %.2f %.2f' % (x0 - pad, y0 - pad, x1 - x0 + 2 * pad, y1 - y0 + 2 * pad)
            head, rest = svg[svg.index('<svg'):].split('>', 1)
            head = re.sub(r'\swidth="[^"]*"', '', head)
            head = re.sub(r'\sheight="[^"]*"', '', head)
            head = re.sub(r'\sviewBox="[^"]*"', '', head)
            head += ' width="%.0f" height="%.0f" viewBox="%s"' % (x1 - x0 + 2 * pad, y1 - y0 + 2 * pad, vb)
            open(svg_path, 'w', encoding='utf-8').write(head + '>' + rest)
            png = os.path.join(PNG_OUT, 'logo-%s-%s.png' % (name, kind))
            im.save(png)
            print('   %-14s %s  %dx%d' % (name, os.path.basename(svg_path), im.width, im.height))
        br.close()


if __name__ == '__main__':
    main()
