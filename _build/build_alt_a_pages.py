# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif A iç sayfaları

  yatirimci-iliskileri.html  Yatırımcı İlişkileri ana sayfası (T06)
  vsancaktepe-merkez.html    VSancaktepe Merkez proje sitesi ana sayfası (P01)
  hakkimizda.html            Statik içerik sayfası (T03)

Kabuk, header/footer ve ana sayfa blokları build_alt_a.py'den gelir. Blok
sırası ve VakıfBank komponent karşılıkları _docs/VakifGYO_OnerilenSiteHaritasi
tablolarıyla aynıdır.

İçerik kaynağı: vakifgyo.com.tr taraması (9 Ekim 2026) — Hakkımızda metni,
Yönetim Politikası (4.png infografiği HTML'e taşındı), VSancaktepe proje
metni ve daire planı ölçüleri, KAP açıklama / genel kurul / rapor başlıkları.
TEMSİLÎ olanlar sayfada ve bu dosyada işaretlidir: hisse fiyatı ve grafik,
özet finansal göstergeler, finansal takvim tarihleri, ulaşım süreleri
(metro dışında), satış ofisi çalışma saatleri.

Çalıştırma:  python _build/build_alt_a_pages.py   (önce build_alt_a.py)
"""
import os
import random
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_alt_a as b  # noqa: E402

IMG = b.IMG
NEW_TAB = b.NEW_TAB
ICON_EXT = b.ICON_EXT


# ---------------------------------------------------------------------------
# Ortak parçalar
# ---------------------------------------------------------------------------

def arrow(text, href='#', outline=True, extra=''):
    return ('<a class="arrow-link%s" href="%s"%s><span class="svg svg--arrow-right" aria-hidden="true">'
            '</span><span>%s</span></a>' % (' outline' if outline else '', href, extra, text))


def breadcrumb(trail):
    lis = ''.join('<li><a href="%s">%s</a></li>' % (h, t) for t, h in trail[:-1])
    lis += '<li aria-current="page"><span>%s</span></li>' % trail[-1][0]
    return '<nav class="breadcrumb" aria-label="Sayfa konumu"><ul>%s</ul></nav>' % lis


def subpage_banner(trail, title, lede='', btns=None):
    """Kurumsal sarı sayfa bandı (.subpage-banner): ekmek kırıntısı + h1.
    btns: [(etiket, bağlantı)] — kurumsal .subpage-banner.with-button: başlığın
    yanında buton grubu (ilki dolu, diğerleri çerçeveli)."""
    lede = '<p class="gyo-subpage-lede">%s</p>' % lede if lede else ''
    if not btns:
        return '''<section class="subpage-banner">
<div class="container">
%s
<div class="subpage-banner-title"><h1 class="searchTitle">%s</h1></div>
%s
</div>
</section>''' % (breadcrumb(trail), title, lede)
    bs = ''.join('<a href="%s" class="btn %s">%s</a>'
                 % (h, 'btn-primary' if i == 0 else 'btn-outline-primary', t)
                 for i, (t, h) in enumerate(btns))
    return '''<section class="subpage-banner with-button">
<div class="container">
%s
<div class="d-flex justify-content-between align-items-center title-and-btns">
<div class="subpage-banner-title"><h1 class="searchTitle">%s</h1>%s</div>
<div class="btns d-flex">%s</div>
</div>
</div>
</section>''' % (breadcrumb(trail), title, lede, bs)


def head(title, hid, link=''):
    return ('<div class="gyo-head"><h2 class="gyo-section-title" id="%s">%s</h2>%s</div>'
            % (hid, title, link))


def doclist(items, cls=''):
    """Doküman / açıklama listesi: tarih, başlık, dosya türü."""
    lis = ''.join(
        '<li><a href="%s"%s>%s<span class="gyo-doclist__title">%s</span>'
        '<span class="gyo-doclist__type">%s</span></a></li>'
        % (h, ' target="_blank" rel="noopener"' if h.startswith('http') else '',
           ('<time datetime="%s">%s</time>' % (iso, date)) if iso else '<span class="gyo-doclist__nodate"></span>',
           title, kind)
        for iso, date, title, kind, h in items)
    return '<ul class="gyo-doclist%s">%s</ul>' % (cls, lis)


def tr_date(iso):
    if not iso:
        return ''
    y, mo, d = iso.split('-')
    return '%s.%s.%s' % (d, mo, y)


# ---------------------------------------------------------------------------
# 1. YATIRIMCI İLİŞKİLERİ ANA SAYFASI (T06)
# ---------------------------------------------------------------------------

IR_TRAIL = [('Ana Sayfa', 'index.html'), ('Yatırımcı İlişkileri', '#')]

# Hızlı erişim — kurumsal .megamenu__links ikon dairesi ritmi
IR_QUICK = [
    ('svg--file', 'Faaliyet Raporları', '#'),
    ('svg--table', 'Yatırımcı Sunumları', '#'),
    ('svg--download', 'Finansal Tablolar', '#'),
    ('svg--guvenlik-duyurulari', 'Özel Durum Açıklamaları', '#aciklamalar'),
    ('svg--individual-two', 'Genel Kurul', '#genel-kurul'),
    ('svg--share', 'KAP Şirket Sayfası',
     'https://www.kap.org.tr/tr/sirket-bilgileri/genel/1116-vakif-gayrimenkul-yatirim-ortakligi-a-s'),
]


def ir_quick():
    items = ''
    for icon, label, h in IR_QUICK:
        ext = h.startswith('http')
        items += ('<li><a class="gyo-quick__item" href="%s"%s><span class="gyo-quick__icon">'
                  '<span class="svg %s" aria-hidden="true"></span></span><span>%s%s</span></a></li>'
                  % (h, ' target="_blank" rel="noopener"' if ext else '', icon, label,
                     (ICON_EXT + NEW_TAB) if ext else ''))
    return '''<section class="gyo-quick" aria-label="Hızlı erişim">
<div class="container"><ul class="gyo-quick__list">%s</ul></div>
</section>''' % items


# --- Hisse grafiği (TEMSİLÎ) ---------------------------------------------------
# Haftalık kapanış, 52 hafta. Tohumlu rastgele yürüyüş, son değer ana sayfadaki
# VKGYO fiyatına (3,27) oturtuluyor.

MONTHS = ['Eki', 'Kas', 'Ara', 'Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl']
MONTHS_LONG = ['Ekim 2025', 'Kasım 2025', 'Aralık 2025', 'Ocak 2026', 'Şubat 2026', 'Mart 2026',
               'Nisan 2026', 'Mayıs 2026', 'Haziran 2026', 'Temmuz 2026', 'Ağustos 2026', 'Eylül 2026']


def stock_series():
    rnd = random.Random(1996)
    v, out = 2.40, []
    for _ in range(52):
        v = max(1.8, v * (1 + rnd.gauss(0.006, 0.035)))
        out.append(v)
    k = 3.27 / out[-1]
    return [round(x * k, 2) for x in out]


SERIES = stock_series()


def tl(v, d=2):
    s = '{:,.{d}f}'.format(v, d=d)
    return s.replace(',', 'X').replace('.', ',').replace('X', '.')


def stock_chart():
    """Tek seri çizgi grafik: 2px çizgi, soluk ızgara, tek eksen. Hover katmanı
    gyo.js'te (artı imleci + değer kutusu); tablo görünümü <details> içinde."""
    W, H, L, R, T, B = 640, 260, 48, 12, 16, 32
    lo, hi = 1.5, 3.5
    pw, ph = W - L - R, H - T - B

    def x(i):
        return L + pw * i / (len(SERIES) - 1)

    def y(v):
        return T + ph * (1 - (v - lo) / (hi - lo))

    grid = ''
    for g in (1.5, 2.0, 2.5, 3.0, 3.5):
        grid += ('<line x1="%d" x2="%d" y1="%.1f" y2="%.1f" class="gyo-chart__grid"/>'
                 '<text x="%d" y="%.1f" class="gyo-chart__ylab">%s</text>'
                 % (L, W - R, y(g), y(g), L - 8, y(g) + 4, tl(g)))
    xl = ''
    for m in range(12):
        i = round(m * 52 / 12)
        xl += '<text x="%.1f" y="%d" class="gyo-chart__xlab">%s</text>' % (x(i), H - 10, MONTHS[m])
    pts = ' '.join('%.1f,%.1f' % (x(i), y(v)) for i, v in enumerate(SERIES))
    area = 'M%.1f,%.1f L%s L%.1f,%.1f Z' % (x(0), y(lo), pts.replace(' ', ' L'), x(len(SERIES) - 1), y(lo))
    rows = ''.join('<tr><th scope="row">%s</th><td>%s ₺</td></tr>'
                   % (MONTHS_LONG[m], tl(SERIES[min(51, round((m + 1) * 52 / 12) - 1)]))
                   for m in range(12))
    data = ','.join('%.2f' % v for v in SERIES)
    return '''<figure class="gyo-chart" data-gyo-chart data-series="%s" data-start="2025-10-03" data-lo="%s" data-hi="%s"
 data-box="%d,%d,%d,%d,%d,%d">
<figcaption class="gyo-chart__cap">VKGYO · son 52 hafta, haftalık kapanış (₺)</figcaption>
<div class="gyo-chart__plot">
<svg viewBox="0 0 %d %d" role="img" aria-label="VKGYO hisse fiyatı son 52 haftada %s ₺ ile %s ₺ arasında, son kapanış %s ₺" focusable="false">
%s%s
<path d="%s" class="gyo-chart__area"/>
<polyline points="%s" class="gyo-chart__line"/>
<line class="gyo-chart__cross" x1="0" x2="0" y1="%d" y2="%d"/>
<circle class="gyo-chart__dot" r="5" cx="%.1f" cy="%.1f"/>
</svg>
<div class="gyo-chart__tip" role="status" aria-live="polite" hidden></div>
</div>
<details class="gyo-chart__table">
<summary>Tablo olarak göster</summary>
<table><caption class="sr-only">VKGYO aylık kapanış</caption>
<thead><tr><th scope="col">Ay</th><th scope="col">Kapanış</th></tr></thead><tbody>%s</tbody></table>
</details>
</figure>''' % (data, lo, hi, W, H, L, R, T, B, W, H, tl(min(SERIES)), tl(max(SERIES)), tl(SERIES[-1]),
                grid, xl, area, pts, T, H - B, x(51), y(SERIES[-1]), rows)


def stock_pane():
    shares = 4_400_000_000          # çıkarılmış sermaye 4,4 milyar ₺ (1 ₺ nominal)
    stats = [
        ('Son Fiyat', '%s ₺' % tl(SERIES[-1])),
        ('Günlük Değişim', '<span class="gyo-up">▲ %1,24</span>'),
        ('İşlem Hacmi', '186,4 milyon ₺'),
        ('Piyasa Değeri', '%s milyar ₺' % tl(SERIES[-1] * shares / 1e9)),
        ('52 Hafta En Düşük', '%s ₺' % tl(min(SERIES))),
        ('52 Hafta En Yüksek', '%s ₺' % tl(max(SERIES))),
    ]
    dl = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % s for s in stats)
    return '''<div class="tab-pane market-info active" id="hisse" role="tabpanel" aria-labelledby="hisse-tab">
<div class="gyo-stock">
<div class="gyo-stock__stats">
<p class="gyo-stock__code">VKGYO <span>Borsa İstanbul</span></p>
<dl>%s</dl>
</div>
%s
</div>
<div class="market-info__bottom gyo-market-bottom">
<div class="consultion-block"><div class="button-block">
<a href="#" class="btn btn-outline-secondary btn-icon"><img src="../assets/img/vb/report32.svg" alt="" width="32" height="32">Sermaye Artırımı &amp; Temettü Duyuruları</a>
</div></div>
</div>
</div>''' % (dl, stock_chart())


