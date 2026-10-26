# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif C (deneysel), yalnız ana sayfa: src/alt-c/index.html

  Navigasyon   argosy.co.nz gibi sade: logo, ana menü, hisse fiyatı, menü düğmesi
  Banner       soeiendom.no gibi: dev tipografi videonun üstüne biner; kaydırınca
               video tam ekrana büyür (30. yıl filmi, _build/make_video_30yil.py)
  YI           nz.goodman.com gibi büyük, sayaçlı borsa verileri (gerçek veri:
               _docs/kaynak/borsa-vkgyo.txt, borsa-vkgyo-1y.json)
  Kartlar      büyük; projeler kaydırmayla yatay ilerler, haberler sağa taşar
  Harita       soeiendom.no footer üstü gibi el çizimi Türkiye haritası; portföyün
               illeri ve proje adları (menu.txt Portföy ağacı)

Metinler B ile aynı kaynak verisinden (build_alt_b) gelir.
Çalıştırma:  python _build/build_alt_c.py
"""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_alt_b as b  # noqa: E402

ROOT = b.ROOT
OUT = os.path.join(ROOT, 'src', 'alt-c')
IMG = '../assets/img/b/'
GYO = '../assets/img/gyo/'
V = '../assets/video/'
NEW_TAB = b.NEW_TAB


def ver():
    paths = [os.path.join(ROOT, 'src', 'assets', p) for p in ('css/alt-c/c.css', 'js/alt-c/c.js')]
    return str(int(max(os.path.getmtime(p) for p in paths if os.path.exists(p)) or 1))


def ico(name, cls=''):
    return b.ico(name, cls)


# --- Borsa verisi (gerçek; kaynak dosyasından) ------------------------------
SERIES = json.load(io.open(os.path.join(ROOT, '_docs', 'kaynak', 'borsa-vkgyo-1y.json'), encoding='utf-8'))['series']
STOCK = {'price': 1.43, 'chg': -2.72, 'mcap': 6.29, 'div': 5.44, 'pb': 0.22, 'lo52': 1.39, 'hi52': 2.525,
         'shares': 4.4, 'date': '23 Ekim 2026'}


def tr_num(v, d=2):
    s = '{:,.{d}f}'.format(v, d=d)
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def spark():
    vals = [c for _d, c in SERIES]
    lo, hi = min(vals), max(vals)
    W, H, P = 1000, 220, 10
    pts = ['%.1f,%.1f' % (i * W / (len(vals) - 1), P + (hi - c) / (hi - lo) * (H - 2 * P)) for i, c in enumerate(vals)]
    line = 'M' + ' L'.join(pts)
    area = line + ' L%d,%d L0,%d Z' % (W, H, H)
    return line, area, SERIES[0][0], SERIES[-1][0]


# --- Menü (vakifgyo.com.tr menüsü, _docs/kaynak/menu.txt) -------------------
NAV = ['Kurumsal', 'Portföy', 'Yatırımcı İlişkileri', 'Güncel', 'Sürdürülebilirlik', 'Bize Ulaşın']
MENU = [
    ('Kurumsal', ['Hakkımızda', 'Kurumsal Yönetim', 'IK Politikamız', 'Şirket Bilgileri', 'Bilgi Merkezi']),
    ('Portföy', ['Devam Eden Projeler', 'Tamamlanan Projeler', 'Gayrimenkul Yatırımları']),
    ('Yatırımcı İlişkileri', ['Yatırımcı İlişkileri İletişim', 'Duyurular', 'Özel Durum Açıklamaları',
                              'Raporlar ve Yatırımcı Sunumları', 'Genel Kurul', 'Kurumsal Yönetim']),
    ('Güncel', ['Haberler', 'Duyurular', 'Ödüller']),
    ('Sürdürülebilirlik', ['Kilometre Taşları', 'Raporlar ve Sertifikalar', 'Kurumsal Sosyal Sorumluluk']),
    ('Bize Ulaşın', ['+90 (216) 285 94 00']),
]
HREF = {'Hakkımızda': '../alt-b/hakkimizda.html', 'Yatırımcı İlişkileri': '../alt-b/yatirimci-iliskileri.html'}


def header():
    links = ''.join('<li><a href="%s">%s</a></li>' % (HREF.get(t, '#'), t) for t in NAV)
    up = STOCK['chg'] >= 0
    menu = ''.join('<div class="c-menu__col"><p class="c-menu__head">%s</p><ul>%s</ul></div>'
                   % (h, ''.join('<li><a href="%s">%s</a></li>' % (HREF.get(i, '#'), i) for i in items))
                   for h, items in MENU)
    return '''<header class="c-head" data-c-head>
<a class="c-head__logo" href="index.html"><img class="c-head__logo-on-light" src="%s../gyo/vakif-gyo-logo.svg" alt="Vakıf GYO ana sayfa" width="150" height="26"><img class="c-head__logo-on-dark" src="%svakif-gyo-logo-ters.svg" alt="" width="150" height="26"></a>
<nav class="c-head__nav" aria-label="Ana menü"><ul>%s</ul></nav>
<a class="c-head__stock" href="#yatirimci"><span>VKGYO</span><b>%s ₺</b><i class="%s">%s %%%s</i></a>
<button type="button" class="c-head__menu" aria-expanded="false" aria-controls="c-menu" data-c-menu><span class="sr-only">Menü</span><span class="c-burger" aria-hidden="true"></span></button>
</header>
<div class="c-menu" id="c-menu" hidden data-c-menu-panel>
<div class="c-menu__inner">
<form class="c-menu__search" role="search" action="#"><label class="sr-only" for="c-q">Arama</label><input id="c-q" type="search" placeholder="Arama">%s</form>
<div class="c-menu__cols">%s</div>
<p class="c-menu__foot"><a href="#">EN</a><span>VakıfBank Finans Grubu İştirakidir.</span></p>
</div>
</div>''' % (IMG, IMG, links, tr_num(STOCK['price']), 'is-up' if up else 'is-down', '▲' if up else '▼',
             tr_num(abs(STOCK['chg'])), ico('search'), menu)


def hero():
    return '''<section class="c-hero" aria-label="Vakıf GYO" data-c-hero>
<div class="c-hero__stage">
<h1 class="c-hero__title" data-c-hero-title><span>Geleneğin Gücü,</span> <span>Geleceğin İnşası</span></h1>
<div class="c-hero__frame" data-c-hero-frame>
<video class="c-hero__video" autoplay muted loop playsinline preload="auto" poster="%sb-30yil-poster-1600x900.jpg" aria-hidden="true" data-c-video>
<source src="%sb-30yil-608x1080.mp4" type="video/mp4" media="(orientation: portrait) and (max-width: 899px)">
<source src="%sb-30yil-1600x900.mp4" type="video/mp4">
</video>
</div>
<button type="button" class="c-hero__pause" aria-pressed="false" data-c-video-toggle><span class="sr-only" data-c-video-label>Videoyu durdur</span>%s%s</button>
<a class="c-hero__down" href="#biz" data-c-down><span class="sr-only">Aşağı kaydır</span><svg viewBox="0 0 48 64" aria-hidden="true"><path d="M24 4v54M6 40l18 18 18-18"/></svg></a>
</div>
</section>''' % (IMG, V, V, ico('pause', 'c-ico--pause'), ico('play', 'c-ico--play'))


def statement():
    text = ('Geleneğimizden aldığımız güçle, geleceğin yaşam alanlarını inşa eder, paydaşlarımıza sürdürülebilir '
            'değer sunarız.')
    words = ' '.join('<span>%s</span>' % w for w in text.split())
    figs = ''.join('<div data-c-reveal><dt>%s</dt><dd>%s</dd></div>' % f for f in b.FIGURES)
    return '''<section class="c-statement" id="biz" aria-labelledby="biz-baslik">
<div class="c-wrap">
<h2 class="c-eyebrow" id="biz-baslik">Temel Amaç</h2>
<p class="c-statement__text" data-c-words>%s</p>
<dl class="c-statement__figs">%s</dl>
</div>
</section>''' % (words, figs)


def projects():
    cards = ''
    for key, name, place, status, desc, href, alt in b.INDEX:
        src = '%sdizin-%s-%s.jpg' % (IMG, key, '640x800' if key == 'tablo-adalar' else '1280x1600')
        logo = b.INDEX_LOGOS.get(key)
        if href and href.endswith('.html'):
            href = '../alt-b/' + href
        cards += '''<li class="c-pcard">
<a href="%s">
<span class="c-pcard__media"><img src="%s" alt="%s" width="640" height="800" loading="lazy" decoding="async"></span>
<span class="c-pcard__body">
<span class="c-pill%s">%s</span>
<span class="c-pcard__name">%s</span>
<span class="c-pcard__place">%s</span>
%s
</span>
</a>
</li>''' % (href or '#', src, alt, ' c-pill--live' if status.startswith('Devam') else '', status, name, place,
            '<img class="c-pcard__logo" src="%s" alt="" loading="lazy">' % logo if logo else '')
    return '''<section class="c-projects" id="projeler" aria-labelledby="proje-baslik" data-c-hscroll>
<div class="c-projects__stage">
<div class="c-wrap c-projects__head">
<h2 class="c-h2" id="proje-baslik">Portföy</h2>
<a class="c-more" href="#">Devam Eden Projeler%s</a>
</div>
<div class="c-projects__viewport">
<ol class="c-projects__track" data-c-track>%s</ol>
</div>
<div class="c-wrap"><div class="c-progress" aria-hidden="true"><span data-c-progress></span></div></div>
</div>
</section>''' % (ico('arrow'), cards)


def investor():
    line, area, d0, d1 = spark()
    big = [
        ('VKGYO', STOCK['price'], 2, '', ' ₺', ''),
        ('Piyasa değeri', STOCK['mcap'], 2, '', ' milyar ₺', ''),
        ('Temettü verimi', STOCK['div'], 2, '%', '', ''),
        ('PD/DD', STOCK['pb'], 2, '', '', ''),
    ]
    items = ''.join('''<div class="c-stat" data-c-reveal>
<dt>%s</dt>
<dd><span class="c-stat__num" data-c-count="%s" data-dec="%d" data-pre="%s" data-suf="%s">%s%s%s</span>%s</dd>
</div>''' % (lab, v, d, pre, suf, pre, tr_num(v, d), suf, '<small>%s</small>' % note if note else '') for lab, v, d, pre, suf, note in big)
    chg = STOCK['chg']
    links = ''.join('<li><a href="%s">%s%s</a></li>' % (h, t, ico('arrow')) for t, h in [
        ('Özel Durum Açıklamaları', '../alt-b/yatirimci-iliskileri.html#aciklamalar'),
        ('Raporlar ve Yatırımcı Sunumları', '../alt-b/yatirimci-iliskileri.html#raporlar'),
        ('Genel Kurul', '../alt-b/yatirimci-iliskileri.html#genel-kurul')])
    return '''<section class="c-ir" id="yatirimci" aria-labelledby="yi-baslik">
<div class="c-wrap">
<div class="c-ir__head">
<h2 class="c-h2" id="yi-baslik">Yatırımcı İlişkileri</h2>
<p class="c-ir__meta">Borsa İstanbul · VKGYO · <time datetime="2026-10-23">%s</time> <span class="%s">%s %%%s</span></p>
</div>
<dl class="c-ir__stats">%s</dl>
<figure class="c-ir__chart" data-c-reveal>
<svg viewBox="0 0 1000 220" preserveAspectRatio="none" role="img" aria-label="VKGYO son bir yıl kapanış fiyatları, %s ile %s arası">
<path class="c-ir__area" d="%s"/>
<path class="c-ir__line" d="%s" pathLength="1" data-c-draw/>
</svg>
<figcaption><span>%s</span><span>52 haftalık aralık %s – %s ₺</span><span>%s</span></figcaption>
</figure>
<ul class="c-ir__links">%s</ul>
</div>
</section>''' % (STOCK['date'], 'is-up' if chg >= 0 else 'is-down', '▲' if chg >= 0 else '▼', tr_num(abs(chg)),
                 items, b.tr_date(d0), b.tr_date(d1), area, line, b.tr_date(d0),
                 tr_num(STOCK['lo52']), tr_num(STOCK['hi52']), b.tr_date(d1), links)


def news():
    cards = ''.join('''<li class="c-ncard" data-c-reveal>
<a href="#">
<span class="c-ncard__media"><img src="%s%s" alt="" loading="lazy" decoding="async"></span>
<time datetime="%s">%s</time>
<span class="c-ncard__title">%s</span>
</a>
</li>''' % (IMG, img, d, b.tr_date(d), t) for img, d, t in b.NEWS)
    return '''<section class="c-news" aria-labelledby="haber-baslik">
<div class="c-wrap c-news__head">
<h2 class="c-h2" id="haber-baslik">Haberler</h2>
<div class="c-news__nav">
<button type="button" class="c-round" data-c-prev aria-label="Önceki haberler">%s</button>
<button type="button" class="c-round" data-c-next aria-label="Sonraki haberler">%s</button>
</div>
</div>
<ul class="c-news__track" tabindex="0" aria-label="Haberler, yatay kaydırılabilir" data-c-drag>%s</ul>
</section>''' % (ico('left'), ico('right'), cards)


def duo():
    cards = [
        ('sektor-1600.jpg', 'Sürdürülebilirlik',
         'Sürdürülebilirlik, Vakıf GYO’nun temel stratejilerinden biridir. Çevresel, sosyal ve yönetişim (ESG) '
         'prensipleriyle faaliyet gösteren şirketimiz, gelecek nesillere daha yaşanabilir bir dünya bırakmayı amaçlamaktadır.',
         'Raporlar ve Sertifikalar'),
        ('ifm-gece-1100.jpg', 'Vakıf GYO 30 Yaşında',
         'Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak, 30 yıldır güçlü Türkiye’nin temellerini atıyoruz. '
         'Birlikte nice yıllara…', 'Hakkımızda'),
    ]
    items = ''.join('''<article class="c-big" data-c-reveal>
<img src="%s%s" alt="" loading="lazy" decoding="async">
<div class="c-big__body">
<h2 class="c-big__title">%s</h2>
<p>%s</p>
<a class="c-more c-more--light" href="%s">%s%s</a>
</div>
</article>''' % (IMG, img, t, p, '../alt-b/hakkimizda.html' if l == 'Hakkımızda' else '#', l, ico('arrow'))
                    for img, t, p, l in cards)
    return '<section class="c-duo"><div class="c-wrap c-duo__grid">%s</div></section>' % items


# --- Harita -----------------------------------------------------------------
# Türkiye sınırı: Natural Earth (world-atlas@2, countries-50m) → gorseller/indirilen/harita/turkiye.path
# İzdüşüm: x = (boylam-25,5)·51,28 ; y = (42,3-enlem)·51,28/cos39°  (viewBox -20 -150 1040 640)
VB = (-20, -150, 1040, 640)
CITIES = [
    # (ad, nokta x,y, etiket x,y, projeler — menu.txt Portföy ağacı, ilçeler portfoy-portfoy-*.txt)
    ('İstanbul', (179, 84), (30, -128), ['VSancaktepe Merkez', 'Tablo Adalar', 'İstanbul Uluslararası Finans Merkezi',
                                         'Bizimtepe Aydos', 'Medyan Kadıköy', 'Şişli VakıfBank Ek Hizmet Binası',
                                         'Fatih İş Merkezi', 'İstanbul Sancaktepe']),
    ('Kocaeli', (202, 98), (250, 0), ['Kocaeli Çayırova']),
    ('Ankara', (377, 156), (410, 112), ['Cubes Ankara', 'Kavaklıdere Dükkan', 'Ankara ENH Parselleri']),
    ('Kütahya', (230, 190), (190, 228), ['VKütahya İş Merkezi']),
    ('İzmir', (84, 256), (-6, 300), ['VYeniKonak', 'İzmir Konak', 'Aliağa İş Merkezi']),
    ('Gaziantep', (609, 345), (660, 300), ['Gaziantep Iconova']),
]
LINKS = {'VSancaktepe Merkez': '../alt-b/vsancaktepe-merkez.html', 'Cubes Ankara': '../alt-b/cubes-ankara.html'}

# El çizimi küçük resimler (yerel koordinat, ölçek 1)
SKETCH = {
    'skyline': 'M0 60h150 M6 60V30h14v30 M22 60V18h16v42 M40 60V36h12v24 M56 60V8h10v52 M61 8V0 M70 60V26h18v34 '
               'M92 60V40h12v20 M108 60V22h14v38 M126 60V34h20v26 M26 26h8 M26 34h8 M26 42h8 M74 32h10 M74 40h10 M112 30h6 M112 38h6',
    'cubes': 'M10 80V40h22v40 M6 40h30v-6H6z M10 34V14h22v20 M4 14h34V8H4z M8 8V0h26v8 M44 80V52h18v28 M40 52h26v-5H40z '
             'M44 47V34h18v13 M0 80h72 M16 22h4 M24 22h4 M16 50h4 M24 50h4 M16 62h4 M24 62h4',
    'twin': 'M8 90V10l10-8 10 8v80 M36 90V30l8-6 8 6v60 M0 90h64 M13 20h10 M13 30h10 M13 40h10 M13 50h10 M13 60h10 '
            'M40 40h8 M40 50h8 M40 60h8 M40 70h8',
    'crane': 'M10 70V4 M10 4h60 M10 4l-8 10h8 M10 14l10-10 M20 14l10-10 M30 14l10-10 M40 14l10-10 M66 4v26 M60 30h12v8H60z M0 70h40',
    'tree': 'M14 40V26 M14 2 4 16h6L2 28h24l-8-12h6z',
    'sun': 'M20 20m-8 0a8 8 0 1 0 16 0a8 8 0 1 0-16 0 M20 0v6 M20 34v6 M0 20h6 M34 20h6 M6 6l4 4 M30 30l4 4 M34 6l-4 4 M10 30l-4 4',
    'wave': 'M0 6q6-8 12 0t12 0 12 0 12 0 12 0',
    'boat': 'M0 20h44l-6 8H6z M20 20V0l16 18H20 M20 4 8 18h12',
    'bird': 'M0 4q5-6 10 0q5-6 10 0',
    'block': 'M0 50V14h40v36 M40 50V24h24v26 M-6 50h76 M6 20h6 M18 20h6 M28 20h6 M6 30h6 M18 30h6 M28 30h6 M46 30h6 M54 30h4 M14 50V40h10v10',
}
DECOR = [('skyline', 470, -132, 1.3), ('boat', 700, -90, 1.2), ('wave', 640, -40, 1.4), ('wave', 860, -70, 1.4),
         ('wave', 560, -10, 1), ('bird', 760, -128, 1), ('bird', 790, -118, .8), ('sun', 940, -130, 1.1),
         ('cubes', 760, 92, 1.1), ('twin', 222, 300, .9), ('crane', 300, 40, .8), ('block', 880, 372, .9),
         ('tree', 330, 250, 1), ('tree', 560, 230, 1.1), ('tree', 590, 238, .8), ('tree', 900, 170, 1),
         ('tree', 120, 150, .9), ('wave', 200, 440, 1.4), ('wave', 420, 450, 1.4), ('wave', 50, 420, 1),
         ('boat', 520, 420, 1), ('sun', -10, 420, .9)]


def map_illustration():
    tr = io.open(os.path.join(ROOT, 'gorseller', 'indirilen', 'harita', 'turkiye.path'), encoding='utf-8').read()
    x0, y0, w, h = VB

    def pct(x, y):
        return (x - x0) / w * 100, (y - y0) / h * 100

    deco = ''.join('<g transform="translate(%s %s) scale(%s)"><path class="c-map__sk" d="%s" data-c-pop/></g>'
                   % (x, y, s, SKETCH[k]) for k, x, y, s in DECOR)
    dots, labels = '', ''
    for name, (px, py), (lx, ly), items in CITIES:
        dots += ('<path class="c-map__lead" d="M%s %s L%s %s"/><circle class="c-map__dot" cx="%s" cy="%s" r="7"/>'
                 % (px, py, lx + 20, ly + 30, px, py))
        ax, ay = pct(lx, ly)
        pills = ''.join('<li><a class="c-pill" href="%s">%s</a></li>' % (LINKS.get(i, '#'), i) for i in items)
        labels += ('<div class="c-map__city" style="left:%.2f%%;top:%.2f%%" data-c-pop><p class="c-map__name">%s</p>'
                   '<ul>%s</ul></div>' % (ax, ay, name, pills))
    return '''<section class="c-map" aria-label="Portföy">
<div class="c-map__scroll">
<div class="c-map__canvas">
<svg viewBox="%d %d %d %d" aria-hidden="true">
<defs><filter id="c-rough"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="4"/><feDisplacementMap in="SourceGraphic" scale="3.2"/></filter></defs>
<g filter="url(#c-rough)">
<path class="c-map__land" d="%s"/>
<path class="c-map__road" d="M179 84 C 260 110, 300 140, 377 156 S 520 260, 609 345 M179 84 C 150 160, 120 210, 84 256 M230 190 L377 156"/>
%s
%s
</g>
</svg>
%s
</div>
</div>
</section>''' % (x0, y0, w, h, tr, deco, dots, labels)


def footer():
    cols = ''.join('<div><p class="c-foot__head">%s</p><ul>%s</ul></div>'
                   % (t, ''.join('<li><a href="%s">%s</a></li>' % (h, l) for l, h in links))
                   for t, links in b.FOOT_COLS)
    social = ''.join('<li><a href="%s" target="_blank" rel="noopener">%s%s</a></li>' % (h, t, NEW_TAB)
                     for t, h in b.SOCIAL)
    return '''<footer class="c-foot">
<div class="c-wrap">
<div class="c-foot__cta" data-c-reveal>
<h2 class="c-foot__big">Bize Ulaşın</h2>
<a class="c-foot__phone" href="tel:+902162859400">+90 (216) 285 94 00</a>
<p class="c-foot__addr">Finanskent Mahallesi, Finans Caddesi, Finans Merkezi Sitesi No:30/20 Kat: 9 PK: 34760 Ümraniye/ İstanbul</p>
</div>
<div class="c-foot__cols">%s</div>
<div class="c-foot__bottom">
<img src="%svakif-gyo-logo-ters.svg" alt="Vakıf GYO" width="140" height="24" loading="lazy">
<p>VakıfBank Finans Grubu İştirakidir.</p>
<ul class="c-foot__social">%s</ul>
</div>
</div>
</footer>''' % (cols, IMG, social)


def page():
    v = ver()
    body = '\n'.join([hero(), statement(), projects(), investor(), news(), duo(), map_illustration()])
    return '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası</title>
<meta name="description" content="Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası. Kurumsal · Portföy · Yatırımcı İlişkileri · Güncel · Sürdürülebilirlik · Bize Ulaşın">
<link rel="icon" href="../assets/img/favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;500&family=Barlow:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Open+Sans:ital,wdth,wght@1,75..100,600..800&family=Inter+Tight:wght@500;600&family=Instrument+Serif:ital@0;1&display=swap">
<script>/* banner başlığı yazı karakteri denemesi: ?t=1 | 2 | 3 */document.documentElement.setAttribute('data-t', (/[?&]t=([123])/.exec(location.search) || [0, '1'])[1]);</script>
<link rel="stylesheet" href="../assets/css/alt-c/c.css?v=%s">
</head>
<body class="c">
<a class="c-skip" href="#biz">İçeriğe atla</a>
%s
<main>
%s
</main>
%s
<script src="../assets/js/alt-c/c.js?v=%s" defer></script>
</body>
</html>
''' % (v, header(), body, footer(), v)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, 'index.html')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(page())
    print('yazıldı:', os.path.relpath(p, ROOT))
