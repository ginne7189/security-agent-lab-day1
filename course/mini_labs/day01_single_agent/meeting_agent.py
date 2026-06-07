#!/usr/bin/env python3
"""
회의 메모 정리 Agent (course/mini_labs/day01_single_agent/meeting_agent.py) — Day 1 Mini Lab

목표: "정책 파일이 출력 형식을 바꾼다"를 코드 수정 없이 체감한다.

- 외부 API 호출 없음 / LLM 호출 없음 / Python 표준 라이브러리만 사용
- meeting_notes.txt 를 읽어 회의 내용을 정리한다
- MEETING_AGENT.md(정책)에 적힌 섹션만 출력한다
  (정책에서 "Risks 섹션 포함" 줄을 지우면 Risks 섹션이 사라진다)

실행:
  python course/mini_labs/day01_single_agent/meeting_agent.py \
    --input course/mini_labs/day01_single_agent/meeting_notes.txt \
    --policy course/mini_labs/day01_single_agent/MEETING_AGENT.md

산출물: reports/meeting_summary.md
"""
import argparse
import os
import re

# 이 스크립트가 있는 폴더 / 저장소 루트 — 인자 없이 실행해도 기본 파일을 찾는다.
_HERE = os.path.dirname(os.path.abspath(__file__))
_REPO = os.path.dirname(os.path.dirname(os.path.dirname(_HERE)))  # day01 → mini_labs → course → repo

# (섹션 키, 정책 파일에서 이 섹션을 켜는 키워드, 리포트 제목)
# 정책 파일 본문에 키워드가 한 번이라도 등장하면 그 섹션이 출력된다.
SECTIONS = [
    ("summary", "Summary", "Summary"),
    ("action_items", "Action Items", "Action Items"),
    ("owners", "Owners", "Owners"),
    ("due_dates", "Due Dates", "Due Dates"),
    ("risks", "Risks", "Risks"),
]

# 구두(대화체) 회의록 파싱용 — "이름: 발언" 형태에서 키워드로 항목을 분류한다.
_SPEAKER_RE = re.compile(r"^\s*([가-힣A-Za-z]{2,5})\s*[:：]\s*(.+)$")
_DUE_RES = [
    re.compile(r"\d{4}-\d{2}-\d{2}"),
    re.compile(r"\d{1,2}\s?월\s?\d{1,2}\s?일"),
    re.compile(r"\d{1,2}\s?일\s?까지"),
    re.compile(r"(?:다음|이번|다다음)\s?주"),
    re.compile(r"내일|모레|오늘"),
]
_ACTION_CUES = ("추가", "작성", "맡", "확인", "준비", "공유", "등록", "통과", "할게요", "할게", "하기로")
_RISK_CUES = ("위험", "리스크", "우려", "걱정", "문제", "실패", "지연", "노출", "막힐")
_SUMMARY_CUES = ("정리하면", "결론", "핵심은", "방향", "우선순위", "합의", "결정")
_SKIP_KEYS = ("일시", "장소", "참석", "회의", "안건", "날짜")


def _find_due(text):
    for rx in _DUE_RES:
        m = rx.search(text)
        if m:
            return m.group(0).strip()
    return None


def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _parse_notes(text):
    """구두(대화체) 회의록을 섹션별로 추출한다.

    'OO: 발언' 형태를 읽어 키워드로 분류한다 — 위험/액션/요약. 잡담(인사·점심 등)은 버린다.
    (LLM 없이 표준 라이브러리 규칙만으로 동작 = '에이전트는 규칙으로도 만들 수 있다'를 보여줌)
    """
    summary, actions, owners, dues, risks = [], [], [], [], []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _SPEAKER_RE.match(line)
        speaker, said = (m.group(1), m.group(2).strip()) if m else (None, line)
        if speaker in _SKIP_KEYS:           # 머리말(일시/참석 등) 건너뛰기
            continue
        if any(c in said for c in _RISK_CUES):
            risks.append(said)
        elif any(c in said for c in _ACTION_CUES):
            actions.append(said)
            if speaker:
                owners.append(speaker)
            d = _find_due(said)
            if d:
                dues.append(d)
        elif any(c in said for c in _SUMMARY_CUES):
            summary.append(said)
        # 그 외(잡담)는 리포트에서 제외 → 에이전트가 '걸러낸다'는 걸 보여줌
    return {
        "summary": summary,
        "action_items": actions,
        "owners": sorted(set(owners)),
        "due_dates": sorted(set(dues)),
        "risks": risks,
    }


def _enabled_sections(policy_text):
    """정책 본문에 키워드가 있는 섹션만 (키, 제목) 으로 반환."""
    enabled = []
    for key, keyword, title in SECTIONS:
        if keyword.lower() in policy_text.lower():
            enabled.append((key, title))
    return enabled


def build_report(data, enabled):
    lines = ["# 회의 정리 리포트 (Day 1 Mini Lab)", ""]
    lines.append(f"> 출력 섹션은 정책 파일이 결정합니다 — 활성 섹션 {len(enabled)}개")
    lines.append("")
    for key, title in enabled:
        lines.append(f"## {title}")
        items = data.get(key, [])
        if not items:
            lines.append("- (해당 항목 없음)")
        else:
            for it in items:
                lines.append(f"- {it}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description="회의 메모 정리 Agent (Day 1 Mini Lab)")
    # 인자를 안 줘도 같은 폴더의 기본 파일을 사용한다 → `python meeting_agent.py` 만으로 실행 가능
    ap.add_argument("--input", default=os.path.join(_HERE, "meeting_notes.txt"), help="회의 메모 txt 경로")
    ap.add_argument("--policy", default=os.path.join(_HERE, "MEETING_AGENT.md"), help="출력 정책 MEETING_AGENT.md 경로")
    ap.add_argument("--out", default=os.path.join(_REPO, "reports", "meeting_summary.md"))
    args = ap.parse_args()

    notes = _read(args.input)
    policy = _read(args.policy)
    data = _parse_notes(notes)
    enabled = _enabled_sections(policy)
    report = build_report(data, enabled)

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(report)

    titles = ", ".join(t for _, t in enabled) or "(없음)"
    print(f"[MeetingAgent] 정책 적용 — 활성 섹션: {titles}")
    print(f"[MeetingAgent] 산출물 저장 → {args.out}")
    if not any(k == "risks" for k, _ in enabled):
        print("  ↳ 정책에 'Risks 섹션 포함'이 없어 Risks 섹션을 출력하지 않았습니다.")


if __name__ == "__main__":
    main()