# Özet finansal göstergeler — TEMSİLÎ (30.06.2026 dönemi için yer tutucu)
KPIS = [
    ('Toplam Aktifler', '28,6', 'milyar ₺'),
    ('Portföy Değeri', '25,9', 'milyar ₺'),
    ('Net Aktif Değer', '22,4', 'milyar ₺'),
    ('Net Dönem Kârı', '1,72', 'milyar ₺'),
    ('Kira Gelirleri', '214', 'milyon ₺'),
]


def kpi_pane():
    tiles = ''.join('<li class="gyo-kpi"><span class="gyo-kpi__label">%s</span>'
                    '<span class="gyo-kpi__value">%s <small>%s</small></span></li>' % k for k in KPIS)
    return '''<div class="tab-pane market-info" id="ozet" role="tabpanel" aria-labelledby="ozet-tab">
<p class="gyo-kpis__period">30 Haziran 2026 itibarıyla · konsolide olmayan</p>
<ul class="gyo-kpis">%s</ul>
<div class="market-info__bottom gyo-market-bottom">
<div class="consultion-block"><div class="button-block">
<a href="#" class="btn btn-outline-secondary btn-icon"><img src="../assets/img/vb/report32.svg" alt="" width="32" height="32">Özet Finansallar (Excel)</a>
</div></div>
</div>
</div>''' % tiles


def ir_tabs():
    # Özet Veriler (uydurma finansallar) ve Finansal Takvim sekmeleri çıkarıldı
    tabs = [('hisse', 'VKGYO', True)]
    lis = ''.join(
        '<li class="nav-item" role="presentation"><a class="nav-link%s" id="%s-tab" data-toggle="tab" '
        'href="#%s" role="tab" aria-controls="%s" aria-selected="%s">%s</a></li>'
        % (' active' if a else '', i, i, i, 'true' if a else 'false', t) for i, t, a in tabs)
    return '''<section class="home-tabs gyo-ir-tabs" aria-labelledby="hisse-baslik">
<div class="container">
<h2 id="hisse-baslik" class="sr-only">VKGYO</h2>
<ul class="nav nav-tabs" role="tablist">%s</ul>
<div class="tab-content">%s</div>
</div>
</section>''' % (lis, stock_pane())


# 4. Son finansal sonuçlar — kurumsal .retirement (başlıklar KAP'tan, gerçek)
RESULTS = '''<section class="retirement gyo-ir-results" aria-labelledby="sonuclar-baslik">
<div class="container">
<div class="row">
<div class="col-md-6">
<picture>
<source media="(min-width: 992px)" srcset="%sir-sonuclar-1078x944.jpg">
<source media="(max-width: 991px)" srcset="%sir-sonuclar-764x776.jpg">
<img src="%sir-sonuclar-1078x944.jpg" alt="" width="539" height="472" loading="lazy">
</picture>
</div>
<div class="col-md-6">
<div class="retirement__option">
<p class="gyo-eyebrow">Son Finansal Sonuçlar</p>
<h2 id="sonuclar-baslik" class="searchContent">30 Haziran 2026 Dönemi</h2>
<a href="#" class="retirement__option__link">
<p>Yönetim Kurulu Faaliyet Raporu</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">PDF · 31.07.2026</span></div>
</a>
<a href="#" class="retirement__option__link">
<p>Yatırımcı Sunumu</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">PDF · 20.08.2026</span></div>
</a>
<a href="#" class="retirement__option__link">
<p>Finansal Tablolar ve Dipnotlar</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">PDF · 30.07.2026</span></div>
</a>
<div class="gyo-retirement-more">%s</div>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG, arrow('Tüm Finansal Sonuçlar'))

# Özel durum açıklamaları — vakifgyo.com.tr/#!ozel-durum-aciklamalari 2026 listesi,
# Türkçe kayıtlar sitedeki sırayla (_docs/kaynak/ozel-durum-aciklamalari-2026.txt).
# Sitede tarih alanı boş; tarih PDF dosya adından. Derecelendirme kaydının dosya
# adında tarih yok, tarih uydurulmadı (boş).
DISCLOSURES = [
    ('2026-10-14', 'Şirket Genel Bilgi Formu'),
    ('2026-10-13', 'Şirket Genel Bilgi Formu'),
    ('2026-10-13', 'Şirketimiz Adres Değişikliği ve Tescili Hakkında'),
    ('', 'Kurumsal Yönetim İlkelerine Uyum Derecelendirmesi'),
    ('2026-09-04', 'Şirketimiz Maddi Duran Varlık Alımı'),
    ('2026-08-03', 'Yönetim Kurulu Komiteleri Güncelleme'),
    ('2026-08-03', 'Yönetim Kurulu Komitelerinin Görev Alanları ve Çalışma Esasları'),
    ('2026-08-03', 'Bağımsız Yönetim Kurulu Üyesi Atama'),
    ('2026-07-31', 'Şirket Genel Bilgi Formu'),
]

ASSEMBLY = [
    ('2026-05-12', 'Pay Sahipleri Soru ve Cevapları', 'PDF'),
    ('2026-04-29', 'Genel Kurul Kararlarının Tescili', 'PDF'),
    ('2026-04-20', 'Toplantı Sonucu, Tutanak ve Hazirun', 'PDF'),
    ('2026-03-23', 'Genel Kurul Daveti ve Bilgilendirme Dokümanı', 'PDF'),
]


def disclosures():
    # Genel kurul doküman listesi (ASSEMBLY) çıkarıldı: başlıklar kaynakta yok
    left = doclist([(d, tr_date(d), t, 'KAP', '#') for d, t in DISCLOSURES])
    return '''<section class="gyo-section" aria-label="Açıklamalar ve genel kurul">
