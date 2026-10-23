# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif B

Esin kaynağı: büyük, etkili görseller (tam ekran slayt, tam genişlik
bantlar) + sabit sol menü. Kurumsal VakıfBank bileşenleri kullanılmaz;
tasarım dili bağımsız, hazır CSS yok.

  Masaüstü (≥1200)  solda sabit koyu menü şeridi; ana başlığa tıklanınca alt
                    menü görselin üstüne açılır (iki katman).
  Tablet / mobil    üstte ince çubuk; menü tam ekran, alt menüler akordeon.
  Ton               karma: menü, görsel bantlar ve vurgu bölümleri koyu;
                    içerik bölümleri açık (taş rengi / beyaz).
  Hareket           slaytlarda yavaş yakınlaşma (Ken Burns) ve çapraz geçiş;
                    parallax yok; "hareketi azalt" tercihinde kapanır.

Veri ve metinler Alternatif A ile aynıdır (build_alt_a, build_alt_a_pages);
iki alternatif aynı içerikle karşılaştırılabilsin diye.

Çalıştırma:  python _build/make_images_b.py   (bir kez)
             python _build/build_alt_b.py
Çıktı:       src/alt-b/      menü solda
             src/alt-b-ust/  menü üstte (aynı içerik, body.b--top)
             {index, yatirimci-iliskileri, vsancaktepe-merkez, hakkimizda}.html
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_alt_a as a  # noqa: E402
import build_alt_a_pages as ap  # noqa: E402

ROOT = a.ROOT
# Menü yerleşimi: 'sol' (sabit sol şerit) ya da 'ust' (üst çubuk); main() ikisini de üretir
LAYOUT = 'sol'
OUTS = {'sol': os.path.join(ROOT, 'src', 'alt-b'), 'ust': os.path.join(ROOT, 'src', 'alt-b-ust')}
IMG = '../assets/img/b/'
IMG_DIR = os.path.join(ROOT, 'src', 'assets', 'img', 'b')
GYO = '../assets/img/gyo/'
LOGO = IMG + 'vakif-gyo-logo-ters.svg'
LOGO_DARK = GYO + 'vakif-gyo-logo.svg'
PHONE = ('tel:+902162859400', '+90 (216) 285 94 00')
NEW_TAB = '<span class="sr-only"> (yeni sekmede açılır)</span>'
RAIL_W = 288     # css: --rail


# ---------------------------------------------------------------------------
# İkonlar — tek çizgi kalınlığı (1.5), 24'lük ızgara
# ---------------------------------------------------------------------------

ICONS = {
    'arrow': '<path d="M4 12h15M13 6l6 6-6 6"/>',
    'left': '<path d="M15 5l-7 7 7 7"/>',
    'right': '<path d="M9 5l7 7-7 7"/>',
    'down': '<path d="M5 9l7 7 7-7"/>',
    'pause': '<path d="M9 6v12M15 6v12"/>',
    'play': '<path d="M8 5.5v13l10.5-6.5z"/>',
    'phone': '<path d="M7.5 3.5 5 3.8c-1 .1-1.8 1-1.6 2C4.3 13 11 19.7 18.2 20.6c1 .1 1.9-.6 2-1.6l.3-2.5-4.3-1.8-1.9 1.9a12 12 0 0 1-5-5l1.9-1.9z"/>',
    'mail': '<rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="M3.5 6.5 12 13l8.5-6.5"/>',
    'pin': '<path d="M12 21s7-6.3 7-11.6A7 7 0 0 0 5 9.4C5 14.7 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    'doc': '<path d="M6.5 3h7l4 4v14h-11z"/><path d="M13.5 3v4h4M9 12h6M9 15.5h6"/>',
    'download': '<path d="M12 4v11M7 10.5l5 5 5-5M5 20h14"/>',
    'ext': '<path d="M14 4h6v6M20 4l-9 9M18 14v6H4V6h6"/>',
    'menu': '<path d="M4 7h16M4 12h16M4 17h16"/>',
    'close': '<path d="M6 6l12 12M18 6 6 18"/>',
    'search': '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    'plus': '<path d="M12 5v14M5 12h14"/>',
    'chat': '<path d="M4 5h16v11H9l-5 4z"/>',
    'calc': '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M8 7h8M8.5 11h.01M12 11h.01M15.5 11h.01M8.5 14.5h.01M12 14.5h.01M15.5 14.5h.01M8.5 18h.01M12 18h3.5"/>',
    'help': '<circle cx="12" cy="12" r="8.5"/><path d="M9.6 9.5a2.5 2.5 0 1 1 3.4 2.3c-.7.3-1 .9-1 1.6v.6M12 17h.01"/>',
    'book': '<path d="M4 5.5C6.5 4.5 9.5 4.5 12 6c2.5-1.5 5.5-1.5 8-.5V19c-2.5-1-5.5-1-8 .5-2.5-1.5-5.5-1.5-8-.5z"/><path d="M12 6v13.5"/>',
    'whatsapp': '<path d="M4.5 19.5l1.2-3.6A8 8 0 1 1 8.4 18.6z"/><path d="M9.2 8.6c.3 2.6 2.4 4.9 5.2 5.4l.9-1.3-1.8-.9-.7.7c-.9-.4-1.7-1.2-2.1-2.1l.7-.7-.9-1.8z"/>',
}


# Logodaki beyaz "V" — kendi koordinatlarıyla (vakif-gyo-logo.svg); arka plan işareti
V_PATH = ('M0 0C-2.47-2.955-17.017-18.729-27.618-30.955-25.358-20.84-21.355 .798-17.82 5.238'
          '-14.344 9.615-9.412 10.318-9.412 10.318-9.412 10.318-27.921 15.43-33.285-6.159'
          '-35.238-14.1-41.274-42.257-41.274-42.257-41.163-42.507-24.411-43.867-16.297-34.755'
          '-12.663-30.674 5.317-9.224 10.265-3.047 20.668 9.991 27.117 10.882 27.117 10.882'
          ' 27.117 10.882 10.57 12.618 0 0')


def swoosh(cls=''):
    return ('<svg class="b-swoosh%s" viewBox="6 -1 69.5 61" aria-hidden="true" focusable="false">'
            '<path transform="matrix(1,0,0,-1,47.431299,15.429993)" d="%s" fill="currentColor"/></svg>'
            % (' ' + cls if cls else '', V_PATH))


def ico(name, cls=''):
    return ('<svg class="b-ico%s" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>'
            % (' ' + cls if cls else '', ICONS[name]))


def link(text, href='#', cls='b-link', extra=''):
    return '<a class="%s" href="%s"%s><span>%s</span>%s</a>' % (cls, href, extra, text, ico('arrow'))


def btn(text, href='#', cls='', extra=''):
    return '<a class="b-btn%s" href="%s"%s>%s</a>' % (' ' + cls if cls else '', href, extra, text)


# ---------------------------------------------------------------------------
# Görseller — üretilmiş genişlikler diskten okunur (srcset)
# ---------------------------------------------------------------------------

def widths(name):
    out = []
    for p in glob.glob(os.path.join(IMG_DIR, name + '-*.jpg')):
        m = re.fullmatch(re.escape(name) + r'-(\d+)\.jpg', os.path.basename(p))
        if m:
            out.append(int(m.group(1)))
    if not out:
        raise SystemExit('görsel yok: %s — önce make_images_b.py' % name)
    return sorted(out)


def srcset(name):
    return ', '.join('%s%s-%d.jpg %dw' % (IMG, name, w, w) for w in widths(name))


def sizes_full():
    return '100vw' if LAYOUT == 'ust' else '(min-width: 1200px) calc(100vw - %dpx), 100vw' % RAIL_W


