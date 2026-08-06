# pages/의 문서에서 업무카드 목록을 뽑아 cards.js(카드 벽이 읽는 자료)를 만드는 스크립트
#
# 쓰는 법.
#   저장소 뿌리에서 python3 tools/build_cards.py
#
# 문서를 고치거나 새로 넣은 뒤에는 이 스크립트를 다시 돌려야 cards.html 에 반영된다.
# 뽑아 두는 것은 카드 벽에 필요한 최소한이다. 제목, 원문 번호, 담당자, 어느 문서·어느 Part인지.
# 본문까지 담으면 파일이 커지고, 검색은 허브가 따로 하고 있으므로 넣지 않는다.

import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGES = ROOT / 'pages'
OUT = ROOT / 'cards.js'

# 같은 역할인데 원문 표기가 갈린 것만 한쪽으로 모은다. index.html 의 ROLE_ALIAS 와 같은 표를 쓴다
ROLE_ALIAS = {
    '담임교사': '학급담임교사',
    '보건업무담당자': '보건담당자',
    '학교업무분장관리자': '학교업무분장관리담당자',
    '동아리업무담당교사': '동아리담당교사',
}

ART = re.compile(r'<article\s+class="task"([^>]*)>(.*?)</article>', re.S)
ATTR = re.compile(r'([\w-]+)="([^"]*)"')
H3 = re.compile(r'<h3[^>]*>(.*?)</h3>', re.S)
TAGS = re.compile(r'<[^>]+>')


def label_of(fname):
    """파일 이름에서 화면에 쓸 문서 제목을 만든다. index.html 의 labelOf 와 같은 규칙이다."""
    s = re.sub(r'\.html$', '', fname, flags=re.I)
    s = re.sub(r'^나이스[_ ]', '', s)
    s = re.sub(r'[_ ]타임라인[_ ]v\d+$', '', s)
    s = re.sub(r'[_ ]v\d+$', '', s)
    return s.replace('_', ' ').strip()


def read_manifest():
    """매니페스트에서 Part 순서와 각 Part의 공개 문서 목록을 읽는다."""
    src = (ROOT / 'manifest.js').read_text(encoding='utf-8')
    src = re.sub(r'^\s*//.*$', '', src, flags=re.M)          # 주석 줄은 걷어낸다
    body = src[src.index('window.NEIS_PARTS'):]

    parts = []
    for chunk in re.findall(r'\{\s*(?:no|tag):.*?\n\s*\}', body, re.S):
        no = re.search(r'no:\s*(\d+)', chunk)
        tag = re.search(r"tag:\s*'([^']*)'", chunk)
        label = re.search(r"label:\s*'([^']*)'", chunk)
        docs = [f for f, ready in re.findall(r"f:\s*'([^']*)'\s*,\s*ready:\s*(\d)", chunk) if ready == '1']
        if not docs:
            continue
        parts.append({
            'no': int(no.group(1)) if no else 0,
            'tag': tag.group(1) if tag else '',
            'label': label.group(1) if label else '',
            'docs': docs,
        })
    return parts


def roles_of(raw):
    out = []
    for t in raw.split():
        r = ROLE_ALIAS.get(t, t)
        if r not in out:
            out.append(r)
    return out


def main():
    parts = read_manifest()
    cards = []
    docs = []
    missing = []

    for p in parts:
        pname = p['tag'] or ('Part %d %s' % (p['no'], p['label']))
        for f in p['docs']:
            path = PAGES / f
            if not path.exists():
                missing.append(f)
                continue
            s = path.read_text(encoding='utf-8')
            di = len(docs)
            n = 0
            for attrs, inner in ART.findall(s):
                a = dict(ATTR.findall(attrs))
                h = H3.search(inner)
                if not a.get('id') or not h:
                    continue
                cards.append({
                    'd': di,
                    'i': a['id'],
                    'n': a.get('data-num', ''),
                    't': TAGS.sub('', h.group(1)).strip(),
                    'w': roles_of(a.get('data-who', '')),
                })
                n += 1
            docs.append({'f': f, 't': label_of(f), 'p': pname, 'n': n})

    if missing:
        print('없는 파일 ·', ', '.join(missing))

    payload = {'built': date.today().isoformat(), 'docs': docs, 'cards': cards}
    OUT.write_text(
        '// 문서에서 뽑아낸 업무카드 목록. 손으로 고치지 말고 tools/build_cards.py 를 돌려 다시 만든다\n'
        'window.NEIS_CARDS = ' + json.dumps(payload, ensure_ascii=False, separators=(',', ':')) + ';\n',
        encoding='utf-8')

    roles = {}
    for c in cards:
        for r in c['w']:
            roles[r] = roles.get(r, 0) + 1
    print('문서 %d편 · 카드 %d장 · 담당자 %d종 · %.0fKB'
          % (len(docs), len(cards), len(roles), OUT.stat().st_size / 1024))
    empty = [c for c in cards if not c['w']]
    if empty:
        print('담당자 표기가 없는 카드 %d장' % len(empty))


if __name__ == '__main__':
    main()