<div class="container">
<div class="row gyo-row-gap">
<div class="col-12 col-lg-7 gyo-disclosures" id="aciklamalar">
%s
%s
</div>
<div class="col-12 col-lg-5" id="genel-kurul">
<div class="gyo-panel">
<p class="gyo-eyebrow">Genel Kurul</p>
<h2 class="gyo-panel__title" id="gk-baslik">2025 Yılı Olağan Genel Kurulumuzu gerçekleştirdik</h2>
<p>2025 Yılı Olağan Genel Kurulumuzu, 17 Nisan 2026 tarihinde gerçekleştirdik.</p>
%s
</div>
</div>
</div>
</div>
</section>''' % (head('Özel Durum Açıklamaları', 'aciklama-baslik'), left, arrow('Devamını Oku'))


# 8–9. Raporlar + Yatırımcı Çantası (ek komponent)
# Açıklama haberden birebir (_docs/kaynak/haber-tsrs.txt); faaliyet raporu için kaynakta açıklama yok
REPORTS = [
    ('ir-faaliyet-raporu-2025-372x526.jpg', '2025 Yılı Faaliyet Raporu', '', 'Devamını Oku'),
    ('ir-tsrs-2025-372x526.jpg', '2025 TSRS Uyumlu Sürdürülebilirlik Raporu', 'Türkiye Sürdürülebilirlik Raporlama Standartları (TSRS) ile uyumlu olarak hazırladığımız 2025 TSRS Uyumlu Sürdürülebilirlik Raporumuzda; sürdürülebilirlik yaklaşımımızı, çevresel, sosyal ve yönetişim alanındaki çalışmalarımızı ve performansımızı paydaşlarımızla şeffaf bir şekilde paylaşıyoruz.', 'Devamını Oku'),
]

BAG = [
    ('30 Haziran 2026 Yönetim Kurulu Faaliyet Raporu', 'PDF'),
    ('30 Haziran 2026 Yatırımcı Sunumu', 'PDF'),
    ('30 Haziran 2026 Finansal Tablolar ve Dipnotlar', 'PDF'),
    ('2025 Yılı Faaliyet Raporu', 'PDF'),
    ('2025 TSRS Uyumlu Sürdürülebilirlik Raporu', 'PDF'),
    ('Özet Finansallar', 'XLSX'),
    ('Esas Sözleşme', 'PDF'),
]


def reports():
    cards = ''.join('''<div class="gyo-report">
<img src="%s%s" alt="" width="186" height="263" loading="lazy">
<div class="gyo-report__body">
<h3 class="gyo-report__title">%s</h3>
%s
%s
</div>
</div>''' % (IMG, img, t, '<p>%s</p>' % d if d else '', arrow(cta)) for img, t, d, cta in REPORTS)
    checks = ''.join('''<li class="checkbox-block"><input type="checkbox" id="canta-%d" name="canta" value="%d"%s data-gyo-bag-item>
<label for="canta-%d">%s <span class="gyo-bag__type">%s</span></label></li>'''
                     % (i, i, ' checked' if i < 3 else '', i, t, k) for i, (t, k) in enumerate(BAG))
    # Yatırımcı Çantası (BAG) çıkarıldı: bileşen ve metinleri kaynakta yok
    return '''<section class="gyo-section gyo-section--gray" id="raporlar" aria-labelledby="rapor-baslik">
<div class="container">
%s
<div class="gyo-reports">%s</div>
</div>
</section>''' % (head('Raporlar ve Yatırımcı Sunumları', 'rapor-baslik'), cards)


# 10. Kurumsal yönetim ve sürdürülebilirlik — kurumsal .sustainable-banking
IR_SUSTAIN = '''<section class="gyo-ir-sustain" aria-labelledby="ky-baslik">
<div class="container">
<div class="sustainable-banking">
<picture class="sustainable-banking__bg">
<source srcset="%ssurdurulebilirlik-750x870.jpg" media="(max-width: 767px)">
<img src="%ssurdurulebilirlik-2280x926.jpg" alt="" loading="lazy">
</picture>
<div class="sustainable-banking__content">
<h2 id="ky-baslik" class="gyo-sustain-title">Kurumsal Yönetim</h2>
<div class="searchContent"><p>Kurumsal Yönetim Derecelendirme Notumuzu 9,42’den 9,48’e çıkardık.</p></div>
<ul>
<li><a href="#" class="arrow-link"><span class="svg svg--arrow-right" aria-hidden="true"></span>Kurumsal Yönetim İlkelerine Uyum Raporları</a></li>
<li><a href="#" class="arrow-link"><span class="svg svg--arrow-right" aria-hidden="true"></span>Kar Dağıtım Politikası</a></li>
<li><a href="#" class="arrow-link"><span class="svg svg--arrow-right" aria-hidden="true"></span>Bilgilendirme Politikası</a></li>
</ul>
</div>
</div>
</div>
</section>''' % (IMG, IMG)


# 11. Hizmetler — kurumsal .mix
def mix4(icon, title, text, link):
    return '''<div class="col-12 col-md-6 col-lg-3">
