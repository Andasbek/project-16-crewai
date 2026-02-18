from __future__ import annotations

from crewai import Task

def build_tasks(
    topic: str,
    audience: str,
    tone: str,
    word_count_min: int = 800,
    word_count_max: int = 1200,
    num_sources: int = 5,
    language: str = "English",
):
    research_task = Task(
        description=(
            f"Research the topic: '{topic}'.\n"
            f"Target audience: {audience}\n"
            f"Tone: {tone}\n"
            f"Language: {language}\n\n"
            "Deliver a structured brief:\n"
            "1) 5–10 key points (facts/insights)\n"
            f"2) At least {num_sources} credible sources with URLs\n"
            "3) Suggested outline (H1/H2)\n"
            "4) Any important caveats/limitations\n"
            "Write the brief in the specified language. Keep sources and URLs as-is.\n"
        ),
        expected_output=(
            f"A research brief with bullet points, outline, and a list of at least {num_sources} sources with URLs."
        ),
    )

    writing_task = Task(
        description=(
            f"Write a Markdown article about '{topic}' using the research brief.\n"
            f"Constraints:\n"
            f"- {word_count_min}–{word_count_max} words\n"
            "- Use Markdown headings (H1, H2)\n"
            "- Include a short intro and conclusion\n"
            "- If you mention numbers/claims, rely on the provided sources\n"
            "- Keep it readable and practical\n"
            f"- Write in {language}\n"
        ),
        expected_output=(
            f"A complete Markdown article between {word_count_min} and {word_count_max} words."
        ),
    )

    editing_task = Task(
        description=(
            "Edit the article to be publish-ready:\n"
            "- Improve clarity and structure\n"
            "- Fix grammar and style\n"
            "- Remove repetition\n"
            "- Ensure the article stays within the word limit range\n"
            "- Keep citations/links\n"
            f"- Ensure the final output is in {language}\n"
            "Return ONLY the final Markdown."
        ),
        expected_output="A polished, publish-ready Markdown article."
    )

    return research_task, writing_task, editing_task
