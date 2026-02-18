from __future__ import annotations

from crewai import Agent
from crewai_tools import SerperDevTool

def build_agents(use_search: bool = True):
    # Поиск (если SERPER_API_KEY задан — будет работать)
    search_tool = SerperDevTool()

    researcher = Agent(
        role="Research Analyst",
        goal="Find up-to-date, credible information and produce a structured brief with sources.",
        backstory=(
            "You are a meticulous research analyst. You verify claims, prefer primary sources, "
            "and provide links and short evidence snippets."
        ),
        tools=[search_tool] if use_search else [],
        verbose=True,
        allow_delegation=False,
    )

    writer = Agent(
        role="Content Writer",
        goal="Write a clear, engaging article in Markdown based on the provided brief.",
        backstory=(
            "You are a strong writer who can explain complex topics simply, use a good structure "
            "(H1/H2, bullets, examples), and keep within word limits."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    editor = Agent(
        role="Senior Editor",
        goal="Polish the article: clarity, structure, correctness, style. Remove fluff. Keep citations intact.",
        backstory=(
            "You are a senior editor. You improve readability, fix grammar, ensure the narrative flows, "
            "and the final text is publish-ready."
        ),
        tools=[],
        verbose=True,
        allow_delegation=False,
    )

    return researcher, writer, editor