def picture(name, alt, cls='', sizes=None, portrait=True, lazy=True, pos=None, ppos=None,
            fetch=''):
    """Tam ekran/bant görseli: dikey ekranlarda 3:5 kesim, diğerlerinde 3:2."""
    ws = widths(name)
    sizes = sizes or sizes_full()
    style = []
    if pos:
        style.append('--pos:%s' % pos)
    if ppos:
        style.append('--ppos:%s' % ppos)
    src = ('<source media="(orientation: portrait) and (max-width: 1199px)" srcset="%s" sizes="100vw">'
           % srcset(name + '-p')) if portrait else ''
    return ('<picture class="%s"%s>%s<img src="%s%s-%d.jpg" srcset="%s" sizes="%s" alt="%s"%s%s></picture>'
            % (cls, ' style="%s"' % ';'.join(style) if style else '', src, IMG, name,
               ws[len(ws) // 2], srcset(name), sizes, alt,
               ' loading="lazy" decoding="async"' if lazy else '',
               ' fetchpriority="%s"' % fetch if fetch else ''))


# ---------------------------------------------------------------------------
# Menü — Alternatif A ile aynı bilgi mimarisi (önerilen site haritası)
# ---------------------------------------------------------------------------

PAGES = {
    'Hakkımızda': 'hakkimizda.html',
    'Vakıf GYO’yu Tanıyalım': 'hakkimizda.html',
    'VSancaktepe Merkez': 'vsancaktepe-merkez.html',
    'Vakıf GYO’ya Yatırım': 'yatirimci-iliskileri.html',
    'Yatırımcı İlişkileri': 'yatirimci-iliskileri.html',
}


def href(t):
    return PAGES.get(t, '#')


SALE = a.SALE
NAV = [
    ('projeler', 'Projeler', GYO + 'menu-projeler-704x484.jpg', [
        ('Satıştaki Projeler', SALE),
        ('Devam Eden Projeler', ['VSancaktepe Merkez', 'VYeniKonak']),
        ('Tamamlanan Projeler', ['İstanbul Uluslararası Finans Merkezi', 'Cubes Ankara',
                                 'Tablo Adalar', 'Bizimtepe Aydos', 'Gaziantep Iconova']),
        ('Kampanyalar', ['Tüm Kampanyalar', 'VSancaktepe Merkez Kampanyaları',
                         'Tablo Adalar Kampanyaları']),
        ('Satın Alma', ['Ön Talep Formu', 'Satış Ofisleri', 'Konut Kredisi Hesaplama',
                        'SarıPanjur Ev Kredisi']),
    ]),
    ('portfoy', 'Portföy', GYO + 'menu-portfoy-704x484.jpg', [
        ('Portföy Özeti', ['Portföy Haritası', 'Portföy Tablosu']),
        ('Gayrimenkul Projeleri', ['Medyan Kadıköy']),
        ('Mülkler', ['Şişli VakıfBank Ek Hizmet Binası', 'Bizimtepe Aydos Ticari Üniteler',
                     'Aliağa İş Merkezi', 'Fatih İş Merkezi', 'Kavaklıdere Dükkân',
                     'VKütahya İş Merkezi']),
        ('Arsalar', ['Ankara ENH Parselleri', 'İzmir Konak', 'İstanbul Sancaktepe',
                     'Kocaeli Çayırova']),
        ('Kiralık Alanlar', ['Kiralık Alanlar', 'Kiralama Talebi']),
    ]),
    ('yatirimci', 'Yatırımcı İlişkileri', GYO + 'menu-yatirimci-704x484.jpg', [
        ('Vakıf GYO’ya Yatırım', ['Yatırımcı İlişkileri', 'Neden Vakıf GYO', 'Ortaklık Yapısı',
                                       'Yönetim Kurulu', 'Komiteler', 'Üst Yönetim']),
        ('Finansal Bilgiler', ['Finansal Sonuçlar', 'Özet Finansallar', 'Finansal Tablolar',
                               'Faaliyet Raporları', 'Yatırımcı Sunumları',
                               'Gayrimenkul Değerleme Raporları', 'Kâr Payı Bilgileri']),
        ('Açıklamalar', ['Özel Durum Açıklamaları', 'Yatırımcı Duyuruları', 'Basın Açıklamaları']),
        ('Kurumsal Yönetim', ['Kurumsal Yönetim Yaklaşımımız', 'Esas Sözleşme', 'Politikalar',
                              'Kurumsal Yönetim Derecelendirme', 'Genel Kurul']),
        ('Hisse ve Takvim', ['Hisse Senedi Bilgileri', 'İnteraktif Hisse Grafiği',
                             'Sermaye Artırımı ve Temettü Geçmişi', 'Finansal Takvim']),
    ]),
    ('kurumsal', 'Kurumsal', GYO + 'menu-kurumsal-704x484.jpg', [
        ('Vakıf GYO’yu Tanıyalım', ['Hakkımızda', 'Vizyon ve Misyon', 'Yönetim Politikası',
                                          '30. Yıl']),
        ('Sektör ve Ödüller', ['GYO Sektörü', 'Ödüller']),
        ('Medya', ['Haberler', 'E-Bülten', 'Logolarımız ve Kurumsal Görseller']),
        ('İnsan Kaynakları', ['İK Politikamız', 'İş Başvurusu']),
        ('İletişim', ['İletişim Formu', 'Müşteri Şikayetleri Yönetim Süreci',
                      'Gizlilik ve KVKK']),
    ]),
    ('surdurulebilirlik', 'Sürdürülebilirlik', GYO + 'menu-surdurulebilirlik-704x484.jpg', [
        ('Yaklaşımımız', ['Kilometre Taşları', 'Yönetişim Yapısı', 'Stratejik Yaklaşım',
                          'Öncelikli Konular']),
        ('Performans', ['Rating ve Endeksler', 'Risk ve Fırsatların Finansal Etkileri']),
        ('Paydaşlar', ['Paydaş Etkileşim Kanalları', 'Paydaş Çalıştayı',
                       'Paydaş Geri Bildirim Anketi']),
        ('Çevre Yönetimi', ['Enerji Yönetimi', 'Su ve Atık Yönetimi', 'Sera Gazı Emisyonları']),
        ('Raporlar', ['Rapor ve Sertifikalar', 'Kurumsal Sosyal Sorumluluk']),
    ]),
]


def flyout(key, title, img, groups):
    cols = ''.join(
        '<div class="b-fly__group"><p class="b-fly__head">%s</p><ul>%s</ul></div>'
        % (g, ''.join('<li><a href="%s">%s</a></li>' % (href(t), t) for t in links))
        for g, links in groups)
    return '''<div class="b-fly" id="fly-%s" role="region" aria-label="%s alt menüsü">
<div class="b-fly__inner">
<p class="b-fly__title" aria-hidden="true">%s</p>
<div class="b-fly__cols">%s</div>
</div>
<img class="b-fly__img" src="%s" alt="" loading="lazy">
</div>''' % (key, title, title, cols, img)


def nav_items(current=None):
    out = ''
    for key, title, img, groups in NAV:
        cur = ' is-current' if key == current else ''
        out += ('<li class="b-nav__item%s"><button type="button" class="b-nav__btn" aria-expanded="false" '
                'aria-controls="fly-%s"><span>%s</span>%s</button>%s</li>'
                % (cur, key, title, ico('right', 'b-nav__chev'), flyout(key, title, img, groups)))
    return out


QUICK = [('Ön Talep Formu', '#', 'plus'), ('Satış Ofisi', '#', 'pin'),
         ('Konut Kredisi Hesaplama', '#', 'calc'), ('Özel Durum Açıklamaları',
         'https://www.kap.org.tr/tr/sirket-bilgileri/genel/1116-vakif-gayrimenkul-yatirim-ortakligi-a-s', 'doc')]


def rail(current=None):
    quick = ''.join('<li><a href="%s"%s>%s<span>%s</span></a></li>'
                    % (h, ' target="_blank" rel="noopener"' if h.startswith('http') else '',
                       ico(i), t + (NEW_TAB if h.startswith('http') else ''))
                    for t, h, i in QUICK)
    return '''<header class="b-rail" data-b-rail>
<div class="b-rail__bar">
<a class="b-rail__logo" href="index.html"><img src="%s" alt="Vakıf GYO ana sayfa" width="184" height="31"></a>
<button type="button" class="b-burger" aria-expanded="false" aria-controls="b-menu" data-b-burger><span class="sr-only">Menü</span>%s%s</button>
</div>
<div class="b-rail__menu" id="b-menu">
<nav class="b-nav" aria-label="Ana menü"><ul>%s</ul></nav>
<ul class="b-rail__quick">%s</ul>
<div class="b-rail__foot">
<a class="b-ticker" href="yatirimci-iliskileri.html#hisse"><span class="b-ticker__code">VKGYO</span><span class="b-ticker__px">3,27 ₺</span><span class="b-up">▲ %%1,24</span></a>
<a class="b-rail__phone" href="%s">%s<span>%s</span></a>
%s
<p class="b-rail__meta"><a href="#" lang="en">EN</a><a href="#" class="b-rail__search">%s<span>Arama</span></a></p>
</div>
</div>
</header>''' % (LOGO, ico('menu', 'b-burger__open'), ico('close', 'b-burger__close'),
                nav_items(current), quick, PHONE[0], ico('phone'), PHONE[1],
                btn('Ön Talep Formu', '#', 'b-btn--yellow b-btn--block'), ico('search'))


# Footer sütunları: vakifgyo.com.tr menü ağacındaki başlıklar (_docs/kaynak/menu.txt)
FOOT_COLS = [
    ('Portföy', [('Devam Eden Projeler', '#'), ('Tamamlanan Projeler', '#'), ('Gayrimenkul Yatırımları', '#'),
                 ('Ön Talep Formu', '#')]),
    ('Yatırımcı İlişkileri', [('Duyurular', '#'),
                              ('Özel Durum Açıklamaları', 'yatirimci-iliskileri.html#aciklamalar'),
                              ('Raporlar ve Yatırımcı Sunumları', 'yatirimci-iliskileri.html#raporlar'),
                              ('Genel Kurul', 'yatirimci-iliskileri.html#genel-kurul'),
                              ('Kurumsal Yönetim', 'yatirimci-iliskileri.html#kurumsal-yonetim')]),
    ('Kurumsal', [('Hakkımızda', 'hakkimizda.html'), ('Sürdürülebilirlik', '#'), ('Ödüller', '#'),
                  ('Haberler', '#'), ('IK Politikamız', '#')]),
]

SOCIAL = [('Instagram', 'https://www.instagram.com/vakifgyo/'),
          ('LinkedIn', 'https://www.linkedin.com/company/vak%C4%B1f-gyo-a-%C5%9F-'),
          ('X', 'https://twitter.com/VakifGYO'), ('Facebook', 'https://www.facebook.com/VakifGYO/')]


def footer():
    cols = ''.join('<div class="b-foot__col"><p class="b-foot__head">%s</p><ul>%s</ul></div>'
                   % (t, ''.join('<li><a href="%s">%s</a></li>' % (h, l) for l, h in links))
                   for t, links in FOOT_COLS)
    social = ''.join('<li><a href="%s" target="_blank" rel="noopener">%s%s</a></li>' % (h, t, NEW_TAB)
                     for t, h in SOCIAL)
    return '''<footer class="b-foot">
%s
<div class="b-wrap">
<div class="b-foot__top">
<div class="b-foot__brand">
<img src="%s" alt="Vakıf GYO" width="230" height="39" loading="lazy">
<p>Geleneğin Gücü, Geleceğin İnşası</p>
<a class="b-foot__phone" href="%s">%s</a>
<p class="b-foot__addr">Finanskent Mahallesi, Finans Caddesi, Finans Merkezi Sitesi No:30/20 Kat: 9 PK: 34760 Ümraniye/ İstanbul</p>
</div>
%s
<div class="b-foot__col"><p class="b-foot__head">Sosyal Medya</p><ul>%s</ul></div>
</div>
<div class="b-foot__bottom">
<p>VakıfBank Finans Grubu İştirakidir.</p>
<ul><li><a href="#">Gizlilik ve Kişisel Verilerin Korunması</a></li><li><a href="#">Bilgi Toplumu Hizmetleri Vakıf GYO</a></li></ul>
</div>
</div>
</footer>''' % (swoosh(), LOGO, PHONE[0], PHONE[1], cols, social)


# ---------------------------------------------------------------------------
# Sayfa iskeleti
# ---------------------------------------------------------------------------

def page(title, desc, body, shell=None, body_cls=''):
    head_html, foot_html = shell if shell else (rail(), footer())
    return '''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#121417">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="../assets/img/favicon.ico" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@300;400;500;600&family=Barlow:ital,wght@0,400;0,500;0,600;1,400&family=Open+Sans:ital,wdth,wght@1,75..100,600..800&display=swap">
<link rel="stylesheet" href="../assets/css/alt-b/b.css?v=%s">
</head>
<body class="b%s%s">
<a class="b-skip" href="#icerik">İçeriğe atla</a>
%s
<div class="b-page">
<main id="icerik" tabindex="-1">
%s
</main>
%s
</div>
<script src="../assets/js/alt-b/b.js?v=%s"></script>
<script src="../assets/js/alt-b/b-gl.js?v=%s"></script>
</body>
</html>
''' % (title, desc, VERSION, ' b--top' if LAYOUT == 'ust' else '', ' ' + body_cls if body_cls else '', head_html, body, foot_html, VERSION, VERSION)


def _version():
    paths = [os.path.join(ROOT, 'src', 'assets', 'css', 'alt-b', 'b.css'),
             os.path.join(ROOT, 'src', 'assets', 'js', 'alt-b', 'b.js'),
             os.path.join(ROOT, 'src', 'assets', 'js', 'alt-b', 'b-gl.js')]
    return str(int(max(os.path.getmtime(p) for p in paths if os.path.exists(p)) or 0)) \
        if any(os.path.exists(p) for p in paths) else '1'


VERSION = _version()


def section_head(title, hid, lede='', more='', cls=''):
    return ('<div class="b-head%s"><div><h2 class="b-h2" id="%s">%s</h2>%s</div>%s</div>'
            % (' ' + cls if cls else '', hid, title,
               '<p class="b-lede">%s</p>' % lede if lede else '', more))


def tr_date(iso):
    return ap.tr_date(iso)


def doclist(items, cls=''):
    lis = ''.join(
        '<li><a href="%s">%s<span class="b-docs__title">%s</span>'
        '<span class="b-docs__type">%s</span>%s</a></li>'
        % (h, ('<time class="b-docs__date" datetime="%s">%s</time>' % (iso, tr_date(iso))) if iso
           else '<span class="b-docs__date">%s</span>' % code, title, kind, ico('arrow'))
        for iso, code, title, kind, h in items)
    return '<ul class="b-docs%s">%s</ul>' % (' ' + cls if cls else '', lis)


# ---------------------------------------------------------------------------
# Hero slayt
# ---------------------------------------------------------------------------

def hero(slides, label, h1=''):
    arts, dots = '', ''
    n = len(slides)
    for i, s in enumerate(slides):
        img, alt, eyebrow, title, lede, cta, href_, pos, ppos = s
        on = i == 0
        head_tag = 'h2'
        arts += '''<article class="b-slide%s" role="group" aria-roledescription="slayt" aria-label="%d / %d: %s"%s>
%s
<div class="b-slide__text">
<p class="b-slide__kicker">%s</p>
<%s class="b-slide__title">%s</%s>
<p class="b-slide__lede">%s</p>
%s
</div>
</article>''' % (' is-active' if on else '', i + 1, n, re.sub('<[^>]+>', ' ', title).replace('  ', ' ').strip(),
                 '' if on else ' aria-hidden="true"',
                 picture(img, alt, 'b-slide__media', lazy=not on, pos=pos, ppos=ppos,
                         fetch='high' if on else ''),
                 eyebrow, head_tag, title, head_tag, lede,
                 link(cta, href_, 'b-link b-link--light', '' if on else ' tabindex="-1"'))
    # Kontrol yalnızca ileri/geri okları (müşteri isteği); ilerleme çubukları ve
    # durdur düğmesi yok. Otomatik geçiş üstüne gelince / odakta durur (b.js).
    # data-b-gl: WebGL görsel geçişi (b-gl.js); "8" dikey yırtılma, "7" çapraz şerit
    return '''<section class="b-hero" aria-roledescription="karusel" aria-label="%s" data-b-hero data-b-gl="8">
%s
<div class="b-hero__slides" aria-live="off">%s</div>
<div class="b-hero__ui">
<div class="b-hero__ctrl">
<button type="button" class="b-hero__btn" data-b-prev aria-label="Önceki slayt">%s</button>
<button type="button" class="b-hero__btn" data-b-next aria-label="Sonraki slayt">%s</button>
</div>
<p class="sr-only" aria-live="polite" data-b-status></p>
</div>
</section>''' % (label, h1, arts, ico('left'), ico('right'))


def pagehero(img, alt, trail, title, lede='', pos=None, ppos=None, cls=''):
    crumbs = ''.join('<li><a href="%s">%s</a></li>' % (h, t) for t, h in trail[:-1])
    crumbs += '<li aria-current="page">%s</li>' % trail[-1][0]
    return '''<section class="b-pagehero%s">
%s
<div class="b-pagehero__text b-wrap">
<nav aria-label="Sayfa konumu"><ol class="b-crumbs">%s</ol></nav>
<h1 class="b-pagehero__title">%s</h1>
%s
</div>
</section>''' % (' ' + cls if cls else '', picture(img, alt, 'b-pagehero__media', lazy=False, pos=pos,
                                                      ppos=ppos, fetch='high'),
                 crumbs, title, '<p class="b-pagehero__lede">%s</p>' % lede if lede else '')


def subnav(items, label):
    lis = ''.join('<li><a href="#%s">%s</a></li>' % (i, t) for i, t in items)
    return ('<nav class="b-subnav" aria-label="%s" data-b-subnav><div class="b-wrap"><ul>%s</ul></div></nav>'
            % (label, lis))


# ---------------------------------------------------------------------------
# 1. ANA SAYFA
# ---------------------------------------------------------------------------

HOME_SLIDES = [
    ('vsancaktepe', 'VSancaktepe Merkez konut bloklarının gün batımında görünümü',
     'İstanbul · Sancaktepe', 'VSancaktepe Merkez’de<br>Yaşam Başlıyor',
     'Anadolu Yakası’nın değerli yaşam merkezi VSancaktepe Merkez’de teslime özel avantajlardan yararlanma fırsatını kaçırmayın.', 'Detaylı Bilgi', 'vsancaktepe-merkez.html',
     '50% 50%', '62% 50%'),
    # Metinler kaynaktaki banner'lardan (yazım düzeltmeleri hariç birebir):
    # VYK — vakifgyo.com.tr ana sayfa slaytındaki haber başlığı ve haberin metni;
    # Cubes — cubesankara.com.tr banner'ı; 30. yıl — vakifgyo.com.tr ana sayfa
    # başlığı ve "Vakıf GYO 30 Yaşında" metni.
    ('vyenikonak', 'VYeniKonak ikiz kulelerinin akşamüstü görünümü',
     'İzmir · Konak', 'VYeniKonak proje<br>lansmanı gerçekleşti',
     'VYeniKonak; konut, ofis ve ticari alanları bir araya getiren karma kullanım konseptiyle '
     'İzmir’in gelişen ticaret ve yaşam aksına yeni bir değer kazandırmayı hedefliyor.',
     'Detaylı Bilgi', '#', '72% 50%', '50% 50%'),
    ('cubes', 'Cubes Ankara kulesinin akşam görünümü',
     'Ankara · Çukurambar', 'Peşin Ödemelerde 30. Yıla özel<br>%30 indirim kampanyası',
     'Ankara Çukurambar’da yer alan karma yaşam projemiz Cubes Ankara’da, peşin ödemelerde '
     '30. yıla özel %30 indirim fırsatı ile ofis/home ofis sahibi olma fırsatını kaçırmayın.',
     'Detaylı Bilgi', '#', '50% 40%', '50% 50%'),
    ('ifm', 'İstanbul Uluslararası Finans Merkezi’nde VakıfBank Genel Müdürlük binası, gece',
     'Vakıf GYO 30 Yaşında', 'Geleneğin Gücü,<br>Geleceğin İnşası',
     'Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak, 30 yıldır güçlü Türkiye’nin '
     'temellerini atıyoruz.', 'Hakkımızda', 'hakkimizda.html',
     '50% 50%', '50% 50%'),
]

# Etiketler Hakkımızda metnindeki ifadeler (_docs/kaynak/vakifgyo.txt, haberler.txt)
FIGURES = [
    ('1996', 'Türkiye’nin ilk Gayrimenkul Yatırım Ortaklığı Şirketi'),
    ('VKGYO', 'Borsa İstanbul'),
    ('9,48', 'Kurumsal Yönetim Derecelendirme Notu'),
]


def statement():
    figs = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (v, t) for v, t in FIGURES)
    return '''<section class="b-statement b-dark" id="devam" aria-labelledby="biz-baslik">
%s
<div class="b-wrap">
<h2 class="sr-only" id="biz-baslik">Vakıf GYO</h2>
<p class="b-statement__text">Geleneğimizden aldığımız güçle, geleceğin yaşam alanlarını inşa eder, paydaşlarımıza sürdürülebilir değer sunarız.</p>
<dl class="b-figures">%s</dl>
%s
</div>
</section>''' % (swoosh(), figs, link('Hakkımızda', 'hakkimizda.html', 'b-link b-link--light'))


