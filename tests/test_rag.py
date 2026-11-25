import numpy as np

from src.documents import DocumentChunk
from src.rag import RagIndex, SearchResult, select_relevant_results


def test_search_returns_most_similar_chunk_first() -> None:
    chunks = [
        DocumentChunk("a", "billing.md", "Refunds", "Annual refund policy"),
        DocumentChunk("b", "security.md", "Passwords", "Password reset policy"),
    ]
    index = RagIndex(chunks, np.asarray([[1.0, 0.0], [0.0, 1.0]]))

    results = index.search([0.9, 0.1], top_k=2)

    assert results[0].chunk.chunk_id == "a"
    assert results[0].score > results[1].score


def test_result_selection_removes_chunks_far_below_best_match() -> None:
    chunk = DocumentChunk("a", "policy.md", "Policy", "Text")
    results = [
        SearchResult(chunk, 0.79),
        SearchResult(chunk, 0.76),
        SearchResult(chunk, 0.70),
    ]

    selected = select_relevant_results(results, min_score=0.30, max_score_gap=0.02)

    assert [result.score for result in selected] == [0.79]
