"""
runner.py — Terminal entry point
=================================
Run the Research Agent from the terminal.
Used for quick testing before opening the Streamlit UI.

Run: python runner.py
"""

import logging
import os
from dotenv import load_dotenv

from config.settings import APP_TITLE, APP_VERSION
from core.agent import build_agent
from report.formatter import build_research_prompt

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.WARNING,  # Suppress INFO noise in terminal — agent verbose handles output
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def validate_env() -> None:
    """
    Fail fast if required API keys are missing.
    Better to crash here with a clear message than deep inside the agent.
    """
    load_dotenv()

    missing = []
    if not os.getenv("OPENAI_API_KEY"):
        missing.append("OPENAI_API_KEY")
    if not os.getenv("TAVILY_API_KEY"):
        missing.append("TAVILY_API_KEY")

    if missing:
        raise EnvironmentError(
            f"Missing required API keys in .env: {', '.join(missing)}\n"
            "Add them to your .env file and restart."
        )


def get_topic() -> str:
    """
    Collect the research topic from the user at runtime.
    No defaults, no hardcoded domains — works for any topic.
    """
    print("\n" + "=" * 65)
    print(f"  {APP_TITLE}  {APP_VERSION}")
    print("=" * 65)
    print("\nThe agent will search the web and write a structured report.\n")

    topic = ""
    while not topic.strip():
        topic = input("Research topic: ").strip()
        if not topic:
            print("  Please enter a topic to continue.")

    return topic


def main() -> None:
    try:
        validate_env()
    except EnvironmentError as e:
        print(f"\n[ERROR] {e}")
        return

    topic = get_topic()

    print(f"\nResearching: '{topic}'")
    print("Watch the agent think below (Thought → Action → Observation)...\n")
    print("-" * 65)

    try:
        executor = build_agent(verbose=True)
        prompt   = build_research_prompt(topic)
        result   = executor.invoke({"input": prompt})

        print("\n" + "=" * 65)
        print("  RESEARCH REPORT")
        print("=" * 65 + "\n")
        print(result["output"])
        print("\n" + "=" * 65)

    except RuntimeError as e:
        print(f"\n[ERROR] {e}")
        logger.error("Agent execution failed: %s", e)


if __name__ == "__main__":
    main()
