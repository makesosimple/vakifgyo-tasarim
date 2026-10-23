# -*- coding: utf-8 -*-
"""
Vakıf GYO — Alternatif A · ana sayfa banner görselleri (kadraja göre işlenmiş)

Kurumsal banner alanının yüksekliği sabit (masaüstü/tablet 519 px, mobil
240 px), genişliği değişken (768–2560 px). Metin kutuları solda, konteyner
(1140 px, ortalı) içinde; en uzun satır konteyner solundan ~700 px'e uzanır
ve 64–305 px satırlarını kaplar.

Yerleşim modeli
  Görsel sağa yaslanmaz; ODAK NOKTASI (ilk bina / 9 rakamı) metin kutusunun
  bittiği yerin 24 px sağına oturur. Bunun için dosyada odak, konteyner
  soluna göre sabit bir x'e yerleştirilir; CSS görseli konteynere bağlı
  konumlar:  left = calc(50% - 570px - K)   (K: dosyadaki sol pay)
    ≥1700 px   banner-<ad>-5200x1040.jpg  K=720   tam kadraj
    1200–1699  banner-<ad>-o-3500x1040.jpg K=290   ana blok kesimi
    768–1199   banner-<ad>-t-3200x1040.jpg sağa yaslı (metin üstüne biner)
    ≤767       banner-<ad>-m-1600x480.jpg  sağa yaslı
  Ekran büyüdükçe görsel metnin yanında kalır; sağda açılan alan görselin
  kendi sağ kenarından türeyen uzantıyla dolar (gökyüzü tonu).

Geçişler
  Görsel panele keskin kenarla değil, şeffaflık rampasıyla karışır. Rampa
  satıra göre uzar: gökyüzünde %35–40, bina kenarına kadar olan payda tam
  pay (bina net kalır), ön planda %20–30. Kenarda içerik bitmesin diye
  görselin kenar şeridi aynalanarak rampanın altına serilir (podyum,
  ağaçlar); bina/rakam aynalanmaz. Panel görselin gökyüzü satırlarından
  türer ve uzaklaştıkça tek gök tonuna kavuşur. Her slaydın gök tonu
  banner-colors.json'a yazılır (slayt zemini; dosya dışına taşarsa).

Kaynaklar:
  VSancaktepe Merkez  gorseller/8/…Sunset… (3000 px render)
  VYeniKonak          vyenikonak.com.tr proje kataloğu s.4 render'ının sağ
                      yarısı: iki kule, 3548x1777 (gorseller/indirilen/vyk-katalog)
  Tablo Adalar        tablo-adalar-brosur-2025.pdf, 2. sayfa genel görünüm
                      (broşürdeki parçalar birleştirildi; 5220x3374, metinsiz)
  Derecelendirme      gorseller/3/DERECELENDİRME (1).jpg — Vakıf GYO'nun
                      haber görseli (altın 9,48); metin bandı kesilip alınır

Çalıştırma:  python _build/make_banners_a.py
Çıktı:       src/assets/img/gyo/banner-*.jpg, banner-colors.json
"""
import json
import os
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_images as m  # noqa: E402

Image.MAX_IMAGE_PIXELS = None
OUT = m.OUT
DL = os.path.join(m.ROOT, 'gorseller', 'indirilen')

GAP = 24          # metin kutusu ile odak arası (CSS px)
K_DESK, K_MID = 720, 290   # CSS'teki sol pay (bkz. 04-gyo.css)


def _smooth(t):
    t = np.clip(t, 0.0, 1.0)
    return t * t * t * (t * (t * 6 - 15) + 10)


def _gauss_rows(a, sigma):
    if sigma < 0.5:
        return a
    r = int(sigma * 3)
    k = np.exp(-0.5 * (np.arange(-r, r + 1) / sigma) ** 2)
    k /= k.sum()
    flat = a.reshape(a.shape[0], -1)
    pad = np.pad(flat, ((r, r), (0, 0)), mode='reflect')
    out = np.stack([np.convolve(pad[:, c], k, mode='valid') for c in range(flat.shape[1])], 1)
    return out.reshape(a.shape)


