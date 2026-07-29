# pages/의 타임라인 문서에 '전체 색인' 복귀 링크와 앞뒤 문서 이동 막대를 주입하는 패치 스크립트
#
# 쓰는 법.
#   저장소 뿌리에서 python3 tools/patch_pages.py
#
# 문서를 새로 만들거나 다시 뽑았을 때 한 번 더 돌리면 된다.
# 이미 적용된 파일은 건너뛰므로 몇 번을 돌려도 같은 결과가 된다.

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'
MANIFEST = ROOT / 'manifest.js'

MARK = 'class="docnav"'          # 이미 패치했는지 알아보는 표시

# ── manifest.js에서 Part별 문서 순서를 읽는다 ────────────────────────────
GROUP_RE = re.compile(r'\{\s*(?:no:\s*(\d+)|tag:\s*\'([^\']*)\')(.*?)\n  \}', re.S)
LABEL_RE = re.compile(r"label:\s*'([^']*)'")
DOC_RE = re.compile(r"\{ f: '([^']+)', ready: (\d) \}")


def read_groups():
    """[(배지, 라벨, [파일명...]), ...] 를 매니페스트에 적힌 순서대로 돌려준다."""
    src = MANIFEST.read_text(encoding='utf-8')
    # 주석 줄은 예시 코드가 섞여 있어 먼저 걷어낸다
    src = '\n'.join(ln for ln in src.split('\n') if not ln.strip().startswith('//'))

    groups = []
    for m in GROUP_RE.finditer(src):
        no, tag, body = m.group(1), m.group(2), m.group(3)
        label = LABEL_RE.search(body)
        docs = [f for f, ready in DOC_RE.findall(body) if ready == '1']
        if not docs:
            continue
        groups.append((tag or ('Part ' + no), label.group(1) if label else '', docs))
    return groups


# ── 끼워 넣을 조각 ──────────────────────────────────────────────────────
CSS = """.topbar .home{margin-left:auto;font-size:12.5px;font-weight:600;color:var(--ink-soft);text-decoration:none;border-bottom:1px solid var(--rule);white-space:nowrap}
.topbar .home:hover{color:var(--mark);border-color:var(--mark)}

/* \u2500\u2500 \uc774\uc6c3 \ubb38\uc11c \uc774\ub3d9 \u2500\u2500 */
.docnav{display:grid;grid-template-columns:1fr auto 1fr;gap:10px;margin:52px 0 0;padding-top:22px;border-top:1.5px solid var(--ink)}
.docnav a{
  display:block;padding:12px 14px;background:var(--sheet);border:1px solid var(--rule);
  text-decoration:none;color:var(--ink);font-size:14px;font-weight:600;line-height:1.45;
  transition:border-color .12s,color .12s;
}
.docnav a:hover{border-color:var(--mark);color:var(--mark)}
.docnav a:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.docnav a span{display:block;font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.1em;color:var(--ink-soft);margin-bottom:3px}
.docnav a:hover span{color:var(--mark)}
.docnav .next{text-align:right}
.docnav .hub{display:flex;align-items:center;font-size:13px;background:none;border-style:dashed;color:var(--ink-soft)}
.docnav .gap{border:0}
@media (max-width:640px){
  .topbar .up{display:none}
  .docnav{grid-template-columns:1fr;gap:8px;margin-top:38px}
  .docnav .next{text-align:left}
  .docnav .hub{justify-content:center}
}"""

SCRIPT = """<script>
// \ud5c8\ube0c \uac80\uc0c9\uc744 \uac70\uccd0 \ub4e4\uc5b4\uc654\ub2e4\uba74 '\uc804\uccb4 \uc0c9\uc778' \ub9c1\ud06c\uac00 \uadf8 \uac80\uc0c9 \uacb0\uacfc\ub85c \ub418\ub3cc\ub9ac\uac8c \ud55c\ub2e4
(function(){
  var p = new URLSearchParams(location.search), keep = [];
  ['q','who'].forEach(function(k){
    var v = p.get(k);
    if(v) keep.push(k + '=' + encodeURIComponent(v));
  });
  if(!keep.length) return;
  document.querySelectorAll('a.home,a.hub').forEach(function(a){
    a.href = '../index.html#' + keep.join('&');
  });
})();
</script>
"""