<div class="mix__content">
<div class="mix__content__top">
<img src="%s" alt="" width="64" height="64">
<div class="mix__content__top__text">
<p class="heading-h5">%s</p>
<p class="searchContent">%s</p>
</div>
</div>
<div class="mix__content__links"><a class="outline" href="#"><span class="svg svg--arrow-right" aria-hidden="true"></span><span>%s</span></a></div>
</div>
</div>''' % (icon, title, text, link)


IR_SERVICES = '''<section class="mix gyo-mix4" aria-labelledby="hizmet-baslik">
<div class="container">
<h2 class="gyo-section-title" id="hizmet-baslik">Yatırımcı İlişkileri İletişim</h2>
<div class="row gyo-row-gap">%s%s%s%s</div>
</div>
</section>''' % (
    # Başlıklar Yatırımcı İlişkileri menüsünden (_docs/kaynak/portfoy-yatirimci-iliskileri.txt, menu.txt)
    mix4('../assets/img/icon/phone-24.svg', 'Yatırımcı İlişkileri İletişim', '', 'Devamını Oku'),
    mix4('../assets/img/icon/envelope-32.svg', 'Duyurular', '', 'Devamını Oku'),
    mix4('../assets/img/icon/file.svg', 'Sürekli Bilgilendirme Formu', '', 'Devamını Oku'),
    mix4('../assets/img/icon/help-22.svg', 'Sıkça Sorulan Sorular', '', 'Devamını Oku'))


def ir_page():
    body = '\n'.join([
        # Gezinme kurumsal bileşenlerle: başlık bandında buton grubu
        # (.subpage-banner.with-button), diğer alt sayfalar mega menüde.
        # Buton adları orijinal Yatırımcı İlişkileri menüsünden.
        subpage_banner(IR_TRAIL, 'Yatırımcı İlişkileri', '',
                       btns=[('Raporlar ve Yatırımcı Sunumları', '#raporlar'),
                             ('Özel Durum Açıklamaları', '#aciklamalar')]),
        # RESULTS (30 Haziran 2026 dönemi doküman listesi) çıkarıldı: başlık ve tarihler kaynakta yok
        ir_tabs(), disclosures(), reports(), IR_SERVICES, IR_SUSTAIN])
    return b.page('Yatırımcı İlişkileri — Vakıf GYO',
                  'Yatırımcı İlişkileri İletişim · Duyurular · Özel Durum Açıklamaları · Genel Kurul '
                  've raporlar.', body, b.TICKER, h1='')


# ---------------------------------------------------------------------------
# 2. VSANCAKTEPE MERKEZ PROJE SİTESİ (P01)
#    Bağımsız alan adından (vsancaktepe.com.tr) yayımlanıyormuş gibi kendi
#    header'ı, menüsü ve footer'ı var; bileşenler kurumsal. Menü bağlantıları
#    landing içindeki bölümlere gider (proje sitesinin iç sayfaları yerine).
# ---------------------------------------------------------------------------

VS_LOGO = IMG + 'vs-logo.svg'
VS_PHONE = ('tel:08502101002', '0850 210 10 02')

VS_MENU = [('Proje Hakkında', '#proje'), ('Daire Planları', '#daireler'), ('Galeri', '#galeri'),
           ('Konum', '#konum'), ('İlerleme Durumu', '#ilerleme'), ('Kampanyalar', '#kampanya'),
           ('İletişim Formu', '#on-talep')]

VS_TOP = '''
<a href="index.html" class="header__links-link gyo-byline"><img src="%s" alt="" width="70" height="12"><span class="header__links-text">Vakıf GYO güvencesiyle</span></a>
<a href="#on-talep" class="header__links-link">%s<span class="header__links-text">Satış Ofisi</span></a>
<a href="%s" class="header__links-link">%s<span class="header__links-text">%s</span></a>
''' % (b.LOGO, b.top_icon('<path d="M8 14.5s4.8-4.4 4.8-8.1A4.8 4.8 0 0 0 3.2 6.4c0 3.7 4.8 8.1 4.8 8.1z"/>'
                          '<circle cx="8" cy="6.4" r="1.7"/>'),
       VS_PHONE[0], b.ICON_PHONE, VS_PHONE[1])

VS_MOBILE_QUICK = '''
<a href="#on-talep" class="header__mobile__quick-link__item"><span class="megamenu__links-icon"><span class="svg svg--plus" aria-hidden="true"></span></span><p>Ön Talep</p></a>
<a href="#daireler" class="header__mobile__quick-link__item"><span class="megamenu__links-icon"><span class="svg svg--table" aria-hidden="true"></span></span><p>Daire Planları</p></a>
<a href="%s" class="header__mobile__quick-link__item"><span class="megamenu__links-icon"><span class="svg svg--phone" aria-hidden="true"></span></span><p>Satış Ofisi</p></a>
''' % VS_PHONE[0]


def vs_header():
    h = b.HEAD
    h = b.sub_block(h, '<div class="header__links">', VS_TOP)
    h = b.sub_block(h, '<div class="header__mobile__quick-link">', VS_MOBILE_QUICK)
    # Kurumsal arama kutusunun "popüler" bağlantıları (VakıfBank ürünleri) kalmasın
    h = b.sub_block(h, '<div class="placeholder-content open">', '')
    h = h.replace('href="/tr" aria-label="VakıfBank Anasayfa"',
                  'href="vsancaktepe-merkez.html" aria-label="VSancaktepe Merkez ana sayfa"')
    h = re.sub(r'(src|srcset)="/Templates/Default/assets/img/(?:footer-)?logo\.svg"',
               r'\1="%s"' % VS_LOGO, h)
    h = h.replace('alt="VakıfBank Logo"', 'alt="VSancaktepe Merkez"')
    h = h.replace('VakıfBank, daima seninle', 'VSancaktepe Merkez')
    h = re.sub(r'<h1 class="site__logo">.*?</h1>', '', h, flags=re.S)
    h = h.replace('<header class="header', '<header class="header gyo-project-header', 1)
    # Proje sitesinde site içi arama yok; mobil arama ikonu kaldırılıyor
    h = re.sub(r'<a href="javascript:;" class="header__menu-search"[^>]*>.*?</a>', '', h, count=1, flags=re.S)
    nav = ''.join('<div class="header__menu-item"><a class="header__menu-link" href="%s">%s</a></div>' % (h_, t)
                  for t, h_ in VS_MENU)
    nav = '<nav class="header__menu" aria-label="Proje menüsü">' + nav + '</nav>'
    tail = b.TAIL.replace(
        re.search(r'<div class="header__btns">.*?</div>', b.TAIL, re.S).group(0),
        '<div class="header__btns"><a href="#on-talep" class="btn btn-primary">Ön Talep</a></div>')
    return h + nav + tail


VS_FOOTER_TOP = '''
<ul>
<li><a href="#proje">Proje Hakkında</a></li>
<li><a href="#daireler">Daire Planları</a></li>
<li><a href="#galeri">Galeri</a></li>
<li><a href="#ilerleme">İlerleme Durumu</a></li>
</ul>
<ul>
<li><a href="#kampanya">Kampanyalar</a></li>
<li><a href="#hesaplama">Konut Kredisi Hesaplama</a></li>
<li><a href="#">Tanıtım Broşürü</a></li>
<li><a href="#on-talep">İletişim Formu</a></li>
</ul>
<ul>
<li><a href="#">Gizlilik ve Kişisel Verilerin Korunması</a></li>
</ul>
'''

VS_FOOTER_BOTTOM = '''
<ul>
<li><a href="index.html">Vakıf GYO</a></li>
<li><a href="https://vyenikonak.com.tr" target="_blank" rel="noopener">VYeniKonak%s</a></li>
<li><a href="https://tabloadalar.com.tr" target="_blank" rel="noopener">Tablo Adalar%s</a></li>
<li><a href="https://www.cubesankara.com.tr" target="_blank" rel="noopener">Cubes Ankara%s</a></li>
</ul>
''' % ((NEW_TAB,) * 3)


def vs_footer():
    f = b.footer()
    f = re.sub(r'<a href="index.html" class="footer__logo">.*?</a>',
               '<a href="vsancaktepe-merkez.html" class="footer__logo gyo-footer-vs">'
               '<img src="%s" alt="VSancaktepe Merkez" width="130" height="60"></a>' % VS_LOGO, f, flags=re.S)
    f = re.sub(r'<a href="tel:[^"]*" class="footer__phone">(.*?)<span>[^<]*</span>',
               r'<a href="%s" class="footer__phone">\1<span>%s</span>' % VS_PHONE, f, flags=re.S)
    f = b.sub_block(f, '<div class="footer__sitemap__top">', VS_FOOTER_TOP)
    f = b.sub_block(f, '<div class="footer__sitemap__bottom">', VS_FOOTER_BOTTOM)
    f = re.sub(r'<p class="footer__copyright">.*?</p>',
               '<p class="footer__copyright gyo-footer-guarantee"><a href="index.html">'
               '<img src="%s" alt="Vakıf GYO" width="115" height="20"></a>'
               'VakıfBank Finans Grubu İştirakidir.</p>' % b.LOGO, f, flags=re.S)
    f = b.sub_block(f, '<div class="footer__mobile__links">',
                    '<a href="index.html" class="footer__mobile__links-link"><span class="footer__mobile__links-text">Vakıf GYO güvencesiyle</span></a>')
    return f


VS_BANNER = [
    ('banner-vsancaktepe-3024x1040.jpg', 'banner-vsancaktepe-2400x828.jpg',
     'banner-vsancaktepe-1536x480.jpg', 'banner-vsancaktepe-828x480.jpg',
     ['VSancaktepe Merkez’de', 'Yaşam Başlıyor'], 'İletişim Formu',
     'VSancaktepe Merkez konut bloklarının gün batımında görünümü', True),
    ('vs-banner-dogallik-1512x520.jpg', 'vs-banner-dogallik-1512x520.jpg',
     'vs-banner-dogallik-1536x480.jpg', 'vs-banner-dogallik-828x480.jpg',
     ['Merkezinde', 'Doğallık Var'], 'Detaylı Bilgi',
     'Bloklar arasındaki havuz, yürüyüş yolları ve peyzaj alanının kuşbakışı görünümü', False),
    ('vs-banner-uyum-1512x520.jpg', 'vs-banner-uyum-1512x520.jpg',
     'vs-banner-uyum-1536x480.jpg', 'vs-banner-uyum-828x480.jpg',
     ['Merkezinde', 'Uyum Var'], 'Detaylı Bilgi',
     'Akşam ışığında havuza bakan balkon ve bloklar', True),
]

# Sanal tur: vsancaktepe.com.tr proje menüsündeki "Sanal Tur" bağlantısı
VS_TOUR = ('https://www.vakifgyo.com.tr/client/webs/vakifgyo/crm/projects/'
           'vsancaktepe-merkez/vtours/index.htm')

VS_APPLY = [('Daire Planları', '#daireler', 'plan'), ('Galeri', '#galeri', 'galeri'),
            ('Sanal Tur', VS_TOUR, 'tur'), ('Konum', '#konum', 'konum'),
            ('Ön Talep Formu', '#on-talep', 'form')]


# 3. Proje özeti — kurumsal .retirement yerleşimi
# DETAYLAR: vakifgyo.com.tr proje sayfası (_docs/kaynak/portfoy-portfoy-vsancaktepe-merkez.txt)
VS_FACTS = [
    ('Lokasyon', 'İstanbul İli, Sancaktepe İlçesi'),
    ('İnşaat Alanı', '58.133,42 m2'),
    ('Ada / Parsel', '6770 / 2'),
]

VS_ABOUT = '''<section class="retirement gyo-vs-about" id="proje" aria-labelledby="proje-baslik">
<div class="container">
<div class="row">
<div class="col-md-6">
<picture>
<source media="(min-width: 992px)" srcset="%svs-ozet-1078x944.jpg">
<source media="(max-width: 991px)" srcset="%svs-ozet-764x776.jpg">
<img src="%svs-ozet-1078x944.jpg" alt="VSancaktepe Merkez vaziyet planı: bloklar, iç avlu ve çevre yolları kuşbakışı" width="539" height="472" loading="lazy">
</picture>
</div>
<div class="col-md-6">
<div class="retirement__option">
<p class="gyo-eyebrow">Proje Hakkında</p>
<h2 id="proje-baslik" class="searchContent">Ve karşınızda VSancaktepe Merkez</h2>
<p class="gyo-lede">Hayalinizdeki huzurlu ve güvenli yaşam alanını Vakıf GYO güvencesiyle sunan VSancaktepe Merkez, yenilikçi mimarisi, geniş yeşil alanları ve çevre dostu özellikleriyle sizi ve sevdiklerinizi bekliyor.</p>
<dl class="gyo-facts">%s</dl>
%s
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG,
                 ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in VS_FACTS),
                 arrow('Vaziyet Planı'))


