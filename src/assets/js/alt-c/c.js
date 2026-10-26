/* Vakıf GYO — Alternatif C (deneysel): kaydırmaya bağlı hareketler */
(function () {
  'use strict';
  var $ = function (s, c) { return (c || document).querySelector(s); };
  var $$ = function (s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); };
  var calm = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var wide = window.matchMedia('(min-width: 900px)');
  var clamp = function (v, a, b) { return Math.min(b, Math.max(a, v)); };
  var lerp = function (a, b, t) { return a + (b - a) * t; };

  /* Başlık çubuğu: banner geçilince koyu zemin */
  var head = $('[data-c-head]');
  var heroEl = $('[data-c-hero]');

  /* Menü */
  var mBtn = $('[data-c-menu]'), panel = $('[data-c-menu-panel]');
  if (mBtn && panel) {
    mBtn.addEventListener('click', function () {
      var open = mBtn.getAttribute('aria-expanded') !== 'true';
      mBtn.setAttribute('aria-expanded', String(open));
      panel.hidden = !open;
      document.documentElement.style.overflow = open ? 'hidden' : '';
      head.classList.toggle('is-open', open);
      if (open) { var q = $('input', panel); if (q) { q.focus(); } }
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && !panel.hidden) { mBtn.click(); mBtn.focus(); }
    });
  }

  /* Video: durdur / oynat */
  var vid = $('[data-c-video]'), vBtn = $('[data-c-video-toggle]');
  if (vid) {
    if (calm) { vid.removeAttribute('autoplay'); vid.pause(); }
    var sync = function () {
      if (!vBtn) { return; }
      vBtn.classList.toggle('is-paused', vid.paused);
      vBtn.setAttribute('aria-pressed', String(vid.paused));
      $('[data-c-video-label]', vBtn).textContent = vid.paused ? 'Videoyu oynat' : 'Videoyu durdur';
    };
    vid.addEventListener('play', sync); vid.addEventListener('pause', sync);
    if (vBtn) { vBtn.addEventListener('click', function () { if (vid.paused) { vid.play(); } else { vid.pause(); } }); }
    sync();
  }

  /* Banner: kaydırınca video çerçevesi tam ekrana büyür, başlık yukarı kayar */
  var frame = $('[data-c-hero-frame]'), title = $('[data-c-hero-title]');
  /* Açılışta çerçeve başlığın hemen altından ekranın altına kadar uzanır (kenarlarda zemin payı) */
  var heroP = 0;
  function heroTick() {
    if (!heroEl || !frame || !title) { return; }
    var r = heroEl.getBoundingClientRect();
    var span = heroEl.offsetHeight - window.innerHeight;
    var p = calm ? 0 : clamp(-r.top / (span * 0.7), 0, 1);
    var e = 1 - Math.pow(1 - p, 3);
    var vw = document.documentElement.clientWidth, vh = window.innerHeight;
    var pad = clamp(vw * 0.044, 20, 72);   /* --pad */
    var gap = Math.max(16, Math.min(36, vh * 0.03));
    var t0 = title.offsetTop + title.offsetHeight + gap;
    heroEl.style.setProperty('--w', lerp(vw - 2 * pad, vw, e) + 'px');
    heroEl.style.setProperty('--h', lerp(vh - t0 - 16, vh, e) + 'px');
    heroEl.style.setProperty('--top', lerp(t0, 0, e) + 'px');
    heroEl.style.setProperty('--rad', lerp(22, 0, e) + 'px');
    heroEl.style.setProperty('--t-op', String(clamp(1 - p * 1.3, 0, 1)));
    heroEl.style.setProperty('--t-y', (-p * 8) + 'vh');
    heroEl.style.setProperty('--d-op', String(clamp(1 - p * 4, 0, 1)));
    heroP = p;
  }

  /* Temel amaç: kelimeler okundukça koyulaşır */
  var words = $('[data-c-words]');
  var wordSpans = words ? $$('span', words) : [];
  function wordsTick() {
    if (!words || calm) { return; }
    var r = words.getBoundingClientRect(), vh = window.innerHeight;
    var p = clamp((vh * 0.85 - r.top) / (r.height + vh * 0.35), 0, 1);
    var n = wordSpans.length;
    wordSpans.forEach(function (s, i) {
      s.style.setProperty('--o', String(clamp(0.16 + (p * n - i) * 0.84, 0.16, 1)));
    });
  }

  /* Portföy: dikey kaydırma kartları yatay ilerletir */
  var hs = $('[data-c-hscroll]'), track = hs && $('[data-c-track]', hs), prog = hs && $('[data-c-progress]', hs);
  var dist = 0;
  function hsLayout() {
    if (!hs) { return; }
    if (!wide.matches || calm) { hs.style.height = ''; track.style.setProperty('--x', '0px'); return; }
    dist = Math.max(0, track.scrollWidth - window.innerWidth);
    hs.style.height = (window.innerHeight + dist) + 'px';
  }
  function hsTick() {
    if (!hs || !wide.matches || calm) { return; }
    var r = hs.getBoundingClientRect();
    var p = clamp(-r.top / Math.max(1, dist), 0, 1);
    track.style.setProperty('--x', (-p * dist) + 'px');
    if (prog) { prog.parentNode.style.setProperty('--p', String(p)); prog.style.transform = 'scaleX(' + p + ')'; }
  }

  function tick() {
    heroTick(); wordsTick(); hsTick();
    if (head) {
      var past = window.scrollY > (heroEl ? heroEl.offsetHeight - 80 : 80);
      head.classList.toggle('is-solid', past);
      head.classList.toggle('is-dark', past || heroP > 0.7);
    }
  }
  var ticking = false;
  window.addEventListener('scroll', function () {
    if (!ticking) { ticking = true; requestAnimationFrame(function () { tick(); ticking = false; }); }
  }, { passive: true });
  window.addEventListener('resize', function () { hsLayout(); tick(); });
  window.addEventListener('load', function () { hsLayout(); tick(); });
  hsLayout(); tick();
  if (document.fonts) { document.fonts.ready.then(function () { hsLayout(); tick(); }); }

  /* Görünür olunca beliren öğeler, sayaçlar, çizgi grafik, harita */
  function fmt(v, dec) {
    return v.toLocaleString('tr-TR', { minimumFractionDigits: dec, maximumFractionDigits: dec });
  }
  function count(el) {
    var to = parseFloat(el.getAttribute('data-c-count')), dec = +el.getAttribute('data-dec') || 0;
    var pre = el.getAttribute('data-pre') || '', suf = el.getAttribute('data-suf') || '';
    if (calm) { el.textContent = pre + fmt(to, dec) + suf; return; }
    var t0 = null, dur = 1600;
    function step(t) {
      if (!t0) { t0 = t; }
      var k = clamp((t - t0) / dur, 0, 1), e = 1 - Math.pow(1 - k, 3);
      el.textContent = pre + fmt(to * e, dec) + suf;
      if (k < 1) { requestAnimationFrame(step); }
    }
    requestAnimationFrame(step);
  }
  var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (ents) {
    ents.forEach(function (en) {
      if (!en.isIntersecting) { return; }
      en.target.classList.add('is-in');
      $$('[data-c-count]', en.target).forEach(count);
      io.unobserve(en.target);
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -8% 0px' }) : null;
  $$('[data-c-reveal], .c-map').forEach(function (el) {
    if (io && !calm) { io.observe(el); } else { el.classList.add('is-in'); }
  });
  /* Harita parçaları sırayla belirir */
  $$('.c-map [data-c-pop]').forEach(function (el, i) { el.style.transitionDelay = (i * 0.045) + 's'; });

  /* Haberler: sürükleyerek ve oklarla kaydırma */
  $$('[data-c-drag]').forEach(function (tr) {
    var sec = tr.closest('section'), prev = $('[data-c-prev]', sec), next = $('[data-c-next]', sec);
    var step = function () { var c = $('li', tr); return c ? c.getBoundingClientRect().width + 24 : 400; };
    var syncNav = function () {
      if (prev) { prev.disabled = tr.scrollLeft < 4; }
      if (next) { next.disabled = tr.scrollLeft > tr.scrollWidth - tr.clientWidth - 4; }
    };
    if (prev) { prev.addEventListener('click', function () { tr.scrollBy({ left: -step(), behavior: 'smooth' }); }); }
    if (next) { next.addEventListener('click', function () { tr.scrollBy({ left: step(), behavior: 'smooth' }); }); }
    tr.addEventListener('scroll', syncNav, { passive: true });
    syncNav();
    var down = false, sx = 0, sl = 0, moved = false;
    tr.addEventListener('pointerdown', function (e) {
      if (e.pointerType !== 'mouse') { return; }
      down = true; moved = false; sx = e.clientX; sl = tr.scrollLeft;
    });
    window.addEventListener('pointermove', function (e) {
      if (!down) { return; }
      var dx = e.clientX - sx;
      if (Math.abs(dx) > 4) { moved = true; tr.classList.add('is-drag'); }
      tr.scrollLeft = sl - dx;
    });
    window.addEventListener('pointerup', function () {
      if (!down) { return; }
      down = false;
      setTimeout(function () { tr.classList.remove('is-drag'); }, 0);
    });
    tr.addEventListener('click', function (e) { if (moved) { e.preventDefault(); } }, true);
  });
})();
