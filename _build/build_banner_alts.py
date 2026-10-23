# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif A · banner seçenekleri karşılaştırma sayfası

Proje görselleri (3:2, kare) geniş banner alanına (1280'de 2,5:1, 1920'de
3,7:1) oturmuyor: kırpılınca bina kesiliyor, uzatılınca ek yeri belli
oluyor. Bu sayfa üç çözümü ana sayfanın dört slaytıyla, gerçek banner
bileşeni üzerinde gösterir:

  0  Şu anki hâl (referans)
  1  Bileşik banner — düz zemin + fotoğraf kendi oranında, kavisli maske
  2  Geniş render talebi — müşteriden istenecek görselin ölçü şeması
  3  Kutulu banner — container genişliğinde, köşeli kutu, oran sabit

Çalıştırma:  python _build/make_images_pages.py banner
             python _build/build_banner_alts.py
Çıktı:       src/alt-a/banner-alternatifleri.html
"""
import os
import re
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_alt_a as b  # noqa: E402

IMG = b.IMG
IMG_DIR = os.path.join(b.ROOT, 'src', 'assets', 'img', 'gyo')

# Ana sayfa slaytları: ad, satırlar, CTA, alt metin
SLIDES = [(s[0].split('-3024')[0].split('-1791')[0].split('-1512')[0].replace('banner-', ''),) + s
          for s in b.BANNER_SLIDES]


def bg_color(name):
    """Seçenek 1 zemini: fotoğrafın sol kenar şeridinin üst yarısının ortalaması."""
    im = Image.open(os.path.join(IMG_DIR, 'bk-%s-h1040.jpg' % name)).convert('RGB')
    w, h = im.size
    r, g, bl = im.crop((0, 0, max(4, w // 25), h // 2)).resize((1, 1), Image.BOX).getpixel((0, 0))
    lum = (0.2126 * r + 0.7152 * g + 0.0722 * bl) / 255
    return '#%02x%02x%02x' % (r, g, bl), w / h, lum < 0.5


def uniq(html, key):
    """Aynı sayfada birden çok banner: kimlikler çakışmasın."""
    html = html.replace('id="all-campaign-link"', 'id="all-campaign-link-%s"' % key)
    return html.replace('hizli-erisim', 'hizli-erisim-%s' % key)


def current():
    return uniq(b.banner(b.BANNER_SLIDES, label='Şu anki banner'), 'o0')


def logo_variant(key):
    """Seçenek 1: logo kavisli bileşik banner (bl-<key>-*). Masaüstü ve
    tablette aynı 3840 px görsel sağa yaslı; mobilde bugünkü mobil kesimler."""
    slides = []
    for name, big, mid, small, phone, lines, cta, alt, dark in SLIDES:
        _, _, is_dark = bg_color(name)
        f = 'bl-%s-%s-3840x1040.jpg' % (key, name)
        slides.append((f, f, small, phone, lines, cta, alt, is_dark))
    return uniq(b.banner(slides, label='Seçenek 1%s' % key), 'o1' + key)


def boxed():
    slides = [('bx-%s-2220x1038.jpg' % name, 'bx-%s-2220x1038.jpg' % name, small, phone,
               lines, cta, alt, dark)
              for name, big, mid, small, phone, lines, cta, alt, dark in SLIDES]
    return uniq(b.banner(slides, label='Seçenek 3: kutulu banner'), 'o3')


def intro(no, title, text, pros, cons):
    li = lambda xs: ''.join('<li>%s</li>' % x for x in xs)
    return '''<div class="container gyo-bv__intro">
<p class="gyo-eyebrow">%s</p>
<h2 class="gyo-bv__title">%s</h2>
<p class="gyo-bv__text">%s</p>
<div class="gyo-bv__pc">
<div><p class="gyo-bv__pc-head">Artı</p><ul class="list">%s</ul></div>
<div><p class="gyo-bv__pc-head">Eksi</p><ul class="list">%s</ul></div>
</div>
</div>''' % (no, title, text, li(pros), li(cons))


SPEC = '''<div class="container">
<figure class="gyo-spec" aria-labelledby="spec-cap">
<div class="gyo-spec__frame">
<div class="gyo-spec__text"><strong>Yazı alanı</strong><span>Sade gökyüzü ya da zemin; bina, ağaç, logo yok</span></div>
<div class="gyo-spec__subject"><strong>Ana konu</strong><span>Bina tam boy; üstte ve altta en az %8 boşluk</span></div>
<div class="gyo-spec__safe"><span>1280 px ekranda görünen alan (2,5:1)</span></div>
<div class="gyo-spec__mobile"><span>Mobil kesim (828x480): konu sağ yarıda</span></div>
<div class="gyo-spec__size">3840 x 1040 px · 3,7:1</div>
</div>
<figcaption id="spec-cap">Müşteriden istenecek banner görselinin yerleşim şeması. Kesikli alanlar farklı ekranlarda görünen bölümleri gösterir; ana konu her ekranda bu alanların içinde kalmalıdır.</figcaption>
</figure>
<ul class="list gyo-spec__list">
<li><strong>Ölçü:</strong> en az 3840x1040 px (masaüstü, 2x); aynı sahneden ayrıca dikey ya da 3:2 bir kare (mobil).</li>
<li><strong>Yerleşim:</strong> bina sağ yarıda; sol %40 metin için sade bırakılır.</li>
<li><strong>Metin:</strong> görselin üstünde yazı, logo ya da rozet olmaz; başlıklar sayfada HTML olarak yazılır.</li>
<li><strong>Çekim:</strong> render ise kamera geniş açıyla, binanın üstünde ve altında boşluk bırakılarak; fotoğrafsa en az 6000 px genişlikte.</li>
<li><strong>Hangi projeler:</strong> VYeniKonak (eldeki görsel kare), Tablo Adalar (1200 px), Kurumsal Yönetim için IFM (1791 px).</li>
</ul>
</div>'''


def page_html():
    body = '\n'.join([
        '''<section class="subpage-banner">
<div class="container">
<div class="subpage-banner-title"><h1 class="searchTitle">Banner Seçenekleri</h1></div>
<p class="gyo-subpage-lede">Proje görselleri 3:2 ya da kare; banner alanı 1280 px ekranda 2,5:1, 1920 px ekranda 3,7:1. Aşağıda aynı dört slayt, üç farklı çözümle. Tarayıcı penceresini daraltıp genişleterek karşılaştırabilirsiniz.</p>
</div>
</section>''',
        '<section class="gyo-bv" aria-labelledby="bv0">',
        intro('Referans', 'Şu anki hâl',
              'Fotoğraf banner alanını tam dolduracak şekilde kırpılıyor ya da kenarından uzatılıyor.',
              ['Kurumsal banner yapısıyla birebir'],
              ['Ekran genişledikçe binanın üstü ve altı kesiliyor',
               'Kare görselde (VYeniKonak) uzatılan gökyüzü ve alttaki bant belli oluyor']).replace(
            '<h2 class="gyo-bv__title">', '<h2 class="gyo-bv__title" id="bv0">'),
        current(), '</section>',
        '<section class="gyo-bv gyo-bv--logo" aria-labelledby="bv1">',
        intro('Seçenek 1 · önerilen', 'Geçişli bileşik banner',
              'Zemin, görselin gökyüzü ve zemin tonlarından üretilen sakin bir dikey renk geçişi; her ekran '
              'genişliğine uzar. Fotoğraf kırpılmadan sağda durur ve zemine çizgisiz, pürüzsüz erir. '
              'Geçişin yönü üç çeşitte farklı: 1A Vakıf GYO / VakıfBank logosundaki “V” kavisini, 1B '
              '“VB” işaretinin yatık dış kenarını izler (eğriler logo dosyasından birebir), 1C düz. '
              'Mobilde bugünkü mobil kesimler kullanılır.',
              ['Bina hiçbir ekranda kesilmez; geçişte çizgi, leke ya da şerit oluşmaz',
               'Geçişin yönü marka işaretinden geliyor (1A, 1B)',
               'Elimizdeki görsellerle hemen uygulanabilir'],
              ['Fotoğraf tam ekran değil; ekranın yarısı ile üçte ikisi arası',
               'Zemin tonu görselden geldiği için slayttan slayta değişir']).replace(
            '<h2 class="gyo-bv__title">', '<h2 class="gyo-bv__title" id="bv1">'),
        '<div class="container"><h3 class="gyo-bv__sub">1A · V kavisi yönünde geçiş</h3></div>', logo_variant('v'),
        '<div class="container"><h3 class="gyo-bv__sub">1B · VB işaretinin kenarı yönünde geçiş</h3></div>', logo_variant('vb'),
        '<div class="container"><h3 class="gyo-bv__sub">1C · Düz geçiş</h3></div>', logo_variant('soft'),
        '</section>',
        '<section class="gyo-bv gyo-bv--spec" aria-labelledby="bv2">',
        intro('Seçenek 2 · kalıcı çözüm', 'Geniş render talebi',
              'Müşteriden banner için özel, geniş görsel istenir. Görsel geldiğinde slayt bugünkü tam ekran '
              'yapıda kalır ve hiçbir ekranda kesilmez. Aşağıdaki şema talebin içeriğidir.',
              ['Tam ekran, en etkileyici sonuç',
               'Kurumsal banner yapısı değişmez'],
              ['Görseller gelene kadar uygulanamaz',
               'Her yeni kampanyada aynı ölçüde görsel üretilmesi gerekir']).replace(
            '<h2 class="gyo-bv__title">', '<h2 class="gyo-bv__title" id="bv2">'),
        SPEC, '</section>',
        '<section class="gyo-bv gyo-bv--box" aria-labelledby="bv3">',
        intro('Seçenek 3', 'Kutulu banner',
              'Banner tam ekran yerine sayfa genişliğinde (1110 px), köşeleri yuvarlatılmış bir kutuda durur; '
              'oran 2,1:1’de sabit kalır, ekran büyüdükçe kırpma artmaz.',
              ['3:2 görseller kutuya çok az kırpılarak oturur',
               'Kurumsal “Sürdürülebilir Bankacılık” ve “Özel Bankacılık” kutularıyla aynı dil'],
              ['Geniş ekranda iki yanda boşluk kalır; tam ekran etkisi yok',
               'Kare görselde (VYeniKonak) yine uzatma gerekiyor']).replace(
            '<h2 class="gyo-bv__title">', '<h2 class="gyo-bv__title" id="bv3">'),
        '<div class="container gyo-bv-box">%s</div>' % boxed(), '</section>',
    ])
    return b.page('Banner Seçenekleri — Vakıf GYO', 'Banner görselleri için üç çözüm seçeneği.',
                  body, b.TICKER, h1='')


def main():
    path = os.path.join(b.OUT, 'banner-alternatifleri.html')
    open(path, 'w', encoding='utf-8', newline='\n').write(page_html())
    print('yazıldı:', os.path.relpath(path, b.ROOT))


if __name__ == '__main__':
    main()
