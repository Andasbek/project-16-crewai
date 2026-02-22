# Проект 16: Мультиагентная генерация контента с CrewAI и Streamlit

>**Подробная документация (RU):** [docs/README_RU.md](docs/README_RU.md)

## Обзор
Этот проект использует **CrewAI** для оркестрации команды AI‑агентов (Researcher, Writer, Editor), которые создают качественные статьи в Markdown по заданной теме. Веб‑интерфейс на **Streamlit** позволяет настраивать параметры и запускать генерацию.

## Возможности
- **Мультиагентный конвейер**:
  - **Researcher**: собирает факты и источники (через Serper).
  - **Writer**: пишет черновик статьи.
  - **Editor**: правит и форматирует финальный текст.
- **Гибкая настройка**: аудитория, тон, диапазон слов, количество источников.
- **Язык результата**: русский или английский.
- **Web UI**: простой интерфейс для запуска и просмотра результата.
- **История**: просмотр ранее сгенерированных статей из папки output.

## Требования
- Python 3.10+
- OpenAI API Key (для LLM)
- Serper.dev API Key (для поиска, опционально)

## Установка

1. **Клонирование репозитория**:
   ```bash
   git clone <repo-url>
   cd project-16-crewai
   ```

2. **Установка зависимостей**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Настройка окружения**:
   Скопируйте `.env.example` в `.env` и заполните ключи:
   ```bash
   cp .env.example .env
   ```
   *Пример `.env`:*
   ```ini
   OPENAI_API_KEY=sk-...
   SERPER_API_KEY=...
   MODEL_NAME=gpt-4o-mini  # или gpt-3.5-turbo
   ```

## Использование

### Веб‑интерфейс (рекомендуется)
Запуск Streamlit:
```bash
streamlit run app.py
```
1. Введите **Topic**.
2. Настройте параметры (Audience, Tone, Word Count, Language).
3. Нажмите **Generate Article**.
4. Посмотрите результат и скачайте Markdown.

### CLI (Legacy)
Можно запустить генерацию по списку тем в `main.py`:
```bash
python main.py
```

## Выходные файлы
Все результаты сохраняются в `output/`:
- `*.md`: финальная статья (имя содержит timestamp и slug).
- `*.json`: метаданные запуска (тема, аудитория, тон, диапазон слов, настройки поиска и т.п.).

## Структура проекта
```
project-16-crewai/
├── app.py             # Streamlit Web UI
├── agents.py          # Определение агентов
├── tasks.py           # Описание задач
├── crew.py            # Оркестрация Crew
├── utils.py           # Утилиты (I/O, история)
├── main.py            # CLI вход (legacy)
├── requirements.txt   # Зависимости
├── docs/              # Документация
└── output/            # Результаты генерации
```

## Troubleshooting
- **Missing API Key**: проверьте корректность `.env`.
- **Search Errors**: при проблемах с Serper отключите "Include Web Research" или проверьте квоту.
- **Streamlit not found**: активируйте окружение или запустите `python -m streamlit run app.py`.
