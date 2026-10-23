# -*- coding: utf-8 -*-
"""Cubes Ankara — tüm konseptlerin ortak veri kaynağı.

Metinler birebir kaynaktan: cubesankara.com.tr (_docs/kaynak/cubes-site.txt,
cubes-daire-planlari.txt), vakifgyo.com.tr proje sayfası
(portfoy-portfoy-cubes.txt) ve proje kataloğu (cubes-katalog.txt).
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KAYNAK = os.path.join(ROOT, '_docs', 'kaynak')

NAME = 'Cubes Ankara'
SITE = 'https://www.cubesankara.com.tr'
PHONE = ('tel:08502101002', '0850 210 10 02')
TOUR = 'https://www.vakifgyo.com.tr/client/webs/vakifgyo/crm/projects/cubesankara/vtours/21_1/index.htm'
BROCHURE = 'https://www.vakifgyo.com.tr/client/webs/vakifgyo/crm/projects/cubesankara/docs/cubes.catalog.pdf'
FILM = 'https://www.vakifgyo.com.tr/client/webs/vakifgyo/crm/projects/cubesankara/slides/cubes-ankara-tanitim-hd.mp4'
LAT, LON = 39.90566, 32.80251   # vakifgyo.com.tr proje sayfası "Lokasyon" bağlantısı

# Logo renkleri (gorseller/logolar/cubes_ankara_logo.png)
PURPLE, PURPLE_DEEP, YELLOW = '#472562', '#2a1540', '#fbba06'

# cubesankara.com.tr banner metinleri
HERO = [
    ('havasi', 'Ankara’nın', 'Yeni Havası',
     'Yeni bir nefes, yeni bir yaşam, yeni bir heyecan... Ankara’nın yeni havası Cubes Ankara, sizi bekliyor.'),
    ('yasam', 'Ankara’nın', 'Yeni Yaşam Tarzı',
     'Ruhunuzu besleyecek kültür sanat etkinlikleri, günün her saatinde size nefes aldıracak kat bahçeleri ve '
     'yeşil alanlar, gökyüzüne kulaç atabileceğiniz havuz, kat aralarında yer alan koşu parkurları, yoga ve '
     'fitness alanları, dünya mutfaklarından lezzetler sunan cafe ve restoranlar, tüm günlük ihtiyaçlarınızı '
     'karşılayabileceğiniz ticari alanlar Cubes Ankara’da sizin için tasarlandı'),
    ('calisma', 'Ankara’nın', 'Yeni Çalışma Alanı',
     'Cubes Ankara, modern ve ferah ofis alanları, çalışma ortamını daha verimli kılan tasarım anlayışı, geniş '
     'otoparkı ve şehir manzaralı kat bahçeleriyle, işinize keyif ve konfor katacak onlarca detaya sahip.'),
]

# vakifgyo.com.tr proje sayfası
ABOUT = ('Ankara Çukurambar\'da yer alan Cubes Ankara Projemiz; 215.984,66 m2 kapalı inşaat alanına sahip '
         '1+1\'den, 6+1\'e kadar değişen konut, home office, ofis ile otel, ticari ve sosyal donatı alanlarından '
         'oluşuyor. Yeşil alanların öneminin farkında olarak kat bahçeleri, teraslar ve ortak alanların da '
         'sunulduğu Cubes Ankara projemiz; çocuklara, evcil hayvanlara, doğaya ve engellilere dost bir proje '
         'olarak öne çıkıyor.')
FACTS = [('Lokasyon', 'Ankara İli, Çankaya İlçesi, Çukurambar Mahallesi'), ('İnşaat Alanı', '215.984,66 m2'),
         ('Ada / Parsel', '16125 / 4 · 16124 / 5')]
KONUM = 'Ankara İli, Çankaya İlçesi, Çukurambar Mahallesi'

# "Ankara'nın Yeni ..." blokları: site + katalog (Yeni Yaşam Tarzı paragrafı katalogdan)
BLOCKS = [
    ('Ankara’nın Yeni Havası',
     'Yeni bir nefes, yeni bir yaşam, yeni bir heyecan... Ankara’nın yeni havası Cubes Ankara, sizi bekliyor.'),
    ('Ankara’nın Yeni Yaşam Tarzı',
     'Konut, ofis, otel, ticari alanlar ve sosyal donatılarla yeni nesil karma yaşamın merkezi olan Cubes Ankara, '
     'kültür sanat alanları, gösteri merkezi, gurme lezzetlere ev sahipliği yapacak cafe&restoranları, alışveriş '
     'noktaları ve spor alanları ile şehrin merkezi Çukurambar’da, yatırım değeri yüksek, avantajlı bir '
     'lokasyonda yükseliyor.'),
    ('Ankara’nın Yeni Modası',
     'Ruhunuzu besleyecek kültür sanat etkinlikleri, günün her saatinde size nefes aldıracak kat bahçeleri ve '
     'yeşil alanlar, gökyüzüne kulaç atabileceğiniz havuz, kat aralarında yer alan koşu parkurları, yoga ve '
     'fitness alanları, dünya mutfaklarından lezzetler sunan cafe ve restoranlar, tüm günlük ihtiyaçlarınızı '
     'karşılayabileceğiniz ticari alanlar Cubes Ankara’da sizin için tasarlandı'),
    ('Ankara’nın Yeni Çalışma Alanı',
     'Cubes Ankara, modern ve ferah ofis alanları, çalışma ortamını daha verimli kılan tasarım anlayışı, geniş '
     'otoparkı ve şehir manzaralı kat bahçeleriyle, işinize keyif ve konfor katacak onlarca detaya sahip.'),
]

CAMPAIGN = ('Cubes Ankara’da', 'Peşin Ödemelerde 30. Yıla özel 30% indirim kampanyası',
            'Ankara Çukurambar\'da yer alan karma yaşam projemiz Cubes Ankara\'da, peşin ödemelerde 30. Yıla özel '
            '30% indirim fırsatı ile ofis/home ofis sahibi olma fırsatını kaçırmayın.',
            'Cazip fiyat avantajları sunan projemiz hakkında detaylı bilgi almak için bize ulaşın.')

SAMPLE = ('Örnek Dairelerimize Sizleri Bekliyoruz',
          'Ankara\'nın tam kalbinde yer alan Cubes Ankara projemizi yerinde deneyimlemek için 0850 210 10 02 nolu '
          'telefondan Satış Ofisimize ulaşabilirsiniz.')

# Katalog render'ları (gorseller/indirilen/cubes-katalog) — galeri sırası ve alt metinleri
GALLERY = [
    ('kuleler', 'Cubes Ankara rezidans ve ofis kuleleri, gündüz görünümü'),
    ('sky-cube', 'Sky Cube dairenin cam cepheli salonu ve gün batımında şehir manzarası'),
    ('havuz', 'Çatı katındaki havuz ve şehir silueti'),
    ('parkur', 'Kat arasındaki gökyüzü koşu parkuru'),
    ('avlu', 'Bloklar arasındaki yeşil avlu ve yürüyüş yolları'),
    ('teras', 'Kat bahçesindeki cafe ve oturma alanları'),
    ('lobi', 'Ofis bloğu lobisi'),
    ('ofis-cephe', 'Ofis bloğunun cadde cephesi'),
]

# Daire planı görselleri: kaynak sırası (cubesankara.com.tr #!proje-plan, bookmark1..20)
PLAN_IMAGES = ['sky-cube-b-konut-1-1-l-2', 'sky-cube-a-konut-1-1-l-1', 'cube-konut-1-1-a',
               'extension-cube-konut-1-1-b', 'corner-large-cube-konut-2-1-c', 'corner-cube-konut-2-1-d',
               'be-long-cube-konut-2-1-e', 'be-long-cube-konut-2-1-e2', 'belong-cube-2-1-konut-2-1-f',
               'be-long-extension-cube-konut-2-1-g', 'cube-2-1-konut-2-1-h', 'extension-cube-konut-2-1-i',
               'corner-cube-3-1-konut-3-1-j', 'corner-large-cube-konut-3-1-k', 'belong-cube-3-1-konut-3-1-m',
               'belong-extension-cube-3-1', 'cube-4-1-konut-4-1-n', 'extension-cube-4-1',
               'cube-6-1-konut-6-1-o', 'cube-p-tip-3-1-dublex']
PLAN_KEYS = ['l2', 'l1', 'a', 'b', 'c', 'd', 'e', 'e2', 'f', 'g', 'h', 'i', 'j', 'k', 'm', 'm2', 'n', 'n2', 'o', 'p']


def _title(s):
    """'CORNER LARGE CUBE' → 'Corner Large Cube' (Türkçe İ/ı korunur)."""
    def word(w):
        if not w:
            return w
        return w[0] + w[1:].replace('İ', 'i').lower()
    return '-'.join(' '.join(word(w) for w in part.split(' ')) for part in s.split('-'))


def plans():
    """Kaynak dosyasından 20 daire tipi: dict(key, group, name, typ, rooms, net, gross, img)."""
    lines = [l.strip() for l in io.open(os.path.join(KAYNAK, 'cubes-daire-planlari.txt'), encoding='utf-8')]
    lines = [l for l in lines[3:] if l]
    entries, cur, head = [], None, []
    i = 0
    while i < len(lines):
        l = lines[i]
        if l.endswith(':'):
            if head:
                cur = {'head': head, 'rooms': [], 'net': None, 'gross': None}
                entries.append(cur)
                head = []
            key, val = l[:-1].strip(), lines[i + 1].replace(' m2', '').replace('.', ',')
            if key == 'Net Alan':
                cur['net'] = val
            elif key == 'Toplam Brüt Alan':
                cur['gross'] = val
            else:
                cur['rooms'].append((key, val))
            i += 2
            continue
        head.append(l)
        i += 1
    out = []
    for n, e in enumerate(entries):
        h = e['head']
        typ = _title(h[-1])                     # 'L 2 Tipi'
        gl = [x for x in h[:-1] if re.fullmatch(r'(KONUT )?\d\+1( DUBLEKS)?', x)]
        group = _title(re.sub(r'^KONUT ', '', gl[-1])) if gl else ''
        name = _title(' '.join(x for x in h[:-1] if x not in gl))
        out.append({'key': PLAN_KEYS[n], 'group': group, 'name': name, 'typ': typ, 'rooms': e['rooms'],
                    'net': e['net'], 'gross': e['gross'], 'img': PLAN_IMAGES[n]})
    assert len(out) == 20, len(out)
    return out


def plan_img_height(name):
    """src/assets/img/gyo/<name> görselinin yüksekliği (width/height öznitelikleri için)."""
    from PIL import Image
    return Image.open(os.path.join(ROOT, 'src', 'assets', 'img', 'gyo', name)).height


def groups():
    """Sekme sırası: 1+1 · 2+1 · 3+1 · 4+1 · 6+1 · 3+1 Dubleks."""
    order = []
    for p in plans():
        if p['group'] not in order:
            order.append(p['group'])
    return order


if __name__ == '__main__':
    for p in plans():
        print(p['key'], '|', p['group'], '|', p['name'], '|', p['typ'], '|', len(p['rooms']), p['net'], p['gross'], p['img'])
    print(groups())
