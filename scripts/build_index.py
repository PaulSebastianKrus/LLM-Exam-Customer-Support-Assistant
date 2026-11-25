from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np

from src.config import Settings
from src.documents import load_knowledge_base
from src.ollama_client import OllamaClient
from src.rag import RagIndex


def main() -> None:
    settings = Settings()
    chunks = load_knowledge_base(settings.knowledge_dir)
    client = OllamaClient(settings.ollama_base_url)
    texts = [f"{chunk.heading}\n{chunk.text}" for chunk in chunks]

    print(f"Embedding {len(chunks)} chunks with {settings.embed_model}...")
    embeddings = np.asarray(client.embed(settings.embed_model, texts), dtype=float)
    RagIndex(chunks, embeddings).save(settings.index_path, settings.embed_model)
    print(f"Saved RAG index to {settings.index_path}")


if __name__ == "__main__":
    main()
