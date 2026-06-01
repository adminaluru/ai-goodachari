"""
core/llm.py
===========
LLM factory — the only file that knows which AI provider is being used.

To swap providers: change LLM_PROVIDER in config/settings.py.
No other file needs to change.
"""

import logging
from config.settings import LLM_PROVIDER, OPENAI_MODEL, TEMPERATURE

logger = logging.getLogger(__name__)


def get_llm():
    """
    Return a configured LLM instance based on LLM_PROVIDER in settings.

    Returns:
        A LangChain-compatible chat model instance.

    Raises:
        ValueError: If LLM_PROVIDER is not a recognised option.
        RuntimeError: If the API key is missing or invalid.
    """
    logger.info("Loading LLM provider: %s", LLM_PROVIDER)

    if LLM_PROVIDER == "openai":
        try:
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=OPENAI_MODEL, temperature=TEMPERATURE)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load OpenAI LLM: {e}\n"
                "Check that OPENAI_API_KEY is set in your .env file."
            ) from e

    elif LLM_PROVIDER == "groq":
        try:
            from langchain_groq import ChatGroq
            from config.settings import GROQ_MODEL
            return ChatGroq(model=GROQ_MODEL, temperature=TEMPERATURE)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Groq LLM: {e}\n"
                "Check that GROQ_API_KEY is set in your .env file."
            ) from e

    elif LLM_PROVIDER == "ollama":
        try:
            from langchain_ollama import ChatOllama
            from config.settings import OLLAMA_MODEL
            return ChatOllama(model=OLLAMA_MODEL, temperature=TEMPERATURE)
        except Exception as e:
            raise RuntimeError(
                f"Failed to load Ollama LLM: {e}\n"
                "Ensure Ollama is running locally: https://ollama.com"
            ) from e

    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER: '{LLM_PROVIDER}'. "
            "Valid options: 'openai' | 'groq' | 'ollama'"
        )
