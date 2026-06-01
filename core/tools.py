"""
core/tools.py
=============
Tool registry — the only file that knows which search provider is being used.

To add a new tool:  add one elif block below + update settings.py.
To swap providers:  change SEARCH_PROVIDER in config/settings.py only.

The agent receives whatever list get_tools() returns — it never
imports search libraries directly.
"""

import logging
from config.settings import SEARCH_PROVIDER, MAX_SEARCH_RESULTS

logger = logging.getLogger(__name__)


def get_tools() -> list:
    """
    Return a list of LangChain tools based on SEARCH_PROVIDER in settings.

    Returns:
        List of LangChain tool instances for the agent to use.

    Raises:
        ValueError: If SEARCH_PROVIDER is not a recognised option.
        RuntimeError: If the tool fails to initialise (missing key, etc.).
    """
    logger.info("Loading search provider: %s", SEARCH_PROVIDER)

    if SEARCH_PROVIDER == "tavily":
        try:
            from langchain_community.tools.tavily_search import TavilySearchResults
            tool = TavilySearchResults(max_results=MAX_SEARCH_RESULTS)
            logger.info("Tavily search tool loaded (max_results=%d)", MAX_SEARCH_RESULTS)
            return [tool]
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Tavily search: {e}\n"
                "Check that TAVILY_API_KEY is set in your .env file."
            ) from e

    elif SEARCH_PROVIDER == "duckduckgo":
        try:
            from langchain_community.tools import DuckDuckGoSearchRun
            return [DuckDuckGoSearchRun()]
        except Exception as e:
            raise RuntimeError(f"Failed to load DuckDuckGo search: {e}") from e

    elif SEARCH_PROVIDER == "wikipedia":
        try:
            from langchain_community.tools import WikipediaQueryRun
            from langchain_community.utilities import WikipediaAPIWrapper
            return [WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())]
        except Exception as e:
            raise RuntimeError(f"Failed to load Wikipedia search: {e}") from e

    else:
        raise ValueError(
            f"Unknown SEARCH_PROVIDER: '{SEARCH_PROVIDER}'. "
            "Valid options: 'tavily' | 'duckduckgo' | 'wikipedia'"
        )