# 4. Daire tipleri + hesaplama — kurumsal .home-tabs; ölçüler mevcut siteden
PLANS = [
    ('1-1', '1+1', 'B 4 Tipi', [('Antre', '6,98'), ('Salon & Mutfak', '22,64'), ('Yatak Odası', '13,35'),
                               ('Banyo', '3,88'), ('Çamaşır Nişi', '0,63'), ('Balkon', '8,96')],
     '47,52', '64,36', '80,29'),
    ('2-1', '2+1', 'A 1 Tipi', [('Antre', '4,04'), ('Salon', '26,48'), ('Mutfak', '10,03'),
                               ('Yatak Odası', '10,68'), ('E.Yatak Odası', '17,17'), ('Banyo', '4,57'),
                               ('E.Banyo', '4,56'), ('Çamaşır Nişi', '0,70'), ('Hol', '6,73'),
                               ('Balkon', '9,63')],
     '84,96', '106,46', '130,52'),
    ('3-1', '3+1', 'C 2 Tipi', [('Antre', '12,32'), ('Salon', '31,29'), ('Mutfak', '12,57'),
                               ('Yatak Odası 1', '12,87'), ('Yatak Odası 2', '10,76'),
                               ('E.Yatak Odası', '24,47'), ('Banyo', '3,91'), ('E.Banyo', '4,03'),
                               ('Çamaşır Nişi', '0,95'), ('Hol', '4,69'), ('Balkon', '17,15')],
     '117,93', '150,44', '189,06'),
    ('4-1', '4+1', 'A Tipi', [('Antre', '12,61'), ('Salon', '37,51'), ('Oturma Odası', '21,86'),
                              ('Mutfak', '14,38'), ('Yatak Odası 1', '12,81'), ('Yatak Odası 2', '19,04'),
                              ('E.Yatak Odası', '31,17'), ('Banyo 1', '4,66'), ('Banyo 2', '4,00'),
                              ('E.Banyo', '5,58'), ('İşlik', '2,32'), ('Hol', '9,30'),
                              ('Hizmetli Odası', '7,13'), ('Merdiven', '7,28'), ('Balkon', '13,51'),
                              ('Teras', '4,30')],
     '189,65', '240,71', '324,67'),
]


def plans_pane():
    tags = ''.join(
        '<button type="button" class="tag%s" role="tab" id="plan-%s-tab" aria-controls="plan-%s" '
        'aria-selected="%s" data-gyo-switch="plan-%s"%s>%s</button>'
        % (' active' if i == 0 else '', k, k, 'true' if i == 0 else 'false', k,
           '' if i == 0 else ' tabindex="-1"', name)
        for i, (k, name, *_r) in enumerate(PLANS))
    panes = ''
    for i, (k, name, typ, rooms, net, gross, sale) in enumerate(PLANS):
        rows = ''.join('<tr><th scope="row">%s</th><td>%s m²</td></tr>' % r for r in rooms)
        panes += '''<div class="gyo-plan" id="plan-%s" role="tabpanel" aria-labelledby="plan-%s-tab"%s>
<figure class="gyo-plan__img"><img src="%svs-plan-%s-960x640.jpg" alt="%s %s daire planı" width="960" height="640" loading="lazy"></figure>
<div class="gyo-plan__info">
<p class="gyo-plan__name">%s <span>%s</span></p>
<ul class="gyo-plan__totals">
<li><span>Net Alan</span><strong>%s m²</strong></li>
<li><span>Brüt Alan</span><strong>%s m²</strong></li>
<li><span>Satışa Esas Brüt Alan</span><strong>%s m²</strong></li>
</ul>
<details class="gyo-plan__rooms"%s>
<summary>Daire Planları</summary>
<table><caption class="sr-only">%s</caption><tbody>%s</tbody></table>
</details>
%s
</div>
</div>''' % (k, k, '' if i == 0 else ' hidden', IMG, k, name, typ, name, typ, net, gross, sale,
             '', name, rows, arrow('İletişim Formu', '#on-talep'))
    return '''<div class="tab-pane active" id="daire-tipleri" role="tabpanel" aria-labelledby="daire-tipleri-tab">
<div class="gyo-plans" data-gyo-switcher>
<div class="tags gyo-plans__tags" role="tablist" aria-label="Daire tipi">%s</div>
%s
</div>
</div>''' % (tags, panes)