# (anahtar, ad, LOKASYON, menü grubu, tanıtım cümlesi, bağlantı, görsel alt metni)
# Lokasyon ve cümleler vakifgyo.com.tr portföy sayfalarından birebir (_docs/kaynak/portfoy-portfoy-*.txt);
# grup adları menüden (Devam Eden Projeler / Tamamlanan Projeler).
INDEX = [
    ('vsancaktepe', 'VSancaktepe Merkez', 'İstanbul İli, Sancaktepe İlçesi', 'Devam Eden Projeler',
     'Konut ve ticari ünitelerden oluşan projemiz, nitelikli peyzaj kurgusu ve ferah mekanlarıyla İstanbul’da özlenen '
     'geleneksel aile hayatını, bahçeli, geniş balkon ve teraslı, sosyal aktiviteli şehir hayatıyla birleştirerek, '
     'pandemi sonrası değişen konut beklentilerini karşılamayı amaçlamaktadır.',
     'vsancaktepe-merkez.html', 'VSancaktepe Merkez blokları gün batımında'),
    ('vyenikonak', 'VYeniKonak', 'İzmir İli, Konak İlçesi, Mersinli Mahallesi', 'Devam Eden Projeler',
     'İş merkezi kulelerinin yükselmekte olduğu, İzmir Konak ilçesinde; ofis, ticari ve konut nitelikli VYeniKonak '
     'Projesi ile müşterilerimize konforlu, sağlıklı yaşam alanı sunmayı ve bölge potansiyelini artırmayı hedefliyoruz.', '#',
     'VYeniKonak ikiz kuleleri'),
    ('tablo-adalar', 'Tablo Adalar', 'İstanbul İli, Maltepe İlçesi, Zümrütevler Mahallesi', 'Tamamlanan Projeler',
     'İstanbul Anadolu Yakası\'nda yer alan, Marmara Denizi ve Adalar manzaralı, merkezi konumdaki "Tablo Adalar" '
     'projemiz, 1+1\'den 5+2\'e kadar değişen konut tiplerinin yanı sıra, geniş balkon, büyük peyzaj alanı ve zengin '
     'sosyal donatıları bulunduruyor.', '#', 'Tablo Adalar konut blokları'),
    ('cubes', 'Cubes Ankara', 'Ankara İli, Çankaya İlçesi, Çukurambar Mahallesi', 'Tamamlanan Projeler',
     'Ankara Çukurambar\'da yer alan Cubes Ankara Projemiz; 215.984,66 m2 kapalı inşaat alanına sahip 1+1\'den, '
     '6+1\'e kadar değişen konut, home office, ofis ile otel, ticari ve sosyal donatı alanlarından oluşuyor.',
     'cubes-ankara.html', 'Cubes Ankara kulesi'),
    ('ifm', 'İstanbul Uluslararası Finans Merkezi', 'İstanbul İli, Ümraniye İlçesi, Küçükbakkalköy Mahallesi',
     'Tamamlanan Projeler',
     'İstanbul\'da yükselen Finans Merkezi Projesi içerisinde yer alan VakıfBank Genel Müdürlük Hizmet Binası ve '
     'Tesisleri projemiz, 261.537 m2 inşaat alanıyla 52 ve 36 katlı iki kuleden oluşuyor.', '#',
     'İstanbul Uluslararası Finans Merkezi’nde VakıfBank kuleleri'),
    ('aydos', 'Bizimtepe Aydos', 'İstanbul İli, Sancaktepe İlçesi, Samandıra Mahallesi', 'Tamamlanan Projeler',
     'Projede sosyal donatı alanları, açık-kapalı yüzme havuzları ve yaklaşık 80 dönüm peyzaj alanı bulunmaktadır.',
     '#', 'Bizimtepe Aydos konut blokları'),
]


# Proje logoları (elde olanlar; IFM ve Bizimtepe Aydos için logo yok)
INDEX_LOGOS = {
    'vsancaktepe': GYO + 'logo-vsancaktepe-renkli.svg',
    'vyenikonak': GYO + 'logo-vyenikonak-renkli.svg',
    'tablo-adalar': GYO + 'logo-tablo-adalar-renkli.svg',
    'cubes': GYO + 'logo-cubes-ankara-renkli.png',
}


def project_index():
    rows, prev = '', ''
    for i, (key, name, place, status, desc, h, alt) in enumerate(INDEX):
        src = '%sdizin-%s-%s.jpg' % (IMG, key, '640x800' if key == 'tablo-adalar' else '1280x1600')
        logo = ('<img class="b-index__logo" src="%s" alt="" loading="lazy" decoding="async">' % INDEX_LOGOS[key]
                if key in INDEX_LOGOS else '')
        rows += '''<li class="b-index__row%s" data-b-key="%s">
<a class="b-index__link" href="%s">
<span class="b-index__name">%s</span>
<span class="b-index__meta">%s · %s</span>
<span class="b-index__desc">%s</span>
%s
</a>
<img class="b-index__thumb" src="%s" alt="" width="640" height="800" loading="lazy" decoding="async">
</li>''' % (' is-active' if i == 0 else '', key, h, name, place, status, desc, logo, src)
        prev += ('<img class="b-index__img%s" data-b-key="%s" src="%s" alt="%s" width="640" height="800" loading="lazy" decoding="async">'
                 % (' is-active' if i == 0 else '', key, src, alt))
    return '''<section class="b-index b-section" id="projeler" aria-labelledby="projeler-baslik">
<div class="b-wrap">
%s
<div class="b-index__grid" data-b-index>
<ol class="b-index__list">%s</ol>
<div class="b-index__preview" aria-hidden="true">%s</div>
</div>
</div>
</section>''' % (section_head('Portföy', 'projeler-baslik',
                              more=link('Devam Eden Projeler', '#')), rows, prev)


