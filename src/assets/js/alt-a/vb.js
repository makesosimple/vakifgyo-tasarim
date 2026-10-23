/* ==========================================================================
   VakıfKart — Alternatif A · vb.js

   Kurumsal markup, Bootstrap'in data-* sözleşmesini kullanıyor
   (data-toggle="collapse", data-toggle="tab", data-target, data-parent).
   Bootstrap ve jQuery bu projede yasak; bu dosya aynı sözleşmeyi vanilla JS
   ile karşılıyor ve üzerine kurumsal sitede eksik olan erişilebilirlik
   davranışlarını ekliyor:

     - aria-expanded / aria-selected durumlarının doğru yönetimi
     - sekmelerde ok tuşu gezinmesi (WAI-ARIA Tabs)
     - mega menüde Esc ile kapatma ve odak tuzağından kaçınma
     - hamburger menüde aria-expanded ve gövde kaydırma kilidi
   ========================================================================== */

(function () {
  'use strict';

  var $$ = function (sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  };

  /* ------------------------------------------------------------------------
     COLLAPSE — kurumsal akordeon
     <button data-toggle="collapse" data-target="#x" aria-controls="x">
     <div id="x" class="collapse" data-parent="#accordion-y">
     data-parent varsa aynı akordeondaki diğer paneller kapanır.
     ------------------------------------------------------------------------ */
  $$('[data-toggle="collapse"]').forEach(function (btn) {
    var sel = btn.getAttribute('data-target') || btn.getAttribute('href');
    var panel = sel && document.querySelector(sel);
    if (!panel) { return; }

    // Başlangıç durumunu DOM'dan oku, aria'yı ona göre kur
    var open = panel.classList.contains('show');
    btn.setAttribute('aria-expanded', String(open));
    btn.classList.toggle('collapsed', !open);

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var willOpen = !panel.classList.contains('show');

      // data-parent: tek seferde tek panel açık kalsın
      var parentSel = panel.getAttribute('data-parent');
      if (willOpen && parentSel) {
        var parent = document.querySelector(parentSel);
        if (parent) {
          $$('.collapse.show', parent).forEach(function (other) {
            if (other === panel) { return; }
            other.classList.remove('show');
            $$('[data-target="#' + other.id + '"]').forEach(function (b) {
              b.setAttribute('aria-expanded', 'false');
              b.classList.add('collapsed');
            });
          });
        }
      }

      panel.classList.toggle('show', willOpen);
      btn.setAttribute('aria-expanded', String(willOpen));
      btn.classList.toggle('collapsed', !willOpen);
    });
  });

  /* ------------------------------------------------------------------------
     TAB — kurumsal sekme çubuğu (.nav-tabs .nav-link + .tab-pane)
     Kurumsal markup role="tab" / aria-selected taşıyor; ok tuşu gezinmesini
     biz ekliyoruz (WCAG 2.1.1 ve WAI-ARIA Tabs deseni).
     ------------------------------------------------------------------------ */
  $$('[role="tablist"]').forEach(function (list) {
    var tabs = $$('[role="tab"]', list);
    if (!tabs.length) { return; }

    function panelOf(tab) {
      var sel = tab.getAttribute('href') || ('#' + tab.getAttribute('aria-controls'));
      try { return document.querySelector(sel); } catch (e) { return null; }
    }

    function select(tab, focus) {
      tabs.forEach(function (t) {
        var active = t === tab;
        t.classList.toggle('active', active);
        t.setAttribute('aria-selected', String(active));
        t.tabIndex = active ? 0 : -1;
        var p = panelOf(t);
        if (p) { p.classList.toggle('active', active); }
      });
      if (focus) { tab.focus(); }
    }

    tabs.forEach(function (tab, i) {
      if (tab.getAttribute('aria-selected') !== 'true') { tab.tabIndex = -1; }

      tab.addEventListener('click', function (e) {
        e.preventDefault();
        select(tab, false);
      });

      tab.addEventListener('keydown', function (e) {
        var next = null;
        if (e.key === 'ArrowRight' || e.key === 'ArrowDown') { next = tabs[(i + 1) % tabs.length]; }
        else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') { next = tabs[(i - 1 + tabs.length) % tabs.length]; }
        else if (e.key === 'Home') { next = tabs[0]; }
        else if (e.key === 'End') { next = tabs[tabs.length - 1]; }
        if (next) { e.preventDefault(); select(next, true); }
      });
    });
  });

  /* ------------------------------------------------------------------------
     HAMBURGER — mobil menü
     Kurumsal sözleşme: .header__dflex.mobile-menu paneli açıyor, body.open__menu
     gövde kaydırmasını kilitliyor, hamburger ikonu .svg--close'a dönüyor.
     Kurumsal sitede Esc ile kapatma yok; erişilebilirlik için ekliyoruz.
     ------------------------------------------------------------------------ */
  (function hamburger() {
    var btn = document.getElementById('hamburgerMenu');
    if (!btn) { return; }
    var dflex = btn.closest ? btn.closest('.header__dflex') : null;
    var scroll = document.querySelector('.header__scroll');
    var icon = btn.querySelector('span');
    if (!dflex || !scroll) { return; }

    scroll.id = scroll.id || 'headerScroll';
    btn.setAttribute('aria-expanded', 'false');
    btn.setAttribute('aria-controls', scroll.id);

    function setOpen(open) {
      btn.setAttribute('aria-expanded', String(open));
      dflex.classList.toggle('mobile-menu', open);
      document.body.classList.toggle('open__menu', open);
      if (icon) {
        icon.classList.toggle('svg--hamburger-menu', !open);
        icon.classList.toggle('svg--close', open);
      }
    }

    btn.addEventListener('click', function (e) {
      e.preventDefault();
      setOpen(btn.getAttribute('aria-expanded') !== 'true');
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') {
        setOpen(false);
        btn.focus();
      }
    });

    // Masaüstüne geçildiğinde açık kalmasın
    window.matchMedia('(min-width: 992px)').addEventListener('change', function (m) {
      if (m.matches) { setOpen(false); }
    });
  })();

  /* ------------------------------------------------------------------------
     MEGA MENÜ
     Masaüstünde hover ile açılır (kurumsal davranış), klavyede Enter/Space ile.
     Kurumsal sitede Esc ile kapanma yok — erişilebilirlik için ekliyoruz.
     ------------------------------------------------------------------------ */
  $$('.header__menu-item').forEach(function (item) {
    var link = item.querySelector('.header__menu-link');
    var menu = item.querySelector('.megamenu');
    if (!link || !menu) { return; }

    // Kurumsal CSS paneli `.megamenu.show` ile açıyor (display:block).
    function setOpen(open) {
      item.classList.toggle('open', open);
      menu.classList.toggle('show', open);
      link.setAttribute('aria-expanded', String(open));
      document.body.classList.toggle('megamenu-open', open);
    }

    function closeOthers() {
      $$('.header__menu-item.open').forEach(function (other) {
        if (other === item) { return; }
        other.classList.remove('open');
        var m = other.querySelector('.megamenu');
        var l = other.querySelector('.header__menu-link');
        if (m) { m.classList.remove('show'); }
        if (l) { l.setAttribute('aria-expanded', 'false'); }
      });
    }

    link.addEventListener('click', function (e) {
      e.preventDefault();
      var willOpen = link.getAttribute('aria-expanded') !== 'true';
      closeOthers();
      setOpen(willOpen);
    });

    // Masaüstünde kurumsal davranış: hover ile açılır.
    var desktop = window.matchMedia('(min-width: 992px)');
    item.addEventListener('mouseenter', function () {
      if (desktop.matches) { closeOthers(); setOpen(true); }
    });
    item.addEventListener('mouseleave', function () {
      if (desktop.matches) { setOpen(false); }
    });

    item.addEventListener('focusout', function (e) {
      if (!item.contains(e.relatedTarget)) { setOpen(false); }
    });

    item.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setOpen(false); link.focus(); }
    });
  });

  /* ------------------------------------------------------------------------
     MEGA MENÜ — mobil kategori akordeonu
     Masaüstünde alt menü hover ile açılıyor (kurumsal). Mobilde hover yok;
     kategoriye dokunmak kendi alt menüsünü açıyor.
     ------------------------------------------------------------------------ */
  (function megamenuMobile() {
    var narrow = window.matchMedia('(max-width: 991px)');

    $$('.megamenu__item').forEach(function (item) {
      var link = item.querySelector('.megamenu__item-link');
      var sub = item.querySelector('.megamenu__sub');
      if (!link || !sub) { return; }

      link.setAttribute('aria-expanded', 'false');

      link.addEventListener('click', function (e) {
        if (!narrow.matches) { return; }   // masaüstünde bağlantı olarak çalışsın
        e.preventDefault();
        var willOpen = !item.classList.contains('open');
        $$('.megamenu__item.open').forEach(function (other) {
          other.classList.remove('open');
          var l = other.querySelector('.megamenu__item-link');
          if (l) { l.setAttribute('aria-expanded', 'false'); }
        });
        item.classList.toggle('open', willOpen);
        link.setAttribute('aria-expanded', String(willOpen));
      });
    });
  })();

  /* ------------------------------------------------------------------------
     BAŞVURU MERKEZİ — kurumsal .banner__apply
     Kurumsal sitede jQuery animate ile açılıyor; burada .open sınıfı ve CSS
     geçişi. Kurumsalda Esc ile kapanma yok, erişilebilirlik için ekliyoruz.
     ------------------------------------------------------------------------ */
  $$('.banner__apply').forEach(function (box) {
    var open = box.querySelector('.banner__apply__closed');
    var close = box.querySelector('.banner__apply__opened__btn');
    if (!open) { return; }

    function setOpen(state) {
      box.classList.toggle('open', state);
      open.setAttribute('aria-expanded', String(state));
      if (state && close) { close.focus(); }
    }

    open.addEventListener('click', function () { setOpen(true); });
    if (close) {
      close.addEventListener('click', function () { setOpen(false); open.focus(); });
    }
    box.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && box.classList.contains('open')) {
        setOpen(false);
        open.focus();
      }
    });
  });

  /* ------------------------------------------------------------------------
     ARAMA KUTUSU
     Kurumsal .header__menu-item[data-module="SearchBox"] öğesi. Panel
     .open sınıfıyla açılıyor; Esc ile kapanıyor ve odak geri veriliyor.
     ------------------------------------------------------------------------ */
  // Masaüstünde navigasyondaki .vk-search, mobilde kurumsal .header__logo-mobile
  // aynı kalıbı taşıyor; ikisi de aynı davranışı alıyor.
  $$('.vk-search, .header__logo-mobile').forEach(function (box) {
    var open = box.querySelector('.header__menu-search');
    var close = box.querySelector('.svg--close');
    var input = box.querySelector('input[name="search"]');
    if (!open) { return; }

    // Kurumsal CSS paneli .header__search-content.open ile görünür yapıyor.
    var panel = box.querySelector('.header__search-content');

    function setOpen(state) {
      if (panel) { panel.classList.toggle('open', state); }
      open.setAttribute('aria-expanded', String(state));
      if (state && input) { input.focus(); }
    }

    open.addEventListener('click', function (e) {
      e.preventDefault();
      setOpen(open.getAttribute('aria-expanded') !== 'true');
    });

    if (close) {
      close.addEventListener('click', function () { setOpen(false); open.focus(); });
      close.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); setOpen(false); open.focus(); }
      });
    }

    box.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { setOpen(false); open.focus(); }
    });

    document.addEventListener('click', function (e) {
      if (!box.contains(e.target)) { setOpen(false); }
    });
  });

  /* ------------------------------------------------------------------------
     BANNER — kurumsal .banner / .swiper markup'ı
     Swiper kütüphanesi yerine minimal geçiş. Kurumsal HomeBanner modülünün
     sözleşmesi birebir korunuyor:
       - .swiper-pagination içindeki noktalar slayta gider
       - AKTİF nokta aynı zamanda oynat/duraklat düğmesidir (.play sınıfı)
       - aktif noktaya süre boyunca dönen ilerleme halkası (@keyframes stroke)
       - CTA tektir: .all-links > a#all-campaign-link, metni ve hedefi aktif
         slaytın data-cmg-text / data-cmg-href değerlerinden okunur
       - aktif slayt .white taşıyorsa .home-banner de .white alır
     Kurumsal sitede noktalar tıklanabilir <span>; klavyeyle erişilemiyor.
     Bizde <button>. Duraklatma kontrolü kurumsalda zaten var, WCAG 2.2.2
     bu sayede karşılanıyor; hareket azaltma tercihi varsa duraklatılmış başlar.
     ------------------------------------------------------------------------ */
  $$('[data-banner]').forEach(function (root) {
    var wrap = root.querySelector('.swiper-wrapper');
    var slides = $$('.swiper-slide', root);
    var dots = $$('.swiper-pagination-bullet', root);
    var cta = root.querySelector('#all-campaign-link');
    var status = root.parentNode.querySelector('[data-banner-status]');
    if (!wrap || slides.length < 2) { return; }

    var delay = parseInt(root.getAttribute('data-timeout'), 10) || 10000;
    // data-banner-fade: slaytlar kaymak yerine üst üste çapraz geçer (CSS)
    var fade = root.hasAttribute('data-banner-fade');
    var reduce = window.matchMedia('(prefers-reduced-motion: reduce)');
    var i = 0;
    var timer = null;
    var paused = reduce.matches;

    var RING = '<svg height="26" width="26" aria-hidden="true" focusable="false">' +
      '<circle class="circle" cx="13" cy="13" r="12" stroke-width="3" fill-opacity="0"></circle></svg>';
    // Kurumsal fill="#FFFFFF" sabit; açık zeminli slaytta üçgen görünmez
    // kalıyor. Renk CSS'e bırakıldı (bkz. 03-vk.css .play-icon).
    var PLAY = '<svg class="play-icon" xmlns="http://www.w3.org/2000/svg" ' +
      'width="24" height="24" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' +
      '<path d="M3 22v-20l18 10-18 10z"/></svg>';

    function label(n) { return (n + 1) + '. görsel'; }

    function paintActiveDot() {
      var d = dots[i];
      var sr = '<span class="sr-only">' + (paused ? 'Geçişi başlat' : 'Geçişi duraklat') + '</span>';
      d.classList.toggle('play', paused);
      d.innerHTML = sr + (paused ? PLAY : RING);
      if (!paused) {
        var c = d.querySelector('circle');
        c.style.animation = 'none';
        // reflow, animasyon baştan başlasın
        void c.getBoundingClientRect();
        c.style.animation = 'stroke ' + delay + 'ms linear';
      }
    }

    function show(n) {
      i = (n + slides.length) % slides.length;
      if (!fade) { wrap.style.transform = 'translateX(' + (-i * 100) + '%)'; }

      slides.forEach(function (sl, k) {
        var on = k === i;
        sl.classList.toggle('swiper-slide-active', on);
        // Görünmeyen slayt klavye sırasından ve ekran okuyucudan çıkar
        if (on) { sl.removeAttribute('aria-hidden'); }
        else { sl.setAttribute('aria-hidden', 'true'); }
        $$('a, button', sl).forEach(function (el) { el.tabIndex = on ? 0 : -1; });
      });

      // Kurumsal: aktif slaytın .white sınıfı banda taşınır
      root.classList.toggle('white', slides[i].classList.contains('white'));

      dots.forEach(function (d, k) {
        var on = k === i;
        d.classList.toggle('swiper-pagination-bullet-active', on);
        if (!on) { d.innerHTML = '<span class="sr-only">' + label(k) + '</span>'; }
      });
      paintActiveDot();

      if (cta) {
        var ds = slides[i].dataset;
        cta.classList.toggle('d-none', !ds.cmgText);
        cta.setAttribute('href', ds.cmgHref || '#');
        cta.querySelector('.text').textContent = ds.cmgText || '';
      }

      if (status) { status.textContent = (i + 1) + ' / ' + slides.length; }
    }

    function stop() { if (timer) { clearInterval(timer); timer = null; } }

    function start() {
      stop();
      if (paused) { return; }
      timer = setInterval(function () { show(i + 1); }, delay);
    }

    dots.forEach(function (d, n) {
      d.addEventListener('click', function () {
        if (n === i) {
          // Kurumsal davranış: aktif noktaya basınca oynat/duraklat
          paused = !paused;
          paintActiveDot();
          if (paused) { stop(); } else { start(); }
          return;
        }
        show(n);
        start();
      });
    });

    // Sekme arka plandayken boşuna dönmesin
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { stop(); } else { start(); }
    });

    show(0);
    start();
  });

  /* ------------------------------------------------------------------------
     Kaydırılabilir tabloya klavye erişimi (WCAG 2.1.1)
     ------------------------------------------------------------------------ */
  /* ------------------------------------------------------------------------
     İÇERİK SLAYTI — kurumsal .campaigns-swiper (Kartlarımız)
     Otomatik geçiş yok (kurumsal sayfada da kullanıcı ilerletir); noktalar
     <button>, görünmeyen slayt ekran okuyucudan ve klavye sırasından çıkar.
     ------------------------------------------------------------------------ */
  $$('[data-vk-swiper]').forEach(function (root) {
    var wrap = root.querySelector('.swiper-wrapper');
    var slides = $$('.swiper-slide', root);
    var dots = $$('.swiper-pagination-bullet', root);
    if (!wrap || slides.length < 2) { return; }
    function show(n) {
      wrap.style.transform = 'translateX(' + (-n * 100) + '%)';
      slides.forEach(function (sl, k) {
        var on = k === n;
        sl.classList.toggle('swiper-slide-active', on);
        if (on) { sl.removeAttribute('aria-hidden'); } else { sl.setAttribute('aria-hidden', 'true'); }
        $$('a, button', sl).forEach(function (el) { el.tabIndex = on ? 0 : -1; });
      });
      dots.forEach(function (d, k) {
        d.classList.toggle('swiper-pagination-bullet-active', k === n);
        if (k === n) { d.setAttribute('aria-current', 'true'); } else { d.removeAttribute('aria-current'); }
      });
    }
    dots.forEach(function (d, k) { d.addEventListener('click', function () { show(k); }); });
    show(0);
  });

  function syncScrollables() {
    $$('.vk-table-scroll').forEach(function (el) {
      if (el.scrollWidth > el.clientWidth + 1) {
        el.setAttribute('tabindex', '0');
        el.setAttribute('role', 'region');
      } else {
        el.removeAttribute('tabindex');
        el.removeAttribute('role');
      }
    });
  }
  syncScrollables();
  window.addEventListener('resize', syncScrollables);
})();
