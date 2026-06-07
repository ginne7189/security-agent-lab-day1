# Day 1 — Security by Design · Harness 기초

> ⚠️ **이 가이드는 전체 모노레포(security-agent-lab) 기준 CLI 실습 설명입니다.**
> 단독 Day 저장소에서는 README의 `streamlit run app.py`(버튼 클릭 실습)만 쓰면 됩니다.
> `check_env.py`·`scripts/`·`orchestrator/`·`mcp_servers/` 는 모노레포에만 있습니다(이 저장소에는 없음).
> `agents/`·`course/mini_labs/`·`policies/`·`sample_app/` 명령은 이 저장소에서도 그대로 동작합니다.


## 오늘의 목표
- "정책 파일이 Agent 의 행동을 통제한다"는 감각을 잡는다.
- 단일 SAST Agent 로 sample_app 을 점검하고, 정책 전/후 결과 차이를 재현한다.

---

## Mini Lab — 회의 메모 정리 Agent
- **목적**: 정책 파일(MEETING_AGENT.md)이 코드 수정 없이 출력 형식을 바꾸는 것을 체감
- **실행 명령**
  ```bash
  python course/mini_labs/day01_single_agent/meeting_agent.py \
    --input course/mini_labs/day01_single_agent/meeting_notes.txt \
    --policy course/mini_labs/day01_single_agent/MEETING_AGENT.md
  ```
- **산출물**: `reports/meeting_summary.md`
- **확인 포인트**: Summary/Action Items/Owners/Due Dates/Risks 섹션이 정책대로 출력되는가? `Risks 섹션 포함` 줄을 지우면 Risks 가 사라지는가?
- **본 실습 연결**: MEETING_AGENT.md 로 출력 기준을 통제한 것처럼, 본 실습은 **policies/CLAUDE.md** 로 보안 판단 기준을 통제한다.
- 자세히: `course/experiments/day01_single_agent_experiment.md`

---

## Main Lab — 단일 SAST Agent + 정책 전/후 비교
- **목적**: CLAUDE 정책이 보안 점검 결과(심각도 가중)를 바꾸는 것을 확인
- **실행 명령**
  ```bash
  python agents/sast_agent.py --target sample_app/ --policy policies/CLAUDE_base.md  # 정책 전
  python agents/sast_agent.py --target sample_app/ --policy policies/CLAUDE.md       # 정책 후
  python scripts/run_lab1_policy_compare.py --target sample_app/                      # 전후 비교 자동화
  python scripts/run_lab1_schema_demo.py --target sample_app/                         # 출력 스키마 고정
  ```
- **산출물**: `reports/lab1_sast.md`, `reports/lab1_policy_compare.md`, `reports/lab1_schema.md`
- **확인 포인트**: control/ 모듈 발견이 정책 후 High → Critical 로 상향되는가? 정답지 9종 중 8종 탐지 + 1종(CWE-532) 의도적 누락을 이해했는가?

---

## 선택 보조: Claude/GPT 저토큰 활용
- 전체 코드베이스를 넣지 않는다.
- `python scripts/make_light_context_pack.py --day 1` 로 `reports/context_pack_day1.md` 만 생성해 복사한다.
- "이 SAST 리포트에서 누락된 설명 3개만 찾아줘" 수준으로 가볍게 사용한다.

---

## 완료 체크리스트
- [ ] `reports/meeting_summary.md` 생성 + Risks 토글 확인
- [ ] `reports/lab1_sast.md` 생성
- [ ] 정책 전/후 control/ 심각도 변화 재현
- [ ] CLAUDE.md 가 "판단 기준"을 통제한다는 개념 이해
