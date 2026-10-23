# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif A (VakıfBank.com.tr tasarım sistemi) sayfa üreteci

Kurumsal header/footer kabuğu vakifbank.com.tr'den alınan parçalardan kurulur
(_build/vb-source/); ana sayfa blokları kurumsal ana sayfanın markup'ı ve
sınıflarıyla BİREBİR yazılır, yalnızca içerik Vakıf GYO'nundur.

Bootstrap / jQuery / Swiper yok: ızgara 01-grid.css, Bootstrap sınıf
sözleşmesi 03-contract.css, davranışlar vb.js + gyo.js.

Çalıştırma:  python _build/build_alt_a.py
Çıktı:       src/alt-a/index.html
Önizleme:    src/ klasörü kök olarak sunulmalı (kurumsal CSS /Assets/… ve
             /Templates/… yollarını kökten çağırıyor):
             python -m http.server 8080 --directory src
             → http://localhost:8080/alt-a/
"""
import hashlib
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '_build', 'vb-source')
# Varyant: A (kurumsal bileşenler birebir) ya da A2 (aynı bileşenler esnetilmiş:
# daha yüksek banner, tam genişlik bantlar, Vakıf GYO yeşili üçüncü renk).
# A2 = build_alt_a2.py (GYO_VARIANT=a2) → src/alt-a2, ek katman 06-a2.css
VARIANT = os.environ.get('GYO_VARIANT', 'a')
A2 = VARIANT == 'a2'
OUT = os.path.join(ROOT, 'src', 'alt-a2' if A2 else 'alt-a')

read = lambda n: open(os.path.join(SRC, n), encoding='utf-8').read().replace('﻿', '')

HEAD = read('vb-header-head.html')
TAIL = read('vb-header-tail.html')
FOOTER = read('vb-footer.html')

IMG = '../assets/img/gyo/'
# Slayt zemin rengi: make_banners_a.py her görselin gök tonunu yazar
_colors_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'assets', 'img', 'gyo', 'banner-colors-a2.json' if A2 else 'banner-colors.json')
BANNER_COLORS = json.load(open(_colors_path, encoding='utf-8')) if os.path.exists(_colors_path) else {}
LOGO = IMG + 'vakif-gyo-logo.svg'


def sub_block(html, open_tag, new_inner):
    """open_tag ile başlayan div'in içeriğini değiştirir (dengeli kapanış)."""
    i = html.find(open_tag)
    if i < 0:
        raise SystemExit('Blok bulunamadı: ' + open_tag)
    start = html.index('>', i) + 1
    depth, k = 1, start
    while depth:
        m = re.compile(r'<(/?)div\b[^>]*>').search(html, k)
        if not m:
            raise SystemExit('Kapanış bulunamadı: ' + open_tag)
        depth += -1 if m.group(1) else 1
        k = m.end()
    return html[:start] + new_inner + html[k - 6:]


# ---------------------------------------------------------------------------
# Header
# ---------------------------------------------------------------------------

def top_icon(paths):
    """Üst şerit ikonu: kurumsal .header__links-icon yuvasında 16px satır içi
    SVG; rengi currentColor."""
    return ('<span class="header__links-icon" aria-hidden="true">'
            '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.3" '
            'stroke-linecap="round" stroke-linejoin="round" focusable="false">%s</svg>'
            '</span>' % paths)


ICON_GLOBE = top_icon('<circle cx="8" cy="8" r="6.2"/><path d="M1.8 8h12.4"/>'
                      '<path d="M8 1.8c1.7 1.8 2.5 3.9 2.5 6.2S9.7 12.4 8 14.2C6.3 12.4 5.5 10.3 5.5 8S6.3 3.6 8 1.8z"/>')
ICON_CHART = top_icon('<path d="M2 13.5h12"/><path d="M3 11l3.2-3.6 2.6 2.2L13 4.6"/><path d="M10.4 4.6H13v2.6"/>')
ICON_DOC = top_icon('<path d="M4 1.8h5.2L12.5 5v9.2H4z"/><path d="M9 1.8V5h3.5"/><path d="M6 8.2h4.5M6 10.6h4.5"/>')
ICON_PHONE = top_icon('<path d="M5.3 2.2 3.6 2.4c-.8.1-1.4.8-1.3 1.6.6 5 4.6 9 9.6 9.6.8.1 1.5-.5 1.6-1.3l.2-1.7'
                      'c.1-.5-.3-1-.8-1.1l-2-.5c-.4-.1-.8 0-1 .3l-.7.9C7.6 9.5 6.5 8.4 5.8 6.8l.9-.7c.3-.2.4-.6.3-1'
                      'l-.5-2c-.1-.5-.6-.9-1.2-.9z"/>')
ICON_EXT = ('<span class="gyo-ext" aria-hidden="true"><svg viewBox="0 0 16 16" fill="none" '
            'stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" '
            'focusable="false"><path d="M9.5 2.5h4v4"/><path d="M13.5 2.5 8 8"/>'
            '<path d="M12 9.5v3a1 1 0 0 1-1 1H3.5a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3"/></svg></span>')

NEW_TAB = '<span class="sr-only"> (yeni sekmede açılır)</span>'

# Üst şerit: orijinal sitedeki EN/TR, İletişim telefonu ve Bilgi Toplumu Hizmetleri
TOP_LINKS = '''
<a href="#" class="header__links-link" lang="en">%s<span class="header__links-text">EN</span></a>
<a href="tel:+902162859400" class="header__links-link">%s<span class="header__links-text">İletişim +90 (216) 285 94 00</span></a>
<a href="https://e-sirket.mkk.com.tr/esir/Dashboard.jsp#/sirketbilgileri/10351" class="header__links-link" target="_blank" rel="noopener">%s<span class="header__links-text">Bilgi Toplumu Hizmetleri</span>%s</a>
''' % (ICON_GLOBE, ICON_PHONE, ICON_DOC, NEW_TAB)

POPULAR = '''
<a class="placeholder-content-link" href="#projeler"><span>Satışı Devam Eden Projelerimiz</span></a>
<a class="placeholder-content-link" href="#"><span>Raporlar ve Yatırımcı Sunumları</span></a>
<a class="placeholder-content-link" href="#"><span>Özel Durum Açıklamaları</span></a>
<a class="placeholder-content-link" href="#"><span>Genel Kurul</span></a>
'''

MOBILE_QUICK = '''
<a href="#projeler" class="header__mobile__quick-link__item"><span class="megamenu__links-icon"><span class="svg svg--plus" aria-hidden="true"></span></span><p>Satışı Devam Eden Projelerimiz</p></a>
<a href="yatirimci-iliskileri.html" class="header__mobile__quick-link__item"><span class="megamenu__links-icon"><span class="svg svg--table" aria-hidden="true"></span></span><p>Yatırımcı İlişkileri</p></a>
<a href="#" class="header__mobile__quick-link__item"><span class="megamenu__links-icon"><span class="svg svg--support" aria-hidden="true"></span></span><p>Bize Ulaşın</p></a>
'''

# Kurumsal mega menü panelinin alt satırı: daire ikonlu hızlı bağlantılar
# (kurumsalda Başvurular · Hesaplama Araçları · Yardım Merkezi).
MEGA_LINKS = '''<div class="col-12"><div class="megamenu__links">
<a href="index.html#projeler" class="megamenu__links-item"><span class="megamenu__links-icon"><span class="svg svg--plus" aria-hidden="true"></span></span><span>Satışı Devam Eden Projelerimiz</span></a>
<a href="#" class="megamenu__links-item"><span class="megamenu__links-icon"><span class="svg svg--support" aria-hidden="true"></span></span><span>Bize Ulaşın</span></a>
</div></div>'''


# Hazır sayfası olan menü maddeleri; diğerleri "#"
PAGES = {
    'Vakıf GYO': 'hakkimizda.html',
    'Hakkımızda': 'hakkimizda.html',
    'VSancaktepe Merkez': 'vsancaktepe-merkez.html',
    'Cubes Ankara': 'cubes-ankara.html',
    'Yatırımcı İlişkileri': 'yatirimci-iliskileri.html',
}


