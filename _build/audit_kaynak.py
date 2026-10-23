# -*- coding: utf-8 -*-
"""src/<klasör> sayfalarındaki görünür metni _docs/kaynak ile karşılaştırır; bulunmayanları listeler."""
import glob, io, os, re, sys
from html.parser import HTMLParser
sys.stdout.reconfigure(encoding='utf-8')
ROOT = sys.argv[1]
DIR = sys.argv[2] if len(sys.argv) > 2 else 'alt-b'      # src/<DIR>
PAGES = sys.argv[3:] or ['index', 'yatirimci-iliskileri', 'vsancaktepe-merkez', 'hakkimizda']

def norm(s):
    s = s.replace('İ', 'i').replace('I', 'ı').lower()
    s = re.sub(r"[’‘`´]", "'", s)
    s = s.replace('“', '"').replace('”', '"')
    s = s.replace(' ', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'[\s\.\,\;\:\!\?\-–—·…]+$', '', s)
    s = re.sub(r'^[\s\.\,\;\:\!\?\-–—·…]+', '', s)
    return s

corpus = []
for p in glob.glob(os.path.join(ROOT, '_docs', 'kaynak', '*.txt')):
    corpus.append(io.open(p, encoding='utf-8', errors='replace').read())
C = norm('\n'.join(corpus))
C1 = re.sub(r'[^\wğüşöçı]+', ' ', C)   # noktalama bağımsız

def found(s):
    n = norm(s)
    if len(n) < 2: return True
    if n in C: return True
    n1 = re.sub(r'[^\wğüşöçı]+', ' ', n).strip()
    return bool(n1) and n1 in C1

class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.stack = []; self.out = []; self.skip = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        self.stack.append((tag, a.get('class', '')))
        if tag in ('script', 'style', 'svg'): self.skip += 1
        for k in ('alt', 'aria-label', 'placeholder', 'title'):
            if a.get(k): self.out.append(('@' + k, tag, a.get('class', ''), a[k]))
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'svg'): self.skip -= 1
        if self.stack: self.stack.pop()
    def handle_data(self, d):
        if self.skip: return
        t = d.strip()
        if not t: return
        tag, cls = self.stack[-1] if self.stack else ('', '')
        self.out.append(('', tag, cls, t))

for page in PAGES:
    html = io.open(os.path.join(ROOT, 'src', DIR, page + '.html'), encoding='utf-8').read()
    html = re.sub(r'<br\s*/?>', ' ', html)
    p = P(); p.feed(html)
    seen = set(); miss = []
    for kind, tag, cls, t in p.out:
        key = (kind, t)
        if key in seen: continue
        seen.add(key)
        if found(t): continue
        # cümlelere böl: tümü bulunursa geç
        parts = [x for x in re.split(r'(?<=[\.\!\?])\s+', t) if x.strip()]
        if len(parts) > 1 and all(found(x) for x in parts): continue
        miss.append((kind, tag, cls, t))
    print('=' * 70); print(page, '—', len(miss), 'bulunamadı /', len(seen), 'metin'); print('=' * 70)
    for kind, tag, cls, t in miss:
        print('%s<%s %s> %s' % (kind + ' ' if kind else '', tag, cls.split(' ')[0], t[:160]))
