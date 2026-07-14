// CSV 매칭/조인 연산 워커 — 메인 스레드 UI가 멈추지 않도록 대용량 데이터 매칭을 여기서 처리
self.onmessage = function (e) {
  const { baseHeaders, baseRows, otherHeaders, otherRows, baseKeyIdx, otherKeyIdx, joinType, collisionSuffix } = e.data;
  const suffix = collisionSuffix || ' (2)';

  // 값 기준 키 정규화: 문자열 변환 + 앞뒤 공백 제거 (숫자/문자 혼용, 트레일링 스페이스 오차 방지)
  const normKey = v => String(v == null ? '' : v).trim();

  // 파일을 키 값 기준으로 인덱싱 — {키: [행 인덱스, ...]} 해시맵으로 O(n+m) 매칭
  function buildIndex(rows, keyIdx) {
    const idx = new Map();
    for (let i = 0; i < rows.length; i++) {
      const k = normKey(rows[i][keyIdx]);
      if (!idx.has(k)) idx.set(k, []);
      idx.get(k).push(i);
    }
    return idx;
  }

  const otherIndex = buildIndex(otherRows, otherKeyIdx);
  const baseIndex = buildIndex(baseRows, baseKeyIdx);

  // 조인 파일 헤더 중 기준 파일과 이름이 겹치면 구분되도록 접미사 부여
  const baseHeaderSet = new Set(baseHeaders);
  const otherHeadersOut = otherHeaders.map(h => (baseHeaderSet.has(h) ? h + suffix : h));
  const headers = [...baseHeaders, ...otherHeadersOut];
  const emptyOther = new Array(otherHeaders.length).fill('');
  const emptyBase = new Array(baseHeaders.length).fill('');

  const rows = [];
  let matchedBase = 0;

  // 기준 파일 → 조인 파일 매칭 (Left / Inner / Full 공통 순회)
  if (joinType === 'left' || joinType === 'inner' || joinType === 'full') {
    for (const baseRow of baseRows) {
      const key = normKey(baseRow[baseKeyIdx]);
      const matches = otherIndex.get(key);
      if (matches && matches.length) {
        matchedBase++;
        // 조인 파일 쪽 키가 중복이면 매칭되는 모든 행과 각각 결합되어 행이 늘어남
        for (const oi of matches) rows.push([...baseRow, ...otherRows[oi]]);
      } else if (joinType !== 'inner') {
        rows.push([...baseRow, ...emptyOther]);
      }
    }
  } else {
    // Right Join: 매칭 통계용으로만 기준 파일 매칭 여부를 별도 계산
    for (const baseRow of baseRows) {
      if (otherIndex.has(normKey(baseRow[baseKeyIdx]))) matchedBase++;
    }
  }

  // 조인 파일 → 기준 파일 매칭 (Right / Full 전용)
  // Full은 위 루프에서 매칭 쌍을 이미 추가했으므로, 여기서는 기준 파일과 매칭 안 된 조인 파일 행만 추가
  if (joinType === 'right' || joinType === 'full') {
    for (const otherRow of otherRows) {
      const key = normKey(otherRow[otherKeyIdx]);
      const matches = baseIndex.get(key);
      if (matches && matches.length) {
        if (joinType === 'right') {
          for (const bi of matches) rows.push([...baseRows[bi], ...otherRow]);
        }
      } else {
        rows.push([...emptyBase, ...otherRow]);
      }
    }
  }

  self.postMessage({
    headers,
    rows,
    totalBase: baseRows.length,
    matchedBase,
    unmatchedBase: baseRows.length - matchedBase,
  });
};
