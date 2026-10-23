/* ==========================================================================
   Vakıf GYO — Alternatif B · b.js

   Bağımlılık yok. Davranışlar:
     - Menü şeridi: masaüstünde alt menü paneli, mobilde tam ekran menü
     - Hero slayt: otomatik geçiş (durdurulabilir), klavye, dokunma
     - Proje dizini: satıra gelince büyük önizleme değişir
     - Bölüm gezgini: görünen bölüm vurgulanır
     - Hisse grafiği, daire tipi sekmeleri, galeri kaydırma,
       yatırımcı çantası, ödeme hesaplama, ön talep formu
   ========================================================================== */

(function () {
  'use strict';

  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };
  var root = document.documentElement;
  var desktop = window.matchMedia('(min-width: 1200px)');
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  var TL = new Intl.NumberFormat('tr-TR', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  var INT = new Intl.NumberFormat('tr-TR', { maximumFractionDigits: 0 });

  /* ------------------------------------------------------------------------
     MENÜ ŞERİDİ
     ------------------------------------------------------------------------ */
  var rail = document.querySelector('[data-b-rail]');
  if (rail) {
    var burger = rail.querySelector('[data-b-burger]');
    var btns = $$('.b-nav__btn[aria-controls]', rail);

    var closeFly = function (except) {
      btns.forEach(function (b) {
        if (b === except) { return; }
        b.setAttribute('aria-expanded', 'false');
        document.getElementById(b.getAttribute('aria-controls')).classList.remove('is-open');
      });
      if (!except) { root.classList.remove('b-has-fly'); }
    };

    btns.forEach(function (b) {
      var panel = document.getElementById(b.getAttribute('aria-controls'));
      b.addEventListener('click', function () {
        var open = b.getAttribute('aria-expanded') !== 'true';
        closeFly(b);
        b.setAttribute('aria-expanded', String(open));
        panel.classList.toggle('is-open', open);
        root.classList.toggle('b-has-fly', open && desktop.matches);
        if (open && desktop.matches) {
          var first = panel.querySelector('a');
          if (first && b.dataset.kbd === '1') { first.focus(); }
        }
        b.dataset.kbd = '';
      });
      b.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { b.dataset.kbd = '1'; }
      });
    });

    var setMenu = function (open) {
      rail.classList.toggle('is-open', open);
      burger.setAttribute('aria-expanded', String(open));
      burger.querySelector('.sr-only').textContent = open ? 'Menüyü kapat' : 'Menü';
      root.classList.toggle('b-lock', open);
      if (!open) { closeFly(); }
    };
    burger.addEventListener('click', function () { setMenu(!rail.classList.contains('is-open')); });

    document.addEventListener('keydown', function (e) {
      if (e.key !== 'Escape') { return; }
      var openBtn = btns.filter(function (b) { return b.getAttribute('aria-expanded') === 'true'; })[0];
      if (openBtn && desktop.matches) { closeFly(); openBtn.focus(); return; }
      if (rail.classList.contains('is-open')) { setMenu(false); burger.focus(); }
    });
    document.addEventListener('click', function (e) {
      if (desktop.matches && !rail.contains(e.target)) { closeFly(); }
    });
    // Sayfa içi bağlantı: mobil menü kapanır
    $$('a[href^="#"]', rail).forEach(function (a) {
      a.addEventListener('click', function () { if (rail.classList.contains('is-open')) { setMenu(false); } });
    });
    desktop.addEventListener('change', function () { setMenu(false); });

    // Mobil üst çubuk: görselin üstünde saydam, kaydırınca koyu
    var solid = function () { rail.classList.toggle('is-solid', window.scrollY > window.innerHeight * 0.6); };
    window.addEventListener('scroll', solid, { passive: true });
    solid();

    // Proje sitesi: menüde görünen bölüm vurgulanır
    var anchors = $$('.b-nav--anchors a', rail);
    if (anchors.length && 'IntersectionObserver' in window) {
      spy(anchors, 'is-active');
    }
  }

  function spy(links, cls) {
    var map = {};
    links.forEach(function (a) {
      var t = document.getElementById(a.getAttribute('href').slice(1));
      if (t) { map[t.id] = a; }
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) { return; }
        links.forEach(function (a) { a.classList.remove(cls); a.removeAttribute('aria-current'); });
        var a = map[en.target.id];
        if (a) {
          a.classList.add(cls);
          a.setAttribute('aria-current', 'true');
          var bar = a.closest('ul');
          if (bar && bar.scrollWidth > bar.clientWidth) {
            bar.scrollTo({ left: a.offsetLeft - 24, behavior: calm.matches ? 'auto' : 'smooth' });
          }
        }
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* ------------------------------------------------------------------------
     BÖLÜM GEZGİNİ
     ------------------------------------------------------------------------ */
  $$('[data-b-subnav]').forEach(function (nav) {
    if ('IntersectionObserver' in window) { spy($$('a', nav), 'is-active'); }
  });

  /* ------------------------------------------------------------------------
     HERO SLAYT — 7 sn, üstüne gelince / odakta durur. Kontrol yalnızca
     ileri/geri okları (müşteri isteği); ekran okuyucuya slayt no. duyurulur.
     ------------------------------------------------------------------------ */
  $$('[data-b-hero]').forEach(function (hero) {
    var slides = $$('.b-slide', hero);
    var status = hero.querySelector('[data-b-status]');
    var DUR = 7000;
    var i = 0;
    var timer = null;
    var userPaused = calm.matches;
    var hover = false;

    hero.style.setProperty('--dur', DUR / 1000 + 's');

    function go(n) {
      var prev = i;
      i = (n + slides.length) % slides.length;
      slides.forEach(function (s, k) {
        var on = k === i;
        s.classList.toggle('is-active', on);
        if (on) { s.removeAttribute('aria-hidden'); } else { s.setAttribute('aria-hidden', 'true'); }
        $$('a', s).forEach(function (a) { if (on) { a.removeAttribute('tabindex'); } else { a.setAttribute('tabindex', '-1'); } });
        var img = s.querySelector('img');
        if (on && img && img.loading === 'lazy') { img.loading = 'eager'; }
      });
      if (status && prev !== i) { status.textContent = (i + 1) + ' / ' + slides.length; }
      // b-gl.js (WebGL geçiş) dinler
      if (prev !== i) { hero.dispatchEvent(new CustomEvent('b-slide', { detail: { from: prev, to: i } })); }
      // Bir sonraki slaydın görselini önceden yükle
      var nx = slides[(i + 1) % slides.length].querySelector('img');
      if (nx && nx.loading === 'lazy') { nx.loading = 'eager'; }
      if (prev !== i) { restart(); }
    }

    function restart() {
      clearTimeout(timer);
      var playing = !userPaused && !hover && !document.hidden;
      hero.classList.toggle('is-playing', playing);
      if (playing) { timer = setTimeout(function () { go(i + 1); }, DUR); }
    }

    hero.querySelector('[data-b-next]').addEventListener('click', function () { go(i + 1); });
    hero.querySelector('[data-b-prev]').addEventListener('click', function () { go(i - 1); });
    hero.addEventListener('mouseenter', function () { hover = true; restart(); });
    hero.addEventListener('mouseleave', function () { hover = false; restart(); });
    hero.addEventListener('focusin', function () { hover = true; restart(); });
    hero.addEventListener('focusout', function (e) { if (!hero.contains(e.relatedTarget)) { hover = false; restart(); } });
    document.addEventListener('visibilitychange', restart);

    hero.addEventListener('keydown', function (e) {
      if (e.target.closest('.b-hero__ui') === null) { return; }
      if (e.key === 'ArrowRight') { e.preventDefault(); go(i + 1); }
      if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1); }
    });

    // Dokunma: yatay kaydırma
    var x0 = null;
    hero.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
    hero.addEventListener('touchend', function (e) {
      if (x0 === null) { return; }
      var dx = e.changedTouches[0].clientX - x0;
      if (Math.abs(dx) > 50) { go(dx < 0 ? i + 1 : i - 1); }
      x0 = null;
    });

    restart();
  });

  /* ------------------------------------------------------------------------
     PROJE DİZİNİ — fare ya da klavye odağı önizlemeyi değiştirir
     ------------------------------------------------------------------------ */
  $$('[data-b-index]').forEach(function (idx) {
    var rows = $$('.b-index__row', idx);
    var imgs = $$('.b-index__img', idx);
    function show(key) {
      rows.forEach(function (r) { r.classList.toggle('is-active', r.getAttribute('data-b-key') === key); });
      imgs.forEach(function (im) { im.classList.toggle('is-active', im.getAttribute('data-b-key') === key); });
    }
    rows.forEach(function (r) {
      var key = r.getAttribute('data-b-key');
      r.addEventListener('mouseenter', function () { show(key); });
      r.addEventListener('focusin', function () { show(key); });
    });
    // Önizleme görselleri ilk etkileşimden önce yüklensin
    var warm = function () { imgs.forEach(function (im) { im.loading = 'eager'; }); idx.removeEventListener('mouseenter', warm); };
    idx.addEventListener('mouseenter', warm);
  });

  /* ------------------------------------------------------------------------
     HİSSE GRAFİĞİ — artı imleci + değer kutusu
     ------------------------------------------------------------------------ */
  var DATE = new Intl.DateTimeFormat('tr-TR', { day: 'numeric', month: 'long', year: 'numeric' });
  $$('[data-b-chart]').forEach(function (fig) {
    var series = fig.getAttribute('data-series').split(',').map(Number);
    var box = fig.getAttribute('data-box').split(',').map(Number);
    var lo = +fig.getAttribute('data-lo');
    var hi = +fig.getAttribute('data-hi');
    var start = new Date(fig.getAttribute('data-start') + 'T00:00:00');
    var svg = fig.querySelector('svg');
    var cross = fig.querySelector('.b-chart__cross');
    var dot = fig.querySelector('.b-chart__dot');
    var tip = fig.querySelector('.b-chart__tip');
    var W = box[0], H = box[1], L = box[2], R = box[3], T = box[4], B = box[5];
    var n = series.length;
    var idx = n - 1;
    var px = function (k) { return L + (W - L - R) * k / (n - 1); };
    var py = function (v) { return T + (H - T - B) * (1 - (v - lo) / (hi - lo)); };

    function show(k) {
      idx = Math.max(0, Math.min(n - 1, k));
      var x = px(idx);
      cross.setAttribute('x1', x); cross.setAttribute('x2', x);
      dot.setAttribute('cx', x); dot.setAttribute('cy', py(series[idx]));
      tip.textContent = DATE.format(new Date(start.getTime() + idx * 7 * 864e5)) + ' · ' + TL.format(series[idx]) + ' ₺';
      tip.hidden = false;
      var w = svg.getBoundingClientRect().width;
      tip.style.left = Math.max(90, Math.min(w - 90, x * w / W)) + 'px';
      fig.classList.add('is-hover');
    }
    function hide() {
      fig.classList.remove('is-hover');
      tip.hidden = true;
      dot.setAttribute('cx', px(n - 1)); dot.setAttribute('cy', py(series[n - 1]));
    }
    function fromEvent(e) {
      var r = svg.getBoundingClientRect();
      return Math.round(((e.clientX - r.left) / r.width * W - L) / (W - L - R) * (n - 1));
    }
    svg.addEventListener('pointermove', function (e) { show(fromEvent(e)); });
    svg.addEventListener('pointerdown', function (e) { show(fromEvent(e)); });
    svg.addEventListener('pointerleave', hide);
    svg.setAttribute('tabindex', '0');
    svg.addEventListener('focus', function () { show(idx); });
    svg.addEventListener('blur', hide);
    svg.addEventListener('keydown', function (e) {
      var k = { ArrowLeft: idx - 1, ArrowRight: idx + 1, Home: 0, End: n - 1 }[e.key];
      if (k !== undefined) { e.preventDefault(); show(k); }
    });
  });

  /* ------------------------------------------------------------------------
     DAİRE TİPİ SEKMELERİ
     ------------------------------------------------------------------------ */
  /* Daire planı noktaları: dokunmada açılır, dışarı dokununca kapanır; tablo satırıyla eşleşir */
  $$('.b-plan').forEach(function (plan) {
    var $ = function (sel, ctx) { return (ctx || document).querySelector(sel); };
    var spots = $$('[data-b-spot]', plan);
    var rows = $$('[data-b-room]', plan);
    function row(id) { return rows.filter(function (r) { return r.getAttribute('data-b-room') === id; })[0]; }
    function clear() {
      spots.forEach(function (s) { s.classList.remove('is-on'); });
      rows.forEach(function (r) { r.classList.remove('is-on'); });
    }
    spots.forEach(function (s) {
      var id = s.getAttribute('data-b-spot');
      s.addEventListener('click', function (e) {
        e.stopPropagation();
        var on = s.classList.contains('is-on');
        clear();
        if (!on) { s.classList.add('is-on'); var r = row(id); if (r) { r.classList.add('is-on'); } }
      });
      s.addEventListener('mouseenter', function () { var r = row(id); if (r) { r.classList.add('is-on'); } });
      s.addEventListener('mouseleave', function () { if (!s.classList.contains('is-on')) { var r = row(id); if (r) { r.classList.remove('is-on'); } } });
    });
    rows.forEach(function (r) {
      var id = r.getAttribute('data-b-room');
      var s = spots.filter(function (x) { return x.getAttribute('data-b-spot') === id; })[0];
      if (!s) { return; }
      r.addEventListener('mouseenter', function () { s.classList.add('is-on'); });
      r.addEventListener('mouseleave', function () { s.classList.remove('is-on'); });
    });
    document.addEventListener('click', function (e) { if (!plan.contains(e.target) && !(zoom && zoom.contains(e.target))) { clear(); } });

    /* Büyüteç merceği: fare altındaki bölgeyi 2,2 kat büyütür (yalnız fareli cihazlar, CSS ile) */
    var frame = $('.b-plan__frame', plan), img = frame && $('img', frame);
    var lens = null, L = 240, nat = +(frame && frame.getAttribute('data-w')) || 900;
    if (frame && img) {
      lens = document.createElement('div'); lens.className = 'b-lens'; lens.setAttribute('aria-hidden', 'true');
      frame.appendChild(lens);
      frame.addEventListener('mousemove', function (e) {
        var r = frame.getBoundingClientRect(), x = e.clientX - r.left, y = e.clientY - r.top;
        /* büyütme: orijinal pikselin ~1,6 katına kadar; küçük kadrajda 2,4, tam ekranda daha az */
        var Z = Math.max(1.5, Math.min(2.4, nat * 1.6 / r.width));
        lens.style.left = x + 'px'; lens.style.top = y + 'px';
        lens.style.backgroundImage = 'url("' + (img.currentSrc || img.src) + '")';
        lens.style.backgroundSize = (r.width * Z) + 'px ' + (r.height * Z) + 'px';
        lens.style.backgroundPosition = (L / 2 - x * Z) + 'px ' + (L / 2 - y * Z) + 'px';
        lens.classList.add('is-on');
      });
      frame.addEventListener('mouseleave', function () { lens.classList.remove('is-on'); });
    }

    /* Büyüt: plan çerçevesi tam ekran katmana taşınır, kapatınca yerine döner */
    var zoomBtn = $('[data-b-zoom]', plan), zoom = null, home = frame && frame.parentNode;
    function closeZoom() {
      if (!zoom) { return; }
      home.insertBefore(frame, home.firstChild);
      zoom.parentNode.removeChild(zoom); zoom = null;
      document.documentElement.style.overflow = '';
      document.removeEventListener('keydown', onKey);
      clear(); zoomBtn.focus();
    }
    function onKey(e) { if (e.key === 'Escape') { closeZoom(); } }
    if (zoomBtn && frame) {
      zoomBtn.addEventListener('click', function () {
        if (zoom) { return; }
        var name = $('.b-plan__name', plan);
        zoom = document.createElement('div');
        zoom.className = 'b-zoom'; zoom.setAttribute('role', 'dialog'); zoom.setAttribute('aria-modal', 'true');
        zoom.setAttribute('aria-label', img.getAttribute('alt') || 'Daire planı');
        zoom.innerHTML = '<div class="b-zoom__bar"><p>' + (name ? name.innerHTML : '') + '</p>' +
          '<button type="button" class="b-zoom__close">' +
          '<svg class="b-ico" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6 6 18"/></svg>' +
          '<span>Kapat</span></button></div><div class="b-zoom__scroll"><div class="b-zoom__box"></div></div>';
        $('.b-zoom__box', zoom).appendChild(frame);
        document.body.appendChild(zoom);
        document.documentElement.style.overflow = 'hidden';
        document.addEventListener('keydown', onKey);
        $('.b-zoom__close', zoom).addEventListener('click', closeZoom);
        $('.b-zoom__scroll', zoom).addEventListener('click', function (e) { if (e.target === e.currentTarget) { closeZoom(); } });
        $('.b-zoom__close', zoom).focus();
      });
    }
  });

  $$('[data-b-switcher]').forEach(function (wrap) {
    var tabs = $$('[data-b-switch]', wrap).filter(function (t) { return t.closest('[data-b-switcher]') === wrap; });
    function select(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.classList.toggle('is-active', on);
        t.setAttribute('aria-selected', String(on));
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute('data-b-switch')).hidden = !on;
      });
      if (focus) { tab.focus(); }
    }
    tabs.forEach(function (t, k) {
      t.addEventListener('click', function () { select(t); });
      t.addEventListener('keydown', function (e) {
        var d = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (d) { e.preventDefault(); select(tabs[(k + d + tabs.length) % tabs.length], true); }
      });
    });
  });

  /* ------------------------------------------------------------------------
     GALERİ — düğmeler bir görsel kaydırır
     ------------------------------------------------------------------------ */
  $$('.b-gallery[data-b-rail]').forEach(function (g) {
    var track = g.querySelector('.b-gallery__track');
    var prev = g.querySelector('[data-b-prev]');
    var next = g.querySelector('[data-b-next]');
    var step = function () { var it = track.querySelector('li'); return it ? it.getBoundingClientRect().width + 16 : track.clientWidth; };
    var sync = function () {
      prev.disabled = track.scrollLeft <= 2;
      next.disabled = track.scrollLeft >= track.scrollWidth - track.clientWidth - 2;
    };
    prev.addEventListener('click', function () { track.scrollBy({ left: -step() }); });
    next.addEventListener('click', function () { track.scrollBy({ left: step() }); });
    track.addEventListener('scroll', sync, { passive: true });
    window.addEventListener('resize', sync);
    sync();
  });

  /* ------------------------------------------------------------------------
     YATIRIMCI ÇANTASI
     ------------------------------------------------------------------------ */
  $$('[data-b-bag]').forEach(function (form) {
    var items = $$('[data-b-bag-item]', form);
    var all = form.querySelector('[data-b-bag-all]');
    var btn = form.querySelector('[data-b-bag-btn]');
    var count = form.querySelector('[data-b-bag-count]');
    function sync() {
      var n = items.filter(function (i) { return i.checked; }).length;
      count.textContent = n;
      btn.disabled = n === 0;
      all.checked = n === items.length;
      all.indeterminate = n > 0 && n < items.length;
    }
    items.forEach(function (i) { i.addEventListener('change', sync); });
    all.addEventListener('change', function () { items.forEach(function (i) { i.checked = all.checked; }); sync(); });
    sync();
  });

  /* ------------------------------------------------------------------------
     ÖDEME HESAPLAMA — anüite; faiz temsilî
     ------------------------------------------------------------------------ */
  $$('[data-b-credit]').forEach(function (box) {
    var amount = box.querySelector('[data-b-amount]');
    var amountR = box.querySelector('[data-b-amount-range]');
    var term = box.querySelector('[data-b-term]');
    var termR = box.querySelector('[data-b-term-range]');
    var rate = parseFloat(box.querySelector('[data-b-rate]').getAttribute('data-rate')) / 100;
    var out = box.querySelector('[data-b-installment]');
    var total = box.querySelector('[data-b-total]');
    var digits = function (v) { return parseInt(String(v).replace(/[^\d]/g, ''), 10) || 0; };
    function calc() {
      var p = +amountR.value, n = +termR.value;
      var m = rate === 0 ? p / n : p * rate / (1 - Math.pow(1 + rate, -n));
      out.textContent = TL.format(m) + ' ₺';
      total.textContent = TL.format(m * n) + ' ₺';
    }
    function link(input, range, fmt) {
      range.addEventListener('input', function () { input.value = fmt(range.value); calc(); });
      input.addEventListener('change', function () {
        range.value = Math.min(Math.max(digits(input.value), +range.min), +range.max);
        input.value = fmt(range.value);
        calc();
      });
    }
    link(amount, amountR, function (v) { return INT.format(v); });
    link(term, termR, String);
    calc();
  });

  /* ------------------------------------------------------------------------
     FORMLAR — zorunlu alan denetimi; önyüz örneğinde gönderim yok
     ------------------------------------------------------------------------ */
  $$('[data-b-form]').forEach(function (form) {
    var done = form.querySelector('.b-form__done');
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
  $$('form[action="#"]').forEach(function (f) {
    f.addEventListener('submit', function (e) { e.preventDefault(); });
  });

  /* Video banner: durdur / oynat; hareket azaltma tercihinde başlamaz (poster kalır) */
  $$('[data-b-video]').forEach(function (v) {
    var btn = document.querySelector('[data-b-video-toggle]');
    var label = btn && btn.querySelector('[data-b-video-label]');
    function sync() {
      var paused = v.paused;
      if (!btn) { return; }
      btn.setAttribute('aria-pressed', String(paused));
      btn.classList.toggle('is-paused', paused);
      label.textContent = paused ? 'Videoyu oynat' : 'Videoyu durdur';
    }
    if (calm.matches) { v.removeAttribute('autoplay'); v.pause(); }
    v.addEventListener('play', sync);
    v.addEventListener('pause', sync);
    if (btn) { btn.addEventListener('click', function () { if (v.paused) { v.play(); } else { v.pause(); } }); }
    sync();
  });
})();