def vs_tabs():
    tabs = [('daire-tipleri', 'Daire Planları', True), ('hesaplama', 'Konut Kredisi Hesaplama', False)]
    lis = ''.join(
        '<li class="nav-item" role="presentation"><a class="nav-link%s" id="%s-tab" data-toggle="tab" '
        'href="#%s" role="tab" aria-controls="%s" aria-selected="%s">%s</a></li>'
        % (' active' if a else '', i, i, i, 'true' if a else 'false', t) for i, t, a in tabs)
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


# 5. Öne çıkan özellikler — ikon satırı (32px kontur, tek sarı vurgu)
def feat_icon(paths):
    return ('<svg class="gyo-feat__icon" viewBox="0 0 48 48" fill="none" stroke="#000" stroke-width="2" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">%s</svg>' % paths)


Y = ' stroke="#fdb913"'
FEATURES = [
    (feat_icon('<path d="M8 34h32l-5-14H13z"/><path d="M18 20l-2 14M30 20l2 14M10 27h28"/>'
               '<circle cx="24" cy="10" r="3.5"%s/><path d="M24 2.5v1.5M31 6l-1 1M17 6l1 1"%s/>' % (Y, Y)),
     'Güneş Panelleri', 'Ortak alanların enerjisi çatıdaki panellerden.'),
    (feat_icon('<path d="M24 6c6 8 10 13 10 18a10 10 0 0 1-20 0c0-5 4-10 10-18z"/>'
               '<path d="M19 26a5 5 0 0 0 5 5"%s/><path d="M8 42h32"/>' % Y),
     'Yağmur Suyu Toplama', 'Toplanan yağmur suyu peyzaj sulamasında kullanılır.'),
    (feat_icon('<rect x="10" y="8" width="18" height="32" rx="3"/><path d="M10 18h18"/>'
               '<path d="M20 22l-4 6h6l-4 6"%s/><path d="M28 16h4a4 4 0 0 1 4 4v12a3 3 0 0 0 6 0V18l-3-4"/>' % Y),
     'Elektrikli Araç Şarjı', 'Otoparkta elektrikli araç şarj istasyonları.'),
    (feat_icon('<path d="M6 30c3 0 3 2 6 2s3-2 6-2 3 2 6 2 3-2 6-2 3 2 6 2 3-2 6-2"%s/>'
               '<path d="M6 38c3 0 3 2 6 2s3-2 6-2 3 2 6 2 3-2 6-2 3 2 6 2 3-2 6-2"/>'
               '<path d="M16 26V10a4 4 0 0 1 8 0M30 26V10a4 4 0 0 1 8 0M16 16h14M16 22h14"/>' % Y),
     'Yüzme Havuzu', 'Bloklar arasındaki avluda açık yüzme havuzu.'),
    (feat_icon('<path d="M24 42V22"/><path d="M24 22c-8 0-13-5-13-13 8 0 13 5 13 13z"%s/>'
               '<path d="M24 28c6 0 10-4 10-10-6 0-10 4-10 10z"/><path d="M12 42h24"/>' % Y),
     'Yeşil Bina', 'Enerji verimliliği ve sürdürülebilir malzeme.'),
    (feat_icon('<circle cx="17" cy="10" r="4"/><path d="M17 14v12l-6 14M17 26l6 14M10 20h14"/>'
               '<path d="M32 40V22l8-8"%s/><path d="M30 40h12"/>' % Y),
     'Çocuk Oyun Alanları', 'Güvenli, yeşille çevrili oyun alanları.'),
]


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
]


def features():
    # FEATURES (ikonlu altı madde) kaynakta yok; sitedeki metin blokları kullanılır
    items = ''.join('<li class="gyo-feat gyo-feat--text"><p class="gyo-feat__title">%s</p><p class="gyo-feat__text">%s</p></li>'
                    % f for f in VS_BLOCKS)
    return '''<section class="gyo-section gyo-section--gray" aria-labelledby="ozellik-baslik">
<div class="container">
<h2 class="gyo-section-title" id="ozellik-baslik">Merkezinde Doğallık Var</h2>
<p class="gyo-section-lede">Enerji verimliliği, yeşil bina standartları ve sürdürülebilir malzemelerin kullanıldığı VSancaktepe Merkez, çevre dostu bir yaşam alanı olarak öne çıkıyor. Elektrikli araç istasyonları ve güneş panelleri ile donatılmış olan bu özel alan, yağmur suyunu toplama sistemi ile doğal kaynakları koruma çabasını bir adım öteye taşıyor.</p>
<ul class="gyo-feats gyo-feats--text">%s</ul>
</div>
</section>''' % items


# 6. Sosyal olanaklar — kurumsal .insurance kart carousel'i (gyo-rail)
AMENITIES = [
    ('havuz', 'Yüzme Havuzu', 'Avlunun ortasında, bloklara yürüme mesafesinde açık havuz.'),
    ('yuruyus', 'Bahçe ve Yürüyüş Yolları', 'Bloklar arasında kıvrılan yürüyüş yolları ve bahçeler.'),
    ('avlu', 'Geniş Avlular', 'Komşularla vakit geçirmek için peyzajlı ortak avlular.'),
    ('peyzaj', 'Peyzaj Alanları', 'Yeşilin her tonunu bulabileceğiniz bahçeler.'),
    ('ticari', 'Ticari Alanlar', 'Cadde boyunca günlük ihtiyaçlar için mağazalar.'),
]


def amenities():
    cards = ''.join('''<div class="col-md-4 swiper-slide">
<div class="insurance__item gyo-project gyo-project--static">
<span class="gyo-project__media"><img src="%svs-olanak-%s-710x410.jpg" alt="" width="355" height="205" class="img-fluid" loading="lazy"></span>
<h3 class="landing-heading-h5">%s</h3>
<p class="gyo-project__desc">%s</p>
</div>
</div>''' % (IMG, k, t, d) for k, t, d in AMENITIES)
    return '''<section class="insurance" aria-labelledby="olanak-baslik">
<div class="container">
<h2 id="olanak-baslik" class="gyo-section-title">Merkezinde Yaşam Var</h2>
<div class="insurance-swiper gyo-rail" data-gyo-rail>
<div class="swiper-wrapper row" tabindex="0" aria-label="Sosyal olanaklar, yatay kaydırılabilir">%s</div>
</div>
<div class="gyo-rail__foot">
<div class="gyo-rail__nav">
<button type="button" class="gyo-rail__btn" data-gyo-prev aria-label="Önceki olanaklar"><span class="svg svg--chevron-left" aria-hidden="true"></span></button>
<button type="button" class="gyo-rail__btn" data-gyo-next aria-label="Sonraki olanaklar"><span class="svg svg--chevron-left gyo-flip" aria-hidden="true"></span></button>
</div>
%s
</div>
</div>
</section>''' % (cards, arrow('Sosyal Olanaklar'))


# 7. Galeri
GALLERY = [
    'Bloklar ve cadde boyunca ticari alanlar, gündüz görünümü',
    'Akşam ışığında havuza bakan balkon',
    'Geniş pencereli salon ve oturma alanı',
    'Ada tezgâhlı açık mutfak',
    'Ebeveyn yatak odası',
    'Cadde cephesi ve bloklar',
]


def gallery():
    figs = ''.join('<li class="gyo-gallery__item"><img src="%svs-galeri-%d-960x640.jpg" alt="%s" width="960" '
                   'height="640" loading="lazy"></li>' % (IMG, i, a) for i, a in enumerate(GALLERY, 1))
    return '''<section class="gyo-section" id="galeri" aria-labelledby="galeri-baslik">
<div class="container">
%s
<ul class="gyo-gallery">%s</ul>
</div>
</section>''' % (head('Galeri', 'galeri-baslik'), figs)


