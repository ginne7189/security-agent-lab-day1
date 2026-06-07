"""대시보드 공용 렌더 모듈 — 키 없이 동작 · 외부 API 호출 없음."""
import importlib.util
import json
import os
import random
import sys

import streamlit as st

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
os.chdir(ROOT)


def _load(path, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(ROOT, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


ma = _load("course/mini_labs/day01_single_agent/meeting_agent.py", "ma")
from agents import sast_agent, llm_client  # noqa: E402

AI_POLICIES = {
    "📋 액션 비서": "당신은 회의록 정리 비서입니다. 회의 내용에서 'Action Items'만 골라 "
                   "담당자와 마감일을 포함해 불릿(-)으로만 출력하세요. 그 외 설명은 쓰지 마세요.",
    "⚠️ 리스크 분석가": "당신은 리스크 분석가입니다. 회의 내용에서 위험요소(Risks)만 최대 3개, "
                      "한 줄씩 불릿(-)으로 출력하세요. 그 외 내용은 쓰지 마세요.",
    "✏️ 한 줄 요약가": "당신은 요약 전문가입니다. 이 회의의 핵심을 정확히 한 문장으로만 요약하세요.",
}

# Day 1 '카톡 답장 톤 봇' — 같은 메시지, '톤(정책)'만 바꾸면 답장이 통째로 바뀐다
TONE_POLICIES = {
    "🩷 다정함": "당신은 다정하고 따뜻한 메신저 비서입니다. 아래 메시지를 의미는 그대로 두되 "
               "받는 사람이 기분 좋아지도록 부드럽고 다정한 말투로, 이모지를 적절히 섞어 한국어로 다시 써주세요.",
    "😏 츤데레": "당신은 츤데레 말투입니다. 아래 메시지를 의미는 그대로 두되 겉으론 툴툴대지만 "
               "속은 챙겨주는 츤데레 톤으로 한국어로 다시 써주세요.",
    "💼 비즈니스": "당신은 정중한 비즈니스 메신저 비서입니다. 아래 메시지를 의미는 그대로 두되 "
                "격식 있고 프로페셔널한 존댓말로 다시 써주세요.",
    "🤙 MZ 인싸": "당신은 MZ 인싸 말투입니다. 아래 메시지를 의미는 그대로 두되 요즘 유행어·줄임말과 "
                "이모지를 섞은 발랄한 톤으로 한국어로 다시 써주세요.",
}

# AI 키가 없을 때 보여줄 결정론적 fallback (진짜 LLM은 아니지만 '톤이 바뀐다'를 체감)
TONE_FALLBACK = {
    "🩷 다정함": lambda m: f"{m} 😊 언제든 편하게 말해줘요, 항상 응원할게요 💕",
    "😏 츤데레": lambda m: f"흥, {m}… 뭐 딱히 너 생각해서 그런 건 아니거든? 😤",
    "💼 비즈니스": lambda m: f"안녕하세요. {m} 확인 부탁드립니다. 감사합니다.",
    "🤙 MZ 인싸": lambda m: f"ㅇㅈ? {m} ㄹㅇ 핵인싸각 ㅋㅋ 🔥",
}

# Day 1 단일 에이전트(Meeting Agent) 구조도 — 입력 → [정책·파서·리포트] → 출력
_DAY1_AGENT_DOT = '''
digraph G {
  rankdir=LR;
  bgcolor="transparent";
  node [shape=box, style="rounded,filled", fontname="sans-serif", fontsize=11, color="#cbd5e1"];
  edge [color="#94a3b8", fontname="sans-serif", fontsize=10];

  input  [label="📥 입력\\n회의 메모(원문)\\n· 기본 예시 또는 업로드 파일", fillcolor="#eef2ff"];
  output [label="📤 출력\\n회의 정리 리포트(Markdown)", fillcolor="#dcfce7"];

  subgraph cluster_agent {
    label="🤖 단일 에이전트 (Meeting Agent)";
    fontname="sans-serif"; fontsize=12; labelloc="t";
    style="rounded,dashed,filled"; fillcolor="#f8fafc"; color="#64748b";
    policy [label="① 정책\\nSECTIONS 체크박스\\n(무엇을 낼지 결정)", fillcolor="#fff7ed"];
    parse  [label="② 파서\\n_parse_notes()\\n(문장 → 섹션 분류)", fillcolor="#ffffff"];
    build  [label="③ 리포트 작성\\nbuild_report()\\n(허용 섹션만 출력)", fillcolor="#ffffff"];
    parse -> build;
    policy -> build [style=dashed, label="필터"];
  }
  input -> parse;
  build -> output;
}
'''


def render_overview():
    st.subheader("👋 이 대시보드는 '데모 실행기'예요")
    st.markdown(
        "AI 에이전트로 **코드·보안 취약점 점검을 자동화**하는 5일 실습을, "
        "터미널 없이 **버튼 클릭**으로 직접 돌려봅니다."
    )

    st.markdown("#### 🧭 사용법 — 딱 3단계")
    s1, s2, s3 = st.columns(3)
    s1.info("**① 위 탭 선택**\n\n🤔 왜 만드나 · Day 1~5 중 하나 클릭")
    s2.info("**② 버튼 누르기**\n\n각 탭의 파란 버튼(🔍 🧰 🐞 🚀 …)을 클릭")
    s3.info("**③ 결과 확인**\n\n표·차트·메시지가 화면에 바로 나타남")

    st.markdown("#### ✨ '뭐가 바뀌는지' 눈으로 보이는 곳 (먼저 가보세요)")
    st.markdown(
        "- **🤔 왜 만드나?** 탭 → 버튼 여러 번 클릭 → *왼쪽(그냥 LLM)은 숫자가 흔들리고 비밀이 새고, "
        "오른쪽(에이전트)은 항상 똑같고 안전* 한 게 **나란히** 보여요.\n"
        "- **Day 1** 탭 → 정책 **체크박스를 껐다 켜면** 결과 리포트가 **즉시** 바뀝니다.\n"
        "- **Day 1** 탭 → SAST 정책을 `CLAUDE_base` ↔ `CLAUDE` 로 바꾸면 차량모듈이 **High → Critical** 로 올라가요."
    )
    st.success("👆 위 두 곳이 '에이전트가 무엇을, 어떻게 바꾸는지' 가장 빨리 체감되는 지점이에요.")

    st.markdown("#### 🤖 어떤 에이전트가 'AI(LLM)를 부르나'?")
    key_on = bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY"))
    st.dataframe([
        {"구성요소": "SAST · Secret · Dependency · Threat · Report", "종류": "⚙️ 규칙(결정론)", "AI 호출": "❌ (키 없이 항상 동작)"},
        {"구성요소": "llm_client · run_llm_interpret", "종류": "🧠 AI 해석(선택)", "AI 호출": "✅ 키 있을 때만 (없으면 규칙 fallback)"},
    ], width="stretch", hide_index=True)
    if key_on:
        st.info("🧠 현재 **AI 키 감지됨** → 해석 레이어가 LLM을 부릅니다.")
    else:
        st.warning("⚙️ 현재 **AI 키 없음** → 5개 에이전트는 전부 **규칙(LLM 없이)** 으로 동작합니다. "
                   "그래도 모든 실습이 끝까지 돌아가요. (키를 넣으면 🧠 해석만 추가됨)")
    st.caption("흐름: ⚙️ 규칙 에이전트가 '발견' → (선택) 🧠 AI가 그 발견을 자연어로 '해석'.")

    with st.expander("📐 전체 구조 그림 보기"):
        arch = os.path.join(ROOT, "docs/diagrams/01_architecture.png")
        if os.path.exists(arch):
            st.image(arch, caption="전체 아키텍처", width="stretch")


def render_why():
    st.subheader("🤔 왜 'LLM 그냥 쓰기'가 아니라 '에이전트를 만드나'?")
    st.markdown(
        "**LLM = 엄청 똑똑한 신입사원** 🧑‍💻\n\n"
        "그냥 \"보안 점검해줘\" 하고 맡기는 것 vs **매뉴얼·검수·결재선·기록을 붙인 것**.\n\n"
        "아래 버튼으로 **같은 일을 두 방식으로** 시켜보세요 👇 (여러 번 눌러보세요!)"
    )
    if st.button("🎬 같은 일, 두 방식으로 시켜보기!", key="why_btn"):
        full = sast_agent.run("sample_app/", "policies/CLAUDE.md")
        raw_secret = next(
            (l.strip() for l in open("sample_app/vulnerability.py", encoding="utf-8")
             if "API_TOKEN" in l and '"' in l and not l.strip().startswith("#")),
            'API_TOKEN = "..."')
        left, right = st.columns(2)
        with left:
            st.markdown("### 😱 그냥 LLM한테 시킴")
            wobble = random.randint(max(1, len(full) - 4), len(full))
            st.error(f"이번엔 **{wobble}건** 찾았대요 🎲 (또 누르면 숫자 바뀜)")
            st.markdown("**비밀값도 그대로 뱉음:**")
            st.code(raw_secret, language="python")
            st.markdown("📋 감사 기록 **없음**  ·  🤥 틀려도 **그냥 통과**")
            st.caption("→ 매번 답이 달라서 못 믿어요.")
        with right:
            st.markdown("### 😎 울타리 친 에이전트 (이 repo)")
            st.success(f"항상 **{len(full)}건** ✅ (몇 번 눌러도 똑같음)")
            st.markdown("**비밀값은 자동 마스킹:**")
            masked = next((r["evidence"] for r in full if "CWE-798" in r["cwe"]), 'API_TOKEN = "****"')
            st.code(masked, language="python")
            st.markdown("📋 감사 로그 1줄 자동 생성:")
            st.code('{"agent":"sast","action":"scan","outcome":"9 findings"}', language="json")
            st.caption("→ 정책·마스킹·검증·감사가 보장돼요.")
        st.info("**핵심**: 실무 AI는 LLM을 '쓰는' 게 아니라 **'울타리로 가둬 믿게 만드는'** 일! "
                "그 울타리를 만드는 게 = **에이전트 엔지니어링** (이 과정의 진짜 주제) 🎯")
    st.markdown("---")
    st.markdown(
        "| | 😱 그냥 LLM | 😎 에이전트 |\n|---|---|---|\n"
        "| 결과 | 매번 다름 🎲 | 항상 같음 ✅ |\n"
        "| 비밀값 | 줄줄 샘 🔓 | 마스킹 🔒 |\n"
        "| 틀리면 | 그냥 통과 | 재시도/차단 🛡️ |\n"
        "| 위험 행동 | 막 실행 | 사람 승인 ✋ |\n"
        "| 기록 | 없음 | 감사 로그 📋 |"
    )


def render_day1():
    st.subheader("Day 1 · 정책이 결과를 바꾼다")

    with st.expander("🧩 이 실습의 '단일 에이전트' 구조 — 어디서 무슨 일을 하나", expanded=True):
        st.graphviz_chart(_DAY1_AGENT_DOT)
        st.caption(
            "회색 점선 박스 전체가 **단일 에이전트 1개**입니다. "
            "입력(회의 메모)을 받아 → ① **정책**(체크박스)이 '무엇을 낼지' 결정하고 "
            "→ ② **파서**가 문장을 섹션별로 분류 → ③ **리포트 작성**이 정책이 허용한 섹션만 "
            "Markdown으로 출력합니다. 아래 Mini Lab에서 정책 체크박스를 끄면 ③의 출력이 즉시 바뀝니다."
        )

    st.markdown("#### ① Mini Lab — 회의 메모 정리 (정책 체크박스를 켜고 꺼보세요!)")
    notes_path = os.path.join(ROOT, "course/mini_labs/day01_single_agent/meeting_notes.txt")
    up = st.file_uploader(
        "📎 회의 메모 파일 올리기 (.txt / .md) — 안 올리면 아래 기본 예시로 진행됩니다",
        type=["txt", "md"], key="d1_upload")
    if up is not None:
        notes = up.getvalue().decode("utf-8", errors="replace")
        st.success(f"업로드한 파일 사용 중: **{up.name}** · {len(notes):,}자 "
                   "— Mini Lab과 ③ AI 하네스가 모두 이 파일 기준으로 동작합니다.")
    elif os.path.exists(notes_path):
        notes = open(notes_path, encoding="utf-8").read()
    else:
        notes = ""
        st.error("기본 meeting_notes.txt 가 없습니다. 위에서 파일을 직접 올려주세요.")

    if notes:
        c1, c2 = st.columns([1, 2])
        with c1:
            st.markdown("**정책: 어떤 섹션을 출력할까?**")
            picked = {}
            for key, kw, title in ma.SECTIONS:
                picked[key] = st.checkbox(title, value=True, key=f"sec_{key}")
            with st.expander("회의 메모 원문 보기"):
                st.code(notes)
        with c2:
            data = ma._parse_notes(notes)
            enabled = [(k, t) for k, kw, t in ma.SECTIONS if picked[k]]
            st.markdown("**📄 결과 (체크 즉시 바뀝니다)**")
            st.markdown(ma.build_report(data, enabled))
            if not picked.get("risks"):
                st.info("👈 'Risks' 체크를 껐더니 결과에서 Risks 섹션이 사라졌죠? "
                        "→ 이게 **정책이 에이전트 출력을 통제**하는 핵심입니다.")
    st.divider()
    st.markdown("#### ② Main Lab — 정책 기반 SAST (같은 코드, 정책만 바꿔보기)")
    pol = st.radio("정책 선택", ["policies/CLAUDE_base.md (가중 없음)", "policies/CLAUDE.md (차량 모듈 가중)"],
                   horizontal=True)
    pol_path = "policies/CLAUDE.md" if "CLAUDE.md (차량" in pol else "policies/CLAUDE_base.md"
    if st.button("🔍 SAST 실행", key="d1_sast"):
        res = sast_agent.run("sample_app/", pol_path)
        rows = [{"심각도": r["severity"], "CWE": r["cwe"],
                 "파일": os.path.basename(r["file"]), "줄": r["line"], "내용": r["title"]} for r in res]
        st.dataframe(rows, width="stretch", hide_index=True)
        ctrl = [r for r in res if "control" in r["file"]]
        if ctrl:
            sev = ctrl[0]["severity"]
            st.success(f"차량 제어 모듈(control/) 발견 심각도 = **{sev}** "
                       + ("→ 정책 가중으로 Critical 상향! 🚨" if sev == "Critical" else "(기본 정책: High)"))

    st.divider()
    st.markdown("#### ③ (보너스) 🧠 AI 하네스 — 같은 회의록, '시스템 프롬프트(정책)'만 바꾸면?")
    st.caption("Day 1 핵심: **정책이 출력을 통제**. ②는 규칙으로, ③은 진짜 AI로 같은 원리를 보여줍니다. "
               "AI 키가 없으면 규칙 fallback 으로 안전하게 동작해요.")
    if notes:
        pick = st.radio("AI 정책(시스템 프롬프트) 고르기", list(AI_POLICIES), horizontal=True, key="d1_ai_pick")
        system = st.text_area("시스템 프롬프트 (직접 고쳐도 됩니다)", value=AI_POLICIES[pick], height=90, key="d1_ai_sys")
        st.caption(f"현재 모드: {llm_client.mode_label()}")
        if st.button("🧠 AI 하네스 실행", key="d1_ai_run"):
            notes2 = notes
            out = llm_client.complete(system, notes2)
            if out:
                st.markdown("**🧠 AI 출력 (정책대로):**")
                st.markdown(out)
                st.success(f"정책을 바꾸면 같은 회의록인데도 AI 출력이 통째로 바뀝니다 — 이게 '하네스'. ({llm_client.mode_label()})")
            else:
                st.warning("AI 키가 없어 **규칙 fallback** 으로 보여줍니다. (키를 넣으면 위 정책대로 진짜 LLM이 작성해요)")
                data2 = ma._parse_notes(notes2)
                fb = {"📋 액션 비서": ("action_items", "Action Items"),
                      "⚠️ 리스크 분석가": ("risks", "Risks"),
                      "✏️ 한 줄 요약가": ("summary", "Summary")}[pick]
                items = data2.get(fb[0], [])
                st.markdown(f"**{fb[1]} (규칙 추출):**")
                st.markdown("\n".join(f"- {x}" for x in items) or "- (없음)")
    st.divider()
    st.markdown("#### ④ 💬 (보너스) 카톡 답장 톤 봇 — 같은 메시지, '톤(정책)'만 바꾸면?")
    st.caption("Day 1 핵심 한 번 더: **정책이 출력을 통제**. 회의록 대신 '카톡 한 줄'로 체감해 보세요. "
               "톤(시스템 프롬프트)만 바꾸면 같은 말도 답장이 통째로 달라집니다.")
    msg = st.text_input("보낼 메시지(원문)", value="나 오늘 좀 늦을 것 같아", key="d1_tone_msg")
    tone = st.radio("답장 톤(정책) 고르기", list(TONE_POLICIES), horizontal=True, key="d1_tone_pick")
    st.caption(f"현재 모드: {llm_client.mode_label()}")
    if st.button("💬 톤 적용해서 답장 만들기", key="d1_tone_run") and msg.strip():
        out = llm_client.complete(TONE_POLICIES[tone], msg.strip())
        if out:
            st.markdown(f"**{tone} 답장:**")
            st.markdown(out)
            st.success(f"메시지는 그대로인데 '톤(정책)'만 바꿨더니 답장이 통째로 바뀌죠? — 이게 하네스. ({llm_client.mode_label()})")
        else:
            st.warning("AI 키 없음 → 규칙 fallback 으로 톤만 입혀 보여줍니다. (키를 넣으면 진짜 LLM이 자연스럽게 다시 씁니다)")
            st.markdown(f"**{tone} 답장 (규칙):**")
            st.markdown(TONE_FALLBACK[tone](msg.strip()))
        st.caption("👉 톤을 바꿔가며 다시 눌러보세요. 같은 메시지가 다정 ↔ 츤데레 ↔ 비즈니스 ↔ MZ 로 변신합니다.")

    with st.expander("🎯 개선 과제 (직접 해보기)"):
        st.markdown(
            "- `meeting_notes.txt` 에 새 발언(예: '현우: 로그 보관 정책도 정리할게요')을 추가 → 자동 분류되는지 확인\n"
            "- `MEETING_AGENT.md` 에서 섹션 줄을 지웠다 살렸다 → 출력이 바뀌는지 확인\n"
            "- (도전) `_parse_notes` 에 '의사결정(Decisions)' 섹션을 새로 만들어 분류 추가"
        )
