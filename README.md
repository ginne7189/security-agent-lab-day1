# 1️⃣ security-agent-lab-day1

**Day 1 · 정책이 에이전트 출력을 통제한다** — 키 없이 버튼 클릭만으로 돌려보는 Streamlit 실습.

> 5일짜리 `security-agent-lab` 과정 중 **Day 1만** 떼어낸 독립 저장소입니다.
> (Day 2~5는 `security-agent-lab-day2to5`, 스캐닝 엔진 코어는 `security-scan-engine` 저장소)

## 무엇을 보여주나
- **Mini Lab** — 회의 메모 정리: 정책 체크박스를 켜고 끄면 결과 리포트가 즉시 바뀜
- **Main Lab** — 정책 기반 SAST: 같은 코드라도 `CLAUDE_base` ↔ `CLAUDE` 정책에 따라 차량 모듈이 High → Critical 로 상향
- **보너스** — AI 하네스: 시스템 프롬프트(정책)만 바꾸면 같은 회의록의 AI 출력이 통째로 달라짐 (키 없으면 규칙 fallback)

## 실행

```bash
pip install -r requirements.txt
streamlit run app.py
```

브라우저가 열리면 위 탭(개요 · 왜 만드나 · Day 1)을 눌러보세요. **AI 키·외부 API 호출 불필요**.

## 구성
- `app.py` / `dashboard_lib.py` — Day 1 Streamlit 대시보드
- `agents/` — `sast_agent`·`llm_client`·`masking` (스캐닝 엔진에서 가져온 코어)
- `sample_app/`·`policies/` — 점검 대상과 정책
- `course/mini_labs/day01_single_agent/` — 회의록 에이전트 미니랩
