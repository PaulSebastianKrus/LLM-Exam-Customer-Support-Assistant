from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.documents import DocumentChunk


@dataclass(frozen=True)
class SearchResult:
    chunk: DocumentChunk
    score: float


class RagIndex:
    def __init__(self, chunks: list[DocumentChunk], embeddings: np.ndarray) -> None:
        if len(chunks) != len(embeddings):
            raise ValueError("Each document chunk must have exactly one embedding.")
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a two-dimensional array.")
        self.chunks = chunks
        self.embeddings = _normalise_rows(embeddings.astype(float))

    def search(self, query_embedding: list[float], top_k: int = 4) -> list[SearchResult]:
        query = np.asarray(query_embedding, dtype=float)
        if query.ndim != 1 or query.shape[0] != self.embeddings.shape[1]:
            raise ValueError("Query embedding has the wrong dimensions.")
        norm = np.linalg.norm(query)
        if norm == 0:
            raise ValueError("Query embedding cannot be a zero vector.")
        scores = self.embeddings @ (query / norm)
        count = min(max(top_k, 1), len(self.chunks))
        indices = np.argsort(scores)[::-1][:count]
        return [SearchResult(self.chunks[index], float(scores[index])) for index in indices]

    def save(self, path: Path, embed_model: str) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "embed_model": embed_model,
            "chunks": [chunk.to_dict() for chunk in self.chunks],
            "embeddings": self.embeddings.tolist(),
        }
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    @classmethod
    def load(cls, path: Path) -> tuple["RagIndex", str]:
        payload = json.loads(path.read_text(encoding="utf-8"))
        chunks = [DocumentChunk.from_dict(item) for item in payload["chunks"]]
        embeddings = np.asarray(payload["embeddings"], dtype=float)
        return cls(chunks, embeddings), payload["embed_model"]


def select_relevant_results(
    results: list[SearchResult],
    min_score: float,
    max_score_gap: float,
) -> list[SearchResult]:
    """Keep results that are strong enough and reasonably close to the best match."""
    if not results:
        return []
    best_score = results[0].score
    cutoff = max(min_score, best_score - max_score_gap)
    return [result for result in results if result.score >= cutoff]


def _normalise_rows(matrix: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Document embeddings cannot contain zero vectors.")
    return matrix / norms