def profile(ph, clean, strip=0.03):
    """Kenar şeridinin satır renkleri; `clean` dışındaki satırlar (nesne var)
    komşu temiz satırlar arasında doğrusal geçişle doldurulur."""
    h, w = ph.shape[:2]
    prof = ph[:, : max(2, round(w * strip))].mean(1)
    ok = np.zeros(h, bool)
    for y0, y1 in clean:
        ok[int(h * y0): int(round(h * y1))] = True
    ys = np.arange(h)
    for c in range(3):
        prof[:, c] = np.interp(ys, ys[ok], prof[ok, c])
    return _gauss_rows(prof, h * 0.02)


def _ramp_len(ch, w, zones, default=0.05):
    L = np.full(ch, default * w, np.float32)
    for y0, y1, f in zones:
        L[int(ch * y0): int(round(ch * y1))] = f * w
    return _gauss_rows(L[:, None], ch * 0.04)[:, 0]


def compose(photo, cw, ch, subject=0.0, sx=None, clean=((0.0, 1.0),), left=None, right=None,
            strip=0.03, fade=0.6, top=0.12, flat=False, ground=None):
    """photo ch yüksekliğine ölçeklenir; odak (görsel genişliğinin `subject`
    oranı) dosyada `sx` px'e oturur (sx None → görsel sağa yaslı, sağ uzantı
    yok). left/right: dict(mirror=aynalanan kenar payı, zones=[(y0,y1,rampa)])
    — rampa ve pay görsel genişliği cinsinden; rampa aynalı şeridin dış
    kenarından başlar. Döndürür: (görsel, gök tonu)."""
    left = left or {}
    right = right if sx is not None else None
    w = round(photo.width * ch / photo.height)
    ph = np.asarray(photo.convert('RGB').resize((w, ch), Image.LANCZOS), dtype=np.float32)
    ml = round(w * left.get('mirror', 0.0))
    mr = round(w * right.get('mirror', 0.0)) if right else 0
    xp = (cw - w) if sx is None else sx - round(subject * w)
    assert xp - ml >= 0, 'sol pay dar: %d' % (xp - ml)
    assert xp + w + mr <= cw, 'kanvas dar: %d > %d' % (xp + w + mr, cw)

    pl = profile(ph, clean, strip).astype(np.float32)
    pr = profile(ph[:, ::-1], clean, strip).astype(np.float32)
    sky = pl[: max(1, int(ch * top))].mean(0)
    if ground is not None:
        # ufkun altı: son temiz (gök) satırından fotoğrafın zemin tonuna dikey
        # geçiş. Ufuk tonu aşağıya sabit uzatılınca sis gibi okunuyordu.
        y0 = int(round(ch * max(y1 for _, y1 in clean)))
        g = np.asarray(ph[int(ch * 0.85):].reshape(-1, 3).mean(0) * ground, dtype=np.float32)
        t = _smooth(np.linspace(0, 1, ch - y0, dtype=np.float32))[:, None]
        for prof in (pl, pr):
            prof[y0:] = prof[y0 - 1] * (1 - t) + g * t
    if flat:
        # düz panel: tüm satırlar gök tonu. Kenar satır tonları (ufuk/yol) yatayda
        # uzatılınca sis gibi okunuyordu; fotoğraf bu zemine şeffaflıkla karışır.
        pl = pr = np.broadcast_to(sky, (ch, 3)).astype(np.float32)
    xs = np.arange(cw, dtype=np.float32)
    # panel: ek yerinde satır profili, uzaklaştıkça gök tonu
    tl = _smooth((xp - xs) / (fade * w))[None, :, None]
    tr = _smooth((xs - (xp + w)) / (fade * w))[None, :, None]
    mix = np.clip((xs - xp) / w, 0, 1)[None, :, None]
    base = pl[:, None, :] * (1 - mix) + pr[:, None, :] * mix
    base = base * (1 - tl) + sky[None, None, :] * tl
    base = base * (1 - tr) + sky[None, None, :] * tr
    base = np.ascontiguousarray(base, dtype=np.float32)

    layer = base.copy()
    layer[:, xp: xp + w] = ph
    if ml:
        layer[:, xp - ml: xp] = ph[:, :ml][:, ::-1]
    if mr:
        layer[:, xp + w: xp + w + mr] = ph[:, w - mr:][:, ::-1]

    L = _ramp_len(ch, w, left.get('zones', ()))
    a = _smooth((xs[None, :] - (xp - ml)) / L[:, None])
    if right:
        R = _ramp_len(ch, w, right.get('zones', ()))
        a = np.minimum(a, _smooth(((xp + w + mr) - xs[None, :]) / R[:, None]))
    a = a.astype(np.float32)[:, :, None]
    out = base * (1 - a) + layer * a
    img = Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))
    img.info['geo'] = (xp, w)
    return img, tuple(int(v) for v in sky)


