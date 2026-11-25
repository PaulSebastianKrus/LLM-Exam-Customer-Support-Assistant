from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path


HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source: str
    heading: str
    text: str

    def to_dict(self) -> dict[str, str]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> "DocumentChunk":
        return cls(**data)


def _split_long_text(text: str, max_chars: int, overlap_chars: int) -> list[str]:
    """Split text at paragraph boundaries and retain a small overlap."""
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", text) if part.strip()]
    if not paragraphs:
        return []

    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        candidate = f"{current}\n\n{paragraph}".strip()
        if current and len(candidate) > max_chars:
            chunks.append(current)
            overlap = current[-overlap_chars:] if overlap_chars else ""
            current = f"{overlap}\n\n{paragraph}".strip()
        else:
            current = candidate
    if current:
        chunks.append(current)
    return chunks


def chunk_markdown(
    path: Path,
    max_chars: int = 1_200,
    overlap_chars: int = 150,
) -> list[DocumentChunk]:
    """Create chunks that preserve the nearest Markdown heading as metadata."""
    text = path.read_text(encoding="utf-8")
    sections: list[tuple[str, str]] = []
    heading = "Introduction"
    body: list[str] = []

    for line in text.splitlines():
        match = HEADING_PATTERN.match(line)
        if match:
            if body and "\n".join(body).strip():
                sections.append((heading, "\n".join(body).strip()))
            heading = match.group(2).strip()
            body = []
        else:
            body.append(line)

    if body and "\n".join(body).strip():
        sections.append((heading, "\n".join(body).strip()))

    chunks: list[DocumentChunk] = []
    for section_number, (section_heading, section_text) in enumerate(sections, start=1):
        pieces = _split_long_text(section_text, max_chars, overlap_chars)
        for piece_number, piece in enumerate(pieces, start=1):
            chunks.append(
                DocumentChunk(
                    chunk_id=f"{path.stem}:{section_number}:{piece_number}",
                    source=path.name,
                    heading=section_heading,
                    text=piece,
                )
            )
    return chunks


def load_knowledge_base(directory: Path) -> list[DocumentChunk]:
    paths = sorted(directory.glob("*.md"))
    if not paths:
        raise FileNotFoundError(f"No Markdown documents found in {directory}")
    return [chunk for path in paths for chunk in chunk_markdown(path)]