# 기준점. 53편 전부에서 정확히 한 번씩 나오는 것을 확인하고 골랐다
ANCHOR_CSS = '.topbar .up:hover{color:var(--mark);border-color:var(--mark)}'
ANCHOR_PRINT = '  .topbar,.ticker,.tl-scroll,.cardnav{display:none}'
ANCHOR_TOPBAR = '<a class="up" href="#timeline">\ud0c0\uc784\ub77c\uc778 \u2191</a>'
ANCHOR_FOOTER = '    <footer>'
ANCHOR_BODY = '</body>'


def label_of(fname):
    """\ud30c\uc77c\uba85 \u2192 \ubb38\uc11c \uc81c\ubaa9. \ud5c8\ube0c index.html\uc758 labelOf()\uc640 \uac19\uc740 \uaddc\uce59\uc774\ub2e4."""
    s = re.sub(r'\.html$', '', fname, flags=re.I)
    s = re.sub(r'^\ub098\uc774\uc2a4[_ ]', '', s)
    s = re.sub(r'[_ ]\ud0c0\uc784\ub77c\uc778[_ ]v\d+$', '', s)
    s = re.sub(r'[_ ]v\d+$', '', s)
    return s.replace('_', ' ').strip()


def esc(s):
    return (s.replace('&', '&amp;').replace('<', '&lt;')
             .replace('>', '&gt;').replace('"', '&quot;'))


def docnav(badge, label, prev_f, next_f):
    part = (badge + ' ' + label).strip()
    left = ('<a class="prev" href="' + esc(prev_f) + '"><span>\u2190 \uc774\uc804</span>'
            + esc(label_of(prev_f)) + '</a>') if prev_f else '<span class="gap"></span>'
    right = ('<a class="next" href="' + esc(next_f) + '"><span>\ub2e4\uc74c \u2192</span>'
             + esc(label_of(next_f)) + '</a>') if next_f else '<span class="gap"></span>'
    return ('    <nav class="docnav" aria-label="\uc774\uc6c3 \ubb38\uc11c \uc774\ub3d9">\n'
            '      ' + left + '\n'
            '      <a class="hub" href="../index.html">\uc804\uccb4 \uc0c9\uc778 \u00b7 ' + esc(part) + '</a>\n'
            '      ' + right + '\n'
            '    </nav>\n\n')


def patch(path, badge, label, prev_f, next_f):
    s = path.read_text(encoding='utf-8')
    if MARK in s:
        return 'skip'

    for a in (ANCHOR_CSS, ANCHOR_PRINT, ANCHOR_TOPBAR, ANCHOR_FOOTER, ANCHOR_BODY):
        if s.count(a) != 1:
            raise SystemExit('기준점이 1번 나오지 않음 · %s · %r' % (path.name, a[:40]))

    s = s.replace(ANCHOR_CSS, ANCHOR_CSS + '\n' + CSS, 1)
    s = s.replace(ANCHOR_PRINT,
                  '  .topbar,.ticker,.tl-scroll,.cardnav,.docnav{display:none}', 1)
    s = s.replace(ANCHOR_TOPBAR,
                  '<a class="home" href="../index.html">\u2190 \uc804\uccb4 \uc0c9\uc778</a>\n'
                  '    ' + ANCHOR_TOPBAR, 1)
    s = s.replace(ANCHOR_FOOTER,
                  docnav(badge, label, prev_f, next_f) + ANCHOR_FOOTER, 1)
    s = s.replace(ANCHOR_BODY, SCRIPT + ANCHOR_BODY, 1)

    path.write_text(s, encoding='utf-8')
    return 'done'


def main():
    done = skip = 0
    missing = []
    for badge, label, docs in read_groups():
        for i, f in enumerate(docs):
            path = PAGES / f
            if not path.exists():
                missing.append(f)
                continue
            r = patch(path,
                      badge, label,
                      docs[i - 1] if i > 0 else None,
                      docs[i + 1] if i + 1 < len(docs) else None)
            done += (r == 'done')
            skip += (r == 'skip')

    print('패치 %d편 · 이미 적용 %d편' % (done, skip))
    if missing:
        print('매니페스트에 있으나 pages에 없는 파일 %d건' % len(missing))
        for f in missing:
            print('  ', f)
    return 0


if __name__ == '__main__':
    sys.exit(main())
