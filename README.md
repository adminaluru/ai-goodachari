# AI Goodachari — AI Research Agent 🤖

An autonomous AI research agent that searches the web and writes structured reports on any topic — built with LangChain, OpenAI GPT-3.5, and Tavily Search.

## What it does

Enter any research topic. The agent:
1. **Thinks** — decides what to search
2. **Acts** — calls the Tavily web search tool
3. **Observes** — reads the results
4. **Loops** — runs multiple searches until it has enough
5. **Writes** — produces a structured 5-section report

This is the **ReAct pattern** (Reason + Act) — the agent figures out its own plan, no hardcoded steps.

## Report structure

Every report contains:
- Executive Summary
- Key Findings
- Current Trends
- Key Players
- Conclusion

## Architecture

```
streamlit_app.py / runner.py   ← Entry points (UI + terminal)
        ↓
core/agent.py                  ← AgentExecutor factory (ReAct loop)
        ↓
core/llm.py    core/tools.py   ← Provider factories (swappable)
        ↓
config/settings.py             ← All constants in one place
config/prompts.py              ← ReAct prompt template
        ↓
report/formatter.py            ← Report structure definition
```

**Pattern:** Layered architecture + Agentic (ReAct) architecture + Factory pattern for provider abstraction.

## Tech stack

| Component | Technology |
|-----------|-----------|
| LLM | OpenAI GPT-3.5-turbo |
| Agent framework | LangChain (ReAct) |
| Web search | Tavily Search API |
| UI | Streamlit |
| Config | python-dotenv |

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/ai-goodachari.git
cd ai-goodachari

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Add your API keys
cp .env.example .env
# Edit .env and add your keys

# 5. Run
streamlit run streamlit_app.py   # Browser UI
python runner.py                  # Terminal
```

## API keys needed

- **OpenAI** — [platform.openai.com](https://platform.openai.com)
- **Tavily** — [tavily.com](https://tavily.com) (free tier available)

Create a `.env` file:
```
OPENAI_API_KEY=your-key-here
TAVILY_API_KEY=your-key-here
```

## Project series

This is **Project 2** of Shashi's AI Engineering portfolio:

| Project | Description | Status |
|---------|-------------|--------|
| Project 1 | DocChat AI — RAG-based PDF Q&A | ✅ Complete |
| Project 2 | AI Goodachari — Agentic Research Agent | ✅ Complete |
| Project 3 | FastAPI Microservices | 🔜 Coming soon |

---
Built by **Shashi Aluru** · [LinkedIn](https://www.linkedin.com/in/YOUR_PROFILE)
