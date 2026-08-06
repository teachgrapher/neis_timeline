# pages/의 타임라인 문서에 '연수자료 뽑기'(카드 골라 A4 인쇄) 기능을 주입하는 패치 스크립트
#
# 쓰는 법.
#   저장소 뿌리에서 python3 tools/patch_handout.py                 (매니페스트의 공개 문서 전부)
#   저장소 뿌리에서 python3 tools/patch_handout.py 파일이름.html   (그 문서 하나만)
#
# 넣은 조각을 BEGIN/END 표시로 감싸 두었으므로, 디자인을 고친 뒤 다시 돌리면
# 옛 조각을 걷어내고 새것으로 갈아 끼운다. 몇 번을 돌려도 같은 결과가 된다.
#
# 먼저 tools/patch_sitebar_rail.py 가 적용되어 있어야 한다. 전역 상단바에 메뉴를 얹기 때문이다.

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'

CSS_BEGIN = '/* == handout:begin == */'
CSS_END = '/* == handout:end == */'
HTML_BEGIN = '<!-- handout:begin -->'
HTML_END = '<!-- handout:end -->'

CSS = CSS_BEGIN + """
/* ══ 연수자료 뽑기 ══ */
:root{--hobar-h:46px}

/* 상단바 메뉴 버튼 */
.hobtn{
  margin-left:auto;font-family:var(--sans);font-size:12.5px;font-weight:600;
  padding:5px 12px;border:1.5px solid var(--ink);background:var(--sheet);color:var(--ink);
  cursor:pointer;white-space:nowrap;
}
.hobtn:hover{background:var(--ink);color:#fff}
.hobtn:focus-visible{outline:2px solid var(--mark);outline-offset:2px}
.sitebar .hint{margin-left:14px}

/* 고르는 중에 뜨는 막대 */
.hobar{display:none}
body.hoselect .hobar{
  display:block;position:sticky;top:calc(var(--sitebar-h) + var(--sitenav-h));z-index:78;
  background:var(--ink);color:#fff;
}
body.hoselect .topbar{top:calc(var(--sitebar-h) + var(--sitenav-h) + var(--hobar-h))}
body.hoselect{--chrome-h:calc(var(--sitebar-h) + var(--sitenav-h) + var(--hobar-h) + var(--topbar-h))}
.hobar .bar{height:var(--hobar-h);display:flex;align-items:center;gap:10px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none}
.hobar .bar::-webkit-scrollbar{display:none}
.hobar b{font-size:13px;font-weight:700;white-space:nowrap}
.hobar .hocount{font-family:var(--mono);font-size:12px;color:#C8CCC1;white-space:nowrap;font-variant-numeric:tabular-nums}
.hobar label{display:flex;align-items:center;gap:4px;font-size:12px;color:#DFEBDD;white-space:nowrap;cursor:pointer}
.hobar button{
  font-family:var(--sans);font-size:12px;font-weight:600;white-space:nowrap;
  padding:4px 10px;border:1px solid #5C6360;background:none;color:#fff;cursor:pointer;
}
.hobar button:hover{background:#fff;color:var(--ink);border-color:#fff}
.hobar .go{margin-left:auto;background:var(--mark);border-color:var(--mark)}
.hobar .go:hover{background:#fff;color:var(--mark)}
.hobar .go[disabled]{opacity:.4;cursor:default;background:none;border-color:#5C6360;color:#C8CCC1}

/* 카드마다 붙는 선택칸 */
.hopick{display:none}
body.hoselect .hopick{
  display:flex;align-items:center;justify-content:center;gap:5px;
  margin:10px 0 0;font-family:var(--mono);font-size:10.5px;font-weight:700;
  color:var(--ink-soft);cursor:pointer;
}
body.hoselect .hopick input{width:15px;height:15px;accent-color:var(--mark);cursor:pointer}
body.hoselect .task{transition:box-shadow .12s}
body.hoselect .task.hoon{box-shadow:0 0 0 2px var(--mark)}
body.hoselect .task.hoon .gutter{background:var(--dropout)}
@media (max-width:640px){
  body.hoselect .hopick{margin:0 0 0 auto}
}

/* 인쇄용 조각은 화면에서 감춘다 */
.pcover,.pstrip{display:none}

@media print{
  @page{size:A4;margin:13mm 14mm 15mm}
  body{print-color-adjust:exact;-webkit-print-color-adjust:exact;font-size:10.5pt}
  .sitebar,.sitenav,.hobar,.hopick,.tl{display:none!important}
  main{max-width:none;margin:0}

  /* 고른 카드만 남긴다. 뽑기를 거치지 않은 보통 인쇄는 종전 그대로다 */
  body.hoready .task:not(.hoon){display:none}
  body.hoready .pcover,body.hoready .pstrip{display:block}
  body.hoready footer{display:none}
  .pbrk{break-before:page}

  /* 표지 */
  .pcover{padding:0 0 6mm}
  .pcover .pc-eyebrow{font-family:var(--mono);font-size:9pt;letter-spacing:.14em;color:var(--mark);font-weight:700;margin:0 0 6mm}
  .pcover h1{font-size:26pt;font-weight:800;letter-spacing:-.02em;line-height:1.2;margin:0 0 4mm}
  .pcover .pc-sub{font-size:11pt;color:var(--ink-soft);margin:0 0 8mm}
  .pcover .pc-meta{border-top:1.5px solid var(--ink);border-bottom:1px solid var(--rule);padding:3mm 0;margin:0 0 8mm;font-size:9.5pt}
  .pcover .pc-meta div{margin:0 0 1.5mm}
  .pcover .pc-meta b{font-family:var(--mono);font-size:8.5pt;letter-spacing:.1em;color:var(--ink-soft);margin-right:5mm}
  .pcover h2{font-size:12pt;margin:0 0 3mm;padding-bottom:2mm;border-bottom:1.5px solid var(--ink)}
  .pcover ol{list-style:none;margin:0;padding:0;columns:2;column-gap:10mm}
  .pcover li{font-size:9.5pt;line-height:1.7;break-inside:avoid;display:flex;gap:3mm}
  .pcover li i{font-style:normal;font-family:var(--mono);font-weight:700;color:var(--mark)}
  .pcover .pc-foot{margin:8mm 0 0;padding-top:3mm;border-top:1px solid var(--rule);font-size:8.5pt;color:var(--ink-soft);line-height:1.6}

  /* 카드 위 가로 타임라인 */
  .pstrip{margin:0 0 5mm;padding:0 0 3mm;border-bottom:1.5px solid var(--ink);break-after:avoid}
  .pstrip .ps-cap{font-family:var(--mono);font-size:7.5pt;letter-spacing:.12em;color:var(--ink-soft);margin:0 0 2.5mm}
  .pstrip .ps-row{display:grid;gap:0 4mm}
  .ps-p{position:relative;border-top:1.2px solid var(--ink);padding:2.5mm 0 0}
  .ps-p.cond{border-top-style:dashed}
  .ps-p::before{content:"";position:absolute;left:0;top:-3.2px;width:6px;height:6px;border-radius:50%;background:#fff;border:1.2px solid var(--ink)}
  .ps-p .ps-no{font-family:var(--mono);font-size:6.5pt;font-weight:700;letter-spacing:.1em;color:var(--mark);margin:0}
  .ps-p .ps-h{font-size:7.5pt;font-weight:700;line-height:1.3;margin:.5mm 0 1.5mm;letter-spacing:-.01em}
  .ps-p ul{display:flex;flex-wrap:wrap;gap:1mm;list-style:none;margin:0;padding:0}
  .ps-p li{font-family:var(--mono);font-size:6.5pt;font-weight:700;padding:0 1.2mm;border:.8px solid var(--rule);color:var(--ink-soft)}
  .ps-p li.on{background:var(--ink);color:#fff;border-color:var(--ink)}

  /* 카드를 종이에 맞춘다 */
  .task{border:0;box-shadow:none;grid-template-columns:60px minmax(0,1fr);break-inside:auto}
  .gutter{padding:0;background:none;border-right:1px solid var(--rule);text-align:left}
  .gutter b{font-size:16pt}
  .body{padding:0 0 0 6mm}
  .task h3{font-size:15pt;line-height:1.3;margin:0 0 3mm;break-after:avoid}
  .desc{font-size:10pt;margin:0 0 4mm}
  .tags{margin-bottom:3mm}
  .tag{font-size:7.5pt;padding:1px 5px}
  .w6{margin:0 0 4mm;break-inside:avoid}
  .w6 dl{grid-template-columns:88px minmax(0,1fr)}
  .w6 dt{font-size:8.5pt;padding:2mm 3mm}
  .w6 dd{font-size:9.5pt;padding:2mm 0 2mm 4mm}
  .memo{break-inside:avoid;padding:3mm 4mm}
  .memo h4{font-size:8pt;margin-bottom:2mm}
  .memo li{font-size:9pt;line-height:1.6}
  .src{margin:0 0 3mm}
  .srcbtn{border:0;padding:0;margin-right:4mm;background:none;font-size:8.5pt;color:var(--ink-soft);border-radius:0}
  .srcbtn::before{content:""}
  code{font-size:8.5pt;white-space:normal}
}
""" + CSS_END

