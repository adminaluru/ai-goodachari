"""
report/formatter.py
====================
Builds the structured report prompt injected into the agent's input.

WHY this is its own file:
  Changing the report structure (adding sections, changing format)
  should never require touching agent logic. This file owns the output
  shape; core/agent.py owns the reasoning engine. They are separate jobs.
"""


REPORT_SECTIONS = [
    "1. Executive Summary  (2–3 sentences — what is this topic and why does it matter now)",
    "2. Key Findings       (4–5 bullet points drawn directly from your search results)",
    "3. Current Trends     (what is actively changing or emerging in this space right now)",
    "4. Key Players        (companies, researchers, or organisations leading this area)",
    "5. Conclusion         (what this means going forward — one clear paragraph)",
]


def build_research_prompt(topic: str) -> str:
    """
    Return the full instruction string passed to the agent as its task.

    The agent reads this, decides how many searches to run, then
    produces a report matching the section structure below.

    Args:
        topic: The research topic entered by the user at runtime.

    Returns:
        A formatted string that becomes the agent's 'input'.
    """
    sections = "\n".join(REPORT_SECTIONS)

    return f"""
You are a professional research analyst. Your job is to research the following
topic thoroughly using your search tools, then write a structured report.

TOPIC: {topic}

INSTRUCTIONS:
- Search for current, factual information about this topic.
- Run multiple searches if needed to cover the topic well.
- Use ONLY information from your search results — do not invent facts.
- If a section lacks search evidence, say so honestly rather than guessing.
- Write in clear, professional English. Avoid filler phrases.

REPORT STRUCTURE — produce ALL of these sections in order:
{sections}

Format your final report in clean Markdown.
Start directly with the report — no preamble like "Here is your report:".
""".strip()
