# Day 1 과제 — 정책/하네스 (TDD · Output Schema · Secret Masking)
> PPT 개념: TDD · Output Schema · Secret Masking Contract

## 🎬 시나리오
신입이 만든 점검 리포트가 **매번 형식이 다르고 비밀값이 그대로 노출**된다.
출력을 **'계약(Output Schema)'으로 고정**하고, **테스트 먼저**로 사고를 막아라.

## 🟢 기본 과제 (5~10분)
1. `course/mini_labs/day01_single_agent/meeting_notes.txt` 에 발언 한 줄 추가
   (예: `현우: 로그 보관 정책도 정리할게요`) → 다시 실행해 자동 분류되는지 확인.
2. `MEETING_AGENT.md` 에서 `- Risks 섹션 포함` 줄을 지웠다 살렸다 → 출력 변화 확인.
3. `policies/CLAUDE.md` 에 규칙 1줄 추가 후 SAST 재실행 → 심각도/결과 변화 확인.

## 🏗 생성형 과제 — '코드를 만드는 코드' (10~20분)
보일러플레이트 생성기로 **SAST가 놓치는 CWE-532(민감정보 로깅) 에이전트**를 만들어라.
```bash
python scripts/new_agent.py authlog \
  --cwe CWE-532 --title "민감정보 로깅" --pattern "logging.*(token|password)"
python agents/authlog_agent.py --target sample_app/        # 생성된 에이전트 실행
python -m pytest tests/test_authlog_agent.py               # 생성된 테스트 통과
```

## 🧪 TDD 과제
1. `tests/test_authlog_agent.py` 에 실패 테스트부터 추가 → `pytest` 로 **빨강** 확인.
2. 규칙을 보완해 **초록**으로 만들기 (탐색→테스트→구현 순서 체험).

## 🔥 도전 과제
`meeting_agent.py` 의 `_parse_notes` 에 **'의사결정(Decisions)' 섹션**을 새로 만들어 분류 추가.

## ✅ 완료 체크
- [ ] 정책 토글로 출력이 바뀌는 걸 확인
- [ ] `new_agent.py` 로 새 에이전트 생성·실행·테스트
- [ ] 마스킹 계약 테스트 `pytest tests/test_masking_contract.py` 초록
