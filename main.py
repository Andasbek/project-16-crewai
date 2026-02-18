from __future__ import annotations

import os
from dotenv import load_dotenv

from crew import build_crew
from utils import ensure_output_dir, slugify, timestamp, write_text, write_json, OUTPUT_DIR


TOPICS = [
    {
        "topic": "How RAG systems reduce hallucinations in LLM apps",
        "audience": "Software engineers and technical managers",
        "tone": "Professional, practical",
    },
    {
        "topic": "Beginner-friendly guide to personal finance: budgeting and emergency fund",
        "audience": "General audience (18–35)",
        "tone": "Friendly, encouraging",
    },
    {
        "topic": "What is space weather and why it matters for GPS and power grids",
        "audience": "Curious learners with basic science background",
        "tone": "Clear, educational",
    },
]


def run_one(topic: str, audience: str, tone: str, language: str = "Russian") -> dict:
    crew = build_crew(
        topic=topic,
        audience=audience,
        tone=tone,
        word_count_min=800,
        word_count_max=1200,
        # Default values for CLI run
        use_search=True,
        num_sources=5,
        language=language,
    )
    # Удаляем явный вызов tasks здесь, так как build_crew теперь сам их создает
    # Но wait, build_crew в crew.py принимает аргументы и создает tasks внутри.
    # main.py line 31: tasks = build_tasks(...) - это надо удалить.
    
    result = crew.kickoff()
    return {"final": str(result)}
    result = crew.kickoff()
    # CrewAI может вернуть строку или объект — сохраним как текст + метаданные
    return {"final": str(result)}


def main():
    load_dotenv()
    ensure_output_dir()

    # Минимальная проверка ключей (чтобы было понятнее в ошибках)
    if not os.getenv("OPENAI_API_KEY") and not os.getenv("MODEL_NAME"):
        # MODEL_NAME сам по себе не ключ, но иногда люди используют локальные провайдеры.
        # Оставим мягкую подсказку.
        print("⚠️  Hint: set OPENAI_API_KEY in .env (or configure your LLM provider for CrewAI).")

    batch_stamp = timestamp()

    for i, item in enumerate(TOPICS, start=1):
        topic = item["topic"]
        audience = item["audience"]
        tone = item["tone"]

        print(f"\n=== [{i}/{len(TOPICS)}] Running topic: {topic} ===")

        data = run_one(topic=topic, audience=audience, tone=tone)

        base = f"{batch_stamp}_{i:02d}_{slugify(topic)}"
        md_path = OUTPUT_DIR / f"{base}.md"
        meta_path = OUTPUT_DIR / f"{base}.json"

        write_text(md_path, data["final"])
        write_json(meta_path, {"topic": topic, "audience": audience, "tone": tone})

        print(f"✅ Saved: {md_path}")

    print("\nDone. Check ./output")


if __name__ == "__main__":
    main()
