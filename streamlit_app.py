"""
streamlit_app.py — Browser UI entry point
==========================================
Pure UI layer. Contains zero AI logic, zero agent construction,
zero prompt building. All of that lives in core/ and report/.

Run: streamlit run streamlit_app.py
"""

import os
import logging
import streamlit as st
from dotenv import load_dotenv

from config.settings import APP_TITLE, APP_ICON, APP_VERSION, APP_SUBTITLE
from core.agent import build_agent
from report.formatter import build_research_prompt

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
)

# ── Session state init ────────────────────────────────────────────────────────
# All results stored in session_state so they survive tab clicks and reruns.
if "report"       not in st.session_state: st.session_state.report       = None
if "last_topic"   not in st.session_state: st.session_state.last_topic   = ""
if "error"        not in st.session_state: st.session_state.error        = None
if "is_running"   not in st.session_state: st.session_state.is_running   = False

# ── API key validation ────────────────────────────────────────────────────────
openai_key = os.getenv("OPENAI_API_KEY", "")
tavily_key = os.getenv("TAVILY_API_KEY", "")

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("ℹ️ How it works")
    st.markdown("""
1. You enter a research topic
2. The agent **thinks** about what to search
3. It **calls** the Tavily web search tool
4. It **reads** the results
5. It loops until it has enough information
6. It writes a **structured report**

This loop is called the **ReAct pattern**:
> **Re**ason → **Act** → Observe → Repeat
""")
    st.divider()

    st.header("⚙️ Status")
    if openai_key:
        st.success("OpenAI key loaded ✓")
    else:
        st.error("OPENAI_API_KEY missing in .env")

    if tavily_key:
        st.success("Tavily key loaded ✓")
    else:
        st.error("TAVILY_API_KEY missing in .env")

    st.divider()
    st.caption(f"{APP_VERSION} · Project 2 · Shashi AI")

# ── Header ────────────────────────────────────────────────────────────────────
st.title(f"{APP_ICON} {APP_TITLE}")
st.caption(APP_SUBTITLE)

# ── Block if keys missing ─────────────────────────────────────────────────────
if not openai_key or not tavily_key:
    st.error(
        "Both OPENAI_API_KEY and TAVILY_API_KEY must be set in your .env file. "
        "Restart the app after adding them."
    )
    st.stop()

# ── Input ─────────────────────────────────────────────────────────────────────
topic = st.text_input(
    "Research topic",
    placeholder="e.g.  AI in healthcare 2024  |  quantum computing breakthroughs  |  remote work trends",
)

run_button = st.button(
    "🔍 Research",
    type="primary",
    disabled=st.session_state.is_running,
    use_container_width=True,
)

# ── Run agent ─────────────────────────────────────────────────────────────────
if run_button:
    if not topic.strip():
        st.warning("Please enter a research topic.")
        st.stop()

    # Reset previous results before new run
    st.session_state.report     = None
    st.session_state.error      = None
    st.session_state.last_topic = topic.strip()
    st.session_state.is_running = True

    with st.spinner("Agent is researching... this takes 20–60 seconds."):
        try:
            logger.info("Starting research on topic: %s", topic)
            executor = build_agent(verbose=False)   # No terminal noise in UI
            prompt   = build_research_prompt(topic.strip())
            result   = executor.invoke({"input": prompt})

            st.session_state.report = result["output"]
            logger.info("Research completed for topic: %s", topic)

        except Exception as e:
            st.session_state.error = str(e)
            logger.error("Agent failed for topic '%s': %s", topic, e)

    st.session_state.is_running = False
    st.rerun()

# ── Display report ────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(f"Something went wrong: {st.session_state.error}")

if st.session_state.report:
    st.divider()
    st.subheader(f"📄 Report: {st.session_state.last_topic}")

    # Tab layout — Summary tab and Full Report tab
    tab_summary, tab_full = st.tabs(["📋 Full Report", "💾 Export"])

    with tab_summary:
        st.markdown(st.session_state.report)

    with tab_full:
        st.markdown("Copy the raw markdown below to save or share your report.")
        st.code(st.session_state.report, language="markdown")
        st.download_button(
            label="⬇️ Download as .md",
            data=st.session_state.report,
            file_name=f"research_{st.session_state.last_topic[:40].replace(' ', '_')}.md",
            mime="text/markdown",
        )
