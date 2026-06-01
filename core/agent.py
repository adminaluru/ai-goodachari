"""
core/agent.py
=============
AgentExecutor factory — the only file that builds the agent.

Neither runner.py nor streamlit_app.py construct the agent directly.
They call build_agent() and receive a ready-to-use executor.

WHY this matters:
  If LangChain changes the agent API, or we want to swap the ReAct
  prompt for a custom one, we change this file only. The UI and
  terminal runner are completely insulated from that change.
"""

import logging
from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

from config.settings import MAX_ITERATIONS, AGENT_VERBOSE
from config.prompts import REACT_AGENT_PROMPT
from core.llm import get_llm
from core.tools import get_tools

# Prompt loaded from config/prompts.py — edit it there, not here.
REACT_PROMPT = PromptTemplate.from_template(REACT_AGENT_PROMPT)

logger = logging.getLogger(__name__)


def build_agent(verbose: bool = AGENT_VERBOSE) -> AgentExecutor:
    """
    Build and return a configured AgentExecutor.

    Uses the standard ReAct prompt defined in config/prompts.py.
    The agent will loop: Thought → Action (tool call) → Observation
    until it has enough information to write the final report,
    or until MAX_ITERATIONS is reached.

    Args:
        verbose: If True, prints the Thought/Action/Observation loop
                 to the terminal. Set False in the Streamlit UI.

    Returns:
        A configured AgentExecutor ready to call with .invoke().

    Raises:
        RuntimeError: If the LLM or tools fail to load.
    """
    logger.info("Building agent (max_iterations=%d, verbose=%s)", MAX_ITERATIONS, verbose)

    llm   = get_llm()
    tools = get_tools()

    agent = create_react_agent(llm=llm, tools=tools, prompt=REACT_PROMPT)

    executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=verbose,
        max_iterations=MAX_ITERATIONS,      # Safety cap — no runaway loops
        handle_parsing_errors=True,         # Gracefully handles LLM format mistakes
        return_intermediate_steps=False,    # Keep output clean
    )

    logger.info("Agent built successfully")
    return executor
