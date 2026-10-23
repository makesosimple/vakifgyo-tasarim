# -*- coding: utf-8 -*-
"""
Cubes Ankara landing — Alternatif B ve B-üst (cubes-ankara.html)

VSancaktepe sayfasıyla aynı kabuk ve bileşenler; mor (logo rengi) ve Cubes
logosu ayırt eder (b.css ".b--cubes"). Metinler cubes_data.py üzerinden,
birebir kaynaktan. build_alt_b.main() bu modülü çağırır.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_alt_b as b  # noqa: E402
import cubes_data as cd  # noqa: E402

GYO, IMG, LOGO, NEW_TAB = b.GYO, b.IMG, b.LOGO, b.NEW_TAB
ico, btn, link, section_head = b.ico, b.btn, b.link, b.section_head
C_LOGO = GYO + 'cubes-logo-ters.png'
PAGE = 'cubes-ankara.html'

# Sıra cubesankara.com.tr menüsünü izler: Proje Hakkında · Daire Planları · (İlerleme Durumu) · Sanal Tur · Konum;
# Tanıtım Filmi / Tanıtım Broşürü / İletişim Formu sitenin alt menüsünden. İlerleme Durumu: tamamlanan proje, içerik yok.
MENU = [('proje', 'Proje Hakkında'), ('daireler', 'Daire Planları'), ('galeri', 'Galeri'),
        ('tanitim-filmi', 'Tanıtım Filmi'), ('sanal-tur', 'Sanal Tur'), ('konum', 'Konum'),
        ('hesaplama', 'Konut Kredisi Hesaplama'), ('on-talep', 'İletişim Formu')]


def rail():
    items = ('<li class="b-nav__item b-nav__item--home"><a class="b-nav__home" href="index.html">'
             '<img src="%s" alt="Vakıf GYO ana sayfa" width="118" height="20"></a></li>' % LOGO)
    items += ''.join('<li class="b-nav__item"><a class="b-nav__btn" href="#%s"><span>%s</span></a></li>' % m
                     for m in MENU)
    return '''<header class="b-rail b-rail--project" data-b-rail>
<div class="b-rail__bar">
<a class="b-rail__logo b-rail__logo--project b-rail__logo--cubes" href="%s"><img src="%s" alt="Cubes Ankara ana sayfa" width="168" height="35"></a>
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
</header>''' % (PAGE, C_LOGO, ico('menu', 'b-burger__open'), ico('close', 'b-burger__close'), items,
                ico('pin'), cd.PHONE[0], ico('phone'), cd.PHONE[1],
                btn('İletişim Formu', '#on-talep', 'b-btn--yellow b-btn--block'), LOGO)


def footer():
    return '''<footer class="b-foot b-foot--project">
%s
<div class="b-wrap">
<div class="b-foot__top">
<div class="b-foot__brand">
<img src="%s" alt="Cubes Ankara" width="168" height="35" loading="lazy">
<a class="b-foot__phone" href="%s">%s</a>
<p class="b-foot__addr">Satış Ofisi</p>
</div>
<div class="b-foot__col"><p class="b-foot__head">Proje Hakkında</p><ul>
<li><a href="#proje">Proje Hakkında</a></li><li><a href="#daireler">Daire Planları</a></li>
<li><a href="#sanal-tur">Sanal Tur</a></li><li><a href="#konum">Konum</a></li></ul></div>
<div class="b-foot__col"><p class="b-foot__head">Tanıtım</p><ul>
<li><a href="#tanitim-filmi">Tanıtım Filmi</a></li>
<li><a href="%s" target="_blank" rel="noopener">Tanıtım Broşürü%s</a></li><li><a href="#on-talep">İletişim Formu</a></li></ul></div>
<div class="b-foot__col"><p class="b-foot__head">Portföy</p><ul>
<li><a href="vsancaktepe-merkez.html">VSancaktepe Merkez</a></li><li><a href="#">VYeniKonak</a></li><li><a href="#">Tablo Adalar</a></li></ul></div>
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
</footer>''' % (b.swoosh(), C_LOGO, cd.PHONE[0], cd.PHONE[1], cd.BROCHURE, NEW_TAB, LOGO)


def hero():
    _k, l1, l2, lede = cd.HERO[0]
    return '''<section class="b-hero b-hero--single" aria-label="Cubes Ankara">
<div class="b-hero__slides">
<article class="b-slide is-active">
%s
<div class="b-slide__text">
<p class="b-slide__kicker">Ankara · Çukurambar</p>
<h1 class="b-slide__title">%s<br>%s</h1>
<p class="b-slide__lede">%s</p>
<div class="b-actions">%s%s</div>
</div>
</article>
</div>
</section>''' % (b.picture('cubes', 'Cubes Ankara rezidans ve ofis kulelerinin akşam görünümü',
                           'b-slide__media', lazy=False, pos='50% 45%', ppos='36% 50%', fetch='high'),
                 l1, l2, lede,
                 btn('Sanal Tur' + NEW_TAB, cd.TOUR, 'b-btn--yellow', ' target="_blank" rel="noopener"'),
                 btn('Daire Planları', '#daireler', 'b-btn--ghost-light'))


def about():
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in cd.FACTS)
    return '''<section class="b-section" id="proje" aria-labelledby="proje-baslik">
<div class="b-wrap b-about">
<div class="b-about__text">
<h2 class="b-h2" id="proje-baslik">Proje Hakkında</h2>
<p class="b-lede">%s</p>
<dl class="b-facts">%s</dl>
</div>
<figure class="b-about__media">
<img src="%scubes-bloklar-1600x800.jpg" alt="A Blok Rezidans ve B Blok Ofis kuleleri; Sky Cubes, kat bahçeleri ve sosyal alanların yerleri işaretli" width="1600" height="800" loading="lazy">
<figcaption>A Blok Rezidans · B Blok Ofis</figcaption>
</figure>
</div>
</section>''' % (cd.ABOUT, facts, GYO)


def plan_pane(p, first):
    rows = ''.join('<tr><th scope="row">%s</th><td>%s m²</td></tr>' % r for r in p['rooms'])
    totals = ''
    if p['net']:
        totals = ('<dl class="b-plan__totals"><div><dt>Net Alan</dt><dd>%s m²</dd></div>'
                  '<div><dt>Toplam Brüt Alan</dt><dd>%s m²</dd></div></dl>' % (p['net'], p['gross']))
    zoom = '<button type="button" class="b-plan__zoom" data-b-zoom>%s<span>Büyüt</span></button>' % ico('search')
    w, h = 1200, cd.plan_img_height('cubes-plan-%s-1200.jpg' % p['key'])
    return '''<div class="b-plan" id="plan-%s" role="tabpanel" aria-labelledby="plan-%s-tab"%s>
<figure class="b-plan__img"><div class="b-plan__frame" style="--ar:%.4f" data-w="1200"><img src="%scubes-plan-%s-1200.jpg" alt="%s %s %s daire planı" width="%d" height="%d" loading="lazy" decoding="async"></div>%s</figure>
<div class="b-plan__info">
<p class="b-plan__name">%s <span>%s · %s</span></p>
%s
<div class="b-plan__rooms"><table><caption class="sr-only">%s %s</caption><tbody>%s</tbody></table></div>
%s
</div>
</div>''' % (p['key'], p['key'], '' if first else ' hidden', w / h, GYO, p['key'], p['name'], p['group'], p['typ'],
             w, h, zoom, p['group'], p['name'], p['typ'], totals, p['name'], p['typ'], rows,
             link('İletişim Formu', '#on-talep'))


def plans():
    allp = cd.plans()
    groups = cd.groups()
    tabs = ''.join('<button type="button" class="b-tab%s" role="tab" id="grup-%d-tab" aria-controls="grup-%d" '
                   'aria-selected="%s" data-b-switch="grup-%d"%s>%s</button>'
                   % (' is-active' if i == 0 else '', i, i, 'true' if i == 0 else 'false', i,
                      '' if i == 0 else ' tabindex="-1"', g) for i, g in enumerate(groups))
    panes = ''
    for i, g in enumerate(groups):
        ps = [p for p in allp if p['group'] == g]
        sub = ''.join('<button type="button" class="b-tab b-tab--sub%s" role="tab" id="plan-%s-tab" aria-controls="plan-%s" '
                      'aria-selected="%s" data-b-switch="plan-%s"%s>%s <span>%s</span></button>'
                      % (' is-active' if j == 0 else '', p['key'], p['key'], 'true' if j == 0 else 'false', p['key'],
                         '' if j == 0 else ' tabindex="-1"', p['name'], p['typ']) for j, p in enumerate(ps))
        panes += '''<div class="b-plangroup" id="grup-%d" role="tabpanel" aria-labelledby="grup-%d-tab"%s data-b-switcher>
<div class="b-tabs b-tabs--sub b-tabs--scroll" role="tablist" aria-label="%s daire tipleri">%s</div>
%s
</div>''' % (i, i, '' if i == 0 else ' hidden', g, sub, ''.join(plan_pane(p, j == 0) for j, p in enumerate(ps)))
    return '''<section class="b-section b-stone" id="daireler" aria-labelledby="daire-baslik">
<div class="b-wrap" data-b-switcher>
%s
<div class="b-tabs b-tabs--scroll" role="tablist" aria-label="Daire tipi">%s</div>
%s
</div>
</section>''' % (section_head('Daire Planları', 'daire-baslik'), tabs, panes)


def features():
    items = ''.join('<li><h3 class="b-h3">%s</h3><p>%s</p></li>' % blk for blk in cd.BLOCKS)
    return '''<section class="b-section b-dark b-dark--cubes" id="yeni" aria-labelledby="yeni-baslik">
<div class="b-wrap">
<h2 class="sr-only" id="yeni-baslik">Cubes Ankara’da</h2>
<ul class="b-feats b-feats--text">%s</ul>
</div>
</section>''' % items


def gallery():
    figs = ''.join('<li class="b-gallery__item"><img src="%scubes-galeri-%d-1200x800.jpg" alt="%s" width="1200" height="800" loading="lazy" decoding="async"></li>'
                   % (GYO, i, alt) for i, (_k, alt) in enumerate(cd.GALLERY, 1))
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
</section>''' % (section_head('Galeri', 'galeri-baslik', more=link('Sanal Tur', '#sanal-tur')), figs,
                 ico('left'), ico('right'))


def campaign():
    k, title, text, more = cd.CAMPAIGN
    return '''<section class="b-split b-split--flip b-dark b-dark--cubes" id="kampanya" aria-labelledby="kampanya-baslik">
<picture class="b-split__media"><img src="%scubes-kampanya-1078x944.jpg" alt="Ofis bloğunun cadde cephesi" width="1078" height="944" loading="lazy"></picture>
<div class="b-split__body">
<p class="b-split__kicker">%s</p>
<h2 class="b-h2" id="kampanya-baslik">%s</h2>
<p class="b-lede">%s</p>
<p class="b-lede">%s</p>
<div class="b-actions">%s%s</div>
</div>
</section>''' % (GYO, k, title, text, more, btn('Bize Ulaşın', '#on-talep', 'b-btn--yellow'),
                 btn('Satış Ofisi', cd.PHONE[0], 'b-btn--ghost-light'))


def film():
    return '''<section class="b-section" id="tanitim-filmi" aria-labelledby="film-baslik">
<div class="b-wrap">
%s
<figure class="b-video b-video--wide">
<video controls preload="none" playsinline poster="%scubes-film-1280x720.jpg" width="1280" height="720">
<source src="%s" type="video/mp4">
</video>
</figure>
</div>
</section>''' % (section_head('Tanıtım Filmi', 'film-baslik',
                              more=link('Tanıtım Broşürü' + NEW_TAB, cd.BROCHURE, 'b-link', ' target="_blank" rel="noopener"')),
                 GYO, cd.FILM)


def tour():
    return '''<section class="b-band b-band--short b-band--tour" id="sanal-tur" aria-labelledby="tur-baslik">
<picture class="b-band__media">
<source media="(max-width: 767px)" srcset="%scubes-sanal-tur-686x926.jpg">
<img src="%scubes-sanal-tur-2220x926.jpg" alt="Sanal turdan örnek dairenin salonu" width="2220" height="926" loading="lazy" decoding="async">
</picture>
<div class="b-band__text b-wrap">
<h2 class="b-band__title" id="tur-baslik">%s</h2>
<p class="b-band__lede">%s</p>
<div class="b-actions">%s</div>
</div>
</section>''' % (GYO, GYO, cd.SAMPLE[0], cd.SAMPLE[1],
                 btn('Sanal Tur' + NEW_TAB, cd.TOUR, 'b-btn--yellow', ' target="_blank" rel="noopener"'))


def location():
    bbox = '%.4f,%.4f,%.4f,%.4f' % (cd.LON - 0.02, cd.LAT - 0.011, cd.LON + 0.02, cd.LAT + 0.011)
    return '''<section class="b-section b-stone" id="konum" aria-labelledby="konum-baslik">
<div class="b-wrap b-location">
<div>
%s
</div>
<div class="b-map"><iframe title="Konum" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=%s&amp;layer=mapnik&amp;marker=%s,%s"></iframe></div>
</div>
</section>''' % (section_head('Konum', 'konum-baslik', cd.KONUM), bbox, cd.LAT, cd.LON)


def form():
    opts = ''.join('<option>%s</option>' % g for g in cd.groups())
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
<p>%s</p>
<ul>
<li>%s<a href="%s">%s</a></li>
</ul>
</div>
</div>
</section>''' % (section_head('İletişim Formu', 'talep-baslik'), opts, cd.SAMPLE[1], ico('phone'), cd.PHONE[0], cd.PHONE[1])


DOCK = '''<nav class="b-dock" aria-label="Hızlı iletişim">
<a href="%s">%s<span>%s</span></a>
<a href="#on-talep" class="b-dock__main">İletişim Formu</a>
</nav>''' % (cd.PHONE[0], ico('phone'), cd.PHONE[1])


def page():
    body = '\n'.join([hero(), about(), plans(), features(), gallery(), campaign(), film(), tour(), location(),
                      b.vs_calc(), form(), b.vs_guarantee(), DOCK])
    return b.page('Cubes Ankara',
                  'Proje Hakkında · Daire Planları · Tanıtım Filmi · Sanal Tur · Konum · İletişim Formu',
                  body, shell=(rail(), footer()), body_cls='b--project b--cubes')


if __name__ == '__main__':
    b.main()