MARKUP = HTML_BEGIN + """
<div class="hobar" id="hobar" aria-label="연수자료 뽑기">
  <div class="wrap bar">
    <b>연수자료 뽑기</b>
    <span class="hocount" id="hocount">0장 선택</span>
    <button type="button" id="hoall">전체 선택</button>
    <button type="button" id="honone">해제</button>
    <label><input type="checkbox" id="hocover" checked>표지·목차</label>
    <label><input type="checkbox" id="hostrip" checked>카드마다 타임라인</label>
    <button type="button" id="hoclose">닫기</button>
    <button type="button" class="go" id="hogo" disabled>인쇄 · PDF 저장</button>
  </div>
</div>
""" + HTML_END

SCRIPT = HTML_BEGIN + """
<script>
// 업무카드를 골라 표지·가로 타임라인이 붙은 A4 연수자료로 인쇄하는 기능
(function(){
'use strict';
var body = document.body;
var cards = [].slice.call(document.querySelectorAll('article.task'));
if(!cards.length) return;

var countEl = document.getElementById('hocount');
var goBtn = document.getElementById('hogo');
var coverOpt = document.getElementById('hocover');
var stripOpt = document.getElementById('hostrip');
var picked = {};

/* 카드마다 선택칸을 붙인다 */
cards.forEach(function(card){
  var lab = document.createElement('label');
  lab.className = 'hopick';
  var box = document.createElement('input');
  box.type = 'checkbox';
  box.setAttribute('aria-label', (card.querySelector('h3') || {}).textContent || card.id);
  var txt = document.createElement('span');
  txt.textContent = '선택';
  lab.appendChild(box); lab.appendChild(txt);
  (card.querySelector('.gutter') || card).appendChild(lab);
  box.addEventListener('change', function(){ set(card, box.checked); });
  card._hobox = box;
});

function set(card, on){
  if(on) picked[card.id] = true; else delete picked[card.id];
  card.classList.toggle('hoon', on);
  if(card._hobox.checked !== on) card._hobox.checked = on;
  paint();
}
function chosen(){ return cards.filter(function(c){ return picked[c.id]; }); }
function paint(){
  var n = chosen().length;
  countEl.textContent = n + '장 선택';
  goBtn.disabled = !n;
}

/* 단계 정보는 화면 타임라인에서 그대로 읽어 온다 */
var phases = [].slice.call(document.querySelectorAll('.tl-phase')).map(function(ph){
  return {
    no: (ph.querySelector('.tl-no') || {}).textContent || '',
    title: (ph.querySelector('h3') || {}).textContent || '',
    cond: ph.classList.contains('cond'),
    items: [].slice.call(ph.querySelectorAll('.tl-btn')).map(function(b){
      return { id: b.dataset.go, n: (b.querySelector('span') || {}).textContent || '' };
    })
  };
});

function makeStrip(cardId){
  var box = document.createElement('div');
  box.className = 'pstrip';
  var cap = document.createElement('p');
  cap.className = 'ps-cap';
  cap.textContent = '업무 타임라인 · 왼쪽에서 오른쪽으로 갈수록 나중에 하는 일';
  var row = document.createElement('div');
  row.className = 'ps-row';
  row.style.gridTemplateColumns = 'repeat(' + phases.length + ',1fr)';
  phases.forEach(function(p){
    var cell = document.createElement('div');
    cell.className = 'ps-p' + (p.cond ? ' cond' : '');
    var no = document.createElement('p'); no.className = 'ps-no'; no.textContent = p.no;
    var h = document.createElement('p'); h.className = 'ps-h'; h.textContent = p.title;
    var ul = document.createElement('ul');
    p.items.forEach(function(it){
      var li = document.createElement('li');
      li.textContent = it.n;
      if(it.id === cardId) li.className = 'on';
      ul.appendChild(li);
    });
    cell.appendChild(no); cell.appendChild(h); cell.appendChild(ul);
    row.appendChild(cell);
  });
  box.appendChild(cap); box.appendChild(row);
  return box;
}

function txt(sel){ var e = document.querySelector(sel); return e ? e.textContent.trim() : ''; }

function makeCover(list){
  var box = document.createElement('div');
  box.className = 'pcover';
  var d = new Date();
  var stamp = d.getFullYear() + '. ' + (d.getMonth() + 1) + '. ' + d.getDate() + '.';

  var meta = '';
  document.querySelectorAll('.meta-strip div').forEach(function(v){
    var dt = v.querySelector('dt'), dd = v.querySelector('dd');
    if(dt && dd) meta += '<div><b>' + dt.textContent.trim() + '</b>' + dd.textContent.trim() + '</div>';
  });

  var items = list.map(function(c){
    return '<li><i>' + (c.dataset.num || '').replace(/^(\\d)$/, '0$1') + '</i><span>'
         + ((c.querySelector('h3') || {}).textContent || '').trim() + '</span></li>';
  }).join('');

  box.innerHTML =
      '<p class="pc-eyebrow">' + (txt('.eyebrow') || '나이스 업무 타임라인') + '</p>'
    + '<h1>' + (txt('.topbar b') || document.title) + '</h1>'
    + '<p class="pc-sub">업무카드 ' + list.length + '장 · 시간순 · ' + stamp + '</p>'
    + '<div class="pc-meta">' + meta + '</div>'
    + '<h2>담은 업무</h2><ol>' + items + '</ol>'
    + '<p class="pc-foot">' + txt('footer p') + '</p>';
  return box;
}

/* 인쇄 직전에 표지와 타임라인을 끼워 넣는다 */
function clean(){
  document.querySelectorAll('.pcover,.pstrip').forEach(function(n){ n.remove(); });
  cards.forEach(function(c){ c.classList.remove('pbrk'); });
}
function build(){
  clean();
  var list = chosen();
  if(!list.length) return false;
  var main = document.querySelector('main') || body;
  if(coverOpt.checked) main.insertBefore(makeCover(list), main.firstChild);
  list.forEach(function(card, i){
    var first = (i === 0) && !coverOpt.checked;
    if(stripOpt.checked){
      var s = makeStrip(card.id);
      if(!first) s.classList.add('pbrk');
      card.parentNode.insertBefore(s, card);
    }else if(!first){
      card.classList.add('pbrk');
    }
  });
  return true;
}

/* 막대 조작 */
document.getElementById('hobtn').addEventListener('click', function(){
  body.classList.add('hoselect');
});
document.getElementById('hoclose').addEventListener('click', function(){
  body.classList.remove('hoselect');
});
document.getElementById('hoall').addEventListener('click', function(){
  cards.forEach(function(c){ set(c, true); });
});
document.getElementById('honone').addEventListener('click', function(){
  cards.forEach(function(c){ set(c, false); });
});
goBtn.addEventListener('click', function(){
  if(!build()) return;
  body.classList.add('hoready');
  window.print();
});
window.addEventListener('afterprint', function(){
  body.classList.remove('hoready');
  clean();
});
document.addEventListener('keydown', function(e){
  if(e.key === 'Escape' && body.classList.contains('hoselect') && document.activeElement.id !== 'siteq'){
    body.classList.remove('hoselect');
  }
});
})();
</script>
""" + HTML_END

