from __future__ import annotations

from crewai import Crew, Process
from agents import build_agents
from tasks import build_tasks

def build_crew(
    topic: str,
    audience: str,
    tone: str,
    word_count_min: int,
    word_count_max: int,
    use_search: bool,
    num_sources: int,
    language: str = "English",
):
    researcher, writer, editor = build_agents(use_search=use_search)
    research_task, writing_task, editing_task = build_tasks(
        topic=topic,
        audience=audience,
        tone=tone,
        word_count_min=word_count_min,
        word_count_max=word_count_max,
        num_sources=num_sources,
        language=language,
    )

    # Привязка задач к агентам:
    research_task.agent = researcher
    writing_task.agent = writer
    editing_task.agent = editor

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=[research_task, writing_task, editing_task],
        process=Process.sequential,
        verbose=True,
    )
    return crew
