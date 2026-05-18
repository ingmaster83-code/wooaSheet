# WooaSheet 프로젝트 지침

## 프로젝트 개요
- **사이트명:** WooaSheet
- **URL:** https://wooasheet.wooahouse.com
- **배포:** GitHub Pages (main 브랜치 → root)
- **테마 색상:** #16A34A (green-600)

## 기술 스택
- 순수 HTML / CSS / JS (프레임워크 없음)
- **Handsontable@14** — 스프레드시트 UI (`licenseKey: 'non-commercial-and-evaluation'`)
- **HyperFormula@2.6.0** — 수식 엔진 (`licenseKey: 'gpl-v3'`)
- **SheetJS (xlsx@0.18.5)** — CSV / Excel 읽기·쓰기
- **Chart.js@4.4.0** — 차트 생성
- **JSZip@3.10.1** — ZIP 다운로드

## 서비스 목적
브라우저에서 서버 업로드 없이 CSV/Excel 파일을 편집·변환·시각화·관리하는 무료 도구 모음.

## 도구 목록
| 파일 | 기능 |
|------|------|
| editor.html | Handsontable + HyperFormula 스프레드시트 편집기 |
| csv-excel.html | CSV ↔ Excel 상호 변환 |
| chart.html | CSV 데이터로 막대/꺾은선/원형/도넛 차트 생성 |
| deduplicate.html | CSV/Excel 중복 행 제거 |
| merge-csv.html | 여러 CSV 병합 |
| split-csv.html | CSV 분할 → ZIP 다운로드 |

## 작업 규칙
- 새 도구 추가 시: index.html 카드 + sitemap.xml + en/ 영문 페이지 + footer 링크
- 다운로드 버튼 id: `downloadBtn`, `convertBtn`, `processBtn`, `mergeBtn`, `splitBtn`
- CSS/JS 변경 시 sw.js CACHE_NAME 버전 올리기 (현재: wooasheet-v1)
- 영문 페이지는 en/ 폴더, CSS/JS 경로는 `../` 상대경로

## 도구 페이지 레이아웃 (KO/EN 동일 구조 필수)

### 올바른 HTML 구조
```html
<!-- 모바일 상단 광고 -->
<div class="mobile-top-ad">
  <ins class="adsbygoogle" ... data-ad-slot="7080296704" ...></ins>
  <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
</div>

<!-- 본문 + 사이드바 -->
<div class="page-with-sidebar">
  <div class="tool-page">
    <div class="breadcrumb"><a href="[../]index.html">Home</a><span>›</span>도구명</div>
    <div class="tool-header">
      <div class="tool-icon-lg">🔧</div>
      <div><h1>도구명</h1><p>설명</p></div>
    </div>
    <div class="panel">
      <div class="drop-zone" id="dropZone">
        <span class="drop-zone-icon">🔧</span>
        <h3>파일을 여기에 끌어다 놓으세요</h3>
        <p>지원 형식 · 최대 크기</p>
        <label for="fileInput" class="btn-select">파일 선택</label>
        <input type="file" id="fileInput" ... style="display:none">
      </div>
    </div>
    <div id="configPanel" class="hidden">
      <div class="panel">
        <!-- 설정 옵션 -->
        <button class="btn btn-primary btn-full" id="downloadBtn">⬇️ 다운로드</button>
      </div>
    </div>
    <div class="tips-panel"><h3>💡 Tips</h3><ul><li>...</li></ul></div>
    <!-- FAQ (details/summary) -->
  </div>
  <aside class="tool-sidebar">
    <div class="ad-card">
      <ins class="adsbygoogle" style="display:block;width:100%;min-height:250px"
        data-ad-client="ca-pub-6464921081676309" data-ad-slot="1419180025"
        data-ad-format="auto" data-full-width-responsive="true"></ins>
      <script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>
    </div>
    <div class="ad-card">
      <script src="https://ads-partners.coupang.com/g.js"></script>
      <script>new PartnersCoupang.G({"id":986943,"template":"carousel","trackingCode":"AF5600192","width":"160","height":"200","tsource":""});</script>
    </div>
  </aside>
</div>
```

### 버튼 클래스 (WooaSheet style.css 기준)
- `btn btn-primary` — 주요 액션 버튼 (초록)
- `btn btn-secondary` — 보조 버튼 (회색)
- `btn-full` — 전체 너비
- `btn-select` — 파일 선택 label

### EN 페이지 주의사항
- KO 페이지와 **완전히 동일한 HTML 구조** 사용 (클래스, JS 아이디 동일)
- 텍스트(label, placeholder, 안내문, Tips, FAQ)만 영문으로 번역
- CSS 경로: `../css/style.css`, JS 경로: `../js/pwa-install.js`
- lang-switcher: KO 링크 = `../파일명.html`, EN 링크 = `파일명.html`