def band(img, alt, title, hid, text, links, extra='', pos=None, ppos=None, cls='', sid=None):
    ls = ''.join('<li>%s</li>' % link(t, h, 'b-link b-link--light') for t, h in links)
    return '''<section class="b-band%s"%s aria-labelledby="%s">
%s
<div class="b-band__text b-wrap">
<h2 class="b-band__title" id="%s">%s</h2>
%s
%s
<ul class="b-band__links">%s</ul>
</div>
</section>''' % (' ' + cls if cls else '', ' id="%s"' % sid if sid else '', hid,
                 picture(img, alt, 'b-band__media', pos=pos, ppos=ppos),
                 hid, title, '<p class="b-band__lede">%s</p>' % text if text else '', extra, ls)


def portfolio():
    # Adet sayacı yok (6 mülk / 4 arsa / 1 proje): ucuz duruyor; başlık ve bağlantılar yeter.
    return band('aydos-ticari', 'Bizimtepe Aydos ticari üniteleri ve peyzajlı iç avlu, kuşbakışı',
                'Gayrimenkul Yatırımları', 'portfoy-baslik', '',
                [('Gayrimenkul Proje', '#'), ('Gayrimenkul Mülk', '#'), ('Gayrimenkul Arsa', '#')],
                pos='50% 60%')


def sparkline():
    s = ap.SERIES
    W, H = 320, 72
    lo, hi = min(s), max(s)
    pts = ' '.join('%.1f,%.1f' % (W * i / (len(s) - 1), 4 + (H - 8) * (1 - (v - lo) / (hi - lo)))
                   for i, v in enumerate(s))
    return ('<svg class="b-spark" viewBox="0 0 %d %d" role="img" aria-label="VKGYO: %s ₺ ile %s ₺ arasında" '
            'preserveAspectRatio="none"><polyline points="%s"/></svg>' % (W, H, ap.tl(lo), ap.tl(hi), pts))


def ir_teaser():
    disc = doclist([(d, '', t, 'KAP', 'yatirimci-iliskileri.html#aciklamalar') for d, t in ap.DISCLOSURES[:3]],
                   'b-docs--compact')
    return '''<section class="b-ir b-section" aria-labelledby="ir-baslik">
<div class="b-wrap b-ir__grid">
<figure class="b-ir__media">
<img src="%sifm-gece-1100.jpg" srcset="%s" sizes="(min-width: 1200px) 40vw, (min-width: 768px) 45vw, 100vw" alt="İstanbul Uluslararası Finans Merkezi’nde VakıfBank kulesi, gece" width="1100" height="1375" loading="lazy" decoding="async">
</figure>
<div class="b-ir__body">
%s
<div class="b-quote">
<div class="b-quote__px"><span class="b-quote__code">VKGYO</span><strong>3,27 ₺</strong><span class="b-up">▲ %%1,24</span></div>
%s
<dl class="b-quote__stats"><div><dt>Piyasa değeri</dt><dd>%s milyar ₺</dd></div><div><dt>52 hafta</dt><dd>%s – %s ₺</dd></div></dl>
</div>
<h3 class="b-h4">Özel Durum Açıklamaları</h3>
%s
<div class="b-actions">%s%s</div>
</div>
</div>
</section>''' % (IMG, ', '.join('%sifm-gece-%d.jpg %dw' % (IMG, w, w) for w in (720, 1100, 1600)),
                 section_head('Yatırımcı İlişkileri', 'ir-baslik'),
                 sparkline(), ap.tl(3.27 * 4.4), ap.tl(min(ap.SERIES)), ap.tl(max(ap.SERIES)), disc,
                 btn('Yatırımcı İlişkileri', 'yatirimci-iliskileri.html', 'b-btn--dark'),
                 btn('Raporlar ve Yatırımcı Sunumları', 'yatirimci-iliskileri.html#raporlar', 'b-btn--ghost'))


NEWS = [
    # _docs/kaynak/haberler.txt — başlık ve tarih birebir
    ('haber-yasam-basliyor-1200x800.jpg', '2026-09-15', 'VSancaktepe Merkez’de Yaşam Başlıyor'),
    ('haber-vyenikonak-lansman-800x533.jpg', '2026-10-05', 'VYeniKonak proje lansmanı gerçekleşti'),
    ('haber-derecelendirme-1200x800.jpg', '2026-09-18',
     'Kurumsal Yönetim Derecelendirme Notumuzu 9,42’den 9,48’e çıkardık'),
    ('haber-tsrs-800x533.jpg', '2026-08-09', '2025 TSRS Uyumlu Sürdürülebilirlik Raporumuz yayınlandı'),  # haber-tsrs.txt
]


def news():
    cards = ''.join('''<li class="b-card">
<a href="#">
<span class="b-card__media"><img src="%s%s" alt="" loading="lazy" decoding="async"></span>
%s
<span class="b-card__title">%s</span>
</a>
</li>''' % (IMG, img, '<span class="b-card__meta"><time datetime="%s">%s</time></span>' % (d, tr_date(d)) if d else '', t)
        for img, d, t in NEWS)
    return '''<section class="b-news b-section b-stone" aria-labelledby="haber-baslik">
<div class="b-wrap">
%s
<ul class="b-cards">%s</ul>
</div>
</section>''' % (section_head('Haberler', 'haber-baslik',
                              more=link('Güncel', '#')), cards)


def sustain():
    return band('sektor', 'Yeşil teras ve koşu yolu bulunan ofis kulesi, akşam',
                'Sürdürülebilirlik', 'surd-baslik',
                'Sürdürülebilirlik, Vakıf GYO’nun temel stratejilerinden biridir. Çevresel, sosyal ve yönetişim (ESG) prensipleriyle faaliyet gösteren şirketimiz, gelecek nesillere daha yaşanabilir bir dünya bırakmayı amaçlamaktadır.',
                [('Kilometre Taşları', '#'), ('Raporlar ve Sertifikalar', '#'),
                 ('Kurumsal Sosyal Sorumluluk', '#')], pos='50% 55%', cls='b-band--right')


def contact_cta():
    return '''<section class="b-cta b-dark" aria-labelledby="cta-baslik">
<div class="b-wrap b-cta__grid">
<div>
<h2 class="b-h2" id="cta-baslik">Detaylı bilgi almak ve örnek dairemizi ziyaret etmek için bize ulaşın.</h2>
</div>
<div class="b-actions">%s%s<a class="b-cta__phone" href="%s">%s%s</a></div>
</div>
</section>''' % (btn('Ön Talep Formu', '#', 'b-btn--yellow'), btn('Satış Ofisi', '#', 'b-btn--ghost-light'),
                 PHONE[0], ico('phone'), PHONE[1])


def hero_video():
    # 30. yıl reklam filminin yazısız sahneleri (_build/make_video_30yil.py); banner metni yok.
    # Dikey telefon ekranında 9:16 merkez kesim, diğerlerinde 16:9. Ses yok, döngü; durdurulabilir.
    V = '../assets/video/'
    return '''<section class="b-hero b-hero--video" aria-label="Vakıf GYO 30. yıl filmi">
<h1 class="sr-only">Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası</h1>
<video class="b-hero__video" autoplay muted loop playsinline preload="auto" poster="%sb-30yil-poster-1600x900.jpg" aria-hidden="true" data-b-video>
<source src="%sb-30yil-608x1080.mp4" type="video/mp4" media="(orientation: portrait) and (max-width: 899px)">
<source src="%sb-30yil-1600x900.mp4" type="video/mp4">
</video>
<div class="b-hero__ui">
<button type="button" class="b-hero__btn b-hero__toggle" aria-pressed="false" data-b-video-toggle><span class="sr-only" data-b-video-label>Videoyu durdur</span>%s%s</button>
</div>
<a class="b-scrolldown" href="#devam"><span class="sr-only">Aşağı kaydır</span>%s</a>
</section>''' % (IMG, V, V, ico('pause', 'b-ico--pause'), ico('play', 'b-ico--play'), ico('down'))


def index_video():
    body = '\n'.join([hero_video(), statement(), project_index(), portfolio(), ir_teaser(), news(), sustain(),
                      contact_cta()])
    return page('Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası',
                'Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası. Kurumsal · Portföy · Yatırımcı İlişkileri · '
                'Güncel · Sürdürülebilirlik · Bize Ulaşın', body, body_cls='b--home b--video')


def index():
    body = '\n'.join([
        hero(HOME_SLIDES, 'Öne çıkan projeler',
             '<h1 class="sr-only">Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası</h1>'),
        statement(), project_index(), portfolio(), ir_teaser(), news(), sustain(), contact_cta()])
    return page('Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası',
                'Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası. Kurumsal · Portföy · Yatırımcı İlişkileri · '
                'Güncel · Sürdürülebilirlik · Bize Ulaşın', body, body_cls='b--home')


# ---------------------------------------------------------------------------
# 2. YATIRIMCI İLİŞKİLERİ
# ---------------------------------------------------------------------------

# Bölüm adları vakifgyo.com.tr Yatırımcı İlişkileri menüsünden (_docs/kaynak/portfoy-yatirimci-iliskileri.txt)
IR_NAV = [('hisse', 'VKGYO'), ('aciklamalar', 'Özel Durum Açıklamaları'), ('genel-kurul', 'Genel Kurul'),
          ('raporlar', 'Raporlar ve Yatırımcı Sunumları'), ('kurumsal-yonetim', 'Kurumsal Yönetim'),
          ('iletisim', 'Yatırımcı İlişkileri İletişim')]


def chart():
    """A'daki seri; çizim B'nin diliyle (ince çizgi, sarı vurgu)."""
    s = ap.SERIES
    W, H, L, R, T, B = 720, 300, 44, 12, 16, 32
    lo, hi = 1.5, 3.5
    pw, ph = W - L - R, H - T - B

    def x(i):
        return L + pw * i / (len(s) - 1)

    def y(v):
        return T + ph * (1 - (v - lo) / (hi - lo))
    grid = ''.join('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="b-chart__grid"/>'
                   '<text x="%d" y="%.1f" class="b-chart__ylab">%s</text>'
                   % (L, W - R, y(g), y(g), L - 8, y(g) + 4, ap.tl(g, 1)) for g in (1.5, 2.0, 2.5, 3.0, 3.5))
    xl = ''.join('<text x="%.1f" y="%d" class="b-chart__xlab%s">%s</text>'
                 % (x(round(m * 52 / 12)), H - 8, ' b-chart__xlab--odd' if m % 2 else '', ap.MONTHS[m])
                 for m in range(12))
    pts = ' '.join('%.1f,%.1f' % (x(i), y(v)) for i, v in enumerate(s))
    area = 'M%.1f,%.1f L%s L%.1f,%.1f Z' % (x(0), y(lo), pts.replace(' ', ' L'), x(len(s) - 1), y(lo))
    rows = ''.join('<tr><th scope="row">%s</th><td>%s ₺</td></tr>'
                   % (ap.MONTHS_LONG[m], ap.tl(s[min(51, round((m + 1) * 52 / 12) - 1)])) for m in range(12))
    return '''<figure class="b-chart" data-b-chart data-series="%s" data-start="2025-10-03" data-lo="%s" data-hi="%s" data-box="%d,%d,%d,%d,%d,%d">
<figcaption class="b-chart__cap">VKGYO · ₺</figcaption>
<div class="b-chart__plot">
<svg viewBox="0 0 %d %d" role="img" aria-label="VKGYO hisse fiyatı son 52 haftada %s ₺ ile %s ₺ arasında, son kapanış %s ₺. Sol ve sağ ok tuşlarıyla haftalar arasında gezinebilirsiniz." focusable="false">
%s%s
<path d="%s" class="b-chart__area"/>
<polyline points="%s" class="b-chart__line"/>
<line class="b-chart__cross" x1="0" x2="0" y1="%d" y2="%d"/>
<circle class="b-chart__dot" r="5" cx="%.1f" cy="%.1f"/>
</svg>
<div class="b-chart__tip" role="status" aria-live="polite" hidden></div>
</div>
<details class="b-chart__table"><summary>Tablo olarak göster</summary>
<table><caption class="sr-only">VKGYO</caption><thead><tr><th scope="col">Ay</th><th scope="col">Kapanış</th></tr></thead><tbody>%s</tbody></table>
</details>
</figure>''' % (','.join('%.2f' % v for v in s), lo, hi, W, H, L, R, T, B, W, H,
                ap.tl(min(s)), ap.tl(max(s)), ap.tl(s[-1]), grid, xl, area, pts, T, H - B,
                x(len(s) - 1), y(s[-1]), rows)


