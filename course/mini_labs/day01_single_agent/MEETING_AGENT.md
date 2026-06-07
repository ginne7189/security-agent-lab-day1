# MEETING_AGENT 출력 정책 (course/mini_labs/day01_single_agent/MEETING_AGENT.md)

이 파일은 회의 메모 정리 Agent의 **출력 형식**을 통제하는 정책 파일입니다.
아래 "출력 섹션" 목록에 적힌 섹션만 리포트에 포함됩니다.
줄을 지우거나 추가하면, 코드 수정 없이 출력 형식이 바뀝니다.

## 출력 섹션
- Summary 섹션 포함
- Action Items 섹션 포함
- Owners 섹션 포함
- Due Dates 섹션 포함
- Risks 섹션 포함

## 실험 안내
- 위 "Risks 섹션 포함" 줄을 삭제하고 다시 실행하면, 리포트에서 Risks 섹션이 사라집니다.
- 어떤 섹션이든 줄을 지우면 그 섹션만 빠집니다(코드는 그대로).

> 연결: 여기서 MEETING_AGENT.md 로 "출력 기준"을 통제한 것처럼,
> Day 1 본 실습에서는 policies/CLAUDE.md 로 보안 Agent 의 "판단 기준"을 통제합니다.
