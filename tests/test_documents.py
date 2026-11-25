from pathlib import Path

from src.documents import chunk_markdown


def test_chunk_markdown_preserves_source_and_heading(tmp_path: Path) -> None:
    document = tmp_path / "policy.md"
    document.write_text("# Refunds\n\nAnnual renewals have a 14-day window.", encoding="utf-8")

    chunks = chunk_markdown(document)

    assert len(chunks) == 1
    assert chunks[0].source == "policy.md"
    assert chunks[0].heading == "Refunds"
    assert "14-day" in chunks[0].text
