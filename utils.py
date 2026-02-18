from __future__ import annotations

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Any


OUTPUT_DIR = Path("output")


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str, max_len: int = 80) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text, flags=re.UNICODE)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text.strip("-")
    return text[:max_len] if len(text) > max_len else text


def timestamp() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def get_history():
    if not OUTPUT_DIR.exists():
        return []
    
    files = sorted(OUTPUT_DIR.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    history = []
    for f in files:
        name = f.stem
        meta_path = f.with_suffix(".json")
        meta = {}
        if meta_path.exists():
            try:
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
            except:
                pass
        
        history.append({
            "timestamp": name.split("_")[0], # simplified extraction
            "topic": meta.get("topic", name),
            "file": f.name,
            "path": str(f)
        })
    return history
