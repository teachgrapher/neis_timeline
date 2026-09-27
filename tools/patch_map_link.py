# pages/ 문서의 업무카드 끝에 '나이스 지도에서 위치 보기' 링크를 넣는 패치 스크립트
#
# 쓰는 법.
#   저장소 뿌리에서 python3 tools/patch_map_link.py                 (매니페스트의 공개 문서 전부)
#   저장소 뿌리에서 python3 tools/patch_map_link.py 파일이름.html   (그 문서 하나만)
#
# 링크 자료는 map-links.js 에 있다. 그 파일은 neismap 저장소의 tools/build_timeline_links.py 가 만든다.
# 짝을 바꿀 때는 neismap 쪽 연결표(data/timeline-links.txt)를 고치고 그 스크립트를 돌린다. 이 패치는 다시 돌릴 필요 없다.
# 넣은 조각을 표시로 감싸 두므로 다시 돌리면 갈아 끼운다.

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'

CSS_BEGIN = '/* == maplink:begin == */'
CSS_END = '/* == maplink:end == */'
JS_BEGIN = '<!-- maplink:begin -->'
JS_END = '<!-- maplink:end -->'

CSS = CSS_BEGIN + """
.maplinks{display:flex;flex-wrap:wrap;gap:6px 14px;margin:14px 0 0;padding-top:10px;border-top:1px solid var(--rule-soft);font-size:12.5px}
.maplinks a{color:var(--mark);text-decoration:none;border-bottom:1px solid var(--mark);word-break:keep-all;overflow-wrap:normal;hyphens:none}
.maplinks a:hover{border-bottom-width:2px}
.maplinks a:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.cardnav{margin-top:10px}
@media print{.maplinks{display:none}}
""" + CSS_END

JS = JS_BEGIN + """
<script src="../map-links.js"></script>
<script>
(function(){
  var M = window.MAP_LINKS; if(!M) return;
  var f = decodeURIComponent(location.pathname.split('/').pop());
  var here = M.cards[f]; if(!here) return;
  var esc = function(s){ return String(s).replace(/[&<>"]/g, function(c){ return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]; }); };
  document.querySelectorAll('article.task').forEach(function(a){
    var list = here[a.id], body = a.querySelector('.body'); if(!list || !body) return;
    var nav = body.querySelector('.cardnav');
    var box = document.createElement('p'); box.className = 'maplinks';
    box.innerHTML = list.map(function(x){
      return '<a href="' + M.base + 'part' + x[0] + '#' + encodeURIComponent(x[1]) + '" target="_blank" rel="noopener" title="나이스 지도 Part ' + x[0] + ' ' + esc(M.parts[x[0]]) + ' · ' + esc(x[3]) + '">나이스 지도에서 보기 · ' + esc(M.parts[x[0]]) + ' › ' + esc(x[2]) + ' ↗</a>';
    }).join('');
    body.insertBefore(box, nav);
  });
})();
</script>
""" + JS_END


def patch(path):
    s = path.read_text(encoding='utf-8')
    again = JS_BEGIN in s
    if again:
        s = re.sub(re.escape(CSS_BEGIN) + '.*?' + re.escape(CSS_END) + r'\n?', '', s, flags=re.S)
        s = re.sub(re.escape(JS_BEGIN) + '.*?' + re.escape(JS_END) + r'\n?', '', s, flags=re.S)
    for a in ('</style>', '</body>'):
        if s.count(a) != 1:
            raise SystemExit('기준점이 1번 나오지 않음 · %s · %r' % (path.name, a))
    s = s.replace('</style>', CSS + '\n</style>', 1)
    s = s.replace('</body>', JS + '\n</body>', 1)
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