BTN = HTML_BEGIN + '<button type="button" class="hobtn" id="hobtn">연수자료 뽑기</button>' + HTML_END

ANCHOR_CSS = '</style>'
ANCHOR_BTN = '    <p class="hint">Enter를 누르면 전체 색인에서 찾습니다</p>'
ANCHOR_NAV_END = 'id="siteticks"></ol>\n  </div>\n</nav>\n'
ANCHOR_BODY_CLOSE = '</body>'


def strip_old(s):
    """앞서 넣은 조각을 걷어낸다. 디자인을 고쳐 다시 돌릴 수 있게 하려는 것이다."""
    s = re.sub(re.escape(CSS_BEGIN) + '.*?' + re.escape(CSS_END), '', s, flags=re.S)
    s = re.sub(re.escape(HTML_BEGIN) + '.*?' + re.escape(HTML_END), '', s, flags=re.S)
    return s


def patch(path):
    s = path.read_text(encoding='utf-8')
    again = HTML_BEGIN in s
    if again:
        s = strip_old(s)

    if 'v2-sitebar-rail' not in s:
        raise SystemExit('전역 상단바 패치가 먼저 필요함 · ' + path.name)
    for a in (ANCHOR_CSS, ANCHOR_BTN, ANCHOR_BODY_CLOSE):
        if s.count(a) != 1:
            raise SystemExit('기준점이 1번 나오지 않음 · %s · %r' % (path.name, a[:40]))
    if s.count(ANCHOR_NAV_END) != 1:
        raise SystemExit('기준점이 1번 나오지 않음 · %s · nav 끝' % path.name)

    s = s.replace(ANCHOR_CSS, CSS + '\n' + ANCHOR_CSS, 1)
    s = s.replace(ANCHOR_BTN, '    ' + BTN + '\n' + ANCHOR_BTN, 1)
    s = s.replace(ANCHOR_NAV_END, ANCHOR_NAV_END + MARKUP + '\n', 1)
    s = s.replace(ANCHOR_BODY_CLOSE, SCRIPT + ANCHOR_BODY_CLOSE, 1)

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
