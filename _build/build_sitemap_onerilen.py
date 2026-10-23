#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Vakifgyo.com.tr ONERILEN site haritasi (VakifBank.com.tr mantigiyla), teklif formatinda.

    python _Template/docxpack.py unpack _Ornek/VakifKart_DesignDev_Efor_2026_08_05_1206.docx <build>
    python _build/build_sitemap_onerilen.py <build> <logo.png>
    python _Template/docxpack.py pack <build> VakifGYO_OnerilenSiteHaritasi_<tarih>.docx
"""
import os
import re
import shutil
import sys

sys.path.insert(0, "C:/Projects/Business/Quot/_Template")
from build_lorem import NS, para, bullets, pagebreak, cover  # noqa: E402
from build_sitemap import tree, simple_table, LOGO_CX, LOGO_CY  # noqa: E402

SALE_PROJECTS = ["VSancaktepe Merkez", "VYeniKonak", "Tablo Adalar", "Cubes Ankara"]


def body():
    p = []

    # ---- 1. Yaklasim -----------------------------------------------------
    p.append(para("Yaklaşım", "KonuBal"))
    p.append(para(
        "Önerilen yapı, VakıfBank.com.tr'nin bilgi mimarisi ve sayfa mantığı esas alınarak "
        "hazırlanmıştır. Vakıf GYO'nun VakıfBank Finans Grubu içindeki yerini görsel ve "
        "yapısal olarak yansıtmak; ziyaretçinin grup sitelerinde aynı gezinme alışkanlığıyla "
        "ilerleyebilmesini sağlamak hedeflenmiştir."))
    p.append(para("Yapı üç katmandan oluşur:"))
    p.append(bullets([
        "Kurumsal site (vakifgyo.com.tr): Vakıf GYO'nun kurumsal, portföy ve sürdürülebilirlik içerikleri.",
        "Yatırımcı İlişkileri: kurumsal site içinde, kendi ana sayfası ve menü grupları olan bölüm.",
        "Proje siteleri: satıştaki her proje için kendi alan adından yayımlanan, kendi içinde "
        "bütünlüklü bağımsız siteler. Tümü ortak bir şablon setinden üretilir.",
    ]))
    p.append(para("VakıfBank.com.tr'den alınan ilkeler:"))
    p.append(bullets([
        "Kitle odaklı ana menü: VakıfBank'taki Bireysel / Ticari / Bankamız ayrımının karşılığı "
        "olarak konut alıcısı (Projeler), kiracı ve iş ortağı (Portföy), pay sahibi "
        "(Yatırımcı İlişkileri) ve kamuoyu (Kurumsal, Sürdürülebilirlik).",
        "Sütunlu mega menü ve her menüde sabit hızlı bağlantılar (VakıfBank'taki "
        "Başvurular / Hesaplama Araçları / Yardım Merkezi üçlüsünün karşılığı).",
        "Bölüm giriş (hub) sayfaları: alt sayfaları kart ızgarasıyla listeler.",
        "Ortak iç sayfa iskeleti: sayfa bandı, sol bölüm menüsü (sidebar), içerik alanı.",
        "Hiyerarşik ve okunabilir adresler (ör. /tr/yatirimci-iliskileri/kurumsal-yonetim/politikalar).",
    ]))
    p.append(para("Kapsam", "Heading1LessMargin"))
    p.append(para(
        "Çalışma önyüz tasarımı ve kodlamasını kapsar. Hesaplama araçları, hisse bilgisi, "
        "finansal takvim ve formlar önyüzde tam işlevli arayüzler olarak tasarlanır ve "
        "kodlanır; veri kaynağı, servis ve içerik yönetim sistemi bağlantıları kapsam "
        "dışındadır. Sayfa adları ve sıralaması öneri niteliğindedir; iş analizinde "
        "netleştirilecektir."))
    p.append(para("Komponent Dili", "Heading1LessMargin"))
    p.append(para(
        "Tüm sayfalar VakıfBank.com.tr'nin komponentleriyle kurulur: banner alanları, ikonlu "
        "hızlı erişim satırları, sekmeli araç blokları, tanıtım bantları, kart carousel'leri, "
        "sayfa bandı ve sol menülü iç sayfalar. VakıfBank'ta karşılığı olmayan ihtiyaçlar "
        "(daire planları, doküman arşivi gibi) aynı görsel dille ek komponent olarak tasarlanır."))
    p.append(para(
        "Mevcut ana sayfadaki tam ekran animasyonlu şehir sahnesi, paralaks katmanlar ve proje "
        "hotspot'ları yeni sitede yer almaz. Hareket VakıfBank ölçüsündedir: yalnızca hover, "
        "menü, sekme ve slider geçişleri; otomatik slider'larda duraklat kontrolü; videolar "
        "yalnızca kullanıcı başlattığında oynar."))

    # ---- 2. Header / Footer ---------------------------------------------
    p.append(para("Ortak Alanlar", "KonuBal"))
    p.append(para("Header", "Heading1LessMargin"))
    p.append(para("Üst Şerit", "Balk4"))
    p.append(bullets([
        "EN dil seçimi",
        "Hisse bilgisi: VKGYO fiyat ve günlük değişim (Hisse Senedi sayfasına bağlantı)",
        "KAP (şirket sayfası, yeni sekme)",
        "Satış ofisi telefonu: 0850 210 10 02",
    ]))
    p.append(para("Ana Bar", "Balk4"))
    p.append(tree([
        "Vakıf GYO logosu (ana sayfaya bağlantı)",
        ("Ana menü (mega menü)", [
            "Projeler", "Portföy", "Yatırımcı İlişkileri", "Kurumsal", "Sürdürülebilirlik",
        ]),
        ("Mega menüde sabit hızlı bağlantılar", [
            "Ön Talep Formu", "Konut Kredisi Hesaplama", "İletişim",
        ]),
        ("Site içi arama", [
            "Arama alanı açıldığında sık aranan bağlantılar listelenir: Satıştaki Projeler, "
            "Faaliyet Raporları, Özel Durum Açıklamaları, Genel Kurul",
        ]),
        ("Mobil", [
            "Hamburger menü, arama ve hızlı bağlantı ikonları (Ön Talep, Satış Ofisi, İletişim)",
        ]),
    ]))
    p.append(para("Footer", "Heading1LessMargin"))
    p.append(tree([
        "Logo, telefon ve sosyal medya (LinkedIn, X, Facebook, Instagram, YouTube)",
        "Site haritası sütunları: Projeler, Portföy, Yatırımcı İlişkileri, Kurumsal, Sürdürülebilirlik",
        ("Alt bağlantılar", [
            "Bilgi Toplumu Hizmetleri", "Gizlilik ve Kişisel Verilerin Korunması",
            "Çerez Tercihleri", "Erişilebilirlik", "Site Haritası",
        ]),
        ("Grup ve proje siteleri", ["VakıfBank"] + SALE_PROJECTS),
        "“VakıfBank Finans Grubu İştirakidir” ibaresi ve telif satırı",
    ]))

    # ---- 3. Ana Sayfa ------------------------------------------------------
    p.append(pagebreak())
    p.append(para("Ana Sayfa", "KonuBal"))
    p.append(para(
        "Ana sayfa, VakıfBank.com.tr ana sayfasının blok sırasıyla ve aynı komponentlerle "
        "kurgulanır. Mevcut sitedeki tam ekran animasyonlu şehir sahnesinin yerini banner "
        "alanı alır; sayfanın geri kalanı VakıfBank'taki bant ve kart dizisini izler."))
    W = [500, 2500, 4398, 2800]
    p.append(simple_table(
        ["#", "Blok", "Vakıf GYO İçeriği", "VakıfBank Komponenti"],
        [
            ["1", "Banner Alanı", "Kampanya, proje lansmanı ve kurumsal duyuru bannerları",
             "Banner slider"],
            ["2", "Hızlı Erişim", "Ön Talep, Konut Kredisi Hesaplama, Satış Ofisleri, Kiralama "
             "Talebi, Faaliyet Raporu, Özel Durum Açıklamaları", "Başvuru Merkezi"],
            ["3", "Araçlar ve Yatırımcı Bilgileri", "Sekmeler: Konut Kredisi Hesaplama, Hisse "
             "Bilgisi, Finansal Takvim", "Piyasa Bilgileri ve Hesaplama Araçları"],
            ["4", "Proje Rehberi", "İl, daire tipi ve teslim durumuna göre size uygun projeyi bulun",
             "Sarı Rehber"],
            ["5", "Öne Çıkan Proje Bandı", "Görsel, başlık, kısa metin ve iki buton "
             "(ör. VSancaktepe Merkez'de Yaşam Başlıyor)", "Emeklilik tanıtım bandı"],
            ["6", "Sürdürülebilirlik", "Kısa metin; Kilometre Taşları, Raporlar, Derecelendirme "
             "Notu bağlantıları", "Sürdürülebilir Bankacılık"],
            ["7", "Projelerimiz", "Satıştaki projelerin kart carousel'i; her kart proje sitesine gider",
             "Sigorta ürünleri carousel"],
            ["8", "Kurumsal Kartlar", "Yatırımcı İlişkileri ve Portföy tanıtım kartları",
             "Dijital Bankacılık / Ar-Ge kartları"],
            ["9", "Duyurular, Kiralık Alanlar, İnsan Kaynakları", "Üç sütunlu kısa bloklar",
             "Duyurular / Satılık Gayrimenkul / İnsan Kaynakları"],
            ["10", "30. Yıl Bandı", "Görsel, başlık, kısa metin; tanıtım filmi bağlantısı",
             "Özel Bankacılık bandı"],
            ["11", "Satış Ofisi Arama", "İl seçimiyle satış ofisi ve genel müdürlük listesi, harita",
             "Şube & ATM Arama"],
            ["12", "Yardım ve İletişim", "SSS, iletişim formu, telefon", "Yardım ve İletişim"],
        ],
        W, aligns=["center", None, None, None]))
    p.append(para(""))

    p.append(para("Blok Detayları", "Heading1LessMargin"))
    p.append(para("1. Banner Alanı", "Balk4"))
    p.append(tree([
        "VakıfBank banner ölçüsünde ve yerleşiminde: görsel + başlık, kısa metin ve buton kutusu",
        ("Banner içerikleri", [
            "Proje kampanyaları (ör. VSancaktepe teslime özel fırsatlar, Tablo Adalar 30. yıl indirimi)",
            "Proje lansmanları (ör. VYeniKonak)",
            "Kurumsal duyurular (ör. kurumsal yönetim derecelendirme notu, faaliyet raporu)",
        ]),
        "Başlık ve buton metni HTML; görselde metin bulunmaz",
        "Sayfa göstergesi, önceki / sonraki ve duraklat kontrolü",
    ]))
    p.append(para("2. Hızlı Erişim", "Balk4"))
    p.append(para(
        "VakıfBank'taki Başvuru Merkezi gibi ikonlu bağlantı satırı. Konut alıcısı ve "
        "yatırımcının en sık aradığı altı işleme tek tıkla ulaşım."))
    p.append(para("3. Araçlar ve Yatırımcı Bilgileri", "Balk4"))
    p.append(tree([
        "Konut Kredisi Hesaplama: proje ve daire tipi seçimi, tutar ve vade alanları, aylık taksit "
        "sonucu, ödeme planı ve VakıfBank SarıPanjur Ev Kredisi bağlantısı",
        "Hisse Bilgisi: VKGYO fiyatı, günlük değişim, işlem hacmi; Hisse Senedi sayfasına bağlantı",
        "Finansal Takvim: yaklaşan finansal sonuç, genel kurul ve temettü tarihleri",
    ]))
    p.append(para("4. Proje Rehberi", "Balk4"))
    p.append(para(
        "Sarı Rehber'deki soru-yanıt kurgusuyla: “Nerede ev arıyorsunuz?”, “Kaç oda?”, "
        "“Hemen taşınmak mı, yatırım mı?” sorularına göre uygun projeler listelenir."))
    p.append(para("5. ve 10. Tanıtım Bantları", "Balk4"))
    p.append(para(
        "VakıfBank'taki Emeklilik ve Özel Bankacılık bantlarının yerleşimi: büyük görsel, "
        "başlık, kısa metin ve butonlar. İçerik dönemsel olarak değiştirilebilir."))
    p.append(para("7. Projelerimiz", "Balk4"))
    p.append(tree([
        "Kart başına: proje görseli, proje logosu, ilçe / il, daire tipleri, durum etiketi",
        "Kart bağlantısı proje sitesine gider; carousel sonunda “Tüm Projeler”",
    ]))
    p.append(para("9, 11, 12. Kurumsal ve İletişim Blokları", "Balk4"))
    p.append(tree([
        "Duyurular: son 3 duyuru ve haber; “Tümü”",
        "Kiralık Alanlar: kısa metin ve kiralama talebi bağlantısı",
        "İnsan Kaynakları: kısa metin ve başvuru bağlantısı",
        "Satış Ofisi Arama: VakıfBank Şube & ATM aramasının yerleşimiyle il seçimi ve liste",
        "Yardım ve İletişim: SSS, iletişim formu, telefon",
    ]))

    # ---- 4. Ana Navigasyon -----------------------------------------------
    p.append(pagebreak())
    p.append(para("Ana Navigasyon", "KonuBal"))
    p.append(para(
        "Ana başlıklar ve alt sayfalar aşağıdaki gibi planlanmıştır. Her ana başlığın bir "
        "giriş (hub) sayfası vardır."))

    p.append(para("Projeler", "Heading1LessMargin"))
    p.append(para(
        "Konut alıcısına yönelik bölüm. Satıştaki projelerin kartları ilgili proje sitesine "
        "yönlendirir; satışı tamamlanmış projeler kurumsal site içindeki proje detay "
        "sayfasında yer alır."))
    p.append(tree([
        ("Satıştaki Projeler — filtrelenebilir proje listesi (il, daire tipi, durum)",
         [f"{n} → proje sitesi" for n in SALE_PROJECTS]),
        ("Devam Eden Projeler", ["VSancaktepe Merkez → proje sitesi", "VYeniKonak → proje sitesi"]),
        ("Tamamlanan Projeler", [
            "İstanbul Uluslararası Finans Merkezi", "Cubes Ankara → proje sitesi",
            "Tablo Adalar → proje sitesi", "Bizimtepe Aydos", "Gaziantep Iconova",
        ]),
        "Kampanyalar — tüm projelerin kampanyaları, liste ve detay",
        "Konut Kredisi Hesaplama",
        "Ön Talep Formu",
    ]))
    p.append(para("Proje Detay Sayfası (kurumsal site)", "Balk4"))
    p.append(tree([
        "Proje bandı, künye (konum, alan, konut sayısı, teslim yılı)",
        "Tanıtım metni ve galeri",
        "Konum haritası ve değerleme raporları",
    ]))

    p.append(para("Portföy", "Heading1LessMargin"))
    p.append(para("Kiracı, iş ortağı ve yatırımcıya yönelik gayrimenkul yatırımları bölümü."))
    p.append(tree([
        "Portföy Özeti — harita, kategori dağılımı ve portföy tablosu",
        ("Gayrimenkul Projeleri", ["Medyan Kadıköy"]),
        ("Mülkler", [
            "Şişli VakıfBank Ek Hizmet Binası", "Bizimtepe Aydos Ticari Üniteler",
            "Aliağa İş Merkezi", "Fatih İş Merkezi", "Kavaklıdere Dükkân", "VKütahya İş Merkezi",
        ]),
        ("Arsalar", [
            "Ankara ENH Parselleri", "İzmir Konak", "İstanbul Sancaktepe", "Kocaeli Çayırova",
        ]),
        "Kiralık Alanlar ve Kiralama Talebi",
    ]))
    p.append(para("Portföy Detay Sayfası", "Balk4"))
    p.append(tree([
        "Künye tablosu: konum, ada / parsel, yüzölçümü, kullanım, edinme yılı",
        "Açıklama metni ve galeri",
        "Harita",
        "Değerleme raporları (doküman listesi)",
    ]))

    p.append(para("Yatırımcı İlişkileri", "Heading1LessMargin"))
    p.append(para(
        "Kendi ana sayfası olan, menüsü konu gruplarına ayrılmış bölüm. Grup başlıkları "
        "mega menüde sütun olarak yer alır; ayrıntılı ağaç “Yatırımcı İlişkileri” "
        "başlığı altındadır."))

    p.append(para("Kurumsal", "Heading1LessMargin"))
    p.append(para("VakıfBank'taki Hakkımızda bölümünün karşılığı."))
    p.append(tree([
        "Vakıf GYO'yu Tanıyalım — hakkımızda, vizyon ve misyon, yönetim politikası, 30. yıl filmi",
        "GYO Sektörü",
        "Ödüller",
        ("Medya", ["Haberler", "E-Bülten", "Logolarımız ve Kurumsal Görseller"]),
        "İnsan Kaynakları — politika ve iş başvurusu",
        "İletişim — iletişim formu, adres, harita, müşteri şikayetleri yönetim süreci",
        "Gizlilik ve Kişisel Verilerin Korunması",
    ]))

    p.append(para("Sürdürülebilirlik", "Heading1LessMargin"))
    p.append(para("VakıfBank Sürdürülebilirlik bölümünün sıralaması esas alınmıştır."))
    p.append(tree([
        "Kilometre Taşları",
        "Yönetişim Yapısı",
        "Stratejik Yaklaşım",
        "Sürdürülebilirlik Rating ve Endeksleri",
        "Risk ve Fırsatların Finansal Etkileri",
        ("Paydaş Katılımı", [
            "Paydaş Etkileşim Kanalları", "Paydaş Çalıştayı", "Paydaş Geri Bildirim Anketi",
        ]),
        "Öncelikli Konular",
        ("Çevre Yönetimi", ["Enerji Yönetimi", "Su ve Atık Yönetimi", "Sera Gazı Emisyonları"]),
        "Çevresel ve Sosyal Risk Yönetim Sistemi",
        "Kurumsal Sosyal Sorumluluk",
        "Rapor ve Sertifikalar",
    ]))

    # ---- 5. Yatirimci Iliskileri -----------------------------------------
    p.append(pagebreak())
    p.append(para("Yatırımcı İlişkileri", "KonuBal"))
    p.append(para(
        "Yatırımcı İlişkileri, kurumsal sitenin içinde ama kendi ana sayfası olan bir bölüm "
        "olarak kurgulanır. İçerik yapısı, borsada işlem gören büyük şirketlerin yatırımcı "
        "ilişkileri sitelerindeki yaygın düzeni izler: yatırımcının en sık ihtiyaç duyduğu "
        "veri ve dokümanlar ilk ekranda, ayrıntılar konu gruplarında."))

    p.append(para("Yatırımcı İlişkileri Ana Sayfası", "Heading1LessMargin"))
    p.append(para(
        "İçerik blokları referans alınan yatırımcı ilişkileri yapısından; sayfa iskeleti ve "
        "komponentler VakıfBank.com.tr'den gelir."))
    W = [500, 2500, 4398, 2800]
    p.append(simple_table(
        ["#", "Blok", "İçerik", "VakıfBank Komponenti"],
        [
            ["1", "Sayfa Bandı", "Bölüm başlığı, kısa açıklama ve görsel", "Sayfa bandı (subpage banner)"],
            ["2", "Hızlı Erişim", "Faaliyet Raporu, Yatırımcı Sunumu, Finansal Tablolar, "
             "Özel Durum Açıklamaları, Genel Kurul, KAP", "Başvuru Merkezi"],
            ["3", "Hisse ve Özet Veriler", "Sekmeler: Hisse Bilgisi (VKGYO fiyat, değişim, hacim, "
             "grafik), Özet Veriler (toplam aktifler, portföy değeri, net aktif değer, net kâr, "
             "kira gelirleri)", "Piyasa Bilgileri ve Hesaplama Araçları"],
            ["4", "Son Finansal Sonuçlar", "Dönem etiketi; faaliyet raporu, finansal tablolar, "
             "yatırımcı sunumu; “Tümü”", "Tanıtım bandı"],
            ["5", "Finansal Takvim", "Finansal sonuç, genel kurul ve temettü tarihleri",
             "Duyurular listesi"],
            ["6", "Son Özel Durum Açıklamaları", "Son 3–5 açıklama; KAP bağlantısı; “Tümü”",
             "Duyurular listesi"],
            ["7", "Genel Kurul", "Son genel kurulun tarihi ve özeti; davet, tutanak, hazır "
             "bulunanlar", "Kart"],
            ["8", "Faaliyet Raporu ve Bilgi Notu", "Rapor kapağı ve PDF; tek sayfalık bilgi notu",
             "Kart"],
            ["9", "Yatırımcı Çantası", "Son dönemin temel dokümanlarını seçip indirme",
             "Ek komponent"],
            ["10", "Kurumsal Yönetim ve Sürdürülebilirlik", "Derecelendirme notu (9,48), BIST "
             "endeksleri, son TSRS raporu", "Sürdürülebilir Bankacılık bandı"],
            ["11", "Hizmetler", "İletişim, SSS, Yatırımcı E-Bülteni, Sözlük",
             "Yardım ve İletişim"],
        ],
        W, aligns=["center", None, None, None]))
    p.append(para(""))

    p.append(para("Yatırımcı İlişkileri Menüsü", "Heading1LessMargin"))
    p.append(tree([
        ("Vakıf GYO'ya Yatırım", [
            "Neden Vakıf GYO — yatırım teması, rakamlarla Vakıf GYO",
            "Kısaca Vakıf GYO ve Tarihçe",
            "Ortaklık Yapısı",
            "Yönetim Kurulu",
            "Komiteler",
            "Üst Yönetim",
            "Organizasyon Şeması",
            "GYO Sektörü ve Mevzuat",
        ]),
        ("Finansal Bilgiler", [
            "Finansal Sonuçlar — dönem bazlı arşiv",
            "Özet Finansallar ve Göstergeler",
            "Finansal Tablolar",
            "Faaliyet Raporları",
            "Entegre Faaliyet Raporları",
            "Yatırımcı Sunumları",
            "Portföy ve Gayrimenkul Değerleme Raporları",
            "Kâr Payı (Temettü) Bilgileri",
        ]),
        ("Açıklamalar ve Duyurular", [
            "Özel Durum Açıklamaları",
            "Yatırımcı Duyuruları — pay sahipleri bilgilendirme, TTK 198. madde bildirimleri",
            "Basın Açıklamaları",
        ]),
        ("Kurumsal Yönetim", [
            "Kurumsal Yönetim Yaklaşımımız",
            "Esas Sözleşme ve Ticaret Sicil Bilgileri",
            "Politikalar",
            "Kurumsal Yönetim Derecelendirme",
            "Kurumsal Yönetim İlkeleri Uyum Raporları",
            "Genel Kurul",
            "Sürekli Bilgilendirme Formu",
        ]),
        ("Hisse Bilgileri", [
            "Hisse Senedi Genel Bilgilendirme",
            "İnteraktif Hisse Grafiği",
            "Sermaye Artırımı ve Temettü Geçmişi",
        ]),
        "Finansal Takvim",
        "Sürdürülebilirlik (Sürdürülebilirlik bölümüne bağlantı)",
        ("Hizmetler", [
            "İletişim", "Sık Sorulan Sorular", "Yatırımcı E-Bülteni", "Sözlük",
        ]),
    ]))
    p.append(para(
        "Neden Vakıf GYO, Özet Finansallar, Bilgi Notu, Yatırımcı Çantası ve Sözlük mevcut "
        "sitede bulunmayan, yeni hazırlanacak içeriklerdir."))

    # ---- 6. Proje Siteleri ------------------------------------------------
    p.append(pagebreak())
    p.append(para("Proje Siteleri", "KonuBal"))
    p.append(para(
        "Satıştaki her proje, kendi alan adından yayımlanan bağımsız bir site olarak "
        "kurgulanır. Ziyaretçi proje sitesine ister kurumsal siteden ister doğrudan alan "
        "adından ya da bir kampanyadan gelsin, aynı header, menü ve footer ile karşılaşır; "
        "site kendi içinde tutarlıdır."))
    W = [3600, 3300, 3298]
    p.append(simple_table(
        ["Proje", "Alan Adı", "Durum"],
        [
            ["VSancaktepe Merkez", "vsancaktepe.com.tr", "Devam ediyor, satışta"],
            ["VYeniKonak", "vyenikonak.com.tr", "Devam ediyor, satışta"],
            ["Tablo Adalar", "tabloadalar.com.tr", "Tamamlandı, satışta"],
            ["Cubes Ankara", "cubesankara.com.tr", "Tamamlandı, satışta"],
        ],
        W))
    p.append(para(""))
    p.append(para("Tasarım İlkeleri", "Heading1LessMargin"))
    p.append(bullets([
        "Ortak şablon seti: dört proje aynı sayfa yapısını ve komponentleri kullanır; yeni "
        "bir proje sitesi içerik ve tema girilerek üretilir.",
        "Proje teması: logo, ana renk ve vurgu rengi projeye göre değişir (ör. VSancaktepe ve "
        "VYeniKonak'ta sarı “V” ailesi, Tablo Adalar'da lacivert ve turkuaz, Cubes Ankara'da "
        "mor); tipografi, ızgara ve komponentler kurumsal siteyle, yani VakıfBank.com.tr diliyle aynıdır.",
        "Tüm iç bağlantılar proje sitesinin kendi içinde kalır; Vakıf GYO'ya ve diğer projelere "
        "giden bağlantılar açıkça işaretlenir.",
        "Kurumsal sitedeki proje kartları proje sitesine yönlendirir; aynı içerik iki adreste "
        "yayımlanmaz.",
        "Vakıf GYO güvencesi her sayfada görünür: header'da “Bir Vakıf GYO Projesi” işareti, "
        "footer'da Vakıf GYO ve VakıfBank Finans Grubu ibaresi.",
    ]))

    p.append(para("Header ve Footer", "Heading1LessMargin"))
    p.append(tree([
        ("Header", [
            "Proje logosu (proje sitesi ana sayfasına bağlantı)",
            "Proje menüsü: Proje, Daire Planları, Galeri, Konum, İlerleme Durumu, Kampanyalar, İletişim",
            "Satış ofisi telefonu ve “Ön Talep” butonu",
            "“Bir Vakıf GYO Projesi” işareti (vakifgyo.com.tr bağlantısı)",
            "Mobilde sabit alt çubuk: Ara, WhatsApp, Ön Talep",
        ]),
        ("Footer", [
            "Satış ofisi adresi, çalışma saatleri, telefon, e-posta",
            "Proje sosyal medya hesapları",
            "Vakıf GYO'nun diğer projeleri",
            "Vakıf GYO logosu ve “VakıfBank Finans Grubu İştirakidir” ibaresi",
            "KVKK aydınlatma metni, çerez tercihleri, yasal uyarı (görseller temsilîdir)",
        ]),
    ]))

    p.append(para("Proje Sitesi Ana Sayfası (Landing)", "Heading1LessMargin"))
    p.append(para(
        "Proje sitesinin ana sayfası da VakıfBank ana sayfasının komponentleriyle kurulur; "
        "renkler ve logo proje temasından gelir."))
    W = [500, 2500, 4398, 2800]
    p.append(simple_table(
        ["#", "Blok", "İçerik", "VakıfBank Komponenti"],
        [
            ["1", "Banner Alanı", "Proje görselleri ve kampanyalar; başlık, kısa metin, "
             "“Ön Talep” butonu", "Banner slider"],
            ["2", "Hızlı Erişim", "Daire Planları, Galeri, Sanal Tur, Konum, Broşür, Ön Talep",
             "Başvuru Merkezi"],
            ["3", "Proje Özeti", "Kısa tanıtım; arsa alanı, konut sayısı, daire tipleri, "
             "teslim tarihi", "Tanıtım bandı"],
            ["4", "Daire Tipleri ve Hesaplama", "Sekmeler: Daire Tipleri (1+1 – 5+1, m², plan "
             "önizlemesi), Konut Kredisi Hesaplama", "Piyasa Bilgileri ve Hesaplama Araçları"],
            ["5", "Öne Çıkan Özellikler", "İkonlu özellikler: güneş panelleri, yağmur suyu, "
             "elektrikli araç istasyonu, yüzme havuzu", "Başvuru Merkezi ikon satırı"],
            ["6", "Sosyal Olanaklar", "Havuz, peyzaj, yürüyüş yolları, çocuk oyun alanı, "
             "ticari alanlar", "Kart carousel"],
            ["7", "Galeri", "Dış cephe, iç mekân, ortak alan seçkisi; tanıtım filmi", "Kart carousel"],
            ["8", "Kampanya Bandı", "Güncel kampanya; detay bağlantısı", "Emeklilik tanıtım bandı"],
            ["9", "İlerleme Durumu", "Son ayın şantiye videosu ve tarih; tüm aylar", "Tanıtım bandı"],
            ["10", "Konum ve Ulaşım", "Harita; metro, otoyol, hastane, okul mesafeleri",
             "Şube & ATM Arama yerleşimi"],
            ["11", "Ön Talep Formu", "Ad, telefon, e-posta, daire tipi, KVKK onayı", "Form"],
            ["12", "Vakıf GYO Güvencesi", "30 yıllık deneyim, diğer projeler, VakıfBank Finans Grubu",
             "Özel Bankacılık bandı"],
        ],
        W, aligns=["center", None, None, None]))
    p.append(para(""))

    p.append(para("Proje Sitesi Haritası", "Heading1LessMargin"))
    p.append(tree([
        "Ana Sayfa (landing)",
        ("Proje", [
            "Proje Hakkında", "Vaziyet Planı", "Sosyal Olanaklar", "Teknik Şartname",
        ]),
        ("Daire Planları", ["Daire tipi filtresi", "Plan detayı (büyütme, m² tablosu, kat bilgisi)"]),
        ("Galeri", ["Dış Cephe", "İç Mekân", "Ortak Alanlar", "Videolar"]),
        "Sanal Tur",
        "Konum",
        "İlerleme Durumu — aylık video ve fotoğraf arşivi",
        "Kampanyalar — liste ve detay",
        "Konut Kredisi Hesaplama",
        "Dokümanlar — tanıtım broşürü, değerleme raporları",
        "İletişim ve Ön Talep — satış ofisi, harita, form",
        "Yasal sayfalar — KVKK aydınlatma metni, çerez politikası",
    ]))
    p.append(para(
        "Tamamlanmış projelerde (Tablo Adalar, Cubes Ankara) İlerleme Durumu sayfası "
        "yerine “Yaşam” sayfası (tamamlanmış projeden fotoğraflar) kullanılabilir."))

    # ---- 7. Menu disi ---------------------------------------------------
    p.append(para("Menüde Yer Almayan Sayfalar", "KonuBal"))
    p.append(bullets([
        "Arama Sonuçları",
        "Haber Detay ve Kampanya Detay",
        "Form gönderim onay sayfaları (Ön Talep, İletişim, Kiralama, İş Başvurusu)",
        "Site Haritası",
        "404 Hata Sayfası (kurumsal site ve proje siteleri için ayrı)",
    ]))

    # ---- 8. Sablonlar -----------------------------------------------------
    p.append(pagebreak())
    p.append(para("Şablonlar", "KonuBal"))
    p.append(para(
        "Yapı aşağıdaki şablonlarla karşılanır. VakıfBank komponent kitaplığının "
        "karşılamadığı ihtiyaçlar ek komponent olarak tasarlanacaktır."))
    p.append(para("Kurumsal Site", "Heading1LessMargin"))
    W = [700, 3000, 4198, 2300]
    p.append(simple_table(
        ["#", "Şablon", "Kullanıldığı Sayfalar", "VakıfBank'ta"],
        [
            ["T01", "Ana Sayfa", "Ana sayfa", "Var"],
            ["T02", "Bölüm Giriş (Hub)", "Ana bölüm ve alt bölüm girişleri", "Var"],
            ["T03", "Statik İçerik", "Politikalar, tanıtım, sürdürülebilirlik sayfaları", "Var"],
            ["T04", "Proje Listeleme", "Satıştaki, devam eden, tamamlanan projeler", "Ek komponent"],
            ["T05", "Proje / Portföy Detay", "Tamamlanan projeler, mülkler, arsalar", "Ek komponent"],
            ["T06", "Yatırımcı İlişkileri Ana Sayfası", "Yatırımcı İlişkileri girişi", "Ek komponent"],
            ["T07", "Doküman Arşivi", "Özel durum, genel kurul, raporlar, değerleme", "Kısmen"],
            ["T08", "Kişi Listesi", "Yönetim Kurulu, Üst Yönetim", "Var"],
            ["T09", "Haber / Kampanya Listesi", "Haberler, Duyurular, Ödüller, Kampanyalar", "Var"],
            ["T10", "Haber / Kampanya Detay", "Tüm haber ve kampanya kayıtları", "Var"],
            ["T11", "Hisse Senedi", "Hisse bilgisi ve interaktif grafik", "Var"],
            ["T12", "Hesaplama Aracı", "Konut Kredisi Hesaplama", "Var"],
            ["T13", "SSS", "Sık Sorulan Sorular", "Var"],
            ["T14", "Form", "Ön Talep, İletişim, Kiralama, İş Başvurusu", "Var"],
            ["T15", "Arama Sonuçları / 404", "Sistem sayfaları", "Var"],
        ],
        W, aligns=["center", None, None, None]))
    p.append(para(""))
    p.append(para("Proje Siteleri", "Heading1LessMargin"))
    W = [700, 3000, 6498]
    p.append(simple_table(
        ["#", "Şablon", "Kullanıldığı Sayfalar"],
        [
            ["P01", "Proje Ana Sayfası", "Landing"],
            ["P02", "Proje İçerik Sayfası", "Proje Hakkında, Vaziyet Planı, Sosyal Olanaklar, "
             "Teknik Şartname, Konum"],
            ["P03", "Daire Planları", "Plan listesi ve plan detayı"],
            ["P04", "Galeri ve Sanal Tur", "Fotoğraf ve video galerileri, sanal tur"],
            ["P05", "İlerleme Durumu", "Aylık şantiye arşivi"],
            ["P06", "Kampanya Liste / Detay", "Proje kampanyaları"],
            ["P07", "İletişim ve Ön Talep", "Satış ofisi, form, onay sayfası"],
        ],
        W, aligns=["center", None, None]))
    p.append(para(""))
    p.append(para("Ek Komponentler", "Heading1LessMargin"))
    p.append(bullets([
        "Proje kartı (logo, konum, daire tipi, durum rozeti)",
        "Proje teması (logo ve renk token'ları ile proje bazlı görünüm)",
        "Daire planı görüntüleyici (tip filtresi, yakınlaştırma)",
        "İlerleme durumu zaman çizelgesi (ay bazlı video / fotoğraf)",
        "Künye tablosu (ada / parsel, yüzölçümü, kullanım)",
        "Doküman arşivi (yıl ve kategori filtresi, ekli alt dokümanlar, sayfalama)",
        "Yatırımcı çantası (doküman seçip birlikte indirme)",
        "Organizasyon şeması ve zaman çizelgesi (görsel yerine HTML)",
    ]))

    # ---- 9. Mevcut siteden farklar ---------------------------------------
    p.append(pagebreak())
    p.append(para("Mevcut Siteye Göre Değişiklikler", "KonuBal"))
    W = [3400, 3400, 3398]
    p.append(simple_table(
        ["Mevcut", "Önerilen", "Gerekçe"],
        [
            ["Tam ekran animasyonlu şehir sahnesi, paralaks, proje hotspot'ları",
             "Vitrin slider (görsel ve HTML metin), hızlı erişim, satıştaki projeler",
             "Performans, erişilebilirlik, içeriğin kolay güncellenmesi"],
            ["Portföy tek bölüm", "Projeler ve Portföy ayrı", "Konut alıcısı ile kiracı / yatırımcı ayrışır"],
            ["Proje microsite'ları kurumsal uygulamanın içinde",
             "Ortak şablon setinden bağımsız proje siteleri", "Her alan adında tutarlı deneyim"],
            ["VYeniKonak ayrı yapıda", "Diğer projelerle aynı şablon seti", "Tek tasarım dili"],
            ["Yatırımcı İlişkileri giriş sayfası yalnızca liste",
             "Veri ve doküman odaklı ana sayfa", "Yatırımcı ilk ekranda ihtiyacını bulur"],
            ["Bilgi Merkezi (Kurumsal altında)", "Dağıtıldı: SSS ve GYO Mevzuatı → Yatırımcı "
             "İlişkileri, GYO Sektörü → Kurumsal, KVKK → Kurumsal ve footer", "İçerik ilgili kitlenin yanında"],
            ["20 kalemlik politika listesi", "Politikalar sayfası", "Arama ve kategoriyle tek liste"],
            ["Haberler ana menüde", "Kurumsal › Medya; ana sayfada blok", "VakıfBank'taki konum"],
            ["Hisse sayfası yalnızca EN'de", "TR ve EN'de, üst şeritte fiyat", "Yatırımcıya doğrudan erişim"],
            ["KAP bağlantısı tek sayfada", "Üst şeritte ve açıklamalar sayfasında", "Görünürlük"],
            ["Boş Duyuru / Basın Açıklamaları / TTK 198 sayfaları",
             "Yatırımcı Duyuruları altında, kategori etiketiyle", "Boş sayfa kalmaz"],
            ["Risk ve Fırsatların Finansal Etkileri yalnızca EN'de", "TR ve EN'de",
             "Dil ağaçları eşit"],
            ["Hash adresler (/#!sayfa)", "Hiyerarşik adresler (/tr/bolum/sayfa)", "SEO ve paylaşılabilirlik"],
        ],
        W))

    # ---- 10. Acik konular -------------------------------------------------
    p.append(para(""))
    p.append(para("Netleştirilecek Konular", "Heading1NoUpperMargin"))
    p.append(bullets([
        "Proje sitelerinin İngilizce sürümü olacak mı?",
        "Kiralık alanlar listelenecek mi, yoksa yalnızca kiralama talep formu mu sunulacak?",
        "Yatırımcı ilişkileri için yeni içerikler (Neden Vakıf GYO, Özet Finansallar, Bilgi Notu, "
        "Sözlük) Vakıf GYO tarafından mı hazırlanacak?",
        "İngilizce kurumsal sitenin kapsamı: proje ve portföy içeriklerinin çevirisi.",
    ]))
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
        title="Vakifgyo.com.tr Önerilen Site Haritası",
        items=[
            "Kurumsal Site: Ana Sayfa ve Ana Navigasyon",
            "Yatırımcı İlişkileri Ana Sayfası",
            "Proje Siteleri Şablon Seti",
        ],
        date="13 Ekim 2026",
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
