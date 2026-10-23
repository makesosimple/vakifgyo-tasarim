/* ==========================================================================
   Vakıf GYO — Alternatif A · gyo.js

   vb.js kurumsal davranışları (sekme, akordeon, mega menü, banner, Başvuru
   Merkezi) karşılıyor. Bu dosya Vakıf GYO'ya özgü üç davranışı ekler:

     - Konut kredisi hesaplama: kurumsal .credit-cal arayüzü; tutar ve vade
       alanları kaydırıcılarla eş zamanlı, sonuç anüite formülüyle.
       Önyüz örneğidir: faiz oranı temsilî, servis bağlantısı yok.
     - Proje carousel'i: kurumsal .insurance-swiper yerine CSS scroll-snap;
       düğmeler bir kart genişliği kaydırır.
     - Satış ofisi arama formu: önyüz örneğinde gönderim yapılmaz.
   ========================================================================== */

(function () {
  'use strict';

  var $$ = function (sel, ctx) {
    return Array.prototype.slice.call((ctx || document).querySelectorAll(sel));
  };

  var TL = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var INT = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 });

  function digits(v) {
    return parseInt(String(v).replace(/[^\d]/g, ''), 10) || 0;
  }

  function clamp(v, min, max) {
    return Math.min(Math.max(v, min), max);
  }

  /* ------------------------------------------------------------------------
     EV KREDİSİ HESAPLAMA
     ------------------------------------------------------------------------ */
  $$('[data-gyo-credit]').forEach(function (root) {
    var amount = root.querySelector('[data-gyo-amount]');
    var amountRange = root.querySelector('[data-gyo-amount-range]');
    var term = root.querySelector('[data-gyo-term]');
    var termRange = root.querySelector('[data-gyo-term-range]');
    var rateEl = root.querySelector('[data-gyo-rate]');
    var out = root.querySelector('[data-gyo-installment]');
    var total = root.querySelector('[data-gyo-total]');
    var rate = parseFloat(rateEl.getAttribute('data-rate')) / 100;

    // Kaydırıcının dolu kısmı: kurumsal .ui-slider-pip-inrange sarısı
    function paint(range) {
      var p = (range.value - range.min) / (range.max - range.min) * 100;
      range.style.setProperty('--gyo-fill', p + '%');
    }

    function link(input, range, fmt) {
      range.addEventListener('input', function () {
        input.value = fmt(range.value);
        paint(range);
        calc();
      });
      input.addEventListener('change', function () {
        var v = clamp(digits(input.value), +range.min, +range.max);
        range.value = v;
        input.value = fmt(range.value);
        paint(range);
        calc();
      });
      paint(range);
    }

    function calc() {
      var p = +amountRange.value;
      var n = +termRange.value;
      var m = rate === 0 ? p / n : p * rate / (1 - Math.pow(1 + rate, -n));
      out.textContent = TL.format(m) + ' ₺';
      total.textContent = TL.format(m * n) + ' ₺';
    }

    link(amount, amountRange, function (v) { return INT.format(v); });
    link(term, termRange, function (v) { return String(v); });
    root.querySelector('[data-gyo-calc]').addEventListener('click', calc);
    calc();
  });

  /* ------------------------------------------------------------------------
     PROJE CAROUSEL'İ
     ------------------------------------------------------------------------ */
  $$('[data-gyo-rail]').forEach(function (rail) {
    var track = rail.querySelector('.swiper-wrapper');
    var section = rail.parentNode;
    var prev = section.querySelector('[data-gyo-prev]');
    var next = section.querySelector('[data-gyo-next]');
    if (!track || !prev || !next) { return; }

    function step() {
      var card = track.querySelector('.swiper-slide');
      return card ? card.getBoundingClientRect().width : track.clientWidth;
    }

    function sync() {
      var max = track.scrollWidth - track.clientWidth - 1;
      prev.disabled = track.scrollLeft <= 0;
      next.disabled = track.scrollLeft >= max;
      section.classList.toggle('gyo-rail--static', max <= 0);
    }

    prev.addEventListener('click', function () { track.scrollBy({ left: -step(), behavior: 'smooth' }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step(), behavior: 'smooth' }); });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  /* ------------------------------------------------------------------------
     HİSSE GRAFİĞİ — artı imleci + değer kutusu (Yatırımcı İlişkileri)
     Çizgi sunucuda SVG olarak çiziliyor; burada yalnızca hover katmanı.
     Fare, dokunma ve klavye (sol/sağ ok) ile en yakın haftaya oturur.
     ------------------------------------------------------------------------ */
  var DATE = new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });

  $$('[data-gyo-chart]').forEach(function (fig) {
    var series = fig.getAttribute('data-series').split(',').map(Number);
    var box = fig.getAttribute('data-box').split(',').map(Number);   // W,H,L,R,T,B
    var lo = +fig.getAttribute('data-lo');
    var hi = +fig.getAttribute('data-hi');
    var start = new Date(fig.getAttribute('data-start') + 'T00:00:00');
    var svg = fig.querySelector('svg');
    var cross = fig.querySelector('.gyo-chart__cross');
    var dot = fig.querySelector('.gyo-chart__dot');
    var tip = fig.querySelector('.gyo-chart__tip');
    var W = box[0], H = box[1], L = box[2], R = box[3], T = box[4], B = box[5];
    var n = series.length;
    var idx = n - 1;

    function px(i) { return L + (W - L - R) * i / (n - 1); }
    function py(v) { return T + (H - T - B) * (1 - (v - lo) / (hi - lo)); }

    function show(i) {
      idx = Math.max(0, Math.min(n - 1, i));
      var x = px(idx);
      var y = py(series[idx]);
      cross.setAttribute('x1', x);
      cross.setAttribute('x2', x);
      dot.setAttribute('cx', x);
      dot.setAttribute('cy', y);
      var d = new Date(start.getTime() + idx * 7 * 864e5);
      tip.textContent = DATE.format(d) + ' · ' + TL.format(series[idx]) + ' ₺';
      tip.hidden = false;
      var scale = svg.getBoundingClientRect().width / W;
      var left = Math.max(70, Math.min(svg.getBoundingClientRect().width - 70, x * scale));
      tip.style.left = left + 'px';
      fig.classList.add('is-hover');
    }

    function hide() {
      fig.classList.remove('is-hover');
      tip.hidden = true;
      dot.setAttribute('cx', px(n - 1));
      dot.setAttribute('cy', py(series[n - 1]));
    }

    function fromEvent(e) {
      var r = svg.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width * W;
      return Math.round((x - L) / (W - L - R) * (n - 1));
    }

    svg.addEventListener('pointermove', function (e) { show(fromEvent(e)); });
    svg.addEventListener('pointerdown', function (e) { show(fromEvent(e)); });
    svg.addEventListener('pointerleave', hide);

    svg.setAttribute('tabindex', '0');
    svg.addEventListener('focus', function () { show(idx); });
    svg.addEventListener('blur', hide);
    svg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') { e.preventDefault(); show(idx - 1); }
      if (e.key === 'ArrowRight') { e.preventDefault(); show(idx + 1); }
      if (e.key === 'Home') { e.preventDefault(); show(0); }
      if (e.key === 'End') { e.preventDefault(); show(n - 1); }
    });
  });

  /* ------------------------------------------------------------------------
     DAİRE TİPİ SEÇİCİ — kurumsal .tags düğmeleri sekme gibi çalışır
     ------------------------------------------------------------------------ */
  $$('[data-gyo-switcher]').forEach(function (root) {
    var tabs = $$('[data-gyo-switch]', root).filter(function (t) { return t.closest('[data-gyo-switcher]') === root; });

    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle('active', on);
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('data-gyo-switch')).hidden = !on;
      });
      if (focus) { tab.focus(); }
    }

    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var k = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (k) { e.preventDefault(); select(tabs[(i + k + tabs.length) % tabs.length], true); }
      });
    });
  });

  /* Galeri filtresi: önyüz örneğinde yalnızca seçili durum */
  $$('.gyo-gallery__filter').forEach(function (bar) {
    var btns = $$('.tag', bar);
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        btns.forEach(function (o) {
          o.classList.toggle('active', o === btn);
          o.setAttribute('aria-pressed', String(o === btn));
        });
      });
    });
  });

  /* ------------------------------------------------------------------------
     YATIRIMCI ÇANTASI — seçim sayısı, tümünü seç
     ------------------------------------------------------------------------ */
  $$('[data-gyo-bag]').forEach(function (form) {
    var items = $$('[data-gyo-bag-item]', form);
    var all = form.querySelector('[data-gyo-bag-all]');
    var btn = form.querySelector('[data-gyo-bag-btn]');
    var count = form.querySelector('[data-gyo-bag-count]');

    function sync() {
      var n = items.filter(function (i) { return i.checked; }).length;
      count.textContent = n;
      btn.disabled = n === 0;
      all.checked = n === items.length;
      all.indeterminate = n > 0 && n < items.length;
    }

    items.forEach(function (i) { i.addEventListener('change', sync); });
    all.addEventListener('change', function () {
      items.forEach(function (i) { i.checked = all.checked; });
      sync();
    });
    sync();
  });

  /* ------------------------------------------------------------------------
     ÖN TALEP FORMU — zorunlu alan denetimi, gönderim yok
     ------------------------------------------------------------------------ */
  $$('[data-gyo-form]').forEach(function (form) {
    var done = form.querySelector('.gyo-form__done');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var first = null;
      $$('[required]', form).forEach(function (f) {
        var ok = f.type === 'checkbox' ? f.checked : f.value.trim() !== '';
        f.setAttribute('aria-invalid', String(!ok));
        if (!ok && !first) { first = f; }
      });
      if (first) { first.focus(); return; }
      done.hidden = false;
    });
  });

  /* ------------------------------------------------------------------------
     MOBİL MENÜ — sayfa içi bağlantıya dokununca menü kapansın (proje sitesi)
     ------------------------------------------------------------------------ */
  var burger = document.getElementById('hamburgerMenu');
  $$('.header a[href^="#"]').forEach(function (a) {
    if (a.getAttribute('href') === '#' || a.closest('.megamenu')) { return; }
    a.addEventListener('click', function () {
      if (burger && burger.getAttribute('aria-expanded') === 'true') { burger.click(); }
    });
  });

  /* ------------------------------------------------------------------------
     ÖNYÜZ ÖRNEĞİ — formlar gönderilmez
     ------------------------------------------------------------------------ */
  $$('form[action="#"]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });
})();
