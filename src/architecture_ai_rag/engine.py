"""Small, explainable RAG engine for architecture-code review demos.

This POC intentionally uses lexical retrieval instead of opaque embeddings so the
workflow can run offline and every result can be inspected in a code review.
"""
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

_WORD_RE = re.compile(r"[a-z0-9]+(?:\.[a-z0-9]+)?", re.I)


@dataclass(frozen=True)
class CodeChunk:
    chunk_id: str
    section: str
    title: str
    text: str
    source: str
    page: Optional[int] = None
    tags: Tuple[str, ...] = ()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ArchitectureReview:
    question: str
    model_element: str
    model_values: Dict[str, Any]
    findings: List[Dict[str, Any]]
    disclaimer: str = "AI retrieval is advisory. A qualified architect or code official must verify the governing code, jurisdiction, edition, and final design."

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def _tokens(text: str) -> List[str]:
    return [item.lower() for item in _WORD_RE.findall(text)]


def chunk_code_document(text: str, source: str) -> List[CodeChunk]:
    """Split a synthetic code document while keeping section/table/exception context."""
    chunks: List[CodeChunk] = []
    current_section = "UNSPECIFIED"
    current_title = "Untitled requirement"
    buffer: List[str] = []
    index = 0

    def flush() -> None:
        nonlocal index, buffer
        if not buffer:
            return
        body = "\n".join(buffer).strip()
        tags = tuple(sorted(set(_tokens(current_title + " " + body))))
        chunks.append(CodeChunk(
            chunk_id=f"{source}:{current_section}:{index}",
            section=current_section,
            title=current_title,
            text=body,
            source=source,
            tags=tags,
        ))
        index += 1
        buffer = []

    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("## "):
            flush()
            current_section = line[3:].strip()
            current_title = current_section
            continue
        if line.startswith("### "):
            flush()
            current_title = line[4:].strip()
            continue
        buffer.append(line)
    flush()
    return chunks


def load_model(path: Path) -> Dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or "elements" not in payload:
        raise ValueError("model JSON must contain an elements list")
    if not isinstance(payload["elements"], list):
        raise ValueError("model elements must be a list")
    return payload


class ReviewEngine:
    def __init__(self, chunks: Iterable[CodeChunk]) -> None:
        self.chunks = list(chunks)

    def retrieve(self, query: str, limit: int = 5) -> List[Tuple[CodeChunk, int]]:
        query_terms = set(_tokens(query))
        scored: List[Tuple[CodeChunk, int]] = []
        for chunk in self.chunks:
            haystack = set(_tokens(chunk.title + " " + chunk.text))
            score = len(query_terms.intersection(haystack))
            if score:
                scored.append((chunk, score))
        return sorted(scored, key=lambda item: (-item[1], item[0].chunk_id))[:limit]

    def review_element(self, element: Dict[str, Any], question: str = "What requirements should be reviewed?") -> ArchitectureReview:
        model_values = dict(element.get("properties", {}))
        query = " ".join([question, str(element.get("category", "")), str(element.get("type", ""))] + [f"{k} {v}" for k, v in model_values.items()])
        findings = []
        for chunk, score in self.retrieve(query):
            findings.append({
                "chunk_id": chunk.chunk_id,
                "section": chunk.section,
                "title": chunk.title,
                "evidence": chunk.text,
                "source": chunk.source,
                "relevance_score": score,
                "review_status": "architect_review_required",
            })
        return ArchitectureReview(
            question=question,
            model_element=str(element.get("id", "unknown")),
            model_values=model_values,
            findings=findings,
        )

    def review_model(self, model: Dict[str, Any], question: str = "What requirements should be reviewed?") -> List[ArchitectureReview]:
        return [self.review_element(element, question) for element in model["elements"]]