LOGO_DIR = os.path.join(DL, 'logolar-ters')


def put_logo(img, name, spec, kind='ters'):
    """Proje logosunu görselin gökyüzüne yerleştirir. spec: (fx, fy, fh) —
    fx: logonun sol kenarı, fotoğraf genişliğine oran (fotoğrafın kendi
    koordinatı; böylece logo binaya göre sabit durur); fy: üst kenar ve fh:
    yükseklik, banner yüksekliğine oran."""
    if not spec:
        return img
    fx, fy, fh = spec
    xp, w = img.info['geo']
    logo = Image.open(os.path.join(LOGO_DIR, 'logo-%s-%s.png' % (name, kind))).convert('RGBA')
    lh = round(img.height * fh)
    logo = logo.resize((round(logo.width * lh / logo.height), lh), Image.LANCZOS)
    out = img.convert('RGBA')
    x, y = round(xp + fx * w), round(img.height * fy)
    assert 0 <= x and x + logo.width <= img.width, 'logo kanvas dışında: %s' % name
    out.alpha_composite(logo, (x, y))
    res = out.convert('RGB')
    res.info['geo'] = img.info['geo']
    return res


def pad_top(im, frac, seam=0.10):
    """Görselin üstüne yüksekliğinin `frac` oranı kadar uzantı ekler. Uzantı
    her sütunun üst şerit tonundan türer, yatayda güçlüce yumuşatılır ve
    yukarı doğru tek tona kavuşur; ek yeri `seam` oranında yumuşak geçer.
    Aynalama ya da tekrar yok: ışıltı/nesne kopyalanmaz."""
    from PIL import ImageFilter
    w, h = im.size
    ph = round(h * frac)
    a = np.asarray(im.convert('RGB'), dtype=np.float32)
    band = a[: max(4, round(h * 0.04))].mean(0, keepdims=True)
    band_im = Image.fromarray(np.clip(band, 0, 255).astype(np.uint8)).resize((w, 1))
    band = np.asarray(band_im.filter(ImageFilter.GaussianBlur(w * 0.06)).resize((w, 1)), dtype=np.float32)
    flat = band.mean(1, keepdims=True)
    t = _smooth(np.arange(ph, dtype=np.float32)[::-1] / max(1, ph))[:, None, None]
    ext = band[None, 0] * (1 - t) + flat[None, 0] * t
    ext = np.broadcast_to(ext, (ph, w, 3)).astype(np.float32)
    out = np.concatenate([ext, a], 0)
    sh = round(h * seam)
    k = _smooth(np.arange(sh, dtype=np.float32) / sh)[:, None, None]
    out[ph: ph + sh] = out[ph: ph + sh] * k + band[None, 0] * (1 - k)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def crop(im, x0, x1, y0=0.0, y1=1.0):
    w, h = im.size
    return im.crop((round(w * x0), round(h * y0), round(w * x1), round(h * y1)))


def is_dark_bottom_left(im):
    """Sayfalama ve 'Projeyi İncele' bağlantısı sol altta: zemin koyuysa beyaz."""
    w, h = im.size
    r, g, b = im.crop((0, int(h * .7), int(w * .4), h)).resize((1, 1), Image.BOX).getpixel((0, 0))
    return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255 < 0.5


def save(im, name, q=82):
    m.save(m.sharpen(im) if im.width <= 2600 else im, name, q)


