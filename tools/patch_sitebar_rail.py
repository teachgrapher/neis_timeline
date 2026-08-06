# pages/의 타임라인 문서에 전역 상단바(검색·Part 이동)와 왼쪽 세로 타임라인 레일을 주입하는 패치 스크립트
#
# 쓰는 법.
#   저장소 뿌리에서 python3 tools/patch_sitebar_rail.py                 (매니페스트의 공개 문서 전부)
#   저장소 뿌리에서 python3 tools/patch_sitebar_rail.py 파일이름.html   (그 문서 하나만)
#
# 이미 적용된 파일은 건너뛰므로 몇 번을 돌려도 같은 결과가 된다.

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'

MARK = 'v2-sitebar-rail'          # 이미 패치했는지 알아보는 표시

CSS = """
/* ══ 전역 상단바 · 왼쪽 세로 타임라인 (v2-sitebar-rail) ══ */
:root{
  --sitebar-h:50px;
  --sitenav-h:38px;
  --railw:264px;
  --chrome-h:calc(var(--sitebar-h) + var(--sitenav-h) + var(--topbar-h));
  --offset:calc(var(--chrome-h) + var(--ticker-h) + 18px);
}

/* 문서 제목 막대는 전역 막대 아래에 붙는다 */
.topbar{top:calc(var(--sitebar-h) + var(--sitenav-h))}

/* ── 전역 상단바 ── */
.sitebar{position:sticky;top:0;z-index:80;background:rgba(238,240,233,.96);backdrop-filter:saturate(160%) blur(8px);border-bottom:1px solid var(--rule)}
.sitebar .bar{height:var(--sitebar-h);display:flex;align-items:center;gap:14px}
.sitebar .dot{width:8px;height:8px;border-radius:50%;background:var(--mark);flex:none}
.sitebar .brand{font-size:15.5px;font-weight:700;letter-spacing:-.01em;white-space:nowrap;color:var(--ink);text-decoration:none}
.sitebar .brand:hover{color:var(--mark)}
.sitebar .hint{margin-left:auto;font-size:11.5px;font-weight:500;color:var(--ink-soft);white-space:nowrap}
.searchbox{position:relative;flex:1;max-width:520px;margin-left:6px}
.searchbox input{
  width:100%;height:32px;padding:0 66px 0 12px;
  font-family:var(--sans);font-size:14px;font-weight:500;color:var(--ink);
  background:var(--sheet);border:1.5px solid var(--ink);border-radius:0;
}
.searchbox input::placeholder{color:var(--ink-soft);font-weight:400}
.searchbox input:focus{outline:2px solid var(--mark);outline-offset:1px}
.searchbox .kbd{
  position:absolute;right:8px;top:50%;transform:translateY(-50%);
  font-family:var(--mono);font-size:10.5px;font-weight:600;letter-spacing:.06em;
  color:var(--ink-soft);border:1px solid var(--rule);padding:1px 5px;pointer-events:none;
}
.searchbox input:not(:placeholder-shown) ~ .kbd{display:none}

/* ── 전역 Part 네비 ── */
.sitenav{position:sticky;top:var(--sitebar-h);z-index:79;border-bottom:1.5px solid var(--ink);background:rgba(247,249,245,.95);backdrop-filter:saturate(160%) blur(8px)}
.sitenav .bar{height:var(--sitenav-h);display:flex;align-items:center}
.snav-list{display:flex;align-items:center;gap:3px;margin:0;padding:0;list-style:none;overflow-x:auto;scrollbar-width:none}
.snav-list::-webkit-scrollbar{display:none}
.snav-btn{
  display:inline-block;font-size:12px;font-weight:600;padding:3px 8px;line-height:1.5;
  border:1px solid transparent;color:var(--ink-soft);text-decoration:none;white-space:nowrap;
}
.snav-btn:hover{color:var(--ink);border-color:var(--rule)}
.snav-btn:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.snav-btn[aria-current="true"]{background:var(--ink);color:#fff;border-color:var(--ink)}
.snav-btn.tag{color:var(--mark);border-color:var(--rule);letter-spacing:.08em;margin-left:6px}
.snav-btn.tag:hover{color:#fff;background:var(--mark);border-color:var(--mark)}

/* ── 넓은 화면: 타임라인을 왼쪽 고정 레일로 ── */
@media (min-width:1080px){
  :root{--offset:calc(var(--chrome-h) + 18px)}

  /* 본문 전체를 레일 폭만큼 오른쪽으로 민다. 전역 막대는 화면 전체를 덮되 속 내용은 같은 자리에 둔다 */
  body{padding-left:var(--railw)}
  .sitebar,.sitenav{margin-left:calc(-1 * var(--railw));padding-left:var(--railw)}

  /* 레일이 숫자 티커와 '타임라인 ↑'의 역할을 대신한다 */
  .ticker{display:none}
  .topbar .up{display:none}
  .cardnav{display:none}

  .tl{
    position:fixed;left:0;top:var(--chrome-h);bottom:0;width:var(--railw);z-index:50;
    margin:0;padding:0;overflow-y:auto;overscroll-behavior:contain;
    background:#F4F6F0;border-right:1.5px solid var(--ink);
  }
  .tl-head{
    display:block;position:sticky;top:0;z-index:2;
    padding:11px 16px 9px;background:#F4F6F0;border-bottom:1px solid var(--rule);
  }
  .tl-head h2{font-size:14px}
  .tl-head p{display:none}
  .tl-scroll{overflow:visible;padding:0}
  .tl-track{display:block;padding:16px 14px 0;min-width:0}
  .tl-phase{position:relative;min-width:0;padding:0 0 18px 15px;border-left:1.5px solid var(--ink)}
  .tl-phase.cond{border-left-style:dashed}
  .tl-phase:last-child{border-left-color:transparent;padding-bottom:10px}
  .tl-line{
    position:absolute;left:-6.5px;top:5px;width:11px;height:11px;border-radius:50%;
    background:var(--paper);border:1.5px solid var(--ink);
  }
  .tl-phase.cond .tl-line{background:var(--paper)}
  .tl-line::before,.tl-line::after,.tl-phase:last-child .tl-line::after{display:none}
  .tl-body{padding:0}
  .tl-no{font-size:10px;letter-spacing:.12em}
  .tl-phase h3{font-size:13.5px;margin:3px 0 8px}
  .tl-sub{display:none}
  .tl-btns{gap:5px}
  .tl-btn{grid-template-columns:22px minmax(0,1fr);gap:6px;font-size:12.5px;padding:6px 8px}
  .tl-legend{
    display:block;margin:0;padding:12px 16px 22px;font-size:11.5px;line-height:1.6;
    border-top:1px solid var(--rule);
  }
  .tl-legend span{display:block}
}

@media (max-width:640px){
  :root{--sitebar-h:46px;--sitenav-h:36px}
  .sitebar .brand,.sitebar .hint{display:none}
  .searchbox{max-width:none;margin-left:0}
}
@media print{
  .sitebar,.sitenav{display:none}
  body{padding-left:0!important}
  .tl{position:static!important;display:none}
}
"""

