#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vakifgyo.com.tr mevcut site haritasini teklif formatinda (Quot) uretir.

    python _Template/docxpack.py unpack _Ornek/VakifKart_DesignDev_Efor_2026_08_05_1206.docx <build>
    python _build/build_sitemap.py <build> <logo.png>
    python _Template/docxpack.py pack <build> VakifGYO_SiteHaritasi_<tarih>.docx

Stil ve yardimcilar C:/Projects/Business/Quot/_Template/build_lorem.py'den gelir;
format kurallari icin C:/Projects/Business/Quot/CLAUDE.md.
"""
import os
import re
import shutil
import sys

sys.path.insert(0, "C:/Projects/Business/Quot/_Template")
from build_lorem import NS, para, bullets, pagebreak, cell, table, cover, GREEN, MINT  # noqa: E402

LOGO_CX, LOGO_CY = 2750000, 468800  # 7,64 x 1,30 cm (kapak hucresine sigacak sekilde)


# --------------------------------------------------------------------------
# Agac listesi: oge = "metin" ya da ("metin", [alt ogeler])
# 0. seviye ListeParagraf (stil numaralandirmasi), alt seviyeler numId=9 ("-")
# --------------------------------------------------------------------------
def nested(text, ilvl):
    return para(text, "ListeParagraf",
                f'<w:numPr><w:ilvl w:val="{ilvl}"/><w:numId w:val="9"/></w:numPr>')


def tree(items, level=0):
    out = []
    for it in items:
        text, kids = (it, []) if isinstance(it, str) else it
        out.append(para(text, "ListeParagraf") if level == 0 else nested(text, level - 1))
        if kids:
            out.append(tree(kids, level + 1))
    return "".join(out)


def simple_table(head, rows, widths, total=None, aligns=None):
    aligns = aligns or [None] * len(widths)
    n = len(widths)

    def border(i):
        return "right" if i < n - 1 else None

    out = [("head", [cell(h, widths[i], GREEN, border(i), aligns[i], True, "FFFFFF")
                     for i, h in enumerate(head)])]
    for r in rows:
        out.append(("body", [cell(v, widths[i], None, border(i), aligns[i])
                             for i, v in enumerate(r)]))
    if total:
        out.append(("total", [cell(v, widths[i], MINT, border(i), aligns[i], True, GREEN)
                              for i, v in enumerate(total)]))
    return table(5000, widths, out)


# --------------------------------------------------------------------------
# Icerik
# --------------------------------------------------------------------------
def body():
    p = []

    # ---- 1. Genel Bakis ---------------------------------------------------
    p.append(para("Genel Bakış", "KonuBal"))
    p.append(para(
        "Bu doküman, Vakıf GYO kurumsal web sitesinin (www.vakifgyo.com.tr) 9 Ekim 2026 "
        "tarihindeki bilgi mimarisini ortaya koymaktadır. Sayfa ağacı, sitenin kendi "
        "içerik yönetim altyapısından okunmuş ve her sayfa tek tek açılarak içeriği "
        "doğrulanmıştır. Çalışma, yeniden tasarım kapsamındaki şablon ve komponent "
        "planlamasına temel oluşturacaktır."))
    p.append(para("Sitenin kapsamı özetle aşağıdaki gibidir:"))
    p.append(bullets([
        "Türkçe menüde 73, İngilizce menüde 75 sayfa (iki dil ayrı sayfa ağaçlarıyla yönetiliyor).",
        "Menüde yer almayan 32 sayfa: proje microsite'ları, e-bülten sayıları, detay şablonları "
        "ve teknik sayfalar.",
        "18 portföy kaydı: 2 devam eden proje, 5 tamamlanan proje, 11 gayrimenkul yatırımı.",
        "102 Türkçe, 31 İngilizce haber; 2 yatırımcı duyurusu; 7 ödül haberi.",
        "Yatırımcı ilişkileri ve sürdürülebilirlik arşivlerinde yaklaşık 2.600 doküman.",
    ]))
    p.append(para("Ana Bölümler", "Heading1LessMargin"))
    W = [3600, 1500, 5098]
    p.append(simple_table(
        ["Bölüm", "Sayfa", "Öne Çıkan İçerik"],
        [
            ["Ana Sayfa", "1", "Animasyonlu şehir sahnesi, proje hotspot'ları, haber vitrini"],
            ["Kurumsal", "14", "Hakkımızda, yönetim kadrosu, organizasyon şeması, Bilgi Merkezi"],
            ["Portföy", "4 + 18", "Kategori sekmeleri ve 18 proje detay sayfası"],
            ["Yatırımcı İlişkileri", "32", "20 politika/prosedür, 6 doküman arşivi, duyurular"],
            ["Sürdürülebilirlik", "17", "Raporlar, yönetişim, paydaş katılımı, çevre yönetimi, KSS"],
            ["Haberler", "5", "Haberler, Duyurular, Ödüller"],
            ["Bize Ulaşın", "1", "İletişim formu, harita, iletişim bilgileri"],
        ],
        W, aligns=[None, "center", None]))
    p.append(para(""))
    p.append(para(
        "Sayfa sayıları ilgili bölümün giriş sayfasını ve menüde görünen alt sayfaları "
        "içerir; dinamik detay sayfaları (proje, haber) ayrıca belirtilmiştir."))

    # ---- 2. Ortak Alanlar -----------------------------------------------
    p.append(para("Ortak Alanlar", "KonuBal"))
    p.append(para("Header", "Heading1LessMargin"))
    p.append(bullets([
        "Vakıf GYO logosu (ana sayfaya bağlantı)",
        "Site içi arama kutusu",
        "Dil seçici (TR / EN)",
        "Hamburger menü: tam ekran, numaralı ana bölümler; üzerine gelindiğinde alt sayfalar "
        "listelenir (TR 6, EN 7 bölüm)",
    ]))
    p.append(para("İç Sayfa Çerçevesi", "Heading1LessMargin"))
    p.append(bullets([
        "Sol tarafta dikey ana bölüm menüsü",
        "Yeşil başlık etiketi ve italik sayfa açıklaması",
        "Bölüm içi kardeş sayfa menüsü (numaralı liste ya da sekme)",
        "Sağ üstte önceki / üst / sonraki / kapat sayfa gezgini butonları",
    ]))
    p.append(para("Footer", "Heading1LessMargin"))
    p.append(bullets([
        "Sosyal medya: LinkedIn, X, Facebook, Instagram",
        "İletişim telefonu: +90 (216) 285 94 00",
        "Bilgi Toplumu Hizmetleri (MKK e-Şirket bağlantısı)",
        "“VakıfBank Finans Grubu İştirakidir” (vakifbank.com.tr bağlantısı)",
    ]))
    p.append(para(
        "Mevcut sitede ayrı bir footer menüsü, çerez tercih bandı, KAP kısayolu ve "
        "site haritası sayfası bulunmamaktadır."))

    # ---- 3. Ana Navigasyon (TR) ------------------------------------------
    p.append(pagebreak())
    p.append(para("Ana Navigasyon (TR)", "KonuBal"))
    p.append(para("Ana başlıklar ve alt sayfalar aşağıdaki gibidir."))

    p.append(para("Ana Sayfa", "Heading1LessMargin"))
    p.append(tree([
        "Tam ekran animasyonlu şehir sahnesi (gündüz/gece, paralaks katmanlar)",
        ("Şehir silüetinde proje hotspot'ları", [
            "Bizimtepe Aydos, Cubes Ankara, İstanbul Uluslararası Finans Merkezi, "
            "Tablo Adalar, VSancaktepe Merkez",
        ]),
        "“Geleneğin Gücü, Geleceğin İnşası” sloganı",
        "Haber vitrini slider (5 vitrin haberi)",
        "“Satışı Devam Eden Projelerimiz” butonu",
        "Yatay ana menü (Kurumsal, Portföy, Yatırımcı İlişkileri, Güncel, "
        "Sürdürülebilirlik, Bize Ulaşın)",
    ]))

    p.append(para("Kurumsal", "Heading1LessMargin"))
    p.append(tree([
        "VakıfGYO — hakkımızda metni, yönetim politikası görseli, ISO sertifikaları, "
        "tanıtım videosu (YouTube)",
        "Kurumsal Yönetim — Yatırımcı İlişkileri altındaki sayfaya kısayol",
        "İK Politikamız — politika metni ve iş başvuru formu",
        ("Şirket Bilgileri — kendi içeriği gösterilmiyor, ilk alt sayfaya yönlendiriyor", [
            "Kuruluş, Ortaklık ve Sermaye Yapısı — şirket künyesi, ortaklık tablosu, KAP bağlantısı",
            "Yönetim Kurulu — 9 üye (fotoğraf, unvan, özgeçmiş)",
            "Üst Yönetim — 3 kişi (fotoğraf, unvan, özgeçmiş)",
            "Organizasyon Şeması — tek görsel (PNG)",
        ]),
        ("Bilgi Merkezi", [
            "GYO Sektörü",
            "Sıkça Sorulan Sorular — 2 grup akordeon (GYO Mevzuatı 14, Vakıf GYO 11 soru)",
            "Gizlilik ve Kişisel Verilerin Korunması — 3 PDF doküman",
            "Bilgi Toplumu Hizmetleri — MKK e-Şirket (dış bağlantı)",
        ]),
    ]))

    p.append(para("Portföy", "Heading1LessMargin"))
    p.append(para(
        "Giriş sayfası tüm projeleri yatay kaydırmalı kartlarla listeler; üç kategori "
        "sekmesi aynı karusel yapısını filtreler. Her proje kaydı ortak bir detay "
        "şablonunda açılır."))
    p.append(para("Devam Eden Projeler", "Balk4"))
    p.append(tree(["VSancaktepe Merkez", "VYeniKonak"]))
    p.append(para("Tamamlanan Projeler", "Balk4"))
    p.append(tree([
        "İstanbul Uluslararası Finans Merkezi (IFM)", "Cubes Ankara", "Tablo Adalar",
        "Bizimtepe Aydos", "Gaziantep Iconova",
    ]))
    p.append(para("Gayrimenkul Yatırımları", "Balk4"))
    p.append(tree([
        ("Proje", ["Medyan Kadıköy"]),
        ("Mülk", [
            "Şişli VakıfBank Ek Hizmet Binası", "Bizimtepe Aydos Ticari Üniteler",
            "Aliağa İş Merkezi", "Fatih İş Merkezi", "Kavaklıdere Dükkân",
            "VKütahya İş Merkezi",
        ]),
        ("Arsa", [
            "Ankara ENH Parselleri", "İzmir Konak", "İstanbul Sancaktepe", "Kocaeli Çayırova",
        ]),
    ]))
    p.append(para("Proje Detay Şablonu", "Balk4"))
    p.append(tree([
        "Kategori etiketi ve proje adı",
        "Açıklama metni (konum, ada/parsel, alan bilgileri)",
        "Fotoğraf galerisi",
        "Projeye ait gayrimenkul değerleme raporları (PDF listesi)",
        "Harita bağlantısı",
    ]))

    p.append(para("Yatırımcı İlişkileri", "Heading1LessMargin"))
    p.append(para("Kurumsal Yönetim", "Balk4"))
    p.append(para(
        "Politika yayın tarihleri PDF'i ve numaralı 20 kalemlik liste. Kalemlerin 13'ü "
        "HTML sayfa, 6'sı doğrudan PDF, biri doküman arşividir."))
    p.append(tree([
        "Esas Sözleşme (PDF)",
        "Kurumsal Yönetim İlkelerine Uyum Raporları (arşiv, 36 kayıt, 2008–2025)",
        "Kar Dağıtım Politikası",
        "Bilgilendirme Politikası",
        "Bağış ve Yardım Politikası",
        "Ücretlendirme Politikası",
        "Etik İlkeler (PDF)",
        "Müşteri Memnuniyet Politikası",
        "Sürdürülebilirlik Politikası (PDF)",
        "Tazminat Politikası",
        "İnsan Hakları ve Çalışan Hakları Politikası",
        "İş Sağlığı ve Güvenliği Politikası",
        "Yönetim Kurulu Toplantıları Prosedürü",
        "Çalışanların Yönetim Organlarına Katılımına İlişkin Prosedür",
        "Yönetim Kurulu Komitelerinin Görev Alanları ve Çalışma Esasları (PDF)",
        "Fırsat Eşitliği, Çeşitlilik ve Toplumsal Cinsiyet Eşitliği Politikası",
        "Kurumsal Sosyal Sorumluluk Politikası",
        "Bilgi Güvenliği Politikası",
        "KVKK Politikası (PDF)",
        "İklim ve Sürdürülebilirlik Riski Yönetim Politikası (PDF)",
    ]))
    p.append(para("Doküman Arşivleri ve Diğer Sayfalar", "Balk4"))
    p.append(tree([
        "Genel Kurul — davet, sonuç, sirküler, temettü ve sermaye artırımı dokümanları",
        "Sermaye Artırımı & Temettü Duyuruları",
        "Raporlar ve Yatırımcı Sunumları — finansal tablolar, faaliyet raporları, sunumlar",
        "Gayrimenkul Değerleme Raporları",
        "Sürekli Bilgilendirme Formu — SPK zorunlu bilgiler ve tablolar",
        "Özel Durum Açıklamaları",
        ("Duyurular — kart listesi (2 kayıt)", [
            "6102 Sayılı T.T.K. 198. Madde Bildirimleri (boş sayfa)",
            "Basın Açıklamaları (boş sayfa)",
        ]),
        "Yatırımcı İlişkileri İletişim — birim sorumluları ve iletişim bilgileri",
    ]))

    p.append(para("Sürdürülebilirlik", "Heading1LessMargin"))
    p.append(para(
        "Giriş sayfası kapak görseli, giriş metni ve numaralı alt sayfa menüsünden oluşur."))
    p.append(tree([
        "Kilometre Taşları",
        ("Raporlar ve Sertifikalar — PDF doküman ağacı", [
            "TSRS Raporları (2024, 2025)",
            "Sürdürülebilirlik İlkeleri Uyum Raporları (2020–2025)",
            "Entegre Faaliyet Raporları (2021–2023)",
            "Sertifikalar (ISO 9001, 10002, 14064, 27001)",
        ]),
        "Yönetişim Yapısı",
        "Stratejik Yaklaşım",
        ("Paydaş Katılımı", [
            "Paydaş Etkileşim Kanalları (tablo)",
            "Paydaş Çalıştayı",
            "Paydaş Geri Bildirim Anketi",
        ]),
        "Öncelikli Konular",
        ("Çevre Yönetimi", [
            "Enerji Yönetimi",
            "Su ve Atık Yönetimi",
            "Sera Gazı Emisyonları — karbon ayak izi doğrulama raporları (2021–2023)",
        ]),
        "Çevresel ve Sosyal Risk Yönetim Sistemi",
        "Kurumsal Sosyal Sorumluluk — giriş metni ve 7 KSS haber kartı",
        "Sürdürülebilirlik Endeksleri",
    ]))

    p.append(para("Haberler (Güncel)", "Heading1LessMargin"))
    p.append(para("Giriş sayfası son 3 haberi kart olarak gösterir."))
    p.append(tree([
        "Haberler — 102 kayıt (2016–2026); kategoriler: vitrin, haber, ödüller, sosyal",
        ("Duyurular — 2 kayıt", ["6102 Sayılı T.T.K. 198. Madde Bildirimleri (boş; Yatırımcı İlişkileri altındaki sayfanın kopyası)"]),
        "Ödüller — 7 kayıt (2018–2024)",
        "Haber Detay — başlık, tarih, görsel, metin, bölüm alt menüsü",
    ]))

    p.append(para("Bize Ulaşın", "Heading1LessMargin"))
    p.append(tree([
        ("İletişim formu", [
            "Konu: Yatırımcı İlişkileri, Müşteri Talep ve Önerileri, Müşteri Şikayetleri, "
            "Kiralama Talepleri (proje ve m² seçimi), Diğer",
            "Ad soyad, e-posta, telefon, mesaj",
            "KVKK aydınlatma onayı, İYS ve SMS doğrulama",
        ]),
        "Google Harita",
        "İletişim bilgileri (telefon, faks, adres)",
        "Müşteri Şikayetleri Yönetim Süreci bağlantısı",
    ]))

    # ---- 4. Menu disi sayfalar -------------------------------------------
    p.append(pagebreak())
    p.append(para("Menüde Yer Almayan Sayfalar", "KonuBal"))
    p.append(para(
        "Aşağıdaki sayfalar yayında olup menüden erişilemez; ana sayfa butonları, haber "
        "içerikleri, e-postalar ya da proje alan adları üzerinden açılır."))

    p.append(para("Satıştaki Projeler ve Microsite'lar", "Heading1LessMargin"))
    p.append(tree([
        ("Satışı Devam Eden Projelerimiz — ana sayfa butonundan açılan 4 proje kartı", [
            "VSancaktepe Merkez (vsancaktepe.com.tr)",
            "Cubes Ankara (cubesankara.com.tr)",
            "Tablo Adalar (tabloadalar.com.tr)",
            "VYeniKonak (vyenikonak.com.tr — ayrı site)",
        ]),
    ]))
    p.append(para(
        "İlk üç projenin alan adları aynı uygulamadaki microsite şablonuna yönlenir. "
        "Şablonun bölümleri:"))
    p.append(tree([
        "Hero slider (kampanya slaytları)",
        "Proje Hakkında",
        "Vaziyet Planı",
        "Daire Planları",
        "İlerleme Durumu",
        "Sanal Tur (harici 360° tur)",
        "Konum (özel stilli Google Harita)",
        "Tanıtım / reklam filmi, tanıtım broşürü (PDF)",
        "Satış ofisi telefonu (0850 210 10 02) ve Ön Talep Formu",
    ]))

    p.append(para("E-Bülten", "Heading1LessMargin"))
    p.append(para(
        "Tam ekran blok şablonda hazırlanmış 13 sayı; 2023 Nisan ile 2026/01 arası. "
        "Yatırımcı bültenleri ayrı sayılar olarak yayımlanıyor."))
    p.append(tree([
        "2023: Nisan, Temmuz, Eylül–Aralık",
        "2024: 01, 02, 03",
        "2025: 01, 02, 03; Yatırımcı 01, 02",
        "2026: 01; Yatırımcı 01",
    ]))

    p.append(para("Şablon ve Teknik Sayfalar", "Heading1LessMargin"))
    p.append(tree([
        "Haber Detay (TR) ve News Detail (EN)",
        "Arama Sonuçları (TR) ve Search Results (EN)",
        "Müşteri Şikayetleri Yönetim Süreci — Bize Ulaşın formundan bağlantılı",
        "Forms — microsite Ön Talep / Inquiry form konteyneri",
        "Message — teknik mesaj sayfası",
        "VBX Test — yayında kalmış İYS form denemesi",
        "Sosyal Medya Yarışma (2020) ve Dokümanlar — güncelliğini yitirmiş sayfalar",
    ]))

    # ---- 5. Ingilizce site ----------------------------------------------
    p.append(para("İngilizce Site (EN)", "KonuBal"))
    p.append(para(
        "İngilizce site aynı uygulama içinde, ayrı ve elle güncellenen bir sayfa ağacıdır. "
        "Yapı büyük ölçüde Türkçe ile aynıdır; farklar aşağıda listelenmiştir."))
    p.append(para("Yapısal Farklar", "Heading1LessMargin"))
    p.append(bullets([
        "Bilgi Merkezi (Information Center) İngilizcede ana bölümdür; Türkçede Kurumsal altındadır.",
        "Yalnızca İngilizcede bulunan sayfalar: Stock Performance (Foreks hisse widget'ı) ve "
        "Estimated Financial Effects of Risks and Opportunities.",
        "Proje microsite'ları ve e-bültenlerin İngilizce karşılığı yoktur.",
        "Ana sayfada “Satışı Devam Eden Projelerimiz” butonu yoktur.",
    ]))
    p.append(para("İçerik Farkları", "Heading1LessMargin"))
    p.append(bullets([
        "İngilizce haber sayısı 31; en güncel İngilizce haber Haziran 2024 tarihlidir.",
        "Portföy kayıtlarının adları ve açıklamaları İngilizce sitede de Türkçe görünmektedir.",
        "Announcements ve Investor Announcements sayfaları boştur.",
        "Reports and Certificates sayfası boş açılmaktadır; İngilizce dokümanlar veride mevcuttur.",
        "Doküman arşivlerinde dil ayrımı yoktur; Türkçe ve İngilizce dokümanlar aynı listede yer alır.",
        "Başlık uyumsuzlukları: “Sermaye Artırımı & Temettü Duyuruları” ↔ “Capital Increase & "
        "Annual Reports”; “Üst Yönetim” ↔ “Board of Directors”.",
    ]))

    # ---- 6. Dokuman arsivleri --------------------------------------------
    p.append(pagebreak())
    p.append(para("Doküman Arşivleri", "KonuBal"))
    p.append(para(
        "Yatırımcı ilişkileri arşivleri ortak bir doküman listesi bileşeni kullanır: yıl "
        "seçimi (2004–2026), bazı sayfalarda kategori filtresi, ana kayıt ve ekli alt "
        "dokümanlar. Yeni tasarımda en yoğun kullanılacak komponent budur."))
    W = [4298, 1300, 1300, 1700, 1600]
    C = "center"
    p.append(simple_table(
        ["Arşiv", "Kayıt", "Dosya", "Yıllar", "Filtre"],
        [
            ["Özel Durum Açıklamaları", "891", "1.350", "2008–2026", "Yıl"],
            ["Gayrimenkul Değerleme Raporları", "303", "303", "2014–2026", "Yıl"],
            ["Raporlar ve Yatırımcı Sunumları", "244", "305", "2004–2026", "Yıl, kategori"],
            ["Sermaye Artırımı & Temettü", "160", "288", "2010–2026", "Yıl"],
            ["Genel Kurul", "71", "244", "2004–2026", "Yıl, kategori"],
            ["Kurumsal Yönetim Uyum Raporları", "36", "36", "2008–2025", "Yıl"],
            ["Sürdürülebilirlik ve genel dokümanlar", "58", "58", "2020–2026", "Ağaç"],
        ],
        W, total=["TOPLAM", "1.763", "2.584", "", ""],
        aligns=[None, C, C, C, C]))
    p.append(para(""))
    p.append(para(
        "Dosya sayısı, ana kayıtlara ekli alt dokümanları (tutanak, hazır bulunanlar listesi, "
        "izahname vb.) içerir. Arşivlerdeki 212 dosyanın adında boşluk ve Türkçe karakter "
        "bulunmaktadır."))

    # ---- 7. Teknik yapi ---------------------------------------------------
    p.append(para("Teknik Yapı", "KonuBal"))
    p.append(bullets([
        "Site, tek sayfa uygulaması (SPA) olarak çalışır; "
        "içerik istemci tarafında şifreli servis yanıtlarından yüklenir.",
        "Tüm sayfalar tek adreste, hash ile adreslenir (ör. /#!kurumsal). Sunucu tarafında "
        "sayfa adresi, sayfa başına başlık/meta, robots.txt ve sitemap.xml bulunmamaktadır; "
        "arama motorları siteyi tek sayfa olarak görür.",
        "Dosyalar üç ayrı depoda tutulur: /files/, /files/new/ ve /client/webs/vakifgyo/.",
        "VSancaktepe, Cubes Ankara ve Tablo Adalar alan adları aynı uygulamanın microsite "
        "şablonuna yönlenir; VYeniKonak ayrı bir sitedir.",
        "Haber listesi 100 kayıtla sınırlıdır ve sayfalama yoktur; en eski 2 haber listede görünmez.",
    ]))

    # ---- 8. Tespitler ----------------------------------------------------
    p.append(para("Tespitler", "KonuBal"))
    p.append(para("Boş ya da Hatalı Sayfalar", "Heading1LessMargin"))
    p.append(bullets([
        "6102 Sayılı T.T.K. 198. Madde Bildirimleri (TR ve EN'de ikişer kopya) ve Basın "
        "Açıklamaları / Press Releases sayfaları boştur.",
        "Şirket Bilgileri / Corporate Information kendi metnini göstermeden ilk alt sayfaya "
        "yönlenir.",
        "İK Politikamız / Human Resources Policy ve site içi arama, otomatik tarayıcı testinde "
        "içerik döndürmemiştir; gerçek tarayıcıda doğrulanmalıdır.",
        "Cubes Ankara ve Tablo Adalar microsite'larında broşür ve sanal tur bağlantıları başka "
        "projelere gidiyor görünmektedir; doğrulanmalıdır.",
        "VBX Test sayfası yayındadır; 2020 tarihli yarışma sayfası güncelliğini yitirmiştir.",
    ]))
    p.append(para("Yazım ve Adres Hataları", "Heading1LessMargin"))
    p.append(bullets([
        "Sayfa adresleri: “poiltikasi”, “skayetleri”, Türkçe karakter içeren “kurumsal-yönetim-2”",
        "Başlıklar: “Stock Performace”, “Ethical Principals”, “Sürdürülebilirlik Endeksler”, "
        "“GYO Mezvuatı”, “Sürdürülebilirlik İlkeri Uyum Raporu”",
    ]))
    p.append(para("Erişilebilirlik", "Heading1LessMargin"))
    p.append(bullets([
        "Organizasyon şeması, yönetim politikası ve sürdürülebilirlik tablo/şemaları metin "
        "gömülü görsel olarak yayımlanmaktadır; ekran okuyucular ve mobil görünüm için "
        "HTML olarak yeniden kurulmalıdır.",
    ]))

    # ---- 9. Yeni site icin notlar -----------------------------------------
    p.append(para("Yeniden Tasarım İçin Notlar", "KonuBal"))
    p.append(bullets([
        "Hash yerine gerçek sayfa adresleri ve sayfa başına başlık/meta yapısı.",
        "KAP şirket sayfasına ve hisse performansına Türkçe sitede de menüden erişim.",
        "Tek bir doküman arşivi komponenti: yıl ve kategori filtresi, ekli alt dokümanlar, "
        "dil ayrımı, sayfalama.",
        "Portföy için tek detay şablonu; satıştaki projeler için microsite bölümlerini "
        "(daire planları, ilerleme durumu, sanal tur, ön talep formu) aynı şablona eklemek.",
        "Haber listesinde sayfalama ve kategori filtresi; boş duyuru sayfalarının birleştirilmesi.",
        "TR ve EN ağaçlarının eşitlenmesi.",
    ]))

    # ---- Ek: Sayfa adresleri ---------------------------------------------
    p.append(pagebreak())
    p.append(para("Ek: Ana Sayfa Adresleri (TR)", "KonuBal"))
    p.append(para(
        "Yeni sitede yönlendirme planı için mevcut adreslerin listesi. Tüm adresler "
        "https://www.vakifgyo.com.tr/ kökü altındadır."))
    W = [4600, 5598]
    rows = [
        ["Ana Sayfa", "/"],
        ["Kurumsal", "/#!kurumsal"],
        ["VakıfGYO", "/#!vakifgyo"],
        ["İK Politikamız", "/#!insan-kaynaklari"],
        ["Kuruluş, Ortaklık ve Sermaye Yapısı", "/#!kurulus-ortaklik-ve-sermaye-yapisi"],
        ["Yönetim Kurulu", "/#!yonetim-kurulu"],
        ["Üst Yönetim", "/#!ust-yonetim"],
        ["Organizasyon Şeması", "/#!organizasyon-semasi"],
        ["Bilgi Merkezi", "/#!bilgi-merkezi"],
        ["GYO Sektörü", "/#!gyo-sektoru"],
        ["Sıkça Sorulan Sorular", "/#!sikca-sorulan-sorular"],
        ["Gizlilik ve Kişisel Verilerin Korunması", "/#!gizlilik-ve-kisisel-verilerin-korunmasi"],
        ["Portföy", "/#!portfoy"],
        ["Devam Eden Projeler", "/#!devam-eden-projeler"],
        ["Tamamlanan Projeler", "/#!tamamlanan-projeler"],
        ["Gayrimenkul Yatırımları", "/#!gayrimenkul-yatirimlari"],
        ["Proje Detay", "/#!portfoy/<proje-kodu>"],
        ["Satışı Devam Eden Projelerimiz", "/#!proje"],
        ["Proje Microsite", "/#!proje-bilgi/<proje-kodu>"],
        ["Yatırımcı İlişkileri", "/#!yatirimci-iliskileri"],
        ["Kurumsal Yönetim", "/#!kurumsal-yonetim"],
        ["Genel Kurul", "/#!genel-kurul"],
        ["Sermaye Artırımı & Temettü Duyuruları", "/#!sermaye-artirimi"],
        ["Raporlar ve Yatırımcı Sunumları", "/#!raporlar-ve-yatirimci-sunumlari"],
        ["Gayrimenkul Değerleme Raporları", "/#!gayrimenkul-degerleme-raporlari"],
        ["Sürekli Bilgilendirme Formu", "/#!surekli-bilgilendirme-formu"],
        ["Özel Durum Açıklamaları", "/#!ozel-durum-aciklamalari"],
        ["Duyurular (Yatırımcı)", "/#!yatirimci-duyurular"],
        ["Yatırımcı İlişkileri İletişim", "/#!yatirimci-iliskileri-iletisim"],
        ["Sürdürülebilirlik", "/#!vakif-gyo-surdurulebilirlik"],
        ["Raporlar ve Sertifikalar", "/#!raporlar-ve-sertifikalar"],
        ["Kurumsal Sosyal Sorumluluk", "/#!kurumsal-sosyal-sorumluluk"],
        ["Haberler (Güncel)", "/#!guncel"],
        ["Haberler", "/#!haberler"],
        ["Haber Detay", "/#!haberdetay/<haber-kodu>"],
        ["Duyurular", "/#!duyurular"],
        ["Ödüller", "/#!oduller"],
        ["Bize Ulaşın", "/#!bize-ulasin"],
        ["Arama Sonuçları", "/#!aramasonuc"],
        ["İngilizce Ana Sayfa", "/#!en"],
    ]
    p.append(simple_table(["Sayfa", "Adres"], rows, W))
    return "".join(p)


def main():
    build, logo = sys.argv[1], sys.argv[2]
    docpath = os.path.join(build, "word", "document.xml")
    orig = open(docpath, encoding="utf-8").read()
    sects = re.findall(r"<w:sectPr\b.*?</w:sectPr>", orig, flags=re.S)
    if len(sects) != 2:
        sys.exit(f"HATA: 2 sectPr bekleniyordu, {len(sects)} bulundu.")
    sect1, sect2 = sects

    cov = cover(
        LOGO_CX, LOGO_CY,
        title="Vakifgyo.com.tr Site Haritası",
        items=[
            "Mevcut Site Bilgi Mimarisi (TR / EN)",
            "Menü Dışı Sayfalar ve Doküman Arşivleri",
            "Tespitler ve Yeniden Tasarım Notları",
        ],
        date="9 Ekim 2026",
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\r\n'
        f"<w:document {NS}><w:body>{cov}<w:p><w:pPr>{sect1}</w:pPr></w:p>"
        f"{body()}{sect2}</w:body></w:document>"
    )
    open(docpath, "w", encoding="utf-8", newline="").write(xml)
    shutil.copyfile(logo, os.path.join(build, "word", "media", "image1.png"))
    print(f"document.xml yeniden yazildi ({len(xml)} karakter)")


if __name__ == "__main__":
    main()