# 7b. Sanal tur — kurumsal .private-banking (görsel üstünde metin + bağlantı).
# Görsel turun kendi "Salon" panoramasından (_build/make_vs_tour.py); oda adları
# turdaki etiketlerden, dosya adı a1-konut-2-1+ (2+1 daire).
TOUR = '''<section class="private-banking gyo-tour" id="sanal-tur" aria-labelledby="tur-baslik">
<div class="container">
<div class="private-banking__content">
<picture>
<source media="(min-width: 768px)" srcset="%svs-sanal-tur-1110x463.jpg 1x, %svs-sanal-tur-2220x926.jpg 2x">
<source media="(max-width: 767px)" srcset="%svs-sanal-tur-343x463.jpg 1x, %svs-sanal-tur-686x926.jpg 2x">
<img src="%svs-sanal-tur-1110x463.jpg" alt="Sanal turdan 2+1 dairenin salonu" loading="lazy">
</picture>
<div class="private-banking__content__top">
<h2 id="tur-baslik" class="searchContent">Sanal Tur</h2>
<div class="private-banking__content__top__bottom-text">
<a href="%s" class="btn btn-primary gyo-tour__btn" target="_blank" rel="noopener">Sanal Tur%s</a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG, IMG, IMG, VS_TOUR, NEW_TAB)


# 8. Kampanya bandı — kurumsal .retirement (görsel sağda)
CAMPAIGN = '''<section class="retirement gyo-retirement--flip" id="kampanya" aria-labelledby="kampanya-baslik">
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
<p class="gyo-eyebrow">Kampanya</p>
<h2 id="kampanya-baslik" class="searchContent">Teslime özel avantajlar</h2>
<p class="gyo-lede">Anadolu Yakası’nın değerli yaşam merkezi VSancaktepe Merkez’de teslime özel avantajlardan yararlanma fırsatını kaçırmayın.</p>
<a href="#on-talep" class="retirement__option__link">
<p>Detaylı bilgi almak ve örnek dairemizi ziyaret etmek için bize ulaşın.</p>
<div class="retirement__option__link__bottom outline" aria-hidden="true"><span class="svg svg--arrow-right"></span><span class="searchContent">Bize Ulaşın</span></div>
</a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG)


# 9. İlerleme durumu — ay listesi mevcut siteden
PROGRESS = ['Mayıs 2026', 'Nisan 2026', 'Mart 2026', 'Ocak 2026', 'Aralık 2025', 'Kasım 2025',
            'Ekim 2025', 'Eylül 2025', 'Ağustos 2025', 'Temmuz 2025', 'Haziran 2025', 'Mayıs 2025',
            'Şubat 2025', 'Aralık 2024', 'Kasım 2024']


def progress():
    months = ''.join('<li><a href="#"%s><span class="svg svg--play" aria-hidden="true"></span>%s</a></li>'
                     % (' aria-current="true"' if i == 0 else '', m) for i, m in enumerate(PROGRESS))
    return '''<section class="gyo-section gyo-section--gray" id="ilerleme" aria-labelledby="ilerleme-baslik">
<div class="container">
<h2 class="gyo-section-title" id="ilerleme-baslik">İlerleme Durumu</h2>
<div class="row gyo-row-gap gyo-progress">
<div class="col-12 col-lg-8">
<figure class="gyo-video">
<video controls preload="none" playsinline poster="%svs-ilerleme-mayis-2026-1280x720.jpg" width="1280" height="720" aria-label="Mayıs 2026">
<source src="../assets/video/vs-ilerleme-mayis-2026.mp4" type="video/mp4">
</video>
</figure>
</div>
<div class="col-12 col-lg-4">
<div class="gyo-panel gyo-months">
<p class="gyo-panel__title">İlerleme Durumu</p>
<ul>%s</ul>
</div>
</div>
</div>
</div>
</section>''' % (IMG, months)


# 10. Konum ve ulaşım — kurumsal .branch-atm iki sütunu; harita OpenStreetMap
LAT, LON = 40.99127, 29.22487
# Kaynak: vakifgyo.com.tr portföy sayfası — "Sancaktepe metro istasyonuna 5 dk.
# mesafede, planlanan Sancaktepe Millet Bahçesi projesine komşu konumda".
DISTANCES = [
    ('Sancaktepe Metro İstasyonu', '5 dk', False),
    ('Sancaktepe Millet Bahçesi (planlanan)', 'Komşu', False),
]


# Konum metni vakifgyo.com.tr proje sayfasından birebir; mesafe listesi (DISTANCES) kullanılmaz
KONUM = 'Sancaktepe’de yer alan 58.133,42 m2 büyüklüğündeki arsamız, Anadolu Yakası’nın son yıllarda en çok gelişim gösteren Sancaktepe İlçesi’nin merkezinde, Sancaktepe metro istasyonuna 5 dk. mesafede, planlanan Sancaktepe Millet Bahçesi projesine komşu konumda yer almaktadır.'


def location():
    bbox = '%.4f,%.4f,%.4f,%.4f' % (LON - 0.02, LAT - 0.011, LON + 0.02, LAT + 0.011)
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
<iframe title="VSancaktepe Merkez konumu, OpenStreetMap haritası" loading="lazy" src="https://www.openstreetmap.org/export/embed.html?bbox=%s&amp;layer=mapnik&amp;marker=%s,%s"></iframe>
</div>
</div>
</div>
</div>
</section>''' % (KONUM, bbox, LAT, LON)


# 11. Ön talep formu — kurumsal form bileşenleri (.input-block, .checkbox-block)
def lead_form():
    opts = ''.join('<option>%s</option>' % p[1] for p in PLANS)
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
<p>Detaylı bilgi almak ve örnek dairemizi ziyaret etmek için bize ulaşın.</p>
</div>
</div>
</div>
</div>
</section>''' % (opts, VS_PHONE[0], VS_PHONE[1])


# 12. Vakıf GYO güvencesi — kurumsal .private-banking
GUARANTEE = '''<section class="private-banking" aria-labelledby="guvence-baslik">
<div class="container">
<div class="private-banking__content">
<picture>
<source media="(min-width: 768px)" srcset="%s30-yil-1110x463.jpg 1x, %s30-yil-2220x926.jpg 2x">
<source media="(max-width: 767px)" srcset="%s30-yil-343x463.jpg 1x, %s30-yil-686x926.jpg 2x">
<img src="%s30-yil-1110x463.jpg" alt="" loading="lazy">
</picture>
<div class="private-banking__content__top">
<h2 id="guvence-baslik" class="searchContent">Vakıf GYO<br>güvencesiyle</h2>
<div class="private-banking__content__top__bottom-text">
<div class="searchContent"><p>Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak, 30 yıldır güçlü Türkiye’nin temellerini atıyoruz. Birlikte nice yıllara…</p></div>
<a href="hakkimizda.html" class="arrow-link"><span class="svg svg--arrow-right-yellow" aria-hidden="true"></span><span>Hakkımızda</span></a>
</div>
</div>
</div>
</div>
</section>''' % (IMG, IMG, IMG, IMG, IMG)

# Mobilde sabit alt çubuk: Ara · WhatsApp · Ön Talep (site haritası, Header)
VS_DOCK = '''<nav class="gyo-dock" aria-label="Hızlı iletişim">
<a href="%s"><span class="svg svg--phone" aria-hidden="true"></span>Ara</a>
<a href="#on-talep" class="gyo-dock__primary">İletişim Formu</a>
</nav>''' % VS_PHONE[0]


def vs_page():
    banner = b.banner(VS_BANNER, b.apply_center(VS_APPLY), label='VSancaktepe Merkez')
    # amenities() (sosyal olanak kartları) çıkarıldı: kart metinleri kaynakta yok
    body = '\n'.join([banner, VS_ABOUT, vs_tabs(), features(), gallery(), TOUR, CAMPAIGN,
                      progress(), location(), lead_form(), GUARANTEE, VS_DOCK])
    return b.page('VSancaktepe Merkez',
                  'Proje Hakkında · Vaziyet Planı · Daire Planları · İlerleme Durumu · Sanal Tur · Konum · '
                  'İletişim Formu', body,
                  h1='<h1 class="sr-only">VSancaktepe Merkez</h1>',
                  shell=(vs_header(), vs_footer()), main_cls='gyo-vs')