MARKUP = """
<header class="sitebar">
  <div class="wrap bar">
    <span class="dot" aria-hidden="true"></span>
    <a class="brand" href="../index.html">나이스 업무 타임라인</a>
    <div class="searchbox">
      <input id="siteq" type="search" autocomplete="off" spellcheck="false"
             placeholder="업무카드 검색 · 예: 전입, 마감, 승인요청, 학교생활기록부"
             aria-label="업무카드 검색">
      <span class="kbd">Ctrl K</span>
    </div>
    <p class="hint">Enter를 누르면 전체 색인에서 찾습니다</p>
  </div>
</header>

<nav class="sitenav" aria-label="Part 바로가기">
  <div class="wrap bar">
    <ol class="snav-list" id="siteticks"></ol>
  </div>
</nav>
"""

SCRIPT = """<script src="../manifest.js"></script>
<script>
// 전역 상단바(Part 이동·검색)를 만들고, 왼쪽 세로 타임라인이 현재 카드를 따라가게 한다
(function(){
'use strict';
var HUB = '../index.html';

/* Part 네비 · manifest.js 목록으로 만든다 */
var list = document.getElementById('siteticks');
var here = decodeURIComponent((location.pathname.split('/').pop() || ''));
(window.NEIS_PARTS || []).forEach(function(p){
  var mine = (p.docs || []).some(function(d){ return d.f === here; });
  var li = document.createElement('li');
  var a = document.createElement('a');
  a.className = 'snav-btn' + (p.tag ? ' tag' : '');
  a.href = HUB + '#' + (p.id || ('part' + p.no));
  a.textContent = p.tag ? p.tag : ('Part ' + p.no + ' ' + p.label);
  if(mine) a.setAttribute('aria-current', 'true');
  li.appendChild(a);
  list.appendChild(li);
});

/* 검색 · 색인은 허브에만 있으므로 낱말을 들고 허브로 넘어간다 */
var q = document.getElementById('siteq');
q.addEventListener('keydown', function(e){
  if(e.key === 'Enter' && q.value.trim()) location.href = HUB + '#q=' + encodeURIComponent(q.value.trim());
});
document.addEventListener('keydown', function(e){
  if((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k'){ e.preventDefault(); q.focus(); q.select(); }
  if(e.key === 'Escape' && document.activeElement === q){ q.value = ''; q.blur(); }
});

/* 세로 레일 · 지금 보는 카드의 버튼이 레일 밖으로 밀려나지 않게 따라 내린다 */
var rail = document.querySelector('.tl');
var track = document.querySelector('.tl-track');
if(!rail || !track) return;
function follow(btn){
  if(getComputedStyle(rail).position !== 'fixed') return;
  var b = btn.getBoundingClientRect(), r = rail.getBoundingClientRect();
  if(b.top < r.top + 56) rail.scrollTop += b.top - r.top - 56;
  else if(b.bottom > r.bottom - 16) rail.scrollTop += b.bottom - r.bottom + 16;
}
new MutationObserver(function(ms){
  ms.forEach(function(m){
    if(m.target.getAttribute('aria-current') === 'true') follow(m.target);
  });
}).observe(track, {subtree:true, attributes:true, attributeFilter:['aria-current']});
})();
</script>
"""

