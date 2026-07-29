# 나이스 업무 타임라인

Part 1~9로 나뉜 나이스 업무 타임라인 문서 51편을 모아 두고, 업무카드 단위로 검색해 바로 이동하는 색인 사이트다.

## 폴더 구조

```
/
├─ index.html          허브 (Part 목록 + 검색)
├─ manifest.js         Part 구성과 문서 목록
├─ pages/              타임라인 · FAQ html 원본
│   ├─ 나이스_학교업무분장_권한관리_타임라인_v1.html
│   ├─ 나이스_학교교육과정_편성_타임라인_v1.html
│   └─ 나이스_학급담임교사_편성_타임라인_v1.html
├─ templates/          복사해서 쓰는 FAQ 틀
│   └─ 나이스_FAQ_모음_v1.html
├─ checklist.md
└─ context-notes.md
```

`pages/`는 하위 폴더 없이 평평하게 둔다. Part 구분은 폴더가 아니라 `manifest.js`가 한다.

## 배포

1. 이 폴더 전체를 GitHub 저장소에 올린다.
2. Vercel에서 New Project → 그 저장소를 고른다.
3. Framework Preset은 **Other**, Build Command는 비워 둔다. 빌드 과정이 없는 정적 사이트다.
4. Deploy를 누르면 끝이다.

## 문서 한 편 추가하기

1. html 파일을 `pages/`에 넣는다.
2. `manifest.js`에서 그 파일의 `ready: 0`을 `ready: 1`로 바꾼다.
3. 커밋하고 밀어 넣으면 Vercel이 알아서 다시 배포한다.

목록에 없는 새 파일이라면 해당 Part의 `docs` 배열에 아래 한 줄을 넣으면 된다.

```js
{ f: '파일이름.html', ready: 1 },
```

파일 이름은 실제 이름과 글자 하나까지 같아야 한다. 버튼에 "읽지 못함"이 뜨면 대개 이름이 어긋난 경우다.

## FAQ 한 편 추가하기

FAQ도 Part와 똑같은 구조로 굴러간다. 다만 배지가 'Part N' 대신 'FAQ'로 붙는다.

1. `templates/나이스_FAQ_모음_v1.html` 을 `pages/` 로 복사한다.
2. 파일 안의 `<article class="task">` 예시 카드 두 개를 실제 질문으로 바꾼다. 카드를 통째로 복사해 붙이고 `id="t3"`, `data-num="3"` 처럼 번호만 올리면 된다.
3. `manifest.js` 의 FAQ 묶음에서 `ready: 0` 을 `1` 로 바꾼다.

질문 목록은 카드에서 자동으로 만들어지므로 따로 손대지 않아도 된다.
주제를 나눠 여러 편으로 가려면 파일을 복사해 이름만 바꾸고 FAQ 묶음의 `docs` 에 한 줄씩 늘리면 된다.

```js
{ f: '나이스_FAQ_성적_v1.html', ready: 1 },
```

## 로컬에서 확인하기

html 파일을 더블클릭해서 열면 브라우저가 다른 파일 읽기를 막아 **검색이 동작하지 않는다.** 간단한 서버를 띄워야 한다.

```bash
python -m http.server 8000
```

그 뒤 브라우저에서 `http://localhost:8000` 으로 접속한다.

## 쓰는 법

- Part 버튼을 눌러 문서로 들어간다.
- 위 검색창에 낱말을 넣으면 51편 전체의 업무카드에서 찾아 해당 카드로 바로 이동한다.
- 낱말을 띄어 쓰면 둘 다 들어 있는 카드만 걸러진다.
- `Ctrl+K`로 검색창 이동, `Esc`로 검색어 지우기, `↑` `↓`로 결과 사이 이동.

---

created by MSK
