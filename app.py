import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st
import dashboard_lib as L

st.set_page_config(page_title="Day 1 · 정책이 결과를 바꾼다", page_icon="1️⃣", layout="wide")
st.title("1️⃣ Day 1 · 정책이 에이전트 출력을 통제한다")

tabs = st.tabs(["🏠 개요", "🤔 왜 만드나?", "Day 1 · 정책"])
with tabs[0]:
    L.render_overview()
with tabs[1]:
    L.render_why()
with tabs[2]:
    L.render_day1()