def build(name, tx, desk, dspec, main, mspec, mid_gap=GAP, logo=None, logo_kind='ters'):
    """logo: dict(desk=(fx, fy, fh), mid=(fx, fy, fh)) — ≥1200 px dosyalarına
    gömülür; ≤1199 px'te logo HTML'de metin kutularının başında (build_alt_a)."""
    logo = logo or {}
    """tx: metin kutusunun konteyner soluna göre sağ kenarı (CSS px)."""
    sx = 2 * (K_DESK + tx + GAP)
    big, sky = compose(desk, 5200, 1040, sx=sx, **dspec)
    big = put_logo(big, name, logo.get('desk'), logo_kind)
    save(big, 'banner-%s-5200x1040.jpg' % name, 80)
    mid, _ = compose(main, 3500, 1040, sx=2 * (K_MID + tx + mid_gap), **mspec)
    mid = put_logo(mid, name, logo.get('mid'), logo_kind)
    save(mid, 'banner-%s-o-3500x1040.jpg' % name, 80)
    tspec = dict(mspec, right=None)
    tab, _ = compose(main, 3200, 1040, **tspec)
    save(tab, 'banner-%s-t-3200x1040.jpg' % name, 80)
    mob, _ = compose(main, 1600, 480, **tspec)
    save(mob, 'banner-%s-m-1600x480.jpg' % name)
    # 1920 px ekranda görünen bölge: dosya x = 2*(CL - K) … ; CL = 390
    view = big.crop((2 * (K_DESK - 390), 0, 2 * (K_DESK - 390) + 3840, 1040))
    wd = round(desk.width * 1040 / desk.height)
    print('   %s: görsel 1920\'de %%%d, 2560\'ta %%%d; gök tonu #%02x%02x%02x; sol alt koyu = %s'
          % (name, 100 * wd / 3840, 100 * wd / 5120, *sky, is_dark_bottom_left(view)))
    return '#%02x%02x%02x' % sky


