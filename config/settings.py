"""
config/settings.py
==================
Single source of truth for ALL configuration constants.
To change any setting across the entire app — change it here only.
Nothing else needs to be touched.
"""

# ── LLM ───────────────────────────────────────────────────────────────────────
LLM_PROVIDER    = "openai"           # Future swap: "groq" | "ollama"
OPENAI_MODEL    = "gpt-3.5-turbo"
TEMPERATURE     = 0                  # 0 = factual/deterministic (right for research)
MAX_TOKENS      = 4096

# ── Search ────────────────────────────────────────────────────────────────────
SEARCH_PROVIDER     = "tavily"       # Future swap: "duckduckgo" | "wikipedia"
MAX_SEARCH_RESULTS  = 5              # Tavily results per search call

# ── Agent safety ──────────────────────────────────────────────────────────────
MAX_ITERATIONS  = 10    # Hard cap — prevents runaway agent burning API credits
AGENT_VERBOSE   = True  # True = shows Thought/Action/Observe loop in terminal

# ── App identity ──────────────────────────────────────────────────────────────
APP_TITLE    = "AI Goodachari"
APP_ICON     = "🔍"
APP_VERSION  = "v1.0"
APP_SUBTITLE = "Enter a topic. The agent searches the web and writes a structured report."
