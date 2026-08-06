# pages/의 문서 상단바에 '업무카드 모아보기'(cards.html) 링크를 넣는 패치 스크립트
#
# 쓰는 법.
#   저장소 뿌리에서 python3 tools/patch_wall_link.py                 (매니페스트의 공개 문서 전부)
#   저장소 뿌리에서 python3 tools/patch_wall_link.py 파일이름.html   (그 문서 하나만)
#
# 넣은 조각을 표시로 감싸 두므로 다시 돌리면 갈아 끼운다.
# tools/patch_sitebar_rail.py 가 먼저 적용되어 있어야 한다.

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'

CSS_BEGIN = '/* == walllink:begin == */'
CSS_END = '/* == walllink:end == */'
HTML_BEGIN = '<!-- walllink:begin -->'
HTML_END = '<!-- walllink:end -->'

CSS = CSS_BEGIN + """
.wall-link{
  flex:none;font-size:12px;font-weight:700;white-space:nowrap;margin-left:12px;
  padding:3px 9px;border:1px solid var(--ink);color:var(--ink);text-decoration:none;
}
.wall-link:hover{background:var(--ink);color:#fff}
.wall-link:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.sitenav .bar{gap:0}
""" + CSS_END

LINK = HTML_BEGIN + '<a class="wall-link" href="../cards.html">업무카드 모아보기 →</a>' + HTML_END

ANCHOR_CSS = '</style>'
ANCHOR_LINK = '    <ol class="snav-list" id="siteticks"></ol>\n'


def patch(path):
    s = path.read_text(encoding='utf-8')
    again = HTML_BEGIN in s
    if again:
        s = re.sub(re.escape(CSS_BEGIN) + '.*?' + re.escape(CSS_END), '', s, flags=re.S)
        s = re.sub(re.escape(HTML_BEGIN) + '.*?' + re.escape(HTML_END), '', s, flags=re.S)

    if 'v2-sitebar-rail' not in s:
        raise SystemExit('전역 상단바 패치가 먼저 필요함 · ' + path.name)
    for a in (ANCHOR_CSS, ANCHOR_LINK):
        if s.count(a) != 1:
            raise SystemExit('기준점이 1번 나오지 않음 · %s · %r' % (path.name, a[:40]))

    s = s.replace(ANCHOR_CSS, CSS + '\n' + ANCHOR_CSS, 1)
    s = s.replace(ANCHOR_LINK, ANCHOR_LINK + '    ' + LINK + '\n', 1)
    path.write_text(s, encoding='utf-8')
    return 'redo' if again else 'done'


def targets():
    if len(sys.argv) > 1:
        return [PAGES / sys.argv[1]]
    src = (ROOT / 'manifest.js').read_text(encoding='utf-8')
    out = []
    for line in src.split('\n'):
        line = line.strip()
        if line.startswith('//') or 'ready: 1' not in line:
            continue
        out.append(PAGES / line.split("'")[1])
    return out


def main():
    done = redo = 0
    for path in targets():
        if not path.exists():
            print('없는 파일 ·', path.name)
            continue
        r = patch(path)
        done += (r == 'done')
        redo += (r == 'redo')
    print('패치 %d편 · 갈아 끼움 %d편' % (done, redo))
    return 0


if __name__ == '__main__':
    sys.exit(main())
