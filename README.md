# Day 1 · 정책이 결과를 바꾼다

정책 파일(시스템 프롬프트) 한 줄이 에이전트의 출력을 어떻게 바꾸는지 체감합니다.

## 실행
```bash
pip install -r requirements.txt
streamlit run app.py
```
- Codespaces: 우하단 **"브라우저에서 열기"**(포트 8501) 클릭
- 키·토큰 없이 동작 · 외부 API 호출 없음 · 끄기 `Ctrl + C`

## 이 Day에서 보는 것
- 회의 메모 정리 Agent — 정책 체크박스를 켜고 끄면 출력 섹션이 실시간으로 바뀜
- 정책 기반 SAST — `CLAUDE_base` ↔ `CLAUDE` 로 차량 제어 모듈이 High → Critical 로 상향
- (보너스) AI 하네스 — 같은 입력도 시스템 프롬프트(정책)를 바꾸면 AI 출력이 달라짐

## 과제
- `course/exercises/Day01_exercises.md` — 시나리오 + 기본/생성형(보일러플레이트)/도전 과제

## 자세한 가이드
- `course/day_guides/Day01.md`