# ---------------------------------------------------------------------------
# 3. HAKKIMIZDA — statik içerik sayfası (T03)
#    Kurumsal içerik sayfası: sarı sayfa bandı + metin + sağda .sidebar menüsü.
#    Metin vakifgyo.com.tr/#!vakifgyo sayfasından BİREBİR (yazım düzeltmeleri
#    hariç); Yönetim Politikası infografiği (4.png) HTML'e taşındı.
# ---------------------------------------------------------------------------

ABOUT_TRAIL = [('Ana Sayfa', 'index.html'), ('Kurumsal', '#'),
               ('Vakıf GYO', '#'), ('Hakkımızda', '#')]

POLICY = [
    ('Tam Uyumluluk', 'Tüm yasal ve uymakla yükümlü olduğumuz diğer şartlara, şeffaflıkla uyum sağlarız.'),
    ('Sürekli Gelişme', 'Değişimi yöneterek ve kaynakları etkin kullanarak sürekli gelişim sağlarız.'),
    ('Mutlu Müşteri', 'Sunduğumuz ürün ve hizmetlerle, beklentilerin ötesinde ve güven veren bir '
                      'müşteri deneyimi yaşatırız.'),
    ('Mutlu Çalışan', 'Vakıf GYO çalışanları olarak biz, ortak akıl ve ortak duygu ile sağlıklı bir '
                      'kurum iklimi oluştururuz.'),
]

CERTS = ['ISO 9001 Kalite Yönetim Sistemi Tescil Belgesi',
         'ISO 10002 Müşteri Memnuniyeti Yönetim Sistemi Belgesi',
         'ISO 14064 Sera Gazı Doğrulama Beyanı',
         'ISO 27001 Bilgi Güvenliği Yönetim Sistemi Belgesi']

# Hakkımızda metnindeki bilgiler (_docs/kaynak/vakifgyo.txt)
ABOUT_FACTS = [('Kuruluş', '12 Ocak 1996'), ('Halka arz', '24 Aralık 1996'),
               ('Borsa İstanbul', 'VKGYO')]

# vakifgyo.com.tr Kurumsal menüsü (_docs/kaynak/menu.txt)
SIDEBAR = [
    ('Vakıf GYO', ['Hakkımızda']),
    ('Kurumsal Yönetim', []), ('IK Politikamız', []), ('Şirket Bilgileri', []), ('Bilgi Merkezi', []),
]


def sidebar():
    lis = ''
    for title, subs in SIDEBAR:
        if subs:
            sub = ''.join('<li%s><a href="#"%s>%s</a></li>'
                          % (' class="active"' if s == 'Hakkımızda' else '',
                             ' aria-current="page"' if s == 'Hakkımızda' else '', s) for s in subs)
            lis += ('<li class="first__level openable active"><a href="#">%s</a><ul>%s</ul></li>'
                    % (title, sub))
        else:
            lis += '<li class="first__level"><a href="#">%s</a></li>' % title
    return '''<aside class="sidebar sidebar-mobile gyo-sidebar" aria-label="Kurumsal menüsü">
<div class="sidebar-box">
<h2 class="sidebar__title sidebar-h4">Kurumsal</h2>
<ul>%s</ul>
</div>
<div class="gyo-aside-box">
<p class="gyo-aside-box__title">Şirket Bilgileri</p>
<p>Kuruluş, Yönetim ve Organizasyon Şeması</p>
%s
</div>
</aside>''' % (lis, arrow('Şirket Bilgileri'))


def about_page():
    facts = ''.join('<div><dt>%s</dt><dd>%s</dd></div>' % f for f in ABOUT_FACTS)
    policy = ''.join('<div class="helpful-info__content"><h3 class="h5">%s</h3><p>%s</p></div>' % p
                     for p in POLICY)
    certs = doclist([('', c.split(' ', 2)[0] + ' ' + c.split(' ', 2)[1], c.split(' ', 2)[2], 'PDF', '#')
                     for c in CERTS], ' gyo-doclist--certs')
    content = '''<article class="gyo-article searchContent">
<p class="hero">Türkiye’nin ilk Gayrimenkul Yatırım Ortaklığı Şirketi olarak 12 Ocak 1996 tarihinde kurulan Vakıf GYO, güçlü sermayesi, her geçen gün artan portföy büyüklüğü ve piyasa değerinin yanı sıra güvenilir ortaklık yapısı ile de sektörde önemli bir yere sahiptir.</p>
<p>Türkiye’nin en büyük 2. bankası olan T. Vakıflar Bankası T.A.O.’nun hâkim ortağı olduğu Şirketimiz, 24 Aralık 1996 tarihinde paylarını halka arz etmiş olup Borsa İstanbul’da VKGYO kodu ile işlem görmektedir.</p>
<p>Sembol yapılarıyla sektörde değişime yön veren, referans bir kuruluş olma vizyonuna sahip Şirketimiz, Ülkemiz ve sektörümüze değer katmakla birlikte, düzenli kira ve yüksek portföy getirisi sağlayarak büyüme azmini kararlılıkla sürdürmektedir.</p>
<dl class="gyo-facts gyo-facts--3">%s</dl>

<h2 id="amac">Temel Amaç</h2>
<p>Geleneğimizden aldığımız güçle, geleceğin yaşam alanlarını inşa eder, paydaşlarımıza sürdürülebilir değer sunarız.</p>

<h2 id="vizyon">Vizyon</h2>
<p>Yeniliğe öncülük eden güvenilir ve sürdürülebilir projelerle, sektörde referans kuruluş olmak.</p>

<h2 id="kultur">Kurum Kültürü ve Değerler</h2>
<p>Farkındalığımızı geliştirerek; adil, şeffaf, güvene dayalı ortak duygu ve başarı odaklı, sürekli öğrenen ortak akıl ile insan ve çevreye duyarlı, “biz” kültürünü yaşar, yaşatırız.</p>

<h2 id="politika">Yönetim Politikamız</h2>
<p>Sürdürülebilir ekosistem içinde kaliteli yaşam alanları ile değer sunarız.</p>
<div class="helpful-info gyo-policy">%s</div>

<h2 id="belgeler">Kalite Belgelerimiz</h2>
%s

<h2 id="otuz-yil">Vakıf GYO 30 Yaşında</h2>
<figure class="gyo-figure">
<picture>
<source media="(min-width: 768px)" srcset="%s30-yil-1110x463.jpg 1x, %s30-yil-2220x926.jpg 2x">
<img src="%s30-yil-686x926.jpg" alt="İstanbul Uluslararası Finans Merkezi’nde VakıfBank Genel Müdürlük binasının gece görünümü" loading="lazy">
</picture>
</figure>
<p>Türkiye’nin ilk gayrimenkul yatırım ortaklığı olarak 30 yıldır güçlü Türkiye’nin temellerini atıyoruz.</p>
%s
</article>''' % (facts, policy, certs, IMG, IMG, IMG, arrow('Vakıf GYO 30 Yaşında'))
    body = '''%s
<div class="container">
<div class="gyo-layout">
<div class="gyo-layout__main">%s</div>
%s
</div>
</div>''' % (subpage_banner(ABOUT_TRAIL, 'Hakkımızda'), content, sidebar())
    return b.page('Hakkımızda — Vakıf GYO',
                  'Türkiye’nin ilk gayrimenkul yatırım ortaklığı Vakıf GYO: temel amaç, vizyon, '
                  'yönetim politikası ve kalite belgeleri.', body, b.TICKER, h1='',
                  main_cls='mobile-first')


# ---------------------------------------------------------------------------

def main():
    import build_cubes_a
    for name, fn in [('yatirimci-iliskileri.html', ir_page), ('vsancaktepe-merkez.html', vs_page),
                     ('cubes-ankara.html', build_cubes_a.page), ('hakkimizda.html', about_page)]:
        path = os.path.join(b.OUT, name)
        open(path, 'w', encoding='utf-8', newline='\n').write(fn())
        print('yazıldı:', os.path.relpath(path, b.ROOT))


if __name__ == '__main__':
    main()
