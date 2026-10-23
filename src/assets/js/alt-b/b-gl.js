/* ==========================================================================
   Vakıf GYO — Alternatif B · b-gl.js

   Hero slayt geçişi: WebGL görsel geçişi (Codrops "WebGL Image Transitions",
   Yuriy Artyukh). b.js'in slayt değişiminde yaydığı "b-slide" olayını dinler;
   görselleri kanvasta çizer, slaydın kendi <img>'si gizlenir (.has-gl).

   data-b-gl="8"  dikey yırtılma: üst yarı yukarı, alt yarı aşağı kayarak
                  gürültüyle dağılır (demo 8, varsayılan)
   data-b-gl="7"  çapraz şerit kayması (demo 7)

   Ken Burns yakınlaşması burada sürdürülür (CSS'tekiyle aynı: 1.09 → 1, 10 sn).
   Bağımlılık yok; WebGL yoksa, "hareketi azalt" açıksa ya da veri tasarrufu
   isteniyorsa hiçbir şey yapmaz; CSS çapraz geçiş kalır.
   ========================================================================== */

(function () {
  'use strict';

  var calm = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (calm.matches) { return; }
  if (navigator.connection && navigator.connection.saveData) { return; }

  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  var DUR = 1100;          // geçiş süresi (ms)
  var KB = 10000;          // Ken Burns süresi (ms), CSS ile aynı
  var KB_FROM = 1.09;

  var VERT = [
    'attribute vec2 a;',
    'varying vec2 vUv;',
    'void main(){ vUv = vec2(a.x * .5 + .5, .5 - a.y * .5); gl_Position = vec4(a, 0., 1.); }'
  ].join('\n');

  var HEAD = [
    'precision highp float;',
    'uniform sampler2D t1; uniform sampler2D t2;',
    'uniform float progress; uniform vec2 res;',
    'uniform vec4 fitA; uniform vec4 fitB; uniform float zoomA; uniform float zoomB;',
    'varying vec2 vUv;',
    'const float PI = 3.1415926;',
    'vec2 fit(vec2 uv, vec4 f, float z){ vec2 u = (uv - .5) / z + .5; return u * f.xy + f.zw; }',
    'mat2 rotate(float a){ float s = sin(a); float c = cos(a); return mat2(c, -s, s, c); }',
    'float hash(vec2 p){ return fract(1e4 * sin(17.0 * p.x + p.y * 0.1) * (0.1 + abs(sin(p.y * 13.0 + p.x)))); }',
    'float hnoise(vec2 x){ vec2 i = floor(x); vec2 f = fract(x);',
    '  float a = hash(i); float b = hash(i + vec2(1., 0.)); float c = hash(i + vec2(0., 1.)); float d = hash(i + vec2(1., 1.));',
    '  vec2 u = f * f * (3. - 2. * f);',
    '  return mix(a, b, u.x) + (c - a) * u.y * (1. - u.x) + (d - b) * u.x * u.y; }'
  ].join('\n');

  var FX = {
    // Demo 8: merkezden uzaklığa göre dikey itme; gürültüyle dağılır
    '8': [
      'void main(){',
      '  vec2 uv = vUv;',
      '  float hn = hnoise(uv * res / 100.0);',
      '  vec2 d = vec2(0., normalize(vec2(.5) - uv).y);',
      '  vec2 uv1 = uv + d * progress / 5.0 * (1.0 + hn / 2.0);',
      '  vec2 uv2 = uv - d * (1.0 - progress) / 5.0 * (1.0 + hn / 2.0);',
      '  vec4 c1 = texture2D(t1, fit(uv1, fitA, zoomA));',
      '  vec4 c2 = texture2D(t2, fit(uv2, fitB, zoomB));',
      '  gl_FragColor = mix(c1, c2, progress);',
      '}'
    ].join('\n'),
    // Demo 7: 50 dikey şerit, 45° kayar
    '7': [
      'void main(){',
      '  vec2 uv = vUv;',
      '  vec2 div = fract(uv * vec2(50., 1.));',
      '  vec2 uv1 = uv + rotate(PI / 4.) * div * progress * 0.1;',
      '  vec2 uv2 = uv + rotate(PI / 4.) * div * (1. - progress) * 0.1;',
      '  vec4 c1 = texture2D(t1, fit(uv1, fitA, zoomA));',
      '  vec4 c2 = texture2D(t2, fit(uv2, fitB, zoomB));',
      '  gl_FragColor = mix(c1, c2, progress);',
      '}'
    ].join('\n')
  };

  function easeInOut(t) { return t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }   // power2.inOut
  function easeOut(t) { return 1 - (1 - t) * (1 - t); }                                     // CSS ease-out'a yakın
  function zoomAt(since, now) {
    if (since == null) { return 1; }
    var t = Math.min(1, Math.max(0, (now - since) / KB));
    return KB_FROM - (KB_FROM - 1) * easeOut(t);
  }
  function pct(s, i) {
    var parts = (s || '').trim().split(/\s+/);
    var v = parseFloat(parts[i]);
    return isNaN(v) ? .5 : v / 100;
  }

  $$('[data-b-hero]').forEach(function (hero) {
    var slides = $$('.b-slide', hero);
    if (slides.length < 2) { return; }
    var wrap = hero.querySelector('.b-hero__slides');
    var canvas = document.createElement('canvas');
    canvas.className = 'b-hero__gl';
    canvas.setAttribute('aria-hidden', 'true');
    var gl = canvas.getContext('webgl', { antialias: false, alpha: false, premultipliedAlpha: false, powerPreference: 'low-power' })
          || canvas.getContext('experimental-webgl');
    if (!gl) { return; }

    var fx = FX[hero.getAttribute('data-b-gl')] || FX['8'];

    function shader(type, src) {
      var s = gl.createShader(type);
      gl.shaderSource(s, src); gl.compileShader(s);
      if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) { throw new Error(gl.getShaderInfoLog(s)); }
      return s;
    }
    var prog;
    try {
      prog = gl.createProgram();
      gl.attachShader(prog, shader(gl.VERTEX_SHADER, VERT));
      gl.attachShader(prog, shader(gl.FRAGMENT_SHADER, HEAD + '\n' + fx));
      gl.linkProgram(prog);
      if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { throw new Error(gl.getProgramInfoLog(prog)); }
    } catch (e) { return; }
    gl.useProgram(prog);

    var buf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, buf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 1, -1, -1, 1, 1, 1]), gl.STATIC_DRAW);
    var aLoc = gl.getAttribLocation(prog, 'a');
    gl.enableVertexAttribArray(aLoc);
    gl.vertexAttribPointer(aLoc, 2, gl.FLOAT, false, 0, 0);
    var U = {};
    ['t1', 't2', 'progress', 'res', 'fitA', 'fitB', 'zoomA', 'zoomB'].forEach(function (n) { U[n] = gl.getUniformLocation(prog, n); });
    gl.uniform1i(U.t1, 0); gl.uniform1i(U.t2, 1);

    // Dokular: her slaydın <img>'sinden; <picture> kaynağı değişince (dikey ekran) yeniden yüklenir
    var tex = slides.map(function (s) {
      var img = s.querySelector('.b-slide__media img');
      var pic = s.querySelector('.b-slide__media');
      var t = gl.createTexture();
      gl.bindTexture(gl.TEXTURE_2D, t);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      return { img: img, pic: pic, tex: t, ready: false, w: 1, h: 1, fit: [1, 1, 0, 0] };
    });

    var cw = 1, ch = 1, dpr = Math.min(window.devicePixelRatio || 1, 1.5);
    var A = slides.findIndex(function (s) { return s.classList.contains('is-active'); });
    if (A < 0) { A = 0; }
    var B = -1;              // geçiş hedefi
    var t0 = 0;              // geçiş başlangıcı
    var sinceA = null;       // A'nın Ken Burns başlangıcı
    var sinceB = null;
    var pending = -1;        // doku hazır olmayınca bekleyen hedef
    var raf = null;
    var visible = true;

    function fitOf(k) {
      var t = tex[k];
      var portrait = window.matchMedia('(orientation: portrait) and (max-width: 1199px)').matches;
      var pos = t.pic.style.getPropertyValue(portrait && t.pic.style.getPropertyValue('--ppos') ? '--ppos' : '--pos') || '50% 50%';
      var px = pct(pos, 0), py = pct(pos, 1);
      var ca = cw / ch, ia = t.w / t.h, sx, sy, ox, oy;
      if (ia > ca) { sx = ca / ia; sy = 1; ox = (1 - sx) * px; oy = 0; }
      else { sx = 1; sy = ia / ca; ox = 0; oy = (1 - sy) * py; }
      t.fit = [sx, sy, ox, oy];
    }

    function upload(k) {
      var t = tex[k];
      var img = t.img;
      if (!img.complete || !img.naturalWidth) { return; }
      gl.bindTexture(gl.TEXTURE_2D, t.tex);
      try {
        gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGB, gl.RGB, gl.UNSIGNED_BYTE, img);
      } catch (e) { return; }
      t.w = img.naturalWidth; t.h = img.naturalHeight;
      t.ready = true;
      fitOf(k);
      if (!hero.classList.contains('has-gl') && k === A) {
        hero.classList.add('has-gl');
        sinceA = performance.now();
        loop();
      }
      if (pending === k) { pending = -1; start(k); }
      if (!raf) { draw(performance.now()); }
    }

    function resize() {
      var r = hero.getBoundingClientRect();
      cw = Math.max(1, Math.round(r.width)); ch = Math.max(1, Math.round(r.height));
      canvas.width = Math.round(cw * dpr); canvas.height = Math.round(ch * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
      gl.uniform2f(U.res, canvas.width, canvas.height);
      tex.forEach(function (t, k) { if (t.ready) { fitOf(k); } });
      if (!raf) { draw(performance.now()); }
    }

    function draw(now) {
      var a = tex[A], b = tex[B >= 0 ? B : A];
      var p = 0;
      if (B >= 0) {
        p = easeInOut(Math.min(1, (now - t0) / DUR));
      }
      gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, a.tex);
      gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, b.tex);
      gl.uniform4fv(U.fitA, a.fit); gl.uniform4fv(U.fitB, b.fit);
      gl.uniform1f(U.zoomA, zoomAt(sinceA, now));
      gl.uniform1f(U.zoomB, B >= 0 ? zoomAt(sinceB, now) : zoomAt(sinceA, now));
      gl.uniform1f(U.progress, p);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      if (B >= 0 && p >= 1) { A = B; B = -1; sinceA = sinceB; sinceB = null; }
    }

    function loop() {
      raf = null;
      if (!visible || document.hidden) { return; }
      var now = performance.now();
      draw(now);
      // Geçiş ya da Ken Burns sürerken çiz; ikisi de bitince dur
      if (B >= 0 || (sinceA != null && now - sinceA < KB)) { raf = requestAnimationFrame(loop); }
    }

    function start(k) {
      if (k === A && B < 0) { return; }
      if (!tex[k].ready) { pending = k; tex[k].img.loading = 'eager'; return; }
      var now = performance.now();
      if (B >= 0) { A = B; sinceA = sinceB; }      // süren geçişi bitir
      B = k; t0 = now; sinceB = now;
      if (!raf) { loop(); }
    }

    hero.addEventListener('b-slide', function (e) { start(e.detail.to); });

    // Dokuları yükle: etkin slayt hemen, diğerleri art arda (b.js de sonrakini açar)
    tex.forEach(function (t, k) {
      t.img.addEventListener('load', function () { upload(k); });
      if (k === A) { t.img.loading = 'eager'; }
      else { setTimeout(function () { t.img.loading = 'eager'; }, 600 + 500 * k); }
    });

    wrap.insertBefore(canvas, wrap.firstChild);
    resize();
    tex.forEach(function (t, k) { upload(k); });

    if ('ResizeObserver' in window) { new ResizeObserver(resize).observe(hero); }
    else { window.addEventListener('resize', resize); }
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        visible = es[0].isIntersecting;
        if (visible && !raf) { loop(); }
      }).observe(hero);
    }
    document.addEventListener('visibilitychange', function () { if (!document.hidden && !raf) { loop(); } });
    canvas.addEventListener('webglcontextlost', function (e) { e.preventDefault(); hero.classList.remove('has-gl'); });
  });
})();
