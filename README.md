# Vakıf GYO — web sitesi tasarım prototipleri

Statik HTML prototipleri. Çalıştırmak için:

```
python -m http.server 8931 --directory src
```

| Klasör | Konsept |
|---|---|
| `src/alt-a` | A — VakıfBank tasarım sistemi birebir |
| `src/alt-a2` | A2 — A'nın geniş görselli varyantı |
| `src/alt-b` | B — bağımsız koyu tasarım, sol menü (`index-video.html`: 30. yıl filmi banner'lı ana sayfa) |
| `src/alt-b-ust` | B — üst menü |
| `src/alt-c` | C — deneysel ana sayfa (tipografi + video, borsa verileri, el çizimi harita) |

Her konseptte: ana sayfa, Yatırımcı İlişkileri, Hakkımızda, VSancaktepe Merkez ve Cubes Ankara proje sayfaları (C yalnız ana sayfa).

HTML dosyaları `_build/` altındaki Python betikleriyle üretilir (`build_alt_a.py`, `build_alt_a_pages.py`, `build_alt_a2.py`, `build_alt_b.py`, `build_alt_c.py`). Görsel ve video betikleri (`make_*.py`) depoda olmayan `gorseller/` klasöründeki ham malzemeyi kullanır.

Metinler yalnızca kaynak sitelerden alınır (`_docs/kaynak/`); denetim için `python _build/audit_kaynak.py . alt-b index`.