def href(text):
    return PAGES.get(text, '#')


def megamenu(groups, img, alt):
    """Kurumsal mega menü: solda kategori sütunu, kategoriye gelindiğinde sağda
    alt menü + görsel paneli, altta hızlı bağlantı satırı."""
    items = ''
    # Menüde iki sütunlu uzun liste varsa görsel sağda o alt başlıkta yer
    # bulamıyordu (menünün yarısında görsel yok gibi görünüyordu): bu menülerde
    # görsel, sol sütunda alt başlıkların altında durur — tüm alt başlıklarda aynı.
    aside = any(len(links) > 8 for _, links in groups)
    for title, links in groups:
        subs = ''.join(
            '<div class="megamenu__submenu-item"><a href="%s" class="megamenu__submenu-link"><span>%s</span></a></div>' % (href(t), t)
            for t in links)
        news = '' if aside else (
            '<div class="megamenu__news"><div class="megamenu__news-img">'
            '<img src="%s" alt="%s" loading="lazy"></div>'
            '<div class="megamenu__news-content"></div></div>' % (img, alt))
        # Uzun alt listeler (Kurumsal Yönetim'in 14 politikası) tek sütunda paneli
        # aşıyordu: görsel kalkar, liste iki sütuna yayılır (04-gyo.css).
        if len(links) > 8:
            sub = ('<div class="megamenu__sub megamenu__sub--cols"><div class="megamenu__submenu" style="--rows:%d">%s</div></div>'
                   % ((len(links) + 1) // 2, subs))
        else:
            sub = '<div class="megamenu__sub"><div class="megamenu__submenu">%s</div>%s</div>' % (subs, news)
        items += ('<div class="megamenu__item">'
                  '<a class="megamenu__item-link" href="%s"><span>%s</span></a>%s'
                  '</div>' % (href(title), title, sub))
    if aside:
        items += '<div class="megamenu__aside"><img src="%s" alt="%s" loading="lazy"></div>' % (img, alt)
    return ('<div class="megamenu"><div class="container"><div class="row">'
            '<div class="col-12 position-relative megamenu__wrapper">%s</div>'
            '%s</div></div></div>' % (items, MEGA_LINKS))


SALE = ['VSancaktepe Merkez', 'VYeniKonak', 'Tablo Adalar', 'Cubes Ankara']

# Menü ağacı: vakifgyo.com.tr ile birebir (_docs/kaynak/menu.txt). Orijinal
# ana menü: Kurumsal · Portföy · Yatırımcı İlişkileri · Güncel ·
# Sürdürülebilirlik · Bize Ulaşın (sonuncusu header düğmesi).
KY_POLICIES = ['Kurumsal Yönetim İlkelerine Uyum Raporları', 'Kar Dağıtım Politikası',
               'Bilgilendirme Politikası', 'Bağış ve Yardım Politikası', 'Ücretlendirme Politikası',
               'Müşteri Memnuniyet Politikası', 'Tazminat Politikası',
               'İnsan Hakları ve Çalışan Hakları Politikası', 'İş Sağlığı ve Güvenliği Politikası',
               'Yönetim Kurulu Toplantıları Prosedürü',
               'Çalışanların Yönetim Organlarına Katılımına İlişkin Prosedür',
               'Fırsat Eşitliği, Çeşitlilik ve Toplumsal Cinsiyet Eşitliği Politikası',
               'Kurumsal Sosyal Sorumluluk Politikası', 'Bilgi Güvenliği Politikası']
MENUS = [
    ('Kurumsal', megamenu([
        ('Vakıf GYO', ['Hakkımızda']),
        ('Kurumsal Yönetim', KY_POLICIES),
        ('IK Politikamız', ['IK Politikamız & Başvuru Formu']),
        ('Şirket Bilgileri', ['Şirket Bilgileri', 'Yönetim Kurulu', 'Üst Yönetim', 'Organizasyon Şeması']),
        ('Bilgi Merkezi', ['GYO Sektörü', 'Sıkça Sorulan Sorular',
                           'Gizlilik ve Kişisel Verilerin Korunması']),
    ], IMG + 'menu-kurumsal-704x484.jpg', 'VakıfBank Genel Müdürlük binası girişi')),
    ('Portföy', megamenu([
        ('Devam Eden Projeler', ['VSancaktepe Merkez', 'VYeniKonak']),
        ('Tamamlanan Projeler', ['İstanbul Uluslararası Finans Merkezi', 'Cubes Ankara',
                                 'Tablo Adalar', 'Bizimtepe Aydos', 'Gaziantep Iconova']),
        ('Gayrimenkul Yatırımları', ['Medyan Kadıköy', 'Şişli VakıfBank Ek Hizmet Binası',
                                     'Bizimtepe Aydos Ticari Üniteler', 'Aliağa İş Merkezi',
                                     'Fatih İş Merkezi', 'Kavaklıdere Dükkan', 'VKütahya İş Merkezi',
                                     'Ankara ENH Parselleri', 'İzmir Konak', 'İstanbul Sancaktepe',
                                     'Kocaeli Çayırova']),
    ], IMG + 'menu-projeler-704x484.jpg', 'VSancaktepe Merkez cephe görseli')),
    ('Yatırımcı İlişkileri', megamenu([
        ('Yatırımcı İlişkileri', ['Yatırımcı İlişkileri İletişim', 'Duyurular',
                                  'Özel Durum Açıklamaları', 'Sürekli Bilgilendirme Formu',
                                  'Gayrimenkul Değerleme Raporları', 'Raporlar ve Yatırımcı Sunumları',
                                  'Sermaye Artırımı & Temettü Duyuruları', 'Genel Kurul']),
        ('Kurumsal Yönetim', KY_POLICIES),
    ], IMG + 'menu-yatirimci-704x484.jpg', 'İstanbul Uluslararası Finans Merkezi kuleleri')),
    ('Güncel', megamenu([
        ('Haberler', ['Haberler']),
        ('Duyurular', ['Duyurular']),
        ('Ödüller', ['Ödüller']),
    ], IMG + 'menu-portfoy-704x484.jpg', 'Medyan Kadıköy projesinin gece görünümü')),
    ('Sürdürülebilirlik', megamenu([
        ('Sürdürülebilirlik', ['Kilometre Taşları', 'Raporlar ve Sertifikalar', 'Yönetişim Yapısı',
                               'Stratejik Yaklaşım', 'Paydaş Katılımı', 'Öncelikli Konular',
                               'Çevre Yönetimi', 'Çevresel ve Sosyal Risk Yönetim Sistemi',
                               'Kurumsal Sosyal Sorumluluk', 'Sürdürülebilirlik Endeksler']),
    ], IMG + 'menu-surdurulebilirlik-704x484.jpg', 'VSancaktepe Merkez havuz ve peyzaj alanı')),
]

SEARCH_ITEM = '''<div class="header__menu-item position-relative gyo-search">
<a class="header__menu-search header__menu-link" href="#" aria-label="Arama" aria-expanded="false"><span class="svg svg--search" aria-hidden="true"></span></a>
<div class="header__search-content">
<div class="search-box">
<span class="svg svg--close" role="button" tabindex="0" aria-label="Aramayı kapat"></span>
<div class="search-input-content">
<span class="svg svg--search" aria-hidden="true"></span>
<label class="sr-only" for="site-arama">Sitede ara</label>
<input type="search" id="site-arama" name="search" minlength="3" placeholder="Arama">
</div>
<div class="placeholder-content open">%s</div>
</div>
<div class="overlay"></div>
</div>
</div>''' % POPULAR


def nav():
    items = ''.join(
        '<div class="header__menu-item"><a class="header__menu-link" href="#" role="button" '
        'aria-haspopup="true" aria-expanded="false">%s</a>%s</div>' % (label, mm)
        for label, mm in MENUS)
    return '<nav class="header__menu" aria-label="Ana menü">' + items + SEARCH_ITEM + '</nav>'


# Kurumsal .header__btns: "Müşteri Ol" (çerçeveli) + "İnternet Bankacılığı"
# (siyah). Vakıf GYO'da tek eylem: Ön Talep.
HEADER_BTNS = ('<div class="header__btns">'
               '<a href="#" class="btn btn-primary">Bize Ulaşın</a>'
               '</div>')


def header(ticker):
    h = HEAD
    h = sub_block(h, '<div class="header__links">', TOP_LINKS)
    h = sub_block(h, '<div class="placeholder-content open">', POPULAR)
    h = sub_block(h, '<div class="header__mobile__quick-link">', MOBILE_QUICK)
    # Logo: VakıfBank logosu yerine Vakıf GYO logosu (vektör, Illustrator PDF'inden)
    h = h.replace('href="/tr" aria-label="VakıfBank Anasayfa"',
                  'href="index.html" aria-label="Vakıf GYO ana sayfa"')
    h = re.sub(r'(src|srcset)="/Templates/Default/assets/img/(?:footer-)?logo\.svg"',
               r'\1="%s"' % LOGO, h)
    h = h.replace('alt="VakıfBank Logo"', 'alt="Vakıf GYO"')
    h = h.replace('VakıfBank, daima seninle', 'Vakıf GYO')
    # Logo hiçbir sayfada h1 değil; h1 sayfanın gerçek başlığına kalıyor.
    h = re.sub(r'<h1 class="site__logo">.*?</h1>', '', h, flags=re.S)
    t = TAIL.replace(
        re.search(r'<div class="header__btns">.*?</div>', TAIL, re.S).group(0), HEADER_BTNS)
    return h + nav() + t


# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------

FOOTER_TOP = '''
<ul>
<li><a href="#">Kurumsal</a></li>
<li><a href="#">Portföy</a></li>
<li><a href="yatirimci-iliskileri.html">Yatırımcı İlişkileri</a></li>
<li><a href="#">Güncel</a></li>
<li><a href="#">Sürdürülebilirlik</a></li>
</ul>
<ul>
<li><a href="#">Bize Ulaşın</a></li>
<li><a href="#">Müşteri Şikayetleri Yönetim Süreci</a></li>
<li><a href="#">Sıkça Sorulan Sorular</a></li>
<li><a href="#">Gizlilik ve Kişisel Verilerin Korunması</a></li>
</ul>
<ul>
<li><a href="https://e-sirket.mkk.com.tr/esir/Dashboard.jsp#/sirketbilgileri/10351" target="_blank" rel="noopener">Bilgi Toplumu Hizmetleri</a></li>
</ul>
'''

# Footer alt satırı: grup şirketi ve proje siteleri, metin yerine logolarıyla
# (müşteri logoları: gorseller/gorseller/logolar; make_logos_ters.py renkli SVG).
# Son sütun: optik yükseklik (px). Logoların oranları çok farklı; aynı
# yükseklikte VakıfBank yazısı iri, VSancaktepe küçük kalıyordu.
FOOTER_LOGOS = [
    ('https://www.vakifbank.com.tr', 'logo-vakifbank.svg', 'VakıfBank', 20),
    ('https://vsancaktepe.com.tr', 'logo-vsancaktepe-renkli.svg', 'VSancaktepe Merkez', 34),
    ('https://vyenikonak.com.tr', 'logo-vyenikonak-renkli.svg', 'VYeniKonak', 28),
    ('https://tabloadalar.com.tr', 'logo-tablo-adalar-renkli.svg', 'Tablo Adalar', 36),
    ('https://www.cubesankara.com.tr', 'logo-cubes-ankara-renkli.png', 'Cubes Ankara', 26),
]
FOOTER_BOTTOM = '''
<ul class="gyo-footer-logos">
%s
</ul>
''' % '\n'.join('<li><a href="%s" target="_blank" rel="noopener"><img src="%s%s" alt="%s" style="--h:%dpx">%s</a></li>'
                 % (u, IMG, f, n, hh, NEW_TAB) for u, f, n, hh in FOOTER_LOGOS)

SOCIAL = '''<div class="footer__social">
<a href="https://www.instagram.com/vakifgyo/" rel="noopener" aria-label="Vakıf GYO Instagram"><span class="svg svg--social svg--social--instagram" aria-hidden="true"></span></a>
<a href="https://www.facebook.com/VakifGYO/" rel="noopener" aria-label="Vakıf GYO Facebook"><span class="svg svg--social svg--social--facebook" aria-hidden="true"></span></a>
<a href="https://twitter.com/VakifGYO" rel="noopener" aria-label="Vakıf GYO X"><span class="svg svg--social svg--social--twitter" aria-hidden="true"></span></a>
<a href="https://www.linkedin.com/company/vak%C4%B1f-gyo-a-%C5%9F-" rel="noopener" aria-label="Vakıf GYO LinkedIn"><span class="svg svg--social svg--social--linkedin" aria-hidden="true"></span></a>
</div>'''


def footer():
    f = FOOTER
    f = re.sub(r'<script.*?</script>', '', f, flags=re.S)
    f = sub_block(f, '<div class="footer__mobile__links">',
                  '<a href="#" class="footer__mobile__links-link" lang="en"><i class="footer__mobile__links-icon icon-language" aria-hidden="true"></i><span class="footer__mobile__links-text">EN</span></a>'
                  '<a href="#" class="footer__mobile__links-link"><i class="footer__mobile__links-icon icon-file" aria-hidden="true"></i><span class="footer__mobile__links-text">Bize Ulaşın</span></a>')
    f = re.sub(r'<a href="/tr" class="footer__logo">.*?</a>',
               '<a href="index.html" class="footer__logo"><img src="%s" alt="Vakıf GYO" width="230" height="40"></a>' % LOGO,
               f, flags=re.S)
    f = re.sub(r'<a href="tel:[^"]*" class="footer__phone">(.*?)<span>[^<]*</span>',
               r'<a href="tel:+902162859400" class="footer__phone">\1<span>+90 (216) 285 94 00</span>',
               f, flags=re.S)
    f = sub_block(f, '<div class="footer__social">', '')
    f = re.sub(r'<div class="footer__social"></div>', SOCIAL, f)
    f = re.sub(r'<p class="footer__copyright">.*?</p>',
               '<p class="footer__copyright">VakıfBank Finans Grubu İştirakidir.</p>', f, flags=re.S)
    f = sub_block(f, '<div class="footer__sitemap__top">', FOOTER_TOP)
    f = sub_block(f, '<div class="footer__sitemap__bottom">', FOOTER_BOTTOM)
    return f


# ---------------------------------------------------------------------------
# Sayfa iskeleti
# ---------------------------------------------------------------------------

CSS = ['00-base', '01-grid', '02-vb-components', '03-contract', '04-gyo', '05-gyo-pages'] + (['06-a2'] if A2 else [])


def versioned(html):
    """CSS/JS bağlantılarına içerik özeti (?v=…) — yerel sunucuda eski
    dosyanın önbellekten gelmesini önler."""
    def tag(m):
        attr, url = m.group(1), m.group(2)
        path = os.path.join(ROOT, 'src', url[len('../'):])
        if not os.path.exists(path):
            return m.group(0)
        return '%s="%s?v=%s"' % (attr, url, hashlib.md5(open(path, 'rb').read()).hexdigest()[:8])
    return re.sub(r'(href|src)="(\.\./assets/[^"?]+\.(?:css|js))"', tag, html)


def keep_amounts(html):
    """Tutarda birim alt satıra düşmesin: sayı ile birim arasına bölünmez boşluk."""
    return re.sub(r'(\d)[ \t]+(TL|₺|m²|Ay)\b', r'\1&nbsp;\2', html)


HOME_H1 = '<h1 class="sr-only">Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası</h1>'


# Varyant süzgeci: A2 üreteci (build_alt_a2.py) sayfanın son HTML'inde görsel
# adlarını A2 kadrajlarıyla değiştirir.
PAGE_FILTER = None


def page(*args, **kw):
    html = _page(*args, **kw)
    return PAGE_FILTER(html) if PAGE_FILTER else html


def _page(title, desc, body, ticker=None, h1=HOME_H1, shell=None, main_cls='',
          favicon='../assets/img/favicon.ico'):
    """shell: (header, footer) — proje siteleri kendi kabuğunu verir.
    İç sayfalarda h1 gövdenin içindedir (h1='')."""
    head_html, foot_html = shell if shell else (header(ticker), footer())
    links = '\n'.join('<link rel="stylesheet" href="../assets/css/alt-a/%s.css">' % c for c in CSS)
    return versioned('''<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>%s</title>
<meta name="description" content="%s">
<link rel="icon" href="%s" sizes="any">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap">
%s
</head>
<body>
<a class="skip-link" href="#main">İçeriğe atla</a>
%s
<main id="main"%s>
%s%s
</main>
%s
<script src="../assets/js/alt-a/vb.js"></script>
<script src="../assets/js/alt-a/gyo.js"></script>
</body>
</html>
''' % (title, desc, favicon, links, head_html,
       ' class="%s"' % main_cls if main_cls else '', h1, keep_amounts(body), foot_html))


# ---------------------------------------------------------------------------
# Ana sayfa blokları — sıra ve markup vakifbank.com.tr ana sayfasıyla aynı
# ---------------------------------------------------------------------------

# Temsilî veri: tasarım örneği içindir, gerçek piyasa verisi değildir.
TICKER = '<span class="gyo-up" aria-label="yükselişte">▲</span> %1,24'


# 1. Banner — kurumsal .banner / .home-banner ------------------------------
# Proje logosu: ≥1200 px görselin gökyüzüne gömülü (make_banners_a.py),
# ≤1199 px metin kutularının başında koyu kutuda (04-gyo.css .banner__logo).
# Proje adı metinden çıktı; ekran okuyucu için gizli metin olarak kalır.
BANNER_LOGOS = {
    'vsancaktepe': ('logo-vsancaktepe-ters.svg', 'VSancaktepe Merkez'),
    'vyenikonak': ('logo-vyenikonak-ters.svg', 'VYeniKonak'),
    'tablo-adalar': ('logo-tablo-adalar-ters.svg', 'Tablo Adalar'),
}

BANNER_SLIDES = [
    # (≥1700 tam kadraj, 1200–1699 ana blok, 768–1199 sağa yaslı, telefon, satırlar, CTA, alt, koyu zemin mi)
    # Görseller make_banners_a.py ile kadraja göre işlendi: odak nokta metin
    # kutusunun 24 px sağında, görsel konteynere bağlı konumlanır (04-gyo.css),
    # sağda açılan alan görselin kendi gök tonuyla dolar; proje kesilmez.
    # Slaytlar çapraz geçişle değişir; zemin rengi banner-colors.json'dan.
    ('banner-vsancaktepe-5200x1040.jpg', 'banner-vsancaktepe-o-3500x1040.jpg',
     'banner-vsancaktepe-t-3200x1040.jpg', 'banner-vsancaktepe-m-1600x480.jpg',
     ['VSancaktepe Merkez’de', 'Yaşam Başlıyor'], 'Detaylı Bilgi',
     'VSancaktepe Merkez konut bloklarının gün batımında görünümü', True),
    ('banner-vyenikonak-5200x1040.jpg', 'banner-vyenikonak-o-3500x1040.jpg',
     'banner-vyenikonak-t-3200x1040.jpg', 'banner-vyenikonak-m-1600x480.jpg',
     # Metinler kaynaktaki banner'lardan: vakifgyo.com.tr ana sayfa slaytı (VS,
     # VYK, derecelendirme) ve tabloadalar.com.tr banner'ı (Tablo). vyenikonak.com.tr
     # banner'ında metin yok; VYK için ana sayfa slaytındaki haber başlığı.
     ['VYeniKonak proje', 'lansmanı gerçekleşti'], 'Detaylı Bilgi',
     'VYeniKonak’ın iki kulesi', False),
    ('banner-derecelendirme-5200x1040.jpg', 'banner-derecelendirme-o-3500x1040.jpg',
     'banner-derecelendirme-t-3200x1040.jpg', 'banner-derecelendirme-m-1600x480.jpg',
     ['Kurumsal Yönetim Derecelendirme', 'Notumuzu 9,42’den', '9,48’e çıkardık'], 'Detaylı Bilgi',
     'Altın 9,48 rakamı ve defne dalı', False),
    ('banner-tablo-adalar-5200x1040.jpg', 'banner-tablo-adalar-o-3500x1040.jpg',
     'banner-tablo-adalar-t-3200x1040.jpg', 'banner-tablo-adalar-m-1600x480.jpg',
     ['Hemen Taşının', 'Manzaranın Keyfini', 'Siz de Yaşayın'], 'Detaylı Bilgi',
     'Tablo Adalar konut blokları, havuz ve peyzaj alanının genel görünümü', False),
]

# Kurumsal panel dört öğe için ölçülü; fazlası panelden taşıyor.
# Panel etiketleri tek satır: uzun iki ad kısaltıldı. "Devam Eden Projeler"
# orijinal Portföy menüsündeki ad; "Raporlar ve Sunumlar" = Raporlar ve
# Yatırımcı Sunumları.
APPLY_ITEMS = [('Devam Eden Projeler', '#projeler', 'proje'),
               ('Raporlar ve Sunumlar', '#', 'rapor'),
               ('Özel Durum Açıklamaları', '#', 'duyuru'), ('Bize Ulaşın', '#', 'iletisim')]

# Hızlı Erişim ikonları: 24 px çizgi ikon, koyu panel üzerinde beyaz kontur +
# kurumsal sarı vurgu (VakıfBank ikon dilinin koyu zemin karşılığı).
_W = 'stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" fill="none"'
_Y = 'fill="#fdb913"'
APPLY_ICONS = {
    'proje': '<rect x="4" y="3" width="10" height="18" %s/><path d="M14 9h6v12h-6" %s/>'
             '<path d="M7 7h1M10 7h1M7 11h1M10 11h1M7 15h1M10 15h1M17 13h0M17 17h0" %s/>'
             '<rect x="8" y="17.5" width="2" height="3.5" %s/><path d="M2 21h20" %s/>' % (_W, _W, _W, _Y, _W),
    'rapor': '<path d="M6 3h8l4 4v14H6z" %s/><path d="M14 3v4h4" %s/>'
             '<rect x="8.5" y="14" width="2" height="4" %s/><rect x="11.5" y="11" width="2" height="7" %s/>'
             '<rect x="14.5" y="15" width="1.5" height="3" %s/>' % (_W, _W, _Y, _Y, _Y),
    'duyuru': '<path d="M4 10v4h3l7 4V6L7 10z" %s/><path d="M7 14l1.5 5h2.5l-1.3-4.3" %s/>'
              '<path d="M17 9.5a3.5 3.5 0 0 1 0 5" %s/><circle cx="14" cy="12" r="1.2" %s/>' % (_W, _W, _W, _Y),
    'iletisim': '<rect x="3" y="5.5" width="18" height="13" rx="1.5" %s/><path d="M3.5 6.5l8.5 6.5 8.5-6.5" %s/>'
                '<circle cx="18.5" cy="16" r="2.5" %s/>' % (_W, _W, _Y),
    'plan': '<rect x="3.5" y="3.5" width="17" height="17" %s/><path d="M3.5 12h7v8.5M10.5 3.5v5M14 12h6.5M14 12v4" %s/>'
            '<rect x="5" y="5" width="4" height="5.5" %s/>' % (_W, _W, _Y),
    'galeri': '<rect x="3" y="5" width="18" height="14" rx="1.5" %s/><path d="M3.5 17l5-5 4 4 3-3 5 5" %s/>'
              '<circle cx="15.5" cy="9.5" r="1.6" %s/>' % (_W, _W, _Y),
    'konum': '<path d="M12 21s-6.5-6.2-6.5-11a6.5 6.5 0 0 1 13 0c0 4.8-6.5 11-6.5 11z" %s/>'
             '<circle cx="12" cy="10" r="2.4" %s/>' % (_W, _Y),
    # Sanal tur: konut + çevresinde 360° yörünge
    'tur': '<path d="M8 13V8.8l4-3 4 3V13" %s/><path d="M11 13v-2.5h2V13" %s/>'
           '<path d="M5 11.6C3.1 12.3 2 13.1 2 14c0 2.2 4.5 4 10 4s10-1.8 10-4c0-.9-1.1-1.7-3-2.4" '
           'stroke="#fdb913" stroke-width="1.5" stroke-linecap="round" fill="none"/>'
           '<path d="M17.3 10.4l1.8 1.2-1.1 1.8" stroke="#fdb913" stroke-width="1.5" '
           'stroke-linecap="round" stroke-linejoin="round" fill="none"/>' % (_W, _W),
    'form': '<path d="M6 3h12v18H6z" %s/><path d="M9 8h6M9 11.5h6M9 15h3" %s/>'
            '<path d="M14.5 18.5l4.5-4.5 1.5 1.5-4.5 4.5h-1.5z" %s/>' % (_W, _W, _Y),
}


def apply_icon(key):
    return ('<svg class="gyo-apply-ico" width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" '
            'focusable="false">%s</svg>' % APPLY_ICONS[key])


def apply_center(items=None):
    """Kurumsal .banner__apply (Başvuru Merkezi) — Vakıf GYO'da Hızlı Erişim.
    items: başlık ya da (başlık, bağlantı, ikon anahtarı — APPLY_ICONS)."""
    items = [i if isinstance(i, tuple) else (i, '#', None) for i in (items or APPLY_ITEMS)]
    lis = ''.join(
        '<li>%s<a href="%s"%s><p>%s%s</p></a></li>'
        % (apply_icon(k) if k else '<img src="../assets/img/icon/plusgreyborder.svg" alt="" width="24" height="24">',
           h, ' target="_blank" rel="noopener"' if h.startswith('http') else '',
           t, NEW_TAB if h.startswith('http') else '') for t, h, k in items)
    return '''<div class="banner__apply">
<button type="button" class="banner__apply__closed" aria-expanded="false" aria-controls="hizli-erisim">
<picture>
<source media="(min-width: 768px)" srcset="/Templates/Default/assets/img/icon/icon-plus-54.svg" type="image/svg+xml">
<source media="(max-width: 767px)" srcset="/Templates/Default/assets/img/icon/plus-32.svg" type="image/svg+xml">
<img src="/Templates/Default/assets/img/icon/icon-plus-54.svg" alt="" width="54" height="54">
</picture>
<p>Hızlı Erişim</p>
</button>
<div class="banner__apply__opened" id="hizli-erisim">
<div class="banner__apply__opened__menu">
<ul>%s</ul>
</div>
<button type="button" class="banner__apply__opened__btn" aria-label="Hızlı Erişim’i kapat"><i class="icon-close" aria-hidden="true"></i></button>
</div>
</div>''' % lis


def banner(slides_data=None, apply_html=None, label='Projeler ve duyurular', fit=None):
    fit = (slides_data is None or slides_data is BANNER_SLIDES) if fit is None else fit
    slides_data = slides_data or BANNER_SLIDES
    slides = ''
    for n, (big, mid, small, phone, lines, cta, alt, dark) in enumerate(slides_data):
        ps = ''.join('<p>%s</p>' % l for l in lines)
        if fit:
            key = re.sub(r'^banner-(.+)-5200x1040\.jpg$', r'\1', big)
            if A2:
                # A2: daha yüksek bant için ayrı kadrajlar (make_banners_a2.py)
                big, mid, small, phone = ['banner-%s-a2-%s.jpg' % (key, x) for x in 'dotm']
            # ≤767 telefon, ≤1199 sağa yaslı tablet, ≤1699 ana blok (konteynere bağlı), ≥1700 tam kadraj
            sources = ('<source srcset="%s%s" media="(max-width: 767px)">\n'
                       '<source srcset="%s%s" media="(max-width: 1199px)">\n'
                       '<source srcset="%s%s" media="(max-width: 1699px)">' % (IMG, phone, IMG, small, IMG, mid))
            style = ' style="background:%s"' % BANNER_COLORS[key] if key in BANNER_COLORS else ''
        else:
            sources = ('<source srcset="%s%s" media="(max-width: 479px)">\n'
                       '<source srcset="%s%s" media="(max-width: 767px)">\n'
                       '<source srcset="%s%s" media="(max-width: 1199px)">' % (IMG, phone, IMG, small, IMG, mid))
            style = ''
            key = None
        logo = ''
        if fit and key in BANNER_LOGOS:
            lf, ln = BANNER_LOGOS[key]
            logo = ('<span class="sr-only">%s: </span>'
                    '<span class="banner__logo" aria-hidden="true"><img src="%s%s" alt="" width="160" height="60"></span>'
                    % (ln, IMG, lf))
        slides += '''<div class="swiper-slide%s" data-cmg-href="#" data-cmg-text="%s"%s%s>
<a href="#" tabindex="%s">
<picture class="banner__bg">
%s
<img class="radius0" src="%s%s" alt="%s"%s>
</picture>
<div class="container"><div class="banner__text">%s%s</div></div>
</a>
</div>''' % (' white' if dark else '', cta, '' if n == 0 else ' aria-hidden="true"', style,
              '0' if n == 0 else '-1', sources, IMG, big, alt,
              # ana sayfa (fit) slaytlarında görsel genişliği yüklenene kadar 0:
              # tembel yükleme hiç tetiklenmiyordu (A2'de slayt zemini boş kalıyordu).
              # Diğer slaytlar ilk görselden sonra, düşük öncelikle gelir.
              '' if n == 0 else (' fetchpriority="low"' if fit else ' loading="lazy"'), logo, ps)
    dots = ''.join(
        '<button type="button" class="swiper-pagination-bullet%s"><span class="sr-only">%d. görsel</span></button>'
        % (' swiper-pagination-bullet-active' if i == 0 else '', i + 1)
        for i in range(len(slides_data)))
    return '''<section class="banner%s" aria-roledescription="karusel" aria-label="%s">
<div class="swiper home-banner%s" data-banner data-timeout="10000"%s>
<div class="swiper-wrapper">%s</div>
<div class="swiper-controller-wrapper container">
<div class="swiper-pagination">%s</div>
<div class="all-links"><a class="arrow-link" href="#" id="all-campaign-link"><span class="text">%s</span><span class="svg svg--arrow-right-banner" aria-hidden="true"></span></a></div>
</div>
</div>
<p class="sr-only" role="status" data-banner-status></p>
%s
</section>''' % (' banner--fit' if fit else '', label, ' white' if slides_data[0][7] else '',
                ' data-banner-fade' if fit else '', slides, dots,
                slides_data[0][5], apply_center() if apply_html is None else apply_html)


# 2. Araçlar ve Yatırımcı Bilgileri — kurumsal .home-tabs --------------------
PROJECT_OPTIONS = ''.join('<option>%s</option>' % p for p in SALE)

CREDIT_PANE = '''<div class="tab-pane credit-cal" id="hesaplama" role="tabpanel" aria-labelledby="hesaplama-tab" data-gyo-credit>
<div class="credit-cal__left">
<div class="input-block select-100">
<label for="hesap-proje">Proje</label>
<div class="gyo-select"><select id="hesap-proje" name="proje">%s</select></div>
</div>
<div class="input-wrapper">
<div class="input-block">
<label for="hesap-tutar">Kredi Tutarı</label>
<span class="text-input-wrapper">
<input class="amount slider-text" type="text" inputmode="numeric" id="hesap-tutar" name="tutar" value="3.000.000" data-gyo-amount>
<span class="phrase">₺</span>
</span>
</div>
<div class="input-block range">
<div class="range__value"><label aria-hidden="true">500.000 ₺</label><label aria-hidden="true">15.000.000 ₺</label></div>
<input class="gyo-range" type="range" min="500000" max="15000000" step="50000" value="3000000" aria-label="Kredi tutarı kaydırıcısı" data-gyo-amount-range>
</div>
</div>
<div class="input-wrapper">
<div class="input-block">
<label for="hesap-vade">Kredi Vadesi</label>
<span class="text-input-wrapper">
<input class="amount slider-text" type="text" inputmode="numeric" id="hesap-vade" name="vade" value="120" data-gyo-term>
<span class="phrase">Ay</span>
</span>
</div>
<div class="input-block range">
<div class="range__value"><label aria-hidden="true">12 Ay</label><label aria-hidden="true">120 Ay</label></div>
<input class="gyo-range" type="range" min="12" max="120" step="12" value="120" aria-label="Kredi vadesi kaydırıcısı" data-gyo-term-range>
</div>
</div>
<button class="btn btn-outline-secondary btn-calculate" type="button" data-gyo-calc>Hesapla</button>
</div>
<div class="credit-cal__middle"><img src="/Templates/Default/assets/img/icon/equal-to-48.svg" alt="" aria-hidden="true"></div>
<div class="credit-cal__right">
<div class="credit-cal__right__total" aria-live="polite">
<div class="credit-cal__right__total__item">
<div class="credit-cal__right__total__item__icon"><img src="/Templates/Default/assets/img/icon/calendar-tick-64.svg" alt=""></div>
<p>Aylık Taksit</p>
<p class="credit-cal__right__total__item__total" data-gyo-installment>0,00 ₺</p>
</div>
<div class="credit-cal__right__total__item">
<div class="credit-cal__right__total__item__icon"><img src="/Templates/Default/assets/img/icon/payment-64.svg" alt=""></div>
<p>Toplam Geri Ödeme</p>
<p class="credit-cal__right__total__item__total" data-gyo-total>0,00 ₺</p>
</div>
</div>
<div class="credit-cal__right__percentage">
<div class="credit-cal__right__percentage__item"><label>Faiz Oranı</label><p data-gyo-rate data-rate="2.79">%%2,79</p></div>
<div class="credit-cal__right__percentage__item"><label>BSMV</label><p>%%0</p></div>
<div class="credit-cal__right__percentage__item"><label>KKDF</label><p>%%0</p></div>
</div>
<div class="credit-cal__right__bottom">
<a class="btn btn-secondary" href="https://www.vakifbank.com.tr/tr/bireysel/krediler/saripanjur-ev-kredisi" target="_blank" rel="noopener">SarıPanjur Ev Kredisi%s</a>
</div>
</div>
</div>''' % (PROJECT_OPTIONS, NEW_TAB)


def market_rows(header, rows):
    """Kurumsal .market-info__top yapısı: iki sütunlu satır dizisi."""
    head = ('<div class="market-info__top__header d-flex justify-content-between">'
            '<div class="market-info__top__header__title text-left"></div>%s</div>'
            % ''.join('<div class="market-info__top__header__title text-right">%s</div>' % h
                      for h in header))
    out = ('<div class="col-md-6 col-12 market-info__top__container">%s</div>'
           '<div class="col-md-6 col-12 market-info__top__container market-render-right d-md-block d-none">%s</div>'
           % (head, head))
    for r in rows:
        out += ('<div class="col-md-6 col-12 market-render-right"><div class="market-info__top__item d-flex justify-content-between">%s</div></div>'
                % ''.join('<div class="market-info__top__item__title%s">%s</div>'
                          % ('' if i == 0 else ' text-right', c) for i, c in enumerate(r)))
    return out


STOCK_ROWS = [
    # Kurumsal piyasa tablosu kısa kod kullanıyor (USD, EUR); burada BIST kodları.
    ('VKGYO', '3,27', '<span class="gyo-up">%1,24</span>'),
    ('XGMYO', '3.412,58', '<span class="gyo-up">%0,86</span>'),
    ('XU100', '10.284,12', '<span class="gyo-down">-%0,32</span>'),
    ('XUSRD', '13.905,40', '<span class="gyo-up">%0,41</span>'),
    ('XKURY', '12.118,77', '<span class="gyo-up">%0,27</span>'),
]

STOCK_PANE = '''<div class="tab-pane market-info active" id="hisse" role="tabpanel" aria-labelledby="hisse-tab">
<div class="market-info__top">
<div class="container p-md-0 pl-4 pr-4">
<div class="row market-render">%s</div>
</div>
</div>
<div class="market-info__bottom gyo-market-bottom">
<div class="consultion-block">
<div class="button-block">
<a href="#" class="btn btn-outline-secondary btn-icon"><img src="../assets/img/vb/report32.svg" alt="" width="32" height="32">Raporlar ve Yatırımcı Sunumları</a>
</div>
</div>
</div>
</div>''' % market_rows(['Son Fiyat', 'Günlük Değişim'],
                       STOCK_ROWS)

CALENDAR = [
    ('Ekim 2026', '2026 Yılı 9 Aylık Finansal Sonuçlarının Açıklanması'),
    ('Kasım 2026', '9 Aylık Faaliyet Raporu ve Yatırımcı Sunumu'),
    ('Mart 2027', '2026 Yılı Finansal Sonuçlarının Açıklanması'),
    ('Nisan 2027', '2026 Yılı Olağan Genel Kurul Toplantısı'),
]

CALENDAR_PANE = '''<div class="tab-pane market-info" id="takvim" role="tabpanel" aria-labelledby="takvim-tab">
<div class="market-info__top">
<div class="container p-md-0 pl-4 pr-4">
<ul class="gyo-calendar">%s</ul>
</div>
<p class="mt-4 text-right">Kesin tarihler KAP'ta duyurulur.</p>
</div>
</div>''' % ''.join(
    '<li class="gyo-calendar__item"><span class="gyo-calendar__date">%s</span>'
    '<span class="gyo-calendar__title">%s</span>'
    '<a class="arrow-link outline" href="#"><span class="svg svg--arrow-right" aria-hidden="true"></span><span>Takvime Ekle</span></a></li>'
    % c for c in CALENDAR)


def home_tabs():
    tabs = [('hisse', 'VKGYO', True),
            ('hesaplama', 'Konut Kredisi Hesaplama', False)]
    lis = ''.join(
        '<li class="nav-item" role="presentation"><a class="nav-link%s" id="%s-tab" data-toggle="tab" '
        'href="#%s" role="tab" aria-controls="%s" aria-selected="%s">%s</a></li>'
        % (' active' if a else '', i, i, i, 'true' if a else 'false', t) for i, t, a in tabs)
    return '''<section class="home-tabs" aria-labelledby="araclar-baslik">
<div class="container">
<h2 id="araclar-baslik" class="sr-only">Yatırımcı İlişkileri</h2>
<ul class="nav nav-tabs" role="tablist">%s</ul>
<div class="tab-content">%s%s</div>
</div>
</section>''' % (lis, CREDIT_PANE, STOCK_PANE)


# 3. Proje Rehberi — kurumsal .yellow__guide (Sarı Rehber) -------------------
GUIDE = '''<section aria-labelledby="rehber-baslik">
<div class="container">
<div class="yellow__guide">
<h2 id="rehber-baslik" class="searchContent">Size en uygun Vakıf GYO projesini Proje Rehberi’yle bulmak ister misiniz?</h2>
<div class="yellow__guide__links">
<a href="#"><img src="%srehber-oturmak-icin.png" alt="" width="257" height="257"><span>Oturmak<br> İçin</span></a>
<a href="#"><img src="%srehber-yatirim-icin.png" alt="" width="257" height="257"><span>Yatırım<br> İçin</span></a>
</div>
</div>
</div>
</section>''' % (IMG, IMG)


# 4. Öne çıkan proje — kurumsal .retirement --------------------------------
FEATURED = '''<section class="retirement" aria-labelledby="one-cikan-baslik">
<div class="container">
<div class="row">
<div class="col-md-6">
<picture>
<source media="(min-width: 992px)" srcset="%sone-cikan-yasam-basliyor-1078x944.jpg">
<source media="(max-width: 991px)" srcset="%sone-cikan-yasam-basliyor-764x776.jpg">
<img src="%sone-cikan-yasam-basliyor-1078x944.jpg" alt="VSancaktepe Merkez’de anahtar teslim töreninde yeni ev sahibi aile" width="539" height="472" loading="lazy">
</picture>
</div>
<div class="col-md-6">
<div class="retirement__option">
<h2 id="one-cikan-baslik" class="searchContent">VSancaktepe Merkez’de Yaşam Başlıyor</h2>
<a href="#" class="retirement__option__link">
<p>Teslime özel avantajlardan yararlanma fırsatını kaçırmayın</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">Detaylı Bilgi</span></div>
</a>
<a href="#" class="retirement__option__link">
<p>Daire Planları</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">Detaylı Bilgi</span></div>
</a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG)


# 5. Sürdürülebilirlik — kurumsal .sustainable-banking ----------------------
SUSTAIN = '''<section aria-labelledby="surdurulebilirlik-baslik">
<div class="container">
<div class="sustainable-banking">
<picture class="sustainable-banking__bg">
<source srcset="%ssurdurulebilirlik-750x870.jpg" media="(max-width: 767px)">
<img src="%ssurdurulebilirlik-2280x926.jpg" alt="" loading="lazy">
</picture>
<div class="sustainable-banking__content">
<h2 id="surdurulebilirlik-baslik" class="gyo-sustain-title">Sürdürülebilirlik</h2>
<div class="searchContent"><p>Sürdürülebilirlik, Vakıf GYO’nun temel stratejilerinden biridir. Çevresel, sosyal ve yönetişim (ESG) prensipleriyle faaliyet gösteren şirketimiz, gelecek nesillere daha yaşanabilir bir dünya bırakmayı amaçlamaktadır.</p></div>
<ul>
<li><a href="#" class="arrow-link"><span class="svg svg--arrow-right" aria-hidden="true"></span>Kilometre Taşları</a></li>
<li><a href="#" class="arrow-link"><span class="svg svg--arrow-right" aria-hidden="true"></span>Raporlar ve Sertifikalar</a></li>
<li><a href="#" class="arrow-link"><span class="svg svg--arrow-right" aria-hidden="true"></span>Kurumsal Sosyal Sorumluluk</a></li>
</ul>
</div>
</div>
</div>
</section>''' % (IMG, IMG)


# 6. Projelerimiz — kurumsal .insurance (kart carousel) ---------------------
# Lokasyon ve cümleler vakifgyo.com.tr portföy sayfalarından birebir (_docs/kaynak/portfoy-portfoy-*.txt);
# etiketler menü gruplarından (Devam Eden Projeler / Tamamlanan Projeler).
PROJECTS = [
    ('vsancaktepe-merkez', 'VSancaktepe Merkez', 'İstanbul İli, Sancaktepe İlçesi',
     'Konut ve ticari ünitelerden oluşan projemiz, nitelikli peyzaj kurgusu ve ferah mekanlarıyla İstanbul’da özlenen '
     'geleneksel aile hayatını, bahçeli, geniş balkon ve teraslı, sosyal aktiviteli şehir hayatıyla birleştirerek, '
     'pandemi sonrası değişen konut beklentilerini karşılamayı amaçlamaktadır.',
     'Devam Eden Projeler'),
    ('vyenikonak', 'VYeniKonak', 'İzmir İli, Konak İlçesi, Mersinli Mahallesi',
     'İş merkezi kulelerinin yükselmekte olduğu, İzmir Konak ilçesinde; ofis, ticari ve konut nitelikli VYeniKonak '
     'Projesi ile müşterilerimize konforlu, sağlıklı yaşam alanı sunmayı ve bölge potansiyelini artırmayı hedefliyoruz.',
     'Devam Eden Projeler'),
    ('tablo-adalar', 'Tablo Adalar', 'İstanbul İli, Maltepe İlçesi, Zümrütevler Mahallesi',
     'İstanbul Anadolu Yakası\'nda yer alan, Marmara Denizi ve Adalar manzaralı, merkezi konumdaki "Tablo Adalar" '
     'projemiz, 1+1\'den 5+2\'e kadar değişen konut tiplerinin yanı sıra, geniş balkon, büyük peyzaj alanı ve zengin '
     'sosyal donatıları bulunduruyor.',
     'Tamamlanan Projeler'),
    ('cubes-ankara', 'Cubes Ankara', 'Ankara İli, Çankaya İlçesi, Çukurambar Mahallesi',
     'Ankara Çukurambar\'da yer alan Cubes Ankara Projemiz; 215.984,66 m2 kapalı inşaat alanına sahip 1+1\'den, '
     '6+1\'e kadar değişen konut, home office, ofis ile otel, ticari ve sosyal donatı alanlarından oluşuyor.',
     'Tamamlanan Projeler'),
]


def projects():
    cards = ''.join('''<div class="col-md-4 swiper-slide">
<a class="insurance__item gyo-project" href="%s">
<span class="gyo-project__media"><img src="%sproje-%s-710x410.jpg" alt="" width="355" height="205" class="img-fluid" loading="lazy"><span class="gyo-project__tag">%s</span></span>
<span class="gyo-project__place">%s</span>
<span class="landing-heading-h5">%s</span>
<span class="searchContent"><span class="gyo-project__desc">%s</span></span>
</a>
</div>''' % (href(name), IMG, slug, tag, place, name, desc) for slug, name, place, desc, tag in PROJECTS)
    return '''<section class="insurance" id="projeler" aria-labelledby="projeler-baslik">
<div class="container">
<h2 id="projeler-baslik" class="gyo-section-title">Satışı Devam Eden Projelerimiz</h2>
<div class="insurance-swiper gyo-rail" data-gyo-rail>
<div class="swiper-wrapper row" tabindex="0" aria-label="Proje kartları, yatay kaydırılabilir">%s</div>
</div>
<div class="gyo-rail__foot">
<div class="gyo-rail__nav">
<button type="button" class="gyo-rail__btn" data-gyo-prev aria-label="Önceki projeler"><span class="svg svg--chevron-left" aria-hidden="true"></span></button>
<button type="button" class="gyo-rail__btn" data-gyo-next aria-label="Sonraki projeler"><span class="svg svg--chevron-left gyo-flip" aria-hidden="true"></span></button>
</div>
<a href="#" class="arrow-link outline"><span class="svg svg--arrow-right" aria-hidden="true"></span><span>Portföy</span></a>
</div>
</div>
</section>''' % cards


# 7. Kurumsal kartlar — kurumsal .quick-access ------------------------------
def quick_item(cls, name, title, buttons, link_cls='', more='#'):
    btns = ''.join(
        '<a class="quick-access__item__link btn btn-outline-gray" href="#">'
        '<span class="svg %s" aria-hidden="true"></span><span class="content">%s</span></a>'
        % (icon, label) for icon, label in buttons)
    return '''<div class="col-md-6">
<div class="quick-access__item %s">
<picture>
<source media="(min-width: 768px)" srcset="%shizli-%s-1082x1000.jpg">
<source media="(max-width: 767px)" srcset="%shizli-%s-762x1000.jpg">
<img src="%shizli-%s-1082x1000.jpg" alt="" loading="lazy">
</picture>
<div class="quick-access__item__content">
<h2>%s</h2>
<div class="quick-access__item__buttons">
<div>%s</div>
<a href="%s" class="all arrow-link%s"><span class="svg svg--arrow-right" aria-hidden="true"></span><span>Detaylı Bilgi</span></a>
</div>
</div>
</div>
</div>''' % (cls, IMG, name, IMG, name, IMG, name, title, btns, more, link_cls)


QUICK = '''<section class="quick-access">
<div class="container">
<div class="row">%s%s</div>
</div>
</section>''' % (
    quick_item('digital-banking', 'yatirimci-iliskileri', 'Yatırımcı İlişkileri',
               [('svg--file', 'Raporlar ve Yatırımcı Sunumları'), ('svg--info-circle', 'Özel Durum Açıklamaları')],
               more='yatirimci-iliskileri.html'),
    quick_item('digital-banking', 'portfoy', 'Portföy',
               [('svg--branch', 'Tamamlanan Projeler'), ('svg--marker', 'Gayrimenkul Yatırımları')]))


# 8. Duyurular · Kiralık Alanlar · İnsan Kaynakları — kurumsal .mix ---------
def mix_item(icon, title, text, links):
    """icon: kurumsal 96 px ikon dosya adı (assets/img/vb) ya da tam yol.
    Duyurular ve İK kurumsal setten; Ödüller için aynı dille çizilen
    madalya (assets/img/gyo/oduller96.svg) — kurumsal sette ödül ikonu yok."""
    a = ''.join('<a class="outline" href="#"><span class="svg svg--arrow-right" aria-hidden="true"></span><span>%s</span></a>' % l
                for l in links)
    return '''<div class="col-md-4">
<div class="mix__content">
<div class="mix__content__top">
<img src="%s" alt="" width="96" height="96">
<div class="mix__content__top__text">
<p class="heading-h5">%s</p>
<p class="searchContent">%s</p>
</div>
</div>
<div class="mix__content__links%s">%s</div>
</div>
</div>''' % (icon if '/' in icon else '../assets/img/vb/' + icon, title, text, ' double' if len(links) > 1 else '', a)


MIX = '''<section class="mix" aria-label="Duyurular, ödüller ve insan kaynakları">
<div class="container">
<div class="row">%s%s%s</div>
</div>
</section>''' % (
    # metinler: _docs/kaynak/duyurular.txt, oduller.txt, kurumsal.txt
    mix_item('duyurular.svg', 'Duyurular', 'Pay Sahipleri Bilgilendirme', ['Devamını Oku']),
    mix_item('../assets/img/gyo/oduller96.svg', 'Ödüller', 'Vakıf GYO, EFQM Küresel Ödülü’nün sahibi oldu.', ['Devamını Oku']),
    mix_item('hr96.svg', 'IK Politikamız', 'IK Politikamız &amp; Başvuru Formu', ['Detaylı Bilgi']))


# 9. 30. Yıl bandı — kurumsal .private-banking ------------------------------
ANNIVERSARY = '''<section class="private-banking" aria-labelledby="otuz-yil-baslik">
<div class="container">
<div class="private-banking__content">
<picture>
<source media="(min-width: 768px)" srcset="%s30-yil-1110x463.jpg 1x, %s30-yil-2220x926.jpg 2x">
<source media="(max-width: 767px)" srcset="%s30-yil-343x463.jpg 1x, %s30-yil-686x926.jpg 2x">
<img src="%s30-yil-1110x463.jpg" alt="İstanbul Uluslararası Finans Merkezi’nde VakıfBank Genel Müdürlük binasının gece görünümü" loading="lazy">
</picture>
<div class="private-banking__content__top">
<h2 id="otuz-yil-baslik" class="searchContent">Vakıf GYO<br>30 Yaşında</h2>
<div class="private-banking__content__top__bottom-text">
<div class="searchContent"><p>Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak, 30 yıldır güçlü Türkiye’nin temellerini atıyoruz. Birlikte nice yıllara…</p></div>
<a href="hakkimizda.html" class="arrow-link"><span class="svg svg--arrow-right-yellow" aria-hidden="true"></span><span>Hakkımızda</span></a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG, IMG, IMG)


# 10. Satış Ofisi Arama — kurumsal .branch-atm ------------------------------
OFFICES = '''<section class="branch-atm" aria-labelledby="ofis-baslik">
<div class="container">
<p class="heading-h5" id="ofis-baslik">Satış Ofisi Arama</p>
<div class="row">
<div class="col-md-6">
<div class="branch-atm__left">
<p class="searchContent">Size en yakın satış ofisini listeleyebilirsiniz</p>
<a href="#" class="btn btn-outline-gray"><span class="svg svg--pin" aria-hidden="true"></span><span>En yakın satış ofisini listele</span></a>
</div>
</div>
<div class="col-md-6">
<div class="branch-atm__right">
<p class="searchContent">veya arama yapabilirsiniz:</p>
<form class="branch-atm__right__search" role="search" aria-label="Satış ofisi arama" action="#">
<div class="branch-atm__right__search__top">
<div class="checkbox-block"><input type="checkbox" name="ofis" id="ofis-satis" checked><label for="ofis-satis">Satış Ofisi</label></div>
<div class="checkbox-block"><input type="checkbox" name="ofis" id="ofis-gm"><label for="ofis-gm">Genel Müdürlük</label></div>
</div>
<div class="branch-atm__right__search__bottom">
<label class="sr-only" for="ofis-ara">İl, ilçe veya proje adı</label>
<input type="text" id="ofis-ara" placeholder="İl, ilçe veya proje adı">
<button type="submit" class="btn btn-outline-secondary">Ara</button>
</div>
</form>
</div>
</div>
</div>
</div>
</section>'''


# 11. Yardım ve İletişim — kurumsal .help -----------------------------------
HELP = '''<section id="iletisim" aria-labelledby="yardim-baslik">
<h2 id="yardim-baslik" class="sr-only">Yardım ve İletişim</h2>
<div class="container">
<div class="help">
<div class="row">
<div class="col-md-6">
<div class="help__slider swiper">
<div class="swiper-wrapper">
<div class="swiper-slide" style="background-image:url('%syardim-ilerleme-1080x910.jpg');background-size:cover">
<a class="help__slider__top" href="#"><span class="svg svg--play" aria-hidden="true"></span><p class="heading-h5"><strong>VSancaktepe Merkez İlerleme Durumu</strong></p></a>
<div class="all-links"><a class="link-arrow right" href="#">Tüm Şantiye Videoları</a></div>
</div>
</div>
</div>
</div>
<div class="col-md-6">
<div class="help__right">
<a href="#" class="contact-form btn btn-outline-gray searchContent" id="on-talep"><span class="svg svg--envelope" aria-hidden="true"></span><span>Ön Talep Formunu Doldurun</span></a>
<div class="help__center">
<a href="#">
<div class="row">
<div class="col-md-6">
<div class="help__center__top">
<div class="help__center__top__title">
<p class="heading-h5">Sık Sorulan Sorular</p>
<div class="searchContent"><p>Konut satın alma, kredi, teslim ve tapu süreçleriyle ilgili merak ettiklerinize göz atabilirsiniz.</p></div>
</div>
<div class="d-flex"><span class="outline searchContent"><span class="svg svg--arrow-right" aria-hidden="true"></span><span><p>Sık Sorulan Sorular</p></span></span></div>
</div>
</div>
<div class="col-md-6"><img src="../assets/img/vb/yardim-merkezi-223x301.jpg" alt="" width="223" height="301"></div>
</div>
</a>
</div>
</div>
</div>
</div>
</div>
</div>
</section>''' % IMG


def index():
    # Satış Ofisi Arama (OFFICES) çıkarıldı: kaynakta böyle bir bölüm ve metin yok.
    body = '\n'.join([banner(), home_tabs(), FEATURED, SUSTAIN, projects(),
                      QUICK, MIX, ANNIVERSARY])
    return page('Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası',
                'Vakıf GYO — Geleneğin Gücü, Geleceğin İnşası. Kurumsal · Portföy · Yatırımcı İlişkileri · '
                'Güncel · Sürdürülebilirlik · Bize Ulaşın', body, TICKER)


def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, 'index.html')
    open(path, 'w', encoding='utf-8', newline='\n').write(index())
    print('yazıldı:', os.path.relpath(path, ROOT))


if __name__ == '__main__':
    main()