def ir_stock():
    shares = 4_400_000_000
    stats = [('Günlük değişim', '<span class="b-up">▲ %1,24</span>'), ('İşlem hacmi', '186,4 milyon ₺'),
             ('Piyasa değeri', '%s milyar ₺' % ap.tl(ap.SERIES[-1] * shares / 1e9)),
             ('52 hafta en düşük', '%s ₺' % ap.tl(min(ap.SERIES))),
             ('52 hafta en yüksek', '%s ₺' % ap.tl(max(ap.SERIES))), ('Pazar', 'Yıldız Pazar')]
    dl = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % s for s in stats)
    return '''<section class="b-section" id="hisse" aria-labelledby="hisse-baslik">
<div class="b-wrap">
%s
<div class="b-stock">
<div class="b-stock__side">
<p class="b-stock__code">VKGYO <span>Borsa İstanbul</span></p>
<p class="b-stock__px">%s<small> ₺</small></p>
<dl class="b-stock__stats">%s</dl>
<div class="b-actions">%s%s</div>
</div>
%s
</div>
</div>
</section>''' % (section_head('VKGYO', 'hisse-baslik'), ap.tl(ap.SERIES[-1]), dl,
                 link('Sermaye Artırımı & Temettü Duyuruları'), '', chart())


def ir_kpis():
    tiles = ''.join('<li><span class="b-kpi__value">%s<small> %s</small></span><span class="b-kpi__label">%s</span></li>'
                    % (v, u, l) for l, v, u in ap.KPIS)
    return '''<section class="b-section b-stone" id="ozet" aria-labelledby="ozet-baslik">
<div class="b-wrap">
%s
<ul class="b-kpis">%s</ul>
<p class="b-note">Göstergeler temsilîdir; ödenmiş sermaye dışındaki tutarlar örnek değerlerdir.</p>
</div>
</section>''' % (section_head('Özet Veriler', 'ozet-baslik', '30 Haziran 2026 itibarıyla, konsolide olmayan.',
                              more=link('Özet Finansallar (Excel)')), tiles)


RESULT_DOCS = [('2026-07-31', 'Yönetim Kurulu Faaliyet Raporu'), ('2026-08-20', 'Yatırımcı Sunumu'),
               ('2026-07-30', 'Finansal Tablolar ve Dipnotlar')]


def ir_results():
    docs = doclist([(d, '', t, 'PDF', '#') for d, t in RESULT_DOCS], 'b-docs--light')
    return '''<section class="b-split b-dark" id="sonuclar" aria-labelledby="sonuc-baslik">
<picture class="b-split__media"><img src="%sifm-gunduz-1100.jpg" srcset="%s" sizes="(min-width: 900px) 50vw, 100vw" alt="İstanbul Uluslararası Finans Merkezi’nde VakıfBank kuleleri, gündüz" width="1100" height="1375" loading="lazy" decoding="async" style="--pos:50%% 40%%"></picture>
<div class="b-split__body">
<h2 class="b-h2" id="sonuc-baslik">Finansal Sonuçlar</h2>
<p class="b-lede">30 Haziran 2026 dönemi finansal tabloları, faaliyet raporu ve yatırımcı sunumu.</p>
%s
%s
</div>
</section>''' % (IMG, ', '.join('%sifm-gunduz-%d.jpg %dw' % (IMG, w, w) for w in (720, 1100, 1600)),
                 docs, link('Tüm Finansal Sonuçlar', '#', 'b-link b-link--light'))


def ir_disclosures():
    left = doclist([(d, '', t, 'KAP', '#') for d, t in ap.DISCLOSURES])
    return '''<section class="b-section" aria-label="Açıklamalar ve genel kurul">
<div class="b-wrap b-cols">
<div id="aciklamalar">
%s
%s
</div>
<div id="genel-kurul" class="b-panel">
<h2 class="b-h3" id="gk-baslik">Genel Kurul</h2>
<p>2025 Yılı Olağan Genel Kurulumuzu, 17 Nisan 2026 tarihinde gerçekleştirdik.</p>
%s
</div>
</div>
</section>''' % (section_head('Özel Durum Açıklamaları', 'aciklama-baslik'), left, link('Devamını Oku'))


# Rapor adları ve açıklama haberlerden birebir (_docs/kaynak/haberler.txt, haber-tsrs.txt)
REPORTS = [
    ('ir-faaliyet-raporu-2025-372x526.jpg', '2025 Yılı Faaliyet Raporu', ''),
    ('ir-tsrs-2025-372x526.jpg', '2025 TSRS Uyumlu Sürdürülebilirlik Raporu',
     'Türkiye Sürdürülebilirlik Raporlama Standartları (TSRS) ile uyumlu olarak hazırladığımız 2025 TSRS Uyumlu '
     'Sürdürülebilirlik Raporumuzda; sürdürülebilirlik yaklaşımımızı, çevresel, sosyal ve yönetişim alanındaki '
     'çalışmalarımızı ve performansımızı paydaşlarımızla şeffaf bir şekilde paylaşıyoruz.'),
]


def ir_reports():
    covers = ''.join('''<li class="b-report">
<img src="%s%s" alt="" width="186" height="263" loading="lazy">
<div><h3 class="b-h4">%s</h3>%s%s</div>
</li>''' % (GYO, img, t, '<p>%s</p>' % d if d else '', link('Devamını Oku', '#', 'b-link', ''))
                     for img, t, d in REPORTS)
    return '''<section class="b-section b-stone" id="raporlar" aria-labelledby="rapor-baslik">
<div class="b-wrap">
%s
<ul class="b-reports b-reports--row">%s</ul>
</div>
</section>''' % (section_head('Raporlar ve Yatırımcı Sunumları', 'rapor-baslik'), covers)


def ir_calendar():
    items = ''.join('<li><span class="b-cal__date">%s</span><span class="b-cal__title">%s</span>'
                    '<a href="#" class="b-cal__add">%s<span>Takvime ekle</span></a></li>'
                    % (d, t, ico('plus')) for d, t in a.CALENDAR)
    return '''<section class="b-section" id="takvim" aria-labelledby="takvim-baslik">
<div class="b-wrap">
%s
<ol class="b-cal">%s</ol>
<p class="b-note">Tarihler temsilîdir · Kesin tarihler KAP’ta duyurulur.</p>
</div>
</section>''' % (section_head('Finansal Takvim', 'takvim-baslik'), items)


def ir_governance():
    # Cümle haber başlığı (_docs/kaynak/haberler.txt); bağlantılar Kurumsal Yönetim menüsünden (menu.txt)
    return band('medyan', 'Medyan Kadıköy projesi ve İstanbul silüeti, alacakaranlık',
                'Kurumsal Yönetim', 'ky-baslik',
                'Kurumsal Yönetim Derecelendirme Notumuzu 9,42’den 9,48’e çıkardık.',
                [('Kurumsal Yönetim İlkelerine Uyum Raporları', '#'), ('Kar Dağıtım Politikası', '#'),
                 ('Bilgilendirme Politikası', '#')],
                pos='40% 60%', sid='kurumsal-yonetim')


# Yatırımcı İlişkileri menüsü (_docs/kaynak/portfoy-yatirimci-iliskileri.txt, menu.txt)
IR_LINKS = [('Yatırımcı İlişkileri İletişim', '#'), ('Duyurular', '#'), ('Sürekli Bilgilendirme Formu', '#'),
            ('Gayrimenkul Değerleme Raporları', '#'), ('Sermaye Artırımı & Temettü Duyuruları', '#'),
            ('Sıkça Sorulan Sorular', '#')]


def ir_services():
    tiles = ''.join('<li>%s</li>' % link(t, h, 'b-tile') for t, h in IR_LINKS)
    return '''<section class="b-section b-stone" id="iletisim" aria-labelledby="hizmet-baslik">
<div class="b-wrap">
%s
<ul class="b-tiles">%s</ul>
</div>
</section>''' % (section_head('Yatırımcı İlişkileri İletişim', 'hizmet-baslik'), tiles)


def ir_page():
    body = '\n'.join([
        pagehero('ifm', 'İstanbul Uluslararası Finans Merkezi’nde VakıfBank Genel Müdürlük binası, gece',
                 [('Ana Sayfa', 'index.html'), ('Yatırımcı İlişkileri', '#')], 'Yatırımcı İlişkileri'),
        subnav(IR_NAV, 'Yatırımcı İlişkileri bölümleri'),
        ir_stock(), ir_disclosures(), ir_reports(), ir_governance(), ir_services()])
    return page('Yatırımcı İlişkileri — Vakıf GYO',
                'Yatırımcı İlişkileri İletişim · Duyurular · Özel Durum Açıklamaları · Raporlar ve Yatırımcı '
                'Sunumları · Genel Kurul · Kurumsal Yönetim',
                body, shell=(rail('yatirimci'), footer()))


# ---------------------------------------------------------------------------
# 3. VSANCAKTEPE MERKEZ — proje sitesi (kendi alan adında, kendi kabuğu)
# ---------------------------------------------------------------------------

VS_LOGO = IMG + 'vs-logo-ters.svg'
VS_PHONE = ap.VS_PHONE
# Menü: vsancaktepe.com.tr başlıkları (_docs/kaynak/vsancaktepe-site.txt); Konut Kredisi Hesaplama önerilen site haritasından
# Sıra vsancaktepe.com.tr menüsünü izler: Proje Hakkında · Daire Planları · İlerleme Durumu · Sanal Tur · Konum
VS_MENU = [('proje', 'Proje Hakkında'), ('daireler', 'Daire Planları'), ('ozellikler', 'Merkezinde Doğallık Var'),
           ('galeri', 'Galeri'), ('ilerleme', 'İlerleme Durumu'), ('sanal-tur', 'Sanal Tur'), ('konum', 'Konum'),
           ('hesaplama', 'Konut Kredisi Hesaplama'), ('on-talep', 'İletişim Formu')]
VS_TOUR = ap.VS_TOUR