def main():
    colors = {}

    print('\n[banner] VSancaktepe Merkez')
    sun = m.mat('8', 'Vakifbank_Sancaktepe_Vaz_Aci_46_Sunset_Email_C.jpg')
    # tam kadraj: üst gökyüzü ve alt yol payı kırpılır, sağdaki ağaç payı daraltılır;
    # sol blok x=0.07'de başlar (odak). Sol kenar: gökyüzü 0–0.30, blok 0.30–0.78, yol 0.78–1
    # ana blok: orta + sağ blok (x≥0.385); orta blok 0.40'ta başlar
    colors['vsancaktepe'] = build(
        'vsancaktepe', 508,
        crop(sun, 0.0, 0.97, 0.09, 0.90),
        dict(subject=0.07, clean=((0.0, 0.29),),
             left=dict(mirror=0.0, zones=[(0.0, 0.30, 0.35), (0.30, 0.78, 0.07), (0.78, 1.0, 0.22)]),
             right=dict(mirror=0.06, zones=[(0.0, 0.12, 0.35), (0.12, 0.75, 0.14), (0.75, 1.0, 0.25)])),
        crop(sun, 0.385, 0.97, 0.09, 0.90),
        dict(subject=0.026, clean=((0.0, 0.29),),
             left=dict(mirror=0.0, zones=[(0.0, 0.30, 0.30), (0.30, 0.78, 0.026), (0.78, 1.0, 0.20)]),
             right=dict(mirror=0.06, zones=[(0.0, 0.12, 0.35), (0.12, 0.75, 0.14), (0.75, 1.0, 0.25)])),
        # logo: blokların üstündeki gökyüzünde, sol/orta bloğun sol kenarı hizasında
        logo=dict(desk=(0.07, 0.05, 0.14), mid=(0.03, 0.06, 0.13)))

    print('\n[banner] VYeniKonak (katalog render: iki kule)')
    vyk = Image.open(os.path.join(DL, 'vyk-katalog', 'vyk-saat-kulesi-kuleler-3548x1777.png')).convert('RGB')
    # yalnızca proje: kuleler, önlerindeki ağaç sırası ve gökyüzü (render'ın sağ
    # yarısı; Saat Kulesi kadraj dışı). Kuleler x 0.20–0.62, ağaçlar 0.84–1 satırları
    kule = crop(vyk, 0.50, 1.0, 0.27, 0.99)
    kspec = dict(subject=0.20, clean=((0.0, 0.64),),
                 left=dict(mirror=0.10, zones=[(0.0, 0.10, 0.35), (0.10, 0.84, 0.30), (0.84, 1.0, 0.30)]),
                 right=dict(mirror=0.10, zones=[(0.0, 1.0, 0.40)]))
    # logo: uzun kulenin sağındaki boş gökyüzünde, kule tepesi hizasında
    colors['vyenikonak'] = build('vyenikonak', 449, kule, kspec, kule, kspec,
                                 logo=dict(desk=(0.66, 0.12, 0.13), mid=(0.66, 0.12, 0.13)))

    print('\n[banner] Tablo Adalar (broşür genel görünüm)')
    tablo = Image.open(os.path.join(DL, 'tablo-genel-gorunum.png')).convert('RGB')
    # yüksek blok x=0.15'te başlar (odak), sağ blok 0.88'de biter; sol kenar gökyüzü 0–0.58
    colors['tablo-adalar'] = build(
        'tablo-adalar', 422,
        crop(tablo, 0.0, 1.0, 0.07, 0.96),
        dict(subject=0.15, clean=((0.0, 0.58),),
             left=dict(mirror=0.10, zones=[(0.0, 0.05, 0.35), (0.05, 1.0, 0.25)]),
             right=dict(mirror=0.08, zones=[(0.0, 0.30, 0.35), (0.30, 0.85, 0.20), (0.85, 1.0, 0.30)])),
        crop(tablo, 0.08, 0.92, 0.07, 0.96),
        dict(subject=0.083, clean=((0.0, 0.58),),
             left=dict(mirror=0.08, zones=[(0.0, 0.05, 0.30), (0.05, 1.0, 0.16)]),
             right=dict(mirror=0.05, zones=[(0.0, 0.30, 0.30), (0.30, 0.85, 0.10), (0.85, 1.0, 0.20)])),
        # logo: yüksek bloğun sağında, alçak bloğun üstündeki gökyüzünde; açık
        # camgöbeği gökte beyaz zayıf kaldığından orijinal renkli (lacivert)
        logo=dict(desk=(0.52, 0.09, 0.16), mid=(0.52, 0.09, 0.15)), logo_kind='renkli')

    print('\n[banner] Kurumsal Yönetim Derecelendirme (haber görseli, 9,48)')
    der = m.mat('3', 'DERECELENDİRME (1).jpg')
    # Kaynakta (yükseklik oranı): metin bandı 0.51'de biter, rakamlar 0.58–0.74,
    # podyum 0.75–0.90. Kesim 0.53–0.96; rakamlar dikeyde ortalansın diye üste
    # görselin kendi ışık tonundan pürüzsüz uzantı eklenir (pad_top, aynalama yok).
    # Sonuç satırları: uzantı 0–0.17, rakamlar ~0.26–0.58, podyum ~0.58–0.89.
    # 9 rakamı x=0.08'de başlar (odak); podyumun sol ucu görselin sol kenarında,
    # uzun şeffaf rampayla zemine karışır (rakam satırlarında rampa kısa: 9 net).
    # ana blok (1200–1599, tablet, telefon): defne dalı dışarıda, kadraj 8'den sonra biter
    pad = 0.087
    colors['derecelendirme'] = build(
        'derecelendirme', 700,
        pad_top(crop(der, 0.0, 1.0, 0.53, 0.96), pad / 0.43),
        dict(subject=0.08, clean=((0.0, 0.56), (0.91, 1.0)), strip=0.04,
             left=dict(mirror=0.0, zones=[(0.0, 0.20, 0.35), (0.20, 0.60, 0.07), (0.60, 1.0, 0.30)]),
             right=dict(mirror=0.0, zones=[(0.0, 1.0, 0.12)])),
        # ara kesim daha geniş açı: alt kenar 1.0, uzantı 0.13 → rakamlar %15 küçük,
        # 1200–1440 px'te 8 Hızlı Erişim sekmesinin altına girmez.
        # satırlar: uzantı 0–0.22, rakamlar ~0.30–0.57, podyum ~0.57–0.83
        pad_top(crop(der, 0.0, 0.66, 0.53, 1.0), 0.13 / 0.47),
        dict(subject=0.12, clean=((0.0, 0.56), (0.86, 1.0)), strip=0.04,
             left=dict(mirror=0.0, zones=[(0.0, 0.24, 0.35), (0.24, 0.60, 0.10), (0.60, 1.0, 0.32)]),
             right=dict(mirror=0.0, zones=[(0.0, 0.24, 0.30), (0.24, 0.60, 0.04), (0.60, 1.0, 0.15)])),
        mid_gap=12)

    with open(os.path.join(OUT, 'banner-colors.json'), 'w', encoding='utf-8') as f:
        json.dump(colors, f, indent=1)
    print('\n   banner-colors.json:', colors)


if __name__ == '__main__':
    main()
