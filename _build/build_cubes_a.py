# -*- coding: utf-8 -*-
"""
Cubes Ankara landing — Alternatif A ve A2 (cubes-ankara.html)

VSancaktepe proje sitesiyle aynı kurumsal kabuk ve bileşenler; mor (logo
rengi) ve Cubes logosu ayırt eder (05-gyo-pages.css ".gyo-cubes"). Metinler
cubes_data.py üzerinden, birebir kaynaktan. build_alt_a_pages.main() çağırır;
A2 için görseller build_alt_a2.RE_SWAP ile değişir.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_alt_a as b  # noqa: E402
import build_alt_a_pages as ap  # noqa: E402
import cubes_data as cd  # noqa: E402

IMG, NEW_TAB = b.IMG, b.NEW_TAB
C_LOGO = IMG + 'cubes-logo.png'
PAGE = 'cubes-ankara.html'

MENU = [('Proje Hakkında', '#proje'), ('Daire Planları', '#daireler'), ('Galeri', '#galeri'),
        ('Sanal Tur', '#sanal-tur'), ('Konum', '#konum'), ('Kampanyalar', '#kampanya'),
        ('İletişim Formu', '#on-talep')]

TOP = '''
<a href="index.html" class="header__links-link gyo-byline"><img src="%s" alt="" width="70" height="12"><span class="header__links-text">Vakıf GYO güvencesiyle</span></a>
<a href="#on-talep" class="header__links-link">%s<span class="header__links-text">Satış Ofisi</span></a>
<a href="%s" class="header__links-link">%s<span class="header__links-text">%s</span></a>
''' % ('../assets/img/b/vakif-gyo-logo-ters.svg', b.top_icon('<path d="M8 14.5s4.8-4.4 4.8-8.1A4.8 4.8 0 0 0 3.2 6.4c0 3.7 4.8 8.1 4.8 8.1z"/>'
                                                     '<circle cx="8" cy="6.4" r="1.7"/>'),
       cd.PHONE[0], b.ICON_PHONE, cd.PHONE[1])


def header():
    h = b.HEAD
    h = b.sub_block(h, '<div class="header__links">', TOP)
    h = b.sub_block(h, '<div class="header__mobile__quick-link">', ap.VS_MOBILE_QUICK)
    h = b.sub_block(h, '<div class="placeholder-content open">', '')
    h = h.replace('href="/tr" aria-label="VakıfBank Anasayfa"', 'href="%s" aria-label="Cubes Ankara ana sayfa"' % PAGE)
    h = re.sub(r'(src|srcset)="/Templates/Default/assets/img/(?:footer-)?logo\.svg"', r'\1="%s"' % C_LOGO, h)
    h = h.replace('alt="VakıfBank Logo"', 'alt="Cubes Ankara"')
    h = h.replace('VakıfBank, daima seninle', 'Cubes Ankara')
    h = re.sub(r'<h1 class="site__logo">.*?</h1>', '', h, flags=re.S)
    h = h.replace('<header class="header', '<header class="header gyo-project-header gyo-cubes-header', 1)
    h = re.sub(r'<a href="javascript:;" class="header__menu-search"[^>]*>.*?</a>', '', h, count=1, flags=re.S)
    nav = ''.join('<div class="header__menu-item"><a class="header__menu-link" href="%s">%s</a></div>' % (h_, t)
                  for t, h_ in MENU)
    nav = '<nav class="header__menu" aria-label="Proje menüsü">' + nav + '</nav>'
    tail = b.TAIL.replace(
        re.search(r'<div class="header__btns">.*?</div>', b.TAIL, re.S).group(0),
        '<div class="header__btns"><a href="#on-talep" class="btn btn-primary">Ön Talep</a></div>')
    return h + nav + tail


FOOTER_TOP = '''
<ul>
<li><a href="#proje">Proje Hakkında</a></li>
<li><a href="#daireler">Daire Planları</a></li>
<li><a href="#galeri">Galeri</a></li>
<li><a href="#tanitim-filmi">Tanıtım Filmi</a></li>
</ul>
<ul>
<li><a href="#kampanya">Kampanyalar</a></li>
<li><a href="#hesaplama">Konut Kredisi Hesaplama</a></li>
<li><a href="%s" target="_blank" rel="noopener">Tanıtım Broşürü%s</a></li>
<li><a href="#on-talep">İletişim Formu</a></li>
</ul>
<ul>
<li><a href="#">Gizlilik ve Kişisel Verilerin Korunması</a></li>
</ul>
''' % (cd.BROCHURE, NEW_TAB)

FOOTER_BOTTOM = '''
<ul>
<li><a href="index.html">Vakıf GYO</a></li>
<li><a href="vsancaktepe-merkez.html">VSancaktepe Merkez</a></li>
<li><a href="https://vyenikonak.com.tr" target="_blank" rel="noopener">VYeniKonak%s</a></li>
<li><a href="https://tabloadalar.com.tr" target="_blank" rel="noopener">Tablo Adalar%s</a></li>
</ul>
''' % ((NEW_TAB,) * 2)


def footer():
    f = b.footer()
    f = re.sub(r'<a href="index.html" class="footer__logo">.*?</a>',
               '<a href="%s" class="footer__logo gyo-footer-vs gyo-footer-cubes">'
               '<img src="%s" alt="Cubes Ankara" width="150" height="31"></a>' % (PAGE, IMG + 'cubes-logo-ters.png'), f, flags=re.S)
    f = re.sub(r'<a href="tel:[^"]*" class="footer__phone">(.*?)<span>[^<]*</span>',
               r'<a href="%s" class="footer__phone">\1<span>%s</span>' % cd.PHONE, f, flags=re.S)
    f = b.sub_block(f, '<div class="footer__sitemap__top">', FOOTER_TOP)
    f = b.sub_block(f, '<div class="footer__sitemap__bottom">', FOOTER_BOTTOM)
    f = re.sub(r'<p class="footer__copyright">.*?</p>',
               '<p class="footer__copyright gyo-footer-guarantee"><a href="index.html">'
               '<img src="%s" alt="Vakıf GYO" width="115" height="20"></a>'
               'VakıfBank Finans Grubu İştirakidir.</p>' % b.LOGO, f, flags=re.S)
    f = b.sub_block(f, '<div class="footer__mobile__links">',
                    '<a href="index.html" class="footer__mobile__links-link"><span class="footer__mobile__links-text">Vakıf GYO güvencesiyle</span></a>')
    return f


BANNER = [
    ('banner-cubes-3024x1040.jpg', 'banner-cubes-2400x828.jpg', 'banner-cubes-1536x480.jpg', 'banner-cubes-828x480.jpg',
     ['Ankara’nın', 'Yeni Havası'], 'İletişim Formu', 'Cubes Ankara rezidans ve ofis kulelerinin akşam görünümü', True),
    ('cubes-banner-yasam-1512x520.jpg', 'cubes-banner-yasam-1512x520.jpg', 'cubes-banner-yasam-1536x480.jpg',
     'cubes-banner-yasam-828x480.jpg', ['Ankara’nın', 'Yeni Yaşam Tarzı'], 'Detaylı Bilgi',
     'Çatı katındaki havuz ve şehir silueti', True),
    ('cubes-banner-calisma-1512x520.jpg', 'cubes-banner-calisma-1512x520.jpg', 'cubes-banner-calisma-1536x480.jpg',
     'cubes-banner-calisma-828x480.jpg', ['Ankara’nın', 'Yeni Çalışma Alanı'], 'Detaylı Bilgi',
     'Ofis bloğunun cadde cephesi', True),
]

APPLY = [('Daire Planları', '#daireler', 'plan'), ('Galeri', '#galeri', 'galeri'),
         ('Sanal Tur', cd.TOUR, 'tur'), ('Konum', '#konum', 'konum'),
         ('İletişim Formu', '#on-talep', 'form')]


def about():
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in cd.FACTS)
    return '''<section class="retirement gyo-vs-about" id="proje" aria-labelledby="proje-baslik">
<div class="container">
<div class="row">
<div class="col-md-6">
<picture>
<img src="%scubes-bloklar-1600x800.jpg" alt="A Blok Rezidans ve B Blok Ofis kuleleri; Sky Cubes, kat bahçeleri ve sosyal alanların yerleri işaretli" width="800" height="400" loading="lazy">
</picture>
</div>
<div class="col-md-6">
<div class="retirement__option">
<p class="gyo-eyebrow">Proje Hakkında</p>
<h2 id="proje-baslik" class="searchContent">Cubes Ankara</h2>
<p class="gyo-lede">%s</p>
<dl class="gyo-facts">%s</dl>
</div>
</div>
</div>
</div>
</section>''' % (IMG, cd.ABOUT, facts)


def plan_pane(p, first):
    rows = ''.join('<tr><th scope="row">%s</th><td>%s m²</td></tr>' % r for r in p['rooms'])
    totals = ''
    if p['net']:
        totals = ('<ul class="gyo-plan__totals"><li><span>Net Alan</span><strong>%s m²</strong></li>'
                  '<li><span>Toplam Brüt Alan</span><strong>%s m²</strong></li></ul>' % (p['net'], p['gross']))
    h = cd.plan_img_height('cubes-plan-%s-1200.jpg' % p['key'])
    return '''<div class="gyo-plan" id="plan-%s" role="tabpanel" aria-labelledby="plan-%s-tab"%s>
<figure class="gyo-plan__img"><img src="%scubes-plan-%s-1200.jpg" alt="%s %s %s daire planı" width="1200" height="%d" loading="lazy"></figure>
<div class="gyo-plan__info">
<p class="gyo-plan__name">%s <span>%s · %s</span></p>
%s
<div class="gyo-plan__rooms gyo-plan__rooms--open"><table><caption class="sr-only">%s %s</caption><tbody>%s</tbody></table></div>
%s
</div>
</div>''' % (p['key'], p['key'], '' if first else ' hidden', IMG, p['key'], p['name'], p['group'], p['typ'], h,
             p['group'], p['name'], p['typ'], totals, p['name'], p['typ'], rows, ap.arrow('İletişim Formu', '#on-talep'))


def plans_pane():
    allp = cd.plans()
    groups = cd.groups()
    tags = ''.join('<button type="button" class="tag%s" role="tab" id="grup-%d-tab" aria-controls="grup-%d" '
                   'aria-selected="%s" data-gyo-switch="grup-%d"%s>%s</button>'
                   % (' active' if i == 0 else '', i, i, 'true' if i == 0 else 'false', i,
                      '' if i == 0 else ' tabindex="-1"', g) for i, g in enumerate(groups))
    panes = ''
    for i, g in enumerate(groups):
        ps = [p for p in allp if p['group'] == g]
        sub = ''.join('<button type="button" class="tag gyo-tag--sub%s" role="tab" id="plan-%s-tab" aria-controls="plan-%s" '
                      'aria-selected="%s" data-gyo-switch="plan-%s"%s>%s <span>%s</span></button>'
                      % (' active' if j == 0 else '', p['key'], p['key'], 'true' if j == 0 else 'false', p['key'],
                         '' if j == 0 else ' tabindex="-1"', p['name'], p['typ']) for j, p in enumerate(ps))
        panes += '''<div class="gyo-plangroup" id="grup-%d" role="tabpanel" aria-labelledby="grup-%d-tab"%s data-gyo-switcher>
<div class="tags gyo-plans__tags gyo-plans__tags--sub" role="tablist" aria-label="%s daire tipleri">%s</div>
%s
</div>''' % (i, i, '' if i == 0 else ' hidden', g, sub, ''.join(plan_pane(p, j == 0) for j, p in enumerate(ps)))
    return '''<div class="tab-pane active" id="daire-tipleri" role="tabpanel" aria-labelledby="daire-tipleri-tab">
<div class="gyo-plans" data-gyo-switcher>
<div class="tags gyo-plans__tags" role="tablist" aria-label="Daire tipi">%s</div>
%s
</div>
</div>''' % (tags, panes)


def tabs():
    items = [('daire-tipleri', 'Daire Planları', True), ('hesaplama', 'Konut Kredisi Hesaplama', False)]
    lis = ''.join(
        '<li class="nav-item" role="presentation"><a class="nav-link%s" id="%s-tab" data-toggle="tab" '
        'href="#%s" role="tab" aria-controls="%s" aria-selected="%s">%s</a></li>'
        % (' active' if a else '', i, i, i, 'true' if a else 'false', t) for i, t, a in items)
    credit = b.CREDIT_PANE.replace('credit-cal active', 'credit-cal', 1)
    credit = re.sub(r'<div class="input-block select-100">.*?</div>\s*</div>\s*', '', credit, count=1, flags=re.S)
    # SarıPanjur Ev Kredisi bağlantısı proje sitesinde yok
    credit = re.sub(r'<a class="btn btn-secondary" href="https://www.vakifbank.com.tr[^"]*"[^>]*>SarıPanjur Ev Kredisi.*?</a>', '', credit, count=1, flags=re.S)
    return '''<section class="home-tabs gyo-vs-tabs" id="daireler" aria-labelledby="daireler-baslik">
<div class="container">
<h2 id="daireler-baslik" class="gyo-section-title">Daire Planları</h2>
<ul class="nav nav-tabs" role="tablist">%s</ul>
<div class="tab-content">%s%s</div>
</div>
</section>''' % (lis, plans_pane(), credit)


def features():
    first, rest = cd.BLOCKS[0], cd.BLOCKS[1:]
    items = ''.join('<li class="gyo-feat gyo-feat--text"><p class="gyo-feat__title">%s</p><p class="gyo-feat__text">%s</p></li>'
                    % f for f in rest)
    return '''<section class="gyo-section gyo-section--gray" aria-labelledby="yeni-baslik">
<div class="container">
<h2 class="gyo-section-title" id="yeni-baslik">%s</h2>
<p class="gyo-section-lede">%s</p>
<ul class="gyo-feats gyo-feats--text">%s</ul>
</div>
</section>''' % (first[0], first[1], items)


def gallery():
    figs = ''.join('<li class="gyo-gallery__item"><img src="%scubes-galeri-%d-960x640.jpg" alt="%s" width="960" '
                   'height="640" loading="lazy"></li>' % (IMG, i, a) for i, (_k, a) in enumerate(cd.GALLERY, 1))
    return '''<section class="gyo-section" id="galeri" aria-labelledby="galeri-baslik">
<div class="container">
%s
<ul class="gyo-gallery">%s</ul>
</div>
</section>''' % (ap.head('Galeri', 'galeri-baslik'), figs)


TOUR = '''<section class="private-banking gyo-tour" id="sanal-tur" aria-labelledby="tur-baslik">
<div class="container">
<div class="private-banking__content">
<picture>
<source media="(min-width: 768px)" srcset="%scubes-sanal-tur-1110x463.jpg 1x, %scubes-sanal-tur-2220x926.jpg 2x">
<source media="(max-width: 767px)" srcset="%scubes-sanal-tur-343x463.jpg 1x, %scubes-sanal-tur-686x926.jpg 2x">
<img src="%scubes-sanal-tur-1110x463.jpg" alt="Sanal turdan örnek dairenin salonu" loading="lazy">
</picture>
<div class="private-banking__content__top">
<h2 id="tur-baslik" class="searchContent">%s</h2>
<div class="private-banking__content__top__bottom-text">
<div class="searchContent"><p>%s</p></div>
<a href="%s" class="btn btn-primary gyo-tour__btn" target="_blank" rel="noopener">Sanal Tur%s</a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG, IMG, IMG, cd.SAMPLE[0], cd.SAMPLE[1], cd.TOUR, NEW_TAB)


def campaign():
    k, title, text, more = cd.CAMPAIGN
    return '''<section class="retirement gyo-retirement--flip" id="kampanya" aria-labelledby="kampanya-baslik">
<div class="container">
<div class="row">
<div class="col-md-6">
<picture>
<img src="%scubes-kampanya-1078x944.jpg" alt="Ofis bloğunun cadde cephesi" width="539" height="472" loading="lazy">
</picture>
</div>
<div class="col-md-6">
<div class="retirement__option">
<p class="gyo-eyebrow">%s</p>
<h2 id="kampanya-baslik" class="searchContent">%s</h2>
<p class="gyo-lede">%s</p>
<a href="#on-talep" class="retirement__option__link">
<p>%s</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">Bize Ulaşın</span></div>
</a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, k, title, text, more)


def film():
    return '''<section class="gyo-section gyo-section--gray" id="tanitim-filmi" aria-labelledby="film-baslik">
<div class="container">
<h2 class="gyo-section-title" id="film-baslik">Tanıtım Filmi</h2>
<div class="row gyo-row-gap gyo-progress">
<div class="col-12 col-lg-8">
<figure class="gyo-video">
<video controls preload="none" playsinline poster="%scubes-film-1280x720.jpg" width="1280" height="720" aria-label="Tanıtım Filmi">
<source src="%s" type="video/mp4">
</video>
</figure>
</div>
<div class="col-12 col-lg-4">
<div class="gyo-panel gyo-months">
<p class="gyo-panel__title">Tanıtım</p>
<ul>
<li><a href="#tanitim-filmi" aria-current="true"><span class="svg svg--play" aria-hidden="true"></span>Tanıtım Filmi</a></li>
<li><a href="%s" target="_blank" rel="noopener"><span class="svg svg--download" aria-hidden="true"></span>Tanıtım Broşürü%s</a></li>
</ul>
</div>
</div>
</div>
</div>
</section>''' % (IMG, cd.FILM, cd.BROCHURE, NEW_TAB)


def location():
    bbox = '%.4f,%.4f,%.4f,%.4f' % (cd.LON - 0.02, cd.LAT - 0.011, cd.LON + 0.02, cd.LAT + 0.011)
    return '''<section class="gyo-section" id="konum" aria-labelledby="konum-baslik">
<div class="container">
<h2 class="gyo-section-title" id="konum-baslik">Konum</h2>
<div class="row gyo-row-gap">
<div class="col-12 col-lg-5">
<p class="gyo-lede">%s</p>
</div>
<div class="col-12 col-lg-7">
<div class="gyo-map">
<span class="gyo-map__pin" aria-hidden="true"></span>
<iframe title="Cubes Ankara konumu, OpenStreetMap haritası" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=%s&amp;layer=mapnik&amp;marker=%s,%s"></iframe>
</div>
</div>
</div>
</div>
</section>''' % (cd.KONUM, bbox, cd.LAT, cd.LON)


def lead_form():
    opts = ''.join('<option>%s</option>' % g for g in cd.groups())
    return '''<section class="gyo-section gyo-section--gray" id="on-talep" aria-labelledby="talep-baslik">
<div class="container">
<div class="row gyo-row-gap">
<div class="col-12 col-lg-7">
<h2 class="gyo-section-title" id="talep-baslik">İletişim Formu</h2>
<form class="form-content gyo-form" action="#" data-gyo-form novalidate>
<div class="gyo-form__grid">
<div class="input-block"><label for="t-ad">Ad Soyad</label><input type="text" id="t-ad" name="ad" autocomplete="name" required></div>
<div class="input-block"><label for="t-tel">Cep Telefonu</label><input type="tel" id="t-tel" name="telefon" autocomplete="tel" inputmode="tel" placeholder="05xx xxx xx xx" required></div>
<div class="input-block"><label for="t-eposta">E-posta</label><input type="email" id="t-eposta" name="eposta" autocomplete="email"></div>
<div class="input-block"><label for="t-tip">İlgilendiğiniz Daire Tipi</label><div class="gyo-select"><select id="t-tip" name="tip"><option value="">Seçiniz</option>%s</select></div></div>
</div>
<div class="checkbox-block"><input type="checkbox" id="t-kvkk" name="kvkk" required><label for="t-kvkk"><a href="#">Bilgilendirme Metnini</a> Okudum ve Onaylıyorum</label></div>
<button type="submit" class="btn btn-primary gyo-form__btn">Gönder</button>
<p class="gyo-form__done" role="status" hidden>Gönderildi.</p>
</form>
</div>
<div class="col-12 col-lg-5">
<div class="gyo-panel gyo-office">
<p class="gyo-panel__title">Satış Ofisi</p>
<ul class="gyo-office__list">
<li><span class="svg svg--phone" aria-hidden="true"></span><a href="%s">%s</a></li>
</ul>
<p>%s</p>
</div>
</div>
</div>
</div>
</section>''' % (opts, cd.PHONE[0], cd.PHONE[1], cd.SAMPLE[1])


def page():
    banner = b.banner(BANNER, b.apply_center(APPLY), label='Cubes Ankara')
    body = '\n'.join([banner, about(), tabs(), features(), gallery(), TOUR, campaign(), film(), location(),
                      lead_form(), ap.GUARANTEE, ap.VS_DOCK])
    return b.page('Cubes Ankara',
                  'Proje Hakkında · Daire Planları · Tanıtım Filmi · Sanal Tur · Konum · İletişim Formu', body,
                  h1='<h1 class="sr-only">Cubes Ankara</h1>',
                  shell=(header(), footer()), main_cls='gyo-vs gyo-cubes')


if __name__ == '__main__':
    ap.main()