def vs_rail():
    items = ('<li class="b-nav__item b-nav__item--home"><a class="b-nav__home" href="index.html">'
             '<img src="%s" alt="Vakıf GYO ana sayfa" width="118" height="20"></a></li>' % LOGO)
    items += ''.join('<li class="b-nav__item"><a class="b-nav__btn" href="#%s"><span>%s</span></a></li>' % m
                     for m in VS_MENU)
    return '''<header class="b-rail b-rail--project" data-b-rail>
<div class="b-rail__bar">
<a class="b-rail__logo b-rail__logo--project" href="vsancaktepe-merkez.html"><img src="%s" alt="VSancaktepe Merkez ana sayfa" width="160" height="74"></a>
<button type="button" class="b-burger" aria-expanded="false" aria-controls="b-menu" data-b-burger><span class="sr-only">Menü</span>%s%s</button>
</div>
<div class="b-rail__menu" id="b-menu">
<nav class="b-nav b-nav--anchors" aria-label="Proje menüsü"><ul>%s</ul></nav>
<div class="b-rail__foot">
<p class="b-rail__office">%s<span>Satış Ofisi</span></p>
<a class="b-rail__phone" href="%s">%s<span>%s</span></a>
%s
<a class="b-rail__byline" href="index.html"><span>Vakıf GYO güvencesiyle</span><img src="%s" alt="Vakıf GYO" width="120" height="20"></a>
</div>
</div>
</header>''' % (VS_LOGO, ico('menu', 'b-burger__open'), ico('close', 'b-burger__close'), items,
                ico('pin'), VS_PHONE[0], ico('phone'), VS_PHONE[1],
                btn('İletişim Formu', '#on-talep', 'b-btn--yellow b-btn--block'), LOGO)


def vs_footer():
    return '''<footer class="b-foot b-foot--project">
%s
<div class="b-wrap">
<div class="b-foot__top">
<div class="b-foot__brand">
<img src="%s" alt="VSancaktepe Merkez" width="160" height="74" loading="lazy">
<a class="b-foot__phone" href="%s">%s</a>
<p class="b-foot__addr">Satış Ofisi</p>
</div>
<div class="b-foot__col"><p class="b-foot__head">Proje Hakkında</p><ul>
<li><a href="#proje">Vaziyet Planı</a></li><li><a href="#daireler">Daire Planları</a></li>
<li><a href="#ilerleme">İlerleme Durumu</a></li><li><a href="#sanal-tur">Sanal Tur</a></li><li><a href="#konum">Konum</a></li></ul></div>
<div class="b-foot__col"><p class="b-foot__head">Tanıtım</p><ul>
<li><a href="#">Tanıtım Filmi</a></li><li><a href="#">Reklam Filmi</a></li>
<li><a href="#">Tanıtım Broşürü</a></li><li><a href="#on-talep">İletişim Formu</a></li></ul></div>
<div class="b-foot__col"><p class="b-foot__head">Portföy</p><ul>
<li><a href="#">VYeniKonak</a></li><li><a href="#">Tablo Adalar</a></li><li><a href="#">Cubes Ankara</a></li></ul></div>
</div>
<div class="b-foot__guarantee">
<a href="index.html"><img src="%s" alt="Vakıf GYO" width="150" height="26" loading="lazy"></a>
<p>Vakıf GYO güvencesiyle</p>
</div>
<div class="b-foot__bottom">
<p>VakıfBank Finans Grubu İştirakidir.</p>
<ul><li><a href="#">Gizlilik ve Kişisel Verilerin Korunması</a></li></ul>
</div>
</div>
</footer>''' % (swoosh(), VS_LOGO, VS_PHONE[0], VS_PHONE[1], LOGO)


def vs_hero():
    return '''<section class="b-hero b-hero--single" aria-label="VSancaktepe Merkez">
<div class="b-hero__slides">
<article class="b-slide is-active">
%s
<div class="b-slide__text">
<p class="b-slide__kicker">İstanbul · Sancaktepe</p>
<h1 class="b-slide__title">VSancaktepe Merkez’de<br>Yaşam Başlıyor</h1>
<p class="b-slide__lede">Anadolu Yakası’nın değerli yaşam merkezi VSancaktepe Merkez’de teslime özel avantajlardan yararlanma fırsatını kaçırmayın.</p>
<div class="b-actions">%s%s</div>
</div>
</article>
</div>
</section>''' % (picture('vsancaktepe', 'VSancaktepe Merkez konut bloklarının gün batımında görünümü',
                         'b-slide__media', lazy=False, pos='50% 50%', ppos='62% 50%', fetch='high'),
                 btn('Sanal Tur' + NEW_TAB, VS_TOUR, 'b-btn--yellow', ' target="_blank" rel="noopener"'),
                 btn('Daire Planları', '#daireler', 'b-btn--ghost-light'))


# DETAYLAR: vakifgyo.com.tr proje sayfası (_docs/kaynak/portfoy-portfoy-vsancaktepe-merkez.txt)
VS_FACTS = [('Lokasyon', 'İstanbul İli, Sancaktepe İlçesi'), ('İnşaat Alanı', '58.133,42 m2'), ('Ada / Parsel', '6770 / 2')]


def vs_about():
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in VS_FACTS)
    return '''<section class="b-section" id="proje" aria-labelledby="proje-baslik">
<div class="b-wrap b-about">
<div class="b-about__text">
<h2 class="b-h2" id="proje-baslik">Proje Hakkında</h2>
<p class="b-lede">Hayalinizdeki huzurlu ve güvenli yaşam alanını Vakıf GYO güvencesiyle sunan VSancaktepe Merkez, yenilikçi mimarisi, geniş yeşil alanları ve çevre dostu özellikleriyle sizi ve sevdiklerinizi bekliyor.</p>
<dl class="b-facts">%s</dl>
</div>
<figure class="b-about__media">
<img src="%svs-ozet-1078x944.jpg" alt="VSancaktepe Merkez vaziyet planı: bloklar, iç avlu ve çevre yolları kuşbakışı" width="1078" height="944" loading="lazy">
<figcaption>Vaziyet planı</figcaption>
</figure>
</div>
</section>''' % (facts, GYO)


# Oda adları ve ölçüler vsancaktepe.com.tr Daire Planları sayfasıyla birebir (_docs/kaynak/vsancaktepe-daire-planlari.txt)
PLANS = [
    ('1-1', '1+1', 'B 4 Tipi', [('Antre', '6,98'), ('Salon & Mutfak', '22,64'), ('Yatak Odası', '13,35'),
                                ('Banyo', '3,88'), ('Çamaşır Nişi', '0,63'), ('Balkon', '8,96')],
     '47,52', '64,36', '80,29'),
    ('2-1', '2+1', 'A 1 Tipi', [('Antre', '4,04'), ('Salon', '26,48'), ('Mutfak', '10,03'),
                                ('Yatak Odası', '10,68'), ('E.Yatak Odası', '17,17'), ('Banyo', '4,57'),
                                ('E.Banyo', '4,56'), ('Çamaşır Nişi', '0,70'), ('Hol', '6,73'), ('Balkon', '9,63')],
     '84,96', '106,46', '130,52'),
    ('3-1', '3+1', 'C 2 Tipi', [('Antre', '12,32'), ('Salon', '31,29'), ('Mutfak', '12,57'),
                                ('Yatak Odası 1', '12,87'), ('Yatak Odası 2', '10,76'), ('E.Yatak Odası', '24,47'),
                                ('Banyo', '3,91'), ('E.Banyo', '4,03'), ('Çamaşır Nişi', '0,95'), ('Hol', '4,69'),
                                ('Balkon', '17,15')],
     '117,93', '150,44', '189,06'),
    ('4-1', '4+1', 'A Tipi', [('Antre', '12,61'), ('Salon', '37,51'), ('Oturma Odası', '21,86'), ('Mutfak', '14,38'),
                              ('Yatak Odası 1', '12,81'), ('Yatak Odası 2', '19,04'), ('E.Yatak Odası', '31,17'),
                              ('Banyo 1', '4,66'), ('Banyo 2', '4,00'), ('E.Banyo', '5,58'), ('İşlik', '2,32'),
                              ('Hol', '9,30'), ('Hizmetli Odası', '7,13'), ('Merdiven', '7,28'), ('Balkon', '13,51'),
                              ('Teras', '4,30')],
     '189,65', '240,71', '324,67'),
]


# Plandaki numaralı oda işaretlerinin konumu (orijinal plan görselinin pikselleri, gorseller/.../Daire Planları).
# Numaralar görseldeki rakamlarla eşleşir; balkon/teras işaretsiz. Görsel boyutu: (genişlik, yükseklik).
PLAN_SPOTS = {
    '1-1': ((864, 700), {'Antre': (362, 513), 'Salon & Mutfak': (520, 426), 'Banyo': (268, 517),
                         'Yatak Odası': (299, 382), 'Çamaşır Nişi': (406, 404)}),
    '2-1': ((810, 575), {'Antre': (483, 447), 'Salon': (633, 378), 'Mutfak': (465, 276), 'Yatak Odası': (333, 239),
                         'E.Yatak Odası': (160, 337), 'Banyo': (334, 453), 'E.Banyo': (150, 452),
                         'Çamaşır Nişi': (238, 447), 'Hol': (360, 389)}),
    '3-1': ((960, 522), {'Antre': (566, 141), 'Salon': (754, 178), 'Mutfak': (590, 264), 'Yatak Odası 1': (474, 304),
                         'Yatak Odası 2': (226, 146), 'E.Yatak Odası': (288, 304), 'Banyo': (341, 109),
                         'E.Banyo': (355, 239), 'Çamaşır Nişi': (425, 116), 'Hol': (364, 160)}),
    '4-1': ((918, 566), {'Antre': (460, 185), 'Salon': (622, 173), 'Oturma Odası': (378, 112), 'Mutfak': (307, 210),
                         'Yatak Odası 1': (338, 365), 'Yatak Odası 2': (276, 455), 'E.Yatak Odası': (608, 412),
                         'Banyo 1': (424, 120), 'Banyo 2': (398, 468), 'E.Banyo': (580, 468), 'İşlik': (505, 468),
                         'Hol': (458, 448), 'Hizmetli Odası': (404, 393), 'Merdiven': (497, 335)}),
}
# vs-plan-*-1440.jpg: orijinalin boş kenarları kırpılmış (make_images_pages.PLAN_CROP ile aynı kutu),
# planın kendi oranında, %2 kenar payı
PLAN_CROP = {'1-1': (176, 27, 687, 673), '2-1': (64, 32, 748, 546),
             '3-1': (81, 42, 880, 480), '4-1': (78, 43, 843, 524)}
PLAN_W, PLAN_PAD = 1440, 0.02


def plan_crop_size(key):
    x0, y0, x1, y1 = PLAN_CROP[key]
    return x1 - x0, y1 - y0


def plan_dims(key):
    w, h = plan_crop_size(key)
    return PLAN_W, round(PLAN_W * h / w)


def plan_spot_pct(key, x, y):
    x0, y0 = PLAN_CROP[key][:2]
    w, h = plan_crop_size(key)
    W, H = plan_dims(key)
    s = min(W * (1 - 2 * PLAN_PAD) / w, H * (1 - 2 * PLAN_PAD) / h)
    dw, dh = round(w * s), round(h * s)
    ox, oy = (W - dw) // 2, (H - dh) // 2
    return (ox + (x - x0) * s) / W * 100, (oy + (y - y0) * s) / H * 100


