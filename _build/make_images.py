# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif A görsel üreteci

Müşteri materyalinden (gorseller/gorseller/) ana sayfa bloklarının kurumsal
vakifbank.com.tr ölçülerinde görsellerini üretir. Görsellerde METİN YOK:
başlıklar HTML'de (WCAG 1.4.5).

Çalıştırma:  python _build/make_images.py
Çıktı:       src/assets/img/gyo/

Kurumsal ölçüler (vakifbank.com.tr ana sayfası):
  banner            1512x520 (2x 3024x1040) · tablet 2400x828 · mobil 828x480 / 1536x480
  tanıtım bandı     539x472 (.retirement)
  Sarı Rehber       257x257 (.yellow__guide, dairesel)
  sürdürülebilirlik 2280x926 · mobil 750x1100 (.sustainable-banking)
  hızlı erişim      541x500 · mobil 381x500 (.quick-access__item)
  özel bankacılık   1110x463 (2x) · mobil 343x463 (2x) (.private-banking)
  yardım slaytı     540x455 (.help__slider)
"""
import math
import os

import fitz
from PIL import Image, ImageChops, ImageDraw, ImageFilter

Image.MAX_IMAGE_PIXELS = None

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAT = os.path.join(ROOT, 'gorseller', 'gorseller')
OUT = os.path.join(ROOT, 'src', 'assets', 'img', 'gyo')


def mat(*parts):
    return Image.open(os.path.join(MAT, *parts)).convert('RGB')


def save(img, name, q=84):
    path = os.path.join(OUT, name)
    if name.endswith('.png'):
        img.save(path, optimize=True)
    else:
        img.convert('RGB').save(path, 'JPEG', quality=q, subsampling=0,
                                optimize=True, progressive=True)
    print('   %-42s %4dx%-4d %5.0f KB' % (name, img.width, img.height,
                                         os.path.getsize(path) / 1024))


def cover(im, w, h, anchor=(0.5, 0.5)):
    """Oranı koruyarak kutuyu doldurur; `anchor` kırpmanın merkezidir."""
    s = max(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    x = min(max(round(im.width * anchor[0] - w / 2), 0), im.width - w)
    y = min(max(round(im.height * anchor[1] - h / 2), 0), im.height - h)
    return im.crop((x, y, x + w, y + h))


def sharpen(im):
    return im.filter(ImageFilter.UnsharpMask(radius=1.0, percent=45, threshold=3))


def extend_left(im, w, h, place=1.0):
    """Dar/kare kaynağı geniş banda yerleştirir: görsel yüksekliğe ölçeklenip
    `place` oranındaki konuma (sağ kenar) oturur; solda kalan alan görselin
    kendi sol şeridi tek sütuna indirgenip bulanıklaştırılarak doldurulur.
    Böylece kuleler gibi dikey özneler kırpılmadan geniş bantta durur."""
    s = h / im.height
    im = im.resize((round(im.width * s), h), Image.LANCZOS)
    x = round(w * place) - im.width
    canvas = (im.crop((0, 0, max(2, round(im.width * 0.04)), h))
              .resize((1, h), Image.LANCZOS).resize((w, h), Image.BILINEAR)
              .filter(ImageFilter.GaussianBlur(h / 40)))
    fade = round(h * 0.25)
    mask = Image.frombytes('L', (im.width, 1), bytes(
        min(255, round(i * 255 / fade)) for i in range(im.width))).resize((im.width, h))
    canvas.paste(im, (x, 0), mask)
    return canvas


def soft_white(im, side='left', reach=0.55, strength=0.85, hold=0.0):
    """Metin alanı için kenardan içeri doğru beyaza açılan örtü. `hold`
    oranına kadar örtü tam güçte (metnin arkası düz), sonra `reach`
    oranına kadar söner."""
    w, h = im.size
    n = w if side == 'left' else h

    def a(i):
        t = i / n
        if t <= hold:
            return strength
        return strength * max(0.0, 1 - (t - hold) / (reach - hold)) ** 1.4

    ramp = bytes(round(255 * a(i)) for i in range(n))
    if side == 'left':
        mask = Image.frombytes('L', (w, 1), ramp).resize((w, h))
    else:  # top
        mask = Image.frombytes('L', (1, h), ramp).resize((w, h))
    return Image.composite(Image.new('RGB', (w, h), (255, 255, 255)), im, mask)


def circle(im, d):
    """Sarı Rehber dairesi: kurumsal görsel 257x257, saydam zeminli daire."""
    k = 4
    sq = cover(im, d * k, d * k)
    m = Image.new('L', (d * k, d * k), 0)
    ImageDraw.Draw(m).ellipse((0, 0, d * k - 1, d * k - 1), fill=255)
    sq = sq.resize((d, d), Image.LANCZOS)
    out = sq.convert('RGBA')
    out.putalpha(m.resize((d, d), Image.BOX))
    return out


# ---------------------------------------------------------------------------
# Logo — Illustrator PDF'inden vektör SVG
# ---------------------------------------------------------------------------

def build_logo():
    print('\n[1] Logo')
    for src, name in [('VAKIF_GYO_LOGO.pdf', 'vakif-gyo-logo.svg')]:
        doc = fitz.open(os.path.join(MAT, 'logolar', src))
        pg = doc[0]
        r = fitz.Rect()
        for d in pg.get_drawings():
            r |= d['rect']
        pg.set_cropbox(r)
        svg = pg.get_svg_image(text_as_path=True)
        open(os.path.join(OUT, name), 'w', encoding='utf-8').write(svg)
        print('   %-42s %.0fx%.0f pt (vektör)' % (name, r.width, r.height))


# ---------------------------------------------------------------------------
# Banner — kurumsal .banner .home-banner
# ---------------------------------------------------------------------------

BANNER_SIZES = [('3024x1040', 3024, 1040), ('2400x828', 2400, 828)]

# Mobil banner kurumsalda 240 px yüksek: 390 px telefonda oran ~1,6:1,
# 767 px'te 3,2:1. Masaüstü kesimi bu oranlara `cover` ile sığdırılınca
# özne (kuleler, bloklar) kırpılıyordu. Mobil için ayrı kesim: yazı
# etiketleri sol üstte ~yarım genişliği kapladığı için özne sağ yarıya
# yerleşiyor. Telefon 828x480 (2x 414x240), geniş mobil 1536x480 (2x 768x240).
MOBILE_SIZES = [('828x480', 828, 480), ('1536x480', 1536, 480)]


def fade_bottom(im, reach=0.45, strength=0.88, hold=0.2):
    """Alttaki slayt kontrolleri (koyu çerçeveli noktalar, ok bağlantısı)
    kalabalık cephe üstünde okunmuyor; alt kenara açık örtü."""
    f = Image.FLIP_TOP_BOTTOM
    return soft_white(im.transpose(f), 'top', reach, strength, hold).transpose(f)


def build_banners():
    print('\n[2] Banner')
    sunset = mat('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg')
    vyk = mat('10.jpeg')
    ifm = mat('IFM', 'F1.jpg')
    tablo = mat('12', 'TABLO.jpg')
    for key, w, h in BANNER_SIZES:
        save(sharpen(cover(sunset, w, h, (0.5, 0.52))),
             'banner-vsancaktepe-%s.jpg' % key)
        # Kare kaynak: kuleler kırpılmadan sağa yerleşiyor, sol taraf gökyüzü
        save(sharpen(extend_left(vyk, w, h, place=0.98)),
             'banner-vyenikonak-%s.jpg' % key)
    # Kaynaklar 1791 px ve 1200 px: 2x ve tablet yerine tek masaüstü dosyası,
    # kaynağın taşıyabildiği en büyük ölçüde (adı gerçek ölçüyü söyler).
    for name, src, cw, anc in [('derecelendirme', ifm, 1791, (0.62, 0.42)),
                               ('tablo-adalar', tablo, 1512, (0.62, 0.40))]:
        ch = round(cw * 520 / 1512)
        save(sharpen(cover(src, cw, ch, anc)), 'banner-%s-%dx%d.jpg' % (name, cw, ch))

    # Mobil kesimler — (telefon, geniş mobil) için ayrı yerleşim
    for key, w, h in MOBILE_SIZES:
        phone = w < 1000
        # Gün batımı: büyük blok sağda, sol blok yazının arkasında
        save(sharpen(cover(sunset, w, h, (0.60 if phone else 0.5, 0.55))),
             'banner-vsancaktepe-%s.jpg' % key)
        # Kuleler kare kaynağın sol yarısında: kare sağa taşırılıyor, kuleler
        # yazının sağında tam boy kalıyor
        save(sharpen(extend_left(vyk, w, h, place=1.10 if phone else 0.90)),
             'banner-vyenikonak-%s.jpg' % key)
        # İki kule ortada: sağa kaydırılıyor, sol bulut genişletmesi
        save(sharpen(extend_left(ifm, w, h, place=1.15 if phone else 0.92)),
             'banner-derecelendirme-%s.jpg' % key)
        # Kule yazının arkasında, alçak blok ve tepe sağda; alt kenar açık
        save(sharpen(fade_bottom(cover(tablo, w, h, (0.5, 0.62)))),
             'banner-tablo-adalar-%s.jpg' % key)


# ---------------------------------------------------------------------------
# Ana sayfa blokları
# ---------------------------------------------------------------------------

def build_blocks():
    print('\n[3] Bloklar')
    yasam = mat('3', 'web görsel.jpg')
    salon = mat('Sancaktepe_merkez', 'Proje Hakkında', '007.jpg')
    havuz = mat('Sancaktepe_merkez', 'Proje Hakkında', '004.jpg')
    hava = mat('Sancaktepe_merkez', 'Proje Hakkında', '08.jpg')
    sokak = mat('Sancaktepe_merkez', 'Proje Hakkında', '05.jpg')
    sancak3 = mat('Sancaktepe_merkez', 'Proje Hakkında', '003.jpg')
    vyk = mat('10.jpeg')
    tablo = mat('12', 'TABLO.jpg')
    cubes = mat('12', 'CUBES.jpg')
    ifm_e1 = mat('23', 'E1.jpg')
    ifm_c1 = mat('IFM', 'C1.jpg')
    sisli = mat('13', 'Şişli Levent Bina.JPEG')
    medyan = mat('13', 'medyan kadıköy render.jpg')

    # .retirement — öne çıkan proje (539x472, tablet 382x388)
    save(cover(yasam, 539 * 2, 472 * 2, (0.48, 0.55)), 'one-cikan-yasam-basliyor-1078x944.jpg')
    save(cover(yasam, 382 * 2, 388 * 2, (0.48, 0.55)), 'one-cikan-yasam-basliyor-764x776.jpg')

    # .yellow__guide — Proje Rehberi daireleri (257, 2x 514)
    save(circle(salon, 514), 'rehber-oturmak-icin.png')
    save(circle(cover(cubes, 2400, 2400, (0.36, 0.5)), 514), 'rehber-yatirim-icin.png')

    # .sustainable-banking — zemin; metin solda, sol yarı beyaza açılıyor
    save(soft_white(cover(hava, 2280, 926, (0.62, 0.55)), 'left', 0.80, 0.96, hold=0.50),
         'surdurulebilirlik-2280x926.jpg', 80)
    # Mobil blok ~0,86 oranında ve metin bloğun tamamını kaplıyor: görsel
    # yalnızca alt kenarda ipucu olarak kalıyor (kurumsal mobil zemin de sakin).
    save(soft_white(cover(hava, 750, 870, (0.6, 0.7)), 'top', 1.0, 0.96, hold=0.86),
         'surdurulebilirlik-750x870.jpg', 80)

    # .insurance — proje kartları (kurumsal kart görseli ~1,73 oranında)
    for name, im, anc in [('vsancaktepe-merkez', sokak, (0.5, 0.55)),
                          ('vyenikonak', extend_left(vyk, 1420, 820, place=0.92), (0.5, 0.5)),
                          ('tablo-adalar', tablo, (0.5, 0.45)),
                          ('cubes-ankara', cubes, (0.40, 0.5))]:
        save(sharpen(cover(im, 710, 410, anc)), 'proje-%s-710x410.jpg' % name)

    # .quick-access — üstte beyaza açılan alan başlık ve butonlar için
    for name, im, anc in [('yatirimci-iliskileri', ifm_e1, (0.5, 0.55)),
                          ('portfoy', sisli, (0.45, 0.5))]:
        save(soft_white(soft_white(cover(im, 1082, 1000, anc), 'left', 0.62, 0.92), 'top', 0.30, 0.85),
             'hizli-%s-1082x1000.jpg' % name)
        save(soft_white(cover(im, 762, 1000, anc), 'top', 0.70, 0.92),
             'hizli-%s-762x1000.jpg' % name)

    # .help__slider — şantiye videoları (540x455)
    save(cover(sancak3, 1080, 910, (0.5, 0.5)), 'yardim-ilerleme-1080x910.jpg')

    # Mega menü görsel paneli (16:11)
    for name, im, anc in [('projeler', sokak, (0.5, 0.5)), ('portfoy', medyan, (0.55, 0.5)),
                          ('yatirimci', ifm_e1, (0.5, 0.5)), ('kurumsal', ifm_c1, (0.5, 0.6)),
                          ('surdurulebilirlik', havuz, (0.5, 0.5))]:
        save(cover(im, 704, 484, anc), 'menu-%s-704x484.jpg' % name)


# ---------------------------------------------------------------------------
# 30. Yıl bandı — kurumsal .private-banking (kavisli kenarlı koyu bant)
# Geometri VakıfKart _build/process-materials.py'den: kurumsal 1110x463
# görselin alfa kanalından ölçülmüş yay + doğru.
# ---------------------------------------------------------------------------

PB_W, PB_H = 1110, 463
PB_M_W, PB_M_H = 343, 463
PB_ARC = (652.73, 149.79, 149.96)
PB_SLOPE, PB_INTERCEPT = -0.18034, 527.411
PB_TANGENT_Y = 123.19
PB_VEIL, PB_VEIL_M = 51, 88
PB_PHOTO_X, PB_FADE = 420, 90


def edge_mask(w, h, inside=255, outside=0, k=4):
    cx, cy, r = PB_ARC
    sx, sy = w * k / PB_W, h * k / PB_H
    pts = []
    for i in range(361):
        y = PB_TANGENT_Y * i / 360
        pts.append(((cx - math.sqrt(max(r * r - (y - cy) ** 2, 0.0))) * sx, y * sy))
    pts.append(((PB_SLOPE * PB_H + PB_INTERCEPT) * sx, PB_H * sy))
    big = Image.new('L', (w * k, h * k), outside)
    ImageDraw.Draw(big).polygon([(w * k, 0)] + pts + [(w * k, h * k)], fill=inside)
    return big.resize((w, h), Image.BOX)


def ramp(w, h, x0, x1):
    row = bytes(0 if i <= x0 else (255 if i >= x1 else round((i - x0) * 255 / (x1 - x0)))
                for i in range(w))
    return Image.frombytes('L', (w, 1), row).resize((w, h))


def flatten(rgb, veil):
    return Image.composite(rgb, Image.new('RGB', rgb.size, (0, 0, 0)), veil)


def pb_desktop(src, w, h, anchor):
    k = w / PB_W
    photo_x, fade = round(PB_PHOTO_X * k), round(PB_FADE * k)
    photo = sharpen(cover(src, w - photo_x, h, anchor))
    fill = (photo.crop((0, 0, round(48 * k), h)).resize((1, h), Image.LANCZOS)
            .resize((photo_x + fade, h), Image.BILINEAR)
            .filter(ImageFilter.GaussianBlur(18 * k)).point(lambda v: round(v * 0.6)))
    canvas = Image.new('RGB', (w, h))
    canvas.paste(fill, (0, 0))
    layer = Image.new('RGB', (w, h))
    layer.paste(photo, (photo_x, 0))
    canvas = Image.composite(layer, canvas, ramp(w, h, photo_x, photo_x + fade))
    return flatten(canvas, edge_mask(w, h, 255, PB_VEIL))


def pb_mobile(src, w, h, anchor):
    m = sharpen(cover(src, w, h, anchor))
    veil = Image.new('L', (w, h), PB_VEIL_M)
    scrim = Image.linear_gradient('L').resize((w, h))
    top = scrim.point(lambda v: min(255, round(v * 255 / 56)))
    bottom = scrim.point(lambda v: min(255, round((255 - v) * 255 / 102)))
    veil = ImageChops.multiply(veil, ImageChops.darker(top, bottom).point(
        lambda v: 150 + round(v * 105 / 255)))
    return flatten(m, veil)


def build_anniversary():
    print('\n[4] 30. Yıl bandı')
    src = mat('IFM', 'C1.jpg')
    for w, h, fn, anc in [(PB_W, PB_H, pb_desktop, (0.5, 0.55)),
                          (PB_W * 2, PB_H * 2, pb_desktop, (0.5, 0.55)),
                          (PB_M_W, PB_M_H, pb_mobile, (0.5, 0.5)),
                          (PB_M_W * 2, PB_M_H * 2, pb_mobile, (0.5, 0.5))]:
        save(fn(src, w, h, anc), '30-yil-%dx%d.jpg' % (w, h), 86)


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    build_logo()
    build_banners()
    build_blocks()
    build_anniversary()
