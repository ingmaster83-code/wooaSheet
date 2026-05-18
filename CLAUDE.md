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