def plan_spots(key, rooms):
    out = ''
    spots = PLAN_SPOTS[key][1]
    for i, (name, area) in enumerate(rooms):
        if name not in spots:
            continue
        px, py = plan_spot_pct(key, *spots[name])
        cls = ' b-spot--below' if py < 18 else ''
        cls += ' b-spot--left' if px < 14 else (' b-spot--right' if px > 86 else '')
        out += ('<li><button type="button" class="b-spot%s" style="--x:%.2f%%;--y:%.2f%%" data-b-spot="%s-%d" '
                'aria-label="%s, %s m²"><span class="b-spot__tip">%s<b>%s m²</b></span></button></li>'
                % (cls, px, py, key, i, name, area, name, area))
    return '<ul class="b-plan__spots">%s</ul>' % out


def vs_plans():
    tabs = ''.join('<button type="button" class="b-tab%s" role="tab" id="plan-%s-tab" aria-controls="plan-%s" '
                   'aria-selected="%s" data-b-switch="plan-%s"%s>%s</button>'
                   % (' is-active' if i == 0 else '', k, k, 'true' if i == 0 else 'false', k,
                      '' if i == 0 else ' tabindex="-1"', name)
                   for i, (k, name, *_r) in enumerate(PLANS))
    panes = ''
    # Büyüt: planı tam ekran açar (b.js); masaüstünde ayrıca fare altında büyüteç merceği
    zoom_btn = '<button type="button" class="b-plan__zoom" data-b-zoom>%s<span>Büyüt</span></button>' % ico('search')
    for i, (k, name, typ, rooms, net, gross, sale) in enumerate(PLANS):
        rows = ''.join('<tr data-b-room="%s-%d"><th scope="row">%s</th><td>%s m²</td></tr>' % (k, j, n_, a_)
                       for j, (n_, a_) in enumerate(rooms))
        panes += '''<div class="b-plan" id="plan-%s" role="tabpanel" aria-labelledby="plan-%s-tab"%s>
<figure class="b-plan__img"><div class="b-plan__frame" style="--ar:%.4f" data-w="%d"><img src="%svs-plan-%s-1440.jpg" alt="%s %s daire planı" width="%d" height="%d" loading="lazy" decoding="async">%s</div>%s</figure>
<div class="b-plan__info">
<p class="b-plan__name">%s <span>%s</span></p>
<dl class="b-plan__totals"><div><dt>Net Alan</dt><dd>%s m²</dd></div><div><dt>Brüt Alan</dt><dd>%s m²</dd></div><div><dt>Satışa Esas Brüt Alan</dt><dd>%s m²</dd></div></dl>
<div class="b-plan__rooms"><table><caption class="sr-only">%s</caption><tbody>%s</tbody></table></div>
%s
</div>
</div>''' % (k, k, '' if i == 0 else ' hidden', plan_dims(k)[0] / plan_dims(k)[1], plan_crop_size(k)[0], GYO, k, name, typ, plan_dims(k)[0], plan_dims(k)[1],
             plan_spots(k, rooms), zoom_btn, name, typ, net, gross, sale, name, rows, link('İletişim Formu', '#on-talep'))
    return '''<section class="b-section b-stone" id="daireler" aria-labelledby="daire-baslik">
<div class="b-wrap" data-b-switcher>
%s
<div class="b-tabs" role="tablist" aria-label="Daire tipi">%s</div>
%s
</div>
</section>''' % (section_head('Daire Planları', 'daire-baslik'), tabs, panes)


# vsancaktepe.com.tr "Merkezinde ... Var" blokları, birebir (_docs/kaynak/vsancaktepe-site.txt)
VS_BLOCKS = [
    ('Merkezinde Güven Var', 'VSancaktepe Merkez, sadece bir ev değil keyifli bir yaşam alanı sunuyor. Her detayın özenle '
     'planlandığı, huzurlu bir geleceğin anahtarını sunan VSancaktepe Merkez\'de, yaşamın merkezine güveni yerleştirdik.'),
    ('Merkezinde Uyum Var', 'VSancaktepe Merkez, her biri özenle tasarlanmış yaşam alanlarında, mimari ve peyzajın mükemmel '
     'uyumunu bir arada sunuyor. Geniş avlularda komşularınızla huzurla vakit geçirirken yeşilin her tonunu bulabileceğiniz '
     'bahçelerde doğayla iç içe bir yaşamın keyfini sürün.'),
    ('Merkezinde Yaşam Var', 'Bir araya gelmek, evin dışında da hayatın içinde olmak... VSancaktepe Merkez\'de, spor salonu '
     've yüzme havuzu başta olmak üzere, çocuk oyun alanları ve daha birçok aktivite alanı ile dolu sosyal bir yaşamın '
     'kapıları aralanıyor. Ortak etkileşim alanları ile evden dışarıya adım attığınız her an, sosyalliğin ve birlikteliğin '
     'tadını çıkarın.'),
    ('Merkezinde Doğallık Var', 'Enerji verimliliği, yeşil bina standartları ve sürdürülebilir malzemelerin kullanıldığı '
     'VSancaktepe Merkez, çevre dostu bir yaşam alanı olarak öne çıkıyor. Elektrikli araç istasyonları ve güneş panelleri '
     'ile donatılmış olan bu özel alan, yağmur suyunu toplama sistemi ile doğal kaynakları koruma çabasını bir adım öteye '
     'taşıyor.'),
]


def vs_features():
    items = ''.join('<li><h3 class="b-h3">%s</h3><p>%s</p></li>' % b for b in VS_BLOCKS)
    return '''<section class="b-section b-dark" id="ozellikler" aria-labelledby="ozellik-baslik">
<div class="b-wrap">
<h2 class="sr-only" id="ozellik-baslik">Merkezinde Doğallık Var</h2>
<ul class="b-feats b-feats--text">%s</ul>
</div>
</section>''' % items


VS_GALLERY = ap.GALLERY + ['Bloklar arasındaki havuz ve peyzaj', 'Bahçe ve yürüyüş yolları']


def vs_gallery():
    figs = ''.join('<li class="b-gallery__item"><img src="%svs-galeri-%d-1200x800.jpg" alt="%s" width="1200" height="800" loading="lazy" decoding="async"></li>'
                   % (IMG, i, t) for i, t in enumerate(VS_GALLERY, 1))
    return '''<section class="b-section b-gallery-sec" id="galeri" aria-labelledby="galeri-baslik">
<div class="b-wrap">
%s
</div>
<div class="b-gallery" data-b-rail>
<ul class="b-gallery__track" tabindex="0" aria-label="Galeri, yatay kaydırılabilir">%s</ul>
<div class="b-wrap b-gallery__nav">
<button type="button" class="b-round" data-b-prev aria-label="Önceki görsel">%s</button>
<button type="button" class="b-round" data-b-next aria-label="Sonraki görsel">%s</button>
</div>
</div>
</section>''' % (section_head('Galeri', 'galeri-baslik',
                              more=link('Sanal Tur', '#sanal-tur')), figs, ico('left'), ico('right'))


def vs_tour():
    # Sanal tur: vsancaktepe.com.tr menüsündeki bağlantı; görsel turun kendi salon panoraması
    return '''<section class="b-band b-band--short b-band--tour" id="sanal-tur" aria-labelledby="tur-baslik">
<picture class="b-band__media">
<source media="(max-width: 767px)" srcset="%svs-sanal-tur-686x926.jpg">
<img src="%svs-sanal-tur-2220x926.jpg" alt="Sanal turdan 2+1 dairenin salonu" width="2220" height="926" loading="lazy" decoding="async">
</picture>
<div class="b-band__text b-wrap">
<h2 class="b-band__title" id="tur-baslik">Sanal Tur</h2>
<div class="b-actions">%s</div>
</div>
</section>''' % (GYO, GYO, btn('Sanal Tur' + NEW_TAB, VS_TOUR, 'b-btn--yellow', ' target="_blank" rel="noopener"'))


def vs_campaign():
    return '''<section class="b-split b-split--flip b-dark" id="kampanya" aria-labelledby="kampanya-baslik">
<picture class="b-split__media"><img src="%sone-cikan-yasam-basliyor-1078x944.jpg" alt="VSancaktepe Merkez’de anahtar teslim töreninde yeni ev sahibi aile" width="1078" height="944" loading="lazy"></picture>
<div class="b-split__body">
<h2 class="b-h2" id="kampanya-baslik">Teslime özel avantajlar</h2>
<p class="b-lede">Anadolu Yakası’nın değerli yaşam merkezi VSancaktepe Merkez’de teslime özel avantajlardan yararlanma fırsatını kaçırmayın. Detaylı bilgi almak ve örnek dairemizi ziyaret etmek için bize ulaşın.</p>
<div class="b-actions">%s%s</div>
</div>
</section>''' % (GYO, btn('Bize Ulaşın', '#on-talep', 'b-btn--yellow'),
                 btn('Satış Ofisi', '#on-talep', 'b-btn--ghost-light'))


def vs_progress():
    months = ''.join('<li><a href="#"%s>%s%s</a></li>'
                     % (' aria-current="true"' if i == 0 else '', ico('play'), m) for i, m in enumerate(ap.PROGRESS))
    return '''<section class="b-section" id="ilerleme" aria-labelledby="ilerleme-baslik">
<div class="b-wrap">
%s
<div class="b-progress">
<figure class="b-video">
<video controls preload="none" playsinline poster="%svs-ilerleme-mayis-2026-1280x720.jpg" width="1280" height="720">
<source src="../assets/video/vs-ilerleme-mayis-2026.mp4" type="video/mp4">
</video>
<figcaption>Mayıs 2026</figcaption>
</figure>
<div class="b-months"><p class="b-h4">İlerleme Durumu</p><ul>%s</ul></div>
</div>
</div>
</section>''' % (section_head('İlerleme Durumu', 'ilerleme-baslik'), GYO, months)


def vs_location():
    # Metin vakifgyo.com.tr proje sayfasından birebir (_docs/kaynak/portfoy-portfoy-vsancaktepe-merkez.txt)
    bbox = '%.4f,%.4f,%.4f,%.4f' % (ap.LON - 0.02, ap.LAT - 0.011, ap.LON + 0.02, ap.LAT + 0.011)
    return '''<section class="b-section b-stone" id="konum" aria-labelledby="konum-baslik">
<div class="b-wrap b-location">
<div>
%s
</div>
<div class="b-map"><iframe title="Konum" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=%s&amp;layer=mapnik&amp;marker=%s,%s"></iframe></div>
</div>
</section>''' % (section_head('Konum', 'konum-baslik',
                              'Sancaktepe’de yer alan 58.133,42 m2 büyüklüğündeki arsamız, Anadolu Yakası’nın son yıllarda '
                              'en çok gelişim gösteren Sancaktepe İlçesi’nin merkezinde, Sancaktepe metro istasyonuna 5 dk. '
                              'mesafede, planlanan Sancaktepe Millet Bahçesi projesine komşu konumda yer almaktadır.'),
                 bbox, ap.LAT, ap.LON)


def vs_calc():
    return '''<section class="b-section" id="hesaplama" aria-labelledby="hesap-baslik">
<div class="b-wrap">
%s
<div class="b-calc" data-b-credit>
<div class="b-calc__inputs">
<div class="b-field">
<label for="hesap-tutar">Kredi tutarı</label>
<div class="b-field__box"><input type="text" inputmode="numeric" id="hesap-tutar" value="3.000.000" data-b-amount><span>₺</span></div>
<input type="range" min="500000" max="15000000" step="50000" value="3000000" aria-label="Kredi tutarı kaydırıcısı" data-b-amount-range>
<p class="b-field__range" aria-hidden="true"><span>500.000 ₺</span><span>15.000.000 ₺</span></p>
</div>
<div class="b-field">
<label for="hesap-vade">Vade</label>
<div class="b-field__box"><input type="text" inputmode="numeric" id="hesap-vade" value="120" data-b-term><span>ay</span></div>
<input type="range" min="12" max="120" step="12" value="120" aria-label="Vade kaydırıcısı" data-b-term-range>
<p class="b-field__range" aria-hidden="true"><span>12 ay</span><span>120 ay</span></p>
</div>
</div>
<div class="b-calc__out" aria-live="polite">
<div><span>Aylık taksit</span><strong data-b-installment>0,00 ₺</strong></div>
<div><span>Toplam geri ödeme</span><strong data-b-total>0,00 ₺</strong></div>
<div><span>Aylık faiz</span><strong data-b-rate data-rate="2.79">%%2,79</strong></div>
</div>
</div>
</div>
</section>''' % section_head('Konut Kredisi Hesaplama', 'hesap-baslik')


