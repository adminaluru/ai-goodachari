"""
config/prompts.py
=================
Single source of truth for ALL prompt templates.

WHY this is its own file:
  Prompts are configuration, not code. A domain expert or product
  manager should be able to tune prompt wording without touching
  agent logic. Keeping prompts here means:
    - Changes are tracked in Git separately from code changes
    - Prompts can be reviewed and approved independently
    - Swapping prompt strategies requires zero changes to core/

HOW TO EDIT:
  Change the text below. The 4 variables in curly braces MUST stay:
    {tools}            - filled by LangChain with available tool descriptions
    {tool_names}       - filled by LangChain with tool names the agent can call
    {input}            - filled at runtime with the user's research topic
    {agent_scratchpad} - filled by LangChain with the Thought/Action/Observation loop
  Do not rename or remove any of these 4 variables.
"""

# ── ReAct Agent Prompt ────────────────────────────────────────────────────────
# Standard ReAct (Reason + Act) prompt template.
# This is the same template as hub.pull("hwchase17/react") from LangChain Hub,
# defined locally for reliability, speed, and version control.
#
# To tune agent behaviour:
#   - Add domain-specific instructions ABOVE the "Use the following format:" line
#   - Do NOT modify the format block — it controls the Thought/Action/Observation loop

REACT_AGENT_PROMPT = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""
