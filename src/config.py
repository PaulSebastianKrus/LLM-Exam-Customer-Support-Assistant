from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


@dataclass(frozen=True)
class Settings:
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
    chat_model: str = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2:3b")
    embed_model: str = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
    top_k: int = int(os.getenv("RAG_TOP_K", "4"))
    min_score: float = float(os.getenv("RAG_MIN_SCORE", "0.30"))
    max_score_gap: float = float(os.getenv("RAG_MAX_SCORE_GAP", "0.02"))
    app_timezone: str = os.getenv("APP_TIMEZONE", "Europe/Copenhagen")
    knowledge_dir: Path = PROJECT_ROOT / "knowledge_base"
    index_path: Path = PROJECT_ROOT / "data" / "index.json"