def vs_form():
    opts = ''.join('<option>%s</option>' % p[1] for p in PLANS)
    return '''<section class="b-section b-stone" id="on-talep" aria-labelledby="talep-baslik">
<div class="b-wrap b-cols">
<div>
%s
<form class="b-form" action="#" data-b-form novalidate>
<div class="b-form__grid">
<div class="b-field"><label for="t-ad">Ad soyad</label><input type="text" id="t-ad" name="ad" autocomplete="name" required></div>
<div class="b-field"><label for="t-tel">Cep telefonu</label><input type="tel" id="t-tel" name="telefon" autocomplete="tel" inputmode="tel" placeholder="05xx xxx xx xx" required></div>
<div class="b-field"><label for="t-eposta">E-posta <span class="b-opt">(isteğe bağlı)</span></label><input type="email" id="t-eposta" name="eposta" autocomplete="email"></div>
<div class="b-field"><label for="t-tip">İlgilendiğiniz daire tipi</label><select id="t-tip" name="tip"><option value="">Seçiniz</option>%s</select></div>
</div>
<p class="b-check"><input type="checkbox" id="t-kvkk" name="kvkk" required><label for="t-kvkk"><a href="#">Bilgilendirme Metnini</a> Okudum ve Onaylıyorum</label></p>
<button type="submit" class="b-btn b-btn--yellow">Gönder</button>
<p class="b-form__done" role="status" hidden>Gönderildi.</p>
</form>
</div>
<div class="b-panel b-office">
<h3 class="b-h3">Satış Ofisi</h3>
<p>Detaylı bilgi almak ve örnek dairemizi ziyaret etmek için bize ulaşın.</p>
<ul>
<li>%s<a href="%s">%s</a></li>
</ul>
</div>
</div>
</section>''' % (section_head('İletişim Formu', 'talep-baslik'), opts, ico('phone'), VS_PHONE[0], VS_PHONE[1])


def vs_guarantee():
    return band('ifm', 'İstanbul Uluslararası Finans Merkezi’nde VakıfBank Genel Müdürlük binası, gece',
                'Vakıf GYO güvencesiyle', 'guvence-baslik',
                'Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak, 30 yıldır güçlü Türkiye’nin temellerini atıyoruz. '
                'Birlikte nice yıllara…', [('Hakkımızda', 'hakkimizda.html')], cls='b-band--short')


VS_DOCK = '''<nav class="b-dock" aria-label="Hızlı iletişim">
<a href="%s">%s<span>%s</span></a>
<a href="#on-talep" class="b-dock__main">İletişim Formu</a>
</nav>''' % (VS_PHONE[0], ico('phone'), VS_PHONE[1])


def vs_page():
    body = '\n'.join([vs_hero(), vs_about(), vs_plans(), vs_features(), vs_gallery(), vs_campaign(),
                      vs_progress(), vs_tour(), vs_location(), vs_calc(), vs_form(), vs_guarantee(), VS_DOCK])
    return page('VSancaktepe Merkez',
                'Proje Hakkında · Vaziyet Planı · Daire Planları · İlerleme Durumu · Sanal Tur · Konum · '
                'İletişim Formu', body, shell=(vs_rail(), vs_footer()), body_cls='b--project')


# ---------------------------------------------------------------------------
# 4. HAKKIMIZDA — statik içerik sayfası
# ---------------------------------------------------------------------------

# Bölüm adları vakifgyo.com.tr Hakkımızda sayfasındaki başlıklar (_docs/kaynak/vakifgyo.txt)
ABOUT_NAV = [('biz', 'Hakkımızda'), ('amac', 'Temel Amaç'), ('politika', 'Yönetim Politikamız'),
             ('belgeler', 'Kalite Belgelerimiz'), ('otuz-yil', 'Vakıf GYO 30 Yaşında')]

# Yönetim Politikamız infografiği (_docs/kaynak/yonetim-politikamiz.txt)
POLICY = [
    ('Tam Uyumluluk', 'Tüm yasal ve uymakla yükümlü olduğumuz diğer şartlara, şeffaflıkla uyum sağlarız.'),
    ('Sürekli Gelişme', 'Değişimi yöneterek ve kaynakları etkin kullanarak sürekli gelişim sağlarız.'),
    ('Mutlu Müşteri', 'Sunduğumuz ürün ve hizmetlerle, beklentilerin ötesinde ve güven veren bir müşteri deneyimi yaşatırız.'),
    ('Mutlu Çalışan', 'Vakıf GYO çalışanları olarak biz, ortak akıl ve ortak duygu ile sağlıklı bir kurum iklimi oluştururuz.'),
]

PILLARS = [('Temel Amaç', 'Geleneğimizden aldığımız güçle, geleceğin yaşam alanlarını inşa eder, paydaşlarımıza sürdürülebilir değer sunarız.'),
           ('Vizyon', 'Yeniliğe öncülük eden güvenilir ve sürdürülebilir projelerle, sektörde referans kuruluş olmak.'),
           ('Kurum Kültürü ve Değerler', 'Farkındalığımızı geliştirerek; adil, şeffaf, güvene dayalı ortak duygu ve başarı odaklı, sürekli öğrenen ortak akıl ile insan ve çevreye duyarlı, “biz” kültürünü yaşar, yaşatırız.')]

# Kurumsal menüsü (_docs/kaynak/menu.txt)
KURUMSAL = [('Kurumsal Yönetim', '#'), ('Yönetim Politikamız', '#'), ('IK Politikamız', '#'),
            ('Şirket Bilgileri', '#'), ('GYO Sektörü', '#'), ('Sıkça Sorulan Sorular', '#')]


def about_page():
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % (v, l)
                    for l, v in [('Kuruluş', '12 Ocak 1996'), ('Halka arz', '24 Aralık 1996'), ('Borsa İstanbul', 'VKGYO')])
    pillars = ''.join('<div class="b-pillar"><h3 class="b-pillar__title">%s</h3><p>%s</p></div>' % p
                      for p in PILLARS)
    policy = ''.join('<li><h3 class="b-h4">%s</h3><p>%s</p></li>' % p for p in POLICY)
    certs = doclist([('', c.split(' ', 2)[0] + ' ' + c.split(' ', 2)[1], c.split(' ', 2)[2], 'PDF', '#')
                     for c in ap.CERTS], 'b-docs--certs')
    related = ''.join('<li>%s</li>' % link(t, h, 'b-tile') for t, h in KURUMSAL)
    body = '\n'.join([
        pagehero('aydos', 'Bizimtepe Aydos konut blokları ve peyzajlı iç bahçe',
                 [('Ana Sayfa', 'index.html'), ('Kurumsal', '#'), ('Vakıf GYO’yu Tanıyalım', '#'),
                  ('Hakkımızda', '#')], 'Hakkımızda',
                 'Geleneğin Gücü, Geleceğin İnşası', pos='50% 55%'),
        subnav(ABOUT_NAV, 'Sayfa bölümleri'),
        '''<section class="b-section" id="biz" aria-labelledby="biz-baslik">
<div class="b-wrap b-prose-grid">
<h2 class="sr-only" id="biz-baslik">Hakkımızda</h2>
<p class="b-statement__text b-statement__text--dark">Türkiye’nin ilk Gayrimenkul Yatırım Ortaklığı Şirketi olarak 12 Ocak 1996 tarihinde kurulan Vakıf GYO, güçlü sermayesi, her geçen gün artan portföy büyüklüğü ve piyasa değerinin yanı sıra güvenilir ortaklık yapısı ile de sektörde önemli bir yere sahiptir.</p>
<div class="b-prose">
<p>Türkiye’nin en büyük 2. bankası olan T. Vakıflar Bankası T.A.O.’nun hâkim ortağı olduğu Şirketimiz, 24 Aralık 1996 tarihinde paylarını halka arz etmiş olup Borsa İstanbul’da VKGYO kodu ile işlem görmektedir.</p>
<p>Sembol yapılarıyla sektörde değişime yön veren, referans bir kuruluş olma vizyonuna sahip Şirketimiz, Ülkemiz ve sektörümüze değer katmakla birlikte, düzenli kira ve yüksek portföy getirisi sağlayarak büyüme azmini kararlılıkla sürdürmektedir.</p>
</div>
<dl class="b-figures b-figures--light">%s</dl>
</div>
</section>''' % facts,
        '''<section class="b-section b-stone" id="amac" aria-labelledby="amac-baslik">
<div class="b-wrap">
%s
<div class="b-pillars">%s</div>
</div>
</section>''' % (section_head('Temel Amaç', 'amac-baslik'), pillars),
        '''<section class="b-section" id="politika" aria-labelledby="politika-baslik">
<div class="b-wrap">
%s
<ol class="b-policy">%s</ol>
</div>
</section>''' % (section_head('Yönetim Politikamız', 'politika-baslik',
                              'Sürdürülebilir ekosistem içinde kaliteli yaşam alanları ile değer sunarız.'), policy),
        '''<section class="b-section b-stone" id="belgeler" aria-labelledby="belge-baslik">
<div class="b-wrap">
%s
%s
</div>
</section>''' % (section_head('Kalite Belgelerimiz', 'belge-baslik'), certs),
        band('ifm', 'İstanbul Uluslararası Finans Merkezi’nde VakıfBank Genel Müdürlük binası, gece',
             'Vakıf GYO 30 Yaşında', 'otuz-yil-baslik',
             'Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak, 30 yıldır güçlü Türkiye’nin temellerini atıyoruz. '
             'Birlikte nice yıllara…', [], sid='otuz-yil'),
        '''<section class="b-section" aria-labelledby="ilgili-baslik">
<div class="b-wrap">
%s
<ul class="b-tiles">%s</ul>
</div>
</section>''' % (section_head('Kurumsal', 'ilgili-baslik'), related),
    ])
    return page('Hakkımızda — Vakıf GYO',
                'Hakkımızda · Temel Amaç · Vizyon · Kurum Kültürü ve Değerler · Kalite Belgelerimiz · '
                'Vakıf GYO 30 Yaşında', body, shell=(rail('kurumsal'), footer()))


# ---------------------------------------------------------------------------

def main():
    global LAYOUT
    for LAYOUT, out in OUTS.items():
        os.makedirs(out, exist_ok=True)
        sys.modules.setdefault('build_alt_b', sys.modules[__name__])   # __main__ ile aynı örnek (LAYOUT paylaşılır)
        import build_cubes_b
        for name, fn in [('index.html', index), ('index-video.html', index_video), ('yatirimci-iliskileri.html', ir_page),
                         ('vsancaktepe-merkez.html', vs_page), ('cubes-ankara.html', build_cubes_b.page),
                         ('hakkimizda.html', about_page)]:
            path = os.path.join(out, name)
            open(path, 'w', encoding='utf-8', newline='\n').write(fn())
            print('yazıldı:', os.path.relpath(path, ROOT))


if __name__ == '__main__':
    main()
