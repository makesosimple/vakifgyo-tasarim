# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif A iç sayfa görselleri

Yatırımcı İlişkileri ana sayfası, VSancaktepe Merkez proje sitesi ve
Hakkımızda sayfasının görsellerini müşteri materyalinden üretir. Yardımcılar
(cover, extend_left, fade, kaydetme) ana sayfa üretecinden gelir; görsellerde
metin yok.

Çalıştırma:  python _build/make_images_pages.py
Çıktı:       src/assets/img/gyo/  (ir-*, vs-*)
             src/assets/video/vs-ilerleme-mayis-2026.mp4
"""
import os
import subprocess
import sys

import fitz
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_images as m  # noqa: E402

VS = ('Sancaktepe_merkez',)
VIDEO_OUT = os.path.join(m.ROOT, 'src', 'assets', 'video')


def vs(*parts):
    return m.mat(*(VS + parts))


def contain_white(path, w, h, pad=0.06):
    """Saydam zeminli daire planı → beyaz zemin, oran korunarak ortalanır."""
    im = Image.open(path).convert('RGBA')
    box_w, box_h = round(w * (1 - 2 * pad)), round(h * (1 - 2 * pad))
    s = min(box_w / im.width, box_h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    canvas = Image.new('RGBA', (w, h), (255, 255, 255, 255))
    canvas.alpha_composite(im, ((w - im.width) // 2, (h - im.height) // 2))
    return canvas.convert('RGB')


def logo_svg(src, name):
    doc = fitz.open(os.path.join(m.MAT, 'logolar', src))
    pg = doc[0]
    r = fitz.Rect()
    for d in pg.get_drawings():
        r |= d['rect']
    pg.set_cropbox(r)
    open(os.path.join(m.OUT, name), 'w', encoding='utf-8').write(pg.get_svg_image(text_as_path=True))
    print('   %-42s %.0fx%.0f pt (vektör)' % (name, r.width, r.height))


# ---------------------------------------------------------------------------
# Yatırımcı İlişkileri
# ---------------------------------------------------------------------------

def build_ir():
    print('\n[IR] Yatırımcı İlişkileri')
    tower = m.mat('IFM', 'D2.jpg')
    # Kurumsal .retirement görseli 539x472 (2x 1078x944), mobil 382x388 (2x)
    m.save(m.sharpen(m.cover(tower, 1078, 944, (0.5, 0.42))), 'ir-sonuclar-1078x944.jpg')
    m.save(m.sharpen(m.cover(tower, 764, 776, (0.5, 0.42))), 'ir-sonuclar-764x776.jpg')
    cover = m.mat('3', 'VBGYO_FaaliyetRap_2025_KAPAK_TR.jpg')
    m.save(cover.resize((372, 526), Image.LANCZOS), 'ir-faaliyet-raporu-2025-372x526.jpg')
    tsrs = m.mat('3', 'TSRS -WEB-DUYURU.jpg')
    m.save(m.cover(tsrs, 372, 526, (0.5, 0.5)), 'ir-tsrs-2025-372x526.jpg')


# ---------------------------------------------------------------------------
# VSancaktepe Merkez proje sitesi
# ---------------------------------------------------------------------------

# Banner: kaynaklar 1200x800. Masaüstünde tek dosya 1512x520 (kurumsal 1x);
# mobil kesimler ana sayfadaki gibi telefon 828x480 / geniş mobil 1536x480.
VS_SLIDES = [
    ('dogallik', ('Proje Hakkında', '08.jpg'), (0.55, 0.55), 0.62),
    ('uyum', ('Proje Hakkında', '004.jpg'), (0.6, 0.5), 0.70),
]

VS_AMENITIES = [
    ('havuz', '09.jpg', (0.5, 0.55)),
    ('yuruyus', '08.jpg', (0.5, 0.6)),
    ('avlu', '07.jpg', (0.5, 0.55)),
    ('peyzaj', '003.jpg', (0.5, 0.6)),
    ('ticari', '06.jpg', (0.45, 0.6)),
]

VS_GALLERY = ['002.jpg', '004.jpg', '007.jpg', '005.jpg', '006.jpg', '05.jpg']

VS_PLANS = [('1-1', 'b4-konut-1-1.png'), ('2-1', 'a1-konut-2-1.png'),
            ('3-1', 'c2-konut-3-1.png'), ('4-1', 'a-konut-4-1.png')]
# Orijinal PNG'lerdeki boş kenarlar kırpılır (içerik kutusu + 12 px); build_alt_b.PLAN_CROP ile aynı
PLAN_CROP = {'1-1': (176, 27, 687, 673), '2-1': (64, 32, 748, 546),
             '3-1': (81, 42, 880, 480), '4-1': (78, 43, 843, 524)}
PLAN_W, PLAN_PAD = 1440, 0.02


def plan_1440(path, key):
    """Daire planı: kırpılır, kendi oranında 1440 px genişliğe, beyaz zemin, %2 kenar payı."""
    im = Image.open(path).convert('RGBA').crop(PLAN_CROP[key])
    h = round(PLAN_W * im.height / im.width)
    box_w, box_h = round(PLAN_W * (1 - 2 * PLAN_PAD)), round(h * (1 - 2 * PLAN_PAD))
    sc = min(box_w / im.width, box_h / im.height)
    im = im.resize((round(im.width * sc), round(im.height * sc)), Image.LANCZOS)
    canvas = Image.new('RGBA', (PLAN_W, h), (255, 255, 255, 255))
    canvas.alpha_composite(im, ((PLAN_W - im.width) // 2, (h - im.height) // 2))
    return canvas.convert('RGB')


def build_vs_plans():
    for key, src in VS_PLANS:
        path = os.path.join(m.MAT, *VS, 'Daire Planları', src)
        m.save(contain_white(path, 960, 640), 'vs-plan-%s-960x640.jpg' % key)
        m.save(m.sharpen(plan_1440(path, key)), 'vs-plan-%s-1440.jpg' % key, q=88)


def build_vs():
    print('\n[VS] VSancaktepe Merkez')
    logo_svg('SancaktepeMerkezLogo.pdf', 'vs-logo.svg')

    for name, src, anc, phone_x in VS_SLIDES:
        im = vs(*src)
        m.save(m.sharpen(m.cover(im, 1512, 520, anc)), 'vs-banner-%s-1512x520.jpg' % name)
        m.save(m.sharpen(m.cover(im, 1536, 480, anc)), 'vs-banner-%s-1536x480.jpg' % name)
        m.save(m.sharpen(m.cover(im, 828, 480, (phone_x, anc[1]))), 'vs-banner-%s-828x480.jpg' % name)

    plan = vs('vsancaktepe-vaziyet-plani.jpg')
    m.save(m.sharpen(m.cover(plan, 1078, 944, (0.5, 0.5))), 'vs-ozet-1078x944.jpg')
    m.save(m.sharpen(m.cover(plan, 764, 776, (0.55, 0.5))), 'vs-ozet-764x776.jpg')

    build_vs_plans()

    for key, src, anc in VS_AMENITIES:
        m.save(m.sharpen(m.cover(vs('Proje Hakkında', src), 710, 410, anc)),
               'vs-olanak-%s-710x410.jpg' % key)

    for i, src in enumerate(VS_GALLERY, 1):
        im = vs('Proje Hakkında', src)
        m.save(m.sharpen(m.cover(im, 960, 640)), 'vs-galeri-%d-960x640.jpg' % i)


def build_video():
    """İlerleme durumu: Mayıs 2026 videosu web için 720p, sessiz; poster karesi."""
    import imageio_ffmpeg
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    src = os.path.join(m.MAT, *VS, 'İlerleme Durumu', 'vsancaktepe-mayis-2026.mp4')
    os.makedirs(VIDEO_OUT, exist_ok=True)
    out = os.path.join(VIDEO_OUT, 'vs-ilerleme-mayis-2026.mp4')
    poster = os.path.join(m.OUT, 'vs-ilerleme-mayis-2026-1280x720.jpg')
    subprocess.run([ff, '-y', '-loglevel', 'error', '-i', src, '-vf', 'scale=1280:-2',
                    '-c:v', 'libx264', '-crf', '33', '-preset', 'slow', '-an',
                    '-movflags', '+faststart', out], check=True)
    subprocess.run([ff, '-y', '-loglevel', 'error', '-ss', '6', '-i', src, '-frames:v', '1',
                    '-vf', 'scale=1280:-2', '-q:v', '3', poster], check=True)
    print('\n[VS] video  %.1f MB, poster %.0f KB' % (os.path.getsize(out) / 1e6,
                                                     os.path.getsize(poster) / 1024))


# ---------------------------------------------------------------------------
# Banner alternatifleri (karşılaştırma sayfası)
#   bk-*  Seçenek 1, bileşik banner: fotoğraf KIRPILMADAN, kendi oranında,
#         2x yükseklik (1040 px). Zemin rengi sayfada görselin sol şeridinden.
#   bx-*  Seçenek 3, kutulu banner: 2220x1038 (container 1110x519'un 2x'i);
#         kırpma merkezi ana konunun üstünü koruyacak şekilde seçildi.
# ---------------------------------------------------------------------------

BANNER_SOURCES = [
    ('vsancaktepe', ('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg'), (0.55, 0.55)),
    ('vyenikonak', ('10.jpeg',), (0.32, 0.45)),
    ('derecelendirme', ('IFM', 'F1.jpg'), (0.5, 0.0)),
    ('tablo-adalar', ('12', 'TABLO.jpg'), (0.45, 0.0)),
]


def build_banner_alts():
    print('\n[Banner] alternatifler')
    for name, src, anc in BANNER_SOURCES:
        im = m.mat(*src)
        h = 1040
        w = round(im.width * h / im.height)
        m.save(m.sharpen(im.resize((w, h), Image.LANCZOS)), 'bk-%s-h1040.jpg' % name)
        # Kare kaynak (VYeniKonak) kutu oranına kırpılınca kuleler iki uçtan
        # kesiliyor; ana sayfadaki gibi sola uzatılıyor.
        box = (m.extend_left(im, 2220, 1038, place=1.0) if name == 'vyenikonak'
               else m.cover(im, 2220, 1038, anc))
        m.save(m.sharpen(box), 'bx-%s-2220x1038.jpg' % name)


# ---------------------------------------------------------------------------
# Seçenek 1 · logo kavisli bileşik banner (3840x1040, 1920 px ekranın 2x'i)
#
# Kavis VAKIF_GYO_LOGO.pdf'teki vektör yoldan birebir:
#   V  — "V" harfinin sağ kolu: alttaki kıvrım + sağ üste yükselen eğri
#   VB — sarı işaretin sola yatık dış kenarı ve yuvarlatılmış üst köşesi
# Eğri banner yüksekliğine ölçeklenir (oran korunur).
#
# Kesintisiz geçiş için:
#   1. Zemin, fotoğrafın sol kenar şeridinin satır satır renginden üretilir
#      (dikeyde bulanık), sol tarafa doğru tek bir sakin tona yaklaşır.
#   2. Fotoğrafın kavise yakın kısmı aynı zemine erir; kavisin hemen yanında
#      kesik bina, yol, araba kalmaz.
#   3. Kavis kenarı birkaç piksel yumuşatılır (keskin ama tırtıksız).
# Görsel sayfada object-fit:cover + sağa yaslı; dar ekranda soldaki zemin
# kırpılır, fotoğraf ve kavis yerinde kalır.
# ---------------------------------------------------------------------------

def _bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        u = 1 - t
        out.append((u**3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t**3 * p3[0],
                    u**3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t**3 * p3[1]))
    return out


# PDF koordinatları (pt), alttan üste sıralı
CURVES = {
    'v': [((119.7, 427.03), (119.82, 427.28), (136.57, 428.64), (144.68, 419.53)),
          ((144.68, 419.53), (148.32, 415.45), (166.29, 394.0), (171.24, 387.82)),
          ((171.24, 387.82), (181.65, 374.78), (188.1, 373.89), (188.1, 373.89))],
    'vb': [((113.55, 432.05), (113.55, 432.05), (123.66, 385.8), (123.66, 385.8)),
           ((123.66, 385.8), (124.97, 377.53), (132.55, 369.42), (144.67, 369.42))],
}


def curve_points(kind, h):
    """Eğri noktaları: y 0 (üst) … h (alt), x eğrinin en sol noktasından."""
    segs = CURVES[kind]
    pts = [p for s in segs for p in _bez(*s)]
    ys = [p[1] for p in pts]
    top, bot = min(ys), max(ys)
    k = h / (bot - top)
    x0 = min(p[0] for p in pts)
    return [((x - x0) * k, (y - top) * k) for x, y in pts]


def _smooth(t):
    """smootherstep: başında ve sonunda eğimi sıfır, bant/kenar oluşmaz."""
    import numpy as np
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (t * 6 - 15) + 10)


def _gauss1d(a, sigma):
    """Satır profilini dikeyde yumuşatır (kenarlar yansıtılarak)."""
    import numpy as np
    r = int(sigma * 3)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    pad = np.pad(a, ((r, r), (0, 0)), mode='reflect')
    return np.stack([np.convolve(pad[:, c], k, mode='valid') for c in range(a.shape[1])], 1)


def logo_banner(im, kind, top_frac, cw=3840, ch=1040, width=0.42):
    """Pürüzsüz bileşik banner. Bulanıklaştırma ya da maske yok: her satırda
    fotoğraf ile o satırın kendi renk tonu arasında smootherstep geçiş.

    kind:     'v' / 'vb' — geçişin başladığı çizgi logo kavisini izler;
              'line'     — düz (dikey) geçiş.
    top_frac: geçiş çizgisinin üst ucunun fotoğraf genişliğine oranı.
    width:    geçiş genişliği, fotoğraf genişliğine oran."""
    import numpy as np
    w = round(im.width * ch / im.height)
    photo = np.asarray(im.resize((w, ch), Image.LANCZOS), dtype=np.float64)
    xp = cw - w
    W = width * w

    # Geçiş başlangıcı c(y): logo eğrisi (oran korunarak banner yüksekliğine)
    if kind == 'line':
        c = np.full(ch, xp + top_frac * w)
    else:
        pts = sorted(curve_points(kind, ch), key=lambda p: p[1])
        ys = np.array([p[1] for p in pts])
        xs = np.array([p[0] for p in pts])
        c = np.interp(np.arange(ch), ys, xs)
        c += xp + top_frac * w - c[0]

    # Satır tonu: geçişe giren fotoğraf şeridinin satır ortalaması,
    # dikeyde geniş yumuşatma — zemin ile fotoğraf aynı rengi paylaşır
    prof = np.empty((ch, 3))
    for y in range(ch):
        a = int(np.clip(c[y] - xp, 0, w - 2))
        b = int(np.clip(a + 0.30 * W, a + 2, w))
        prof[y] = photo[y, a:b].mean(0)
    mean = prof.mean(0)
    # Zemin: iki duraklı sakin dikey geçiş — üst üçte birin ve alt üçte birin
    # tonu, ortalamaya doğru yarı yarıya yaklaştırılmış. Satır satır renk
    # uzatılmadığı için yatay şerit oluşmaz.
    top = (prof[: ch // 3].mean(0) + mean) / 2
    bot = (prof[-ch // 3:].mean(0) + mean) / 2
    t = _smooth((np.arange(ch) - ch * 0.25) / (ch * 0.6))[:, None]
    col = top * (1 - t) + bot * t

    X = np.arange(cw)[None, :]
    ground = np.broadcast_to(col[:, None, :], (ch, cw, 3)).copy()

    # Fotoğraf katmanı (fotoğrafın solunda zemin)
    layer = ground.copy()
    layer[:, xp:] = photo
    a = _smooth((X - c[:, None]) / W)
    a *= _smooth((X - xp) / (0.10 * w))          # fotoğrafın düz sol kenarı da erir
    out = ground * (1 - a[..., None]) + layer * a[..., None]
    return Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8))


LOGO_SLIDES = [
    # ad, kaynak, kaynak kırpma (x0, x1 oranı), kavis üst ucu (V, VB) —
    # fotoğraf genişliğine oran; ana konu kavisin sağında kalacak şekilde
    ('vsancaktepe', ('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg'), (0.0, 1.0), (0.42, 0.10)),
    ('vyenikonak', ('10.jpeg',), (0.0, 0.82), (0.14, 0.05)),
    ('derecelendirme', ('IFM', 'F1.jpg'), (0.10, 0.92), (0.26, 0.08)),
    ('tablo-adalar', ('12', 'TABLO.jpg'), (0.0, 1.0), (0.24, 0.06)),
]


def build_logo_banners():
    print('\n[Banner] logo kavisli bileşik')
    for name, src, (a, z), (tv, tvb) in LOGO_SLIDES:
        im = m.mat(*src)
        im = im.crop((round(im.width * a), 0, round(im.width * z), im.height))
        for key, kind, tf in (('v', 'v', tv), ('vb', 'vb', tvb), ('soft', 'line', tvb - 0.22)):
            m.save(logo_banner(im, kind, tf), 'bl-%s-%s-3840x1040.jpg' % (key, name), q=84)


if __name__ == '__main__':
    if sys.argv[1:] == ['plans']:
        build_vs_plans()
        sys.exit()
    if sys.argv[1:] == ['banner']:
        build_banner_alts()
        build_logo_banners()
        sys.exit()
    build_ir()
    build_vs()
    build_video()
    build_banner_alts()