ANCHOR_CSS = '</style>'
ANCHOR_BODY_OPEN = '<body>'
ANCHOR_BODY_CLOSE = '</body>'


def patch(path):
    s = path.read_text(encoding='utf-8')
    if MARK in s:
        return 'skip'

    for a in (ANCHOR_CSS, ANCHOR_BODY_OPEN, ANCHOR_BODY_CLOSE):
        if s.count(a) != 1:
            raise SystemExit('기준점이 1번 나오지 않음 · %s · %r' % (path.name, a))

    s = s.replace(ANCHOR_CSS, CSS + ANCHOR_CSS, 1)
    s = s.replace(ANCHOR_BODY_OPEN, ANCHOR_BODY_OPEN + '\n' + MARKUP, 1)
    s = s.replace(ANCHOR_BODY_CLOSE, SCRIPT + ANCHOR_BODY_CLOSE, 1)

    path.write_text(s, encoding='utf-8')
    return 'done'


def targets():
    if len(sys.argv) > 1:
        return [PAGES / sys.argv[1]]
    src = (ROOT / 'manifest.js').read_text(encoding='utf-8')
    out = []
    for line in src.split('\n'):
        line = line.strip()
        if line.startswith('//') or "ready: 1" not in line:
            continue
        out.append(PAGES / line.split("'")[1])
    return out


def main():
    done = skip = 0
    for path in targets():
        if not path.exists():
            print('없는 파일 ·', path.name)
            continue
        r = patch(path)
        done += (r == 'done')
        skip += (r == 'skip')
    print('패치 %d편 · 이미 적용 %d편' % (done, skip))
    return 0


if __name__ == '__main__':
    sys.exit(main())
