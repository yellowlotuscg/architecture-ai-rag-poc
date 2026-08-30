# Architecture AI RAG Proof of Concept

Offline proof of concept for architecture-model data and building-code retrieval.

## What this demonstrates

```text
Revit-style model JSON
    ↓
architecture/code query
    ↓
section-aware code chunks
    ↓
explainable lexical retrieval
    ↓
source-cited review findings
    ↓
architect review required
```

The demo uses synthetic code text and synthetic model data. It does not provide code compliance certification.

## Run locally

```bash
PYTHONPATH=src python3 demo.py
```

Run tests without external dependencies:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

## Public scope

This repository is a small, inspectable technical proof. It intentionally excludes firm-specific controls, private document handling, production connectors, and deployment infrastructure. The private architecture-firm readiness roadmap is maintained separately in Alfred.

## Technical evolution

1. Add PDF ingestion with page and section metadata.
2. Add firm-scoped document collections.
3. Add embeddings behind the same explainable retrieval contract.
4. Add IFC and Revit export adapters rather than depending on a live Revit plugin first.
5. Add a review queue with architect comments and decisions.
6. Add code-edition and jurisdiction validation.
7. Add a private FastAPI + SQLite deployment for a controlled pilot, with storage selected during implementation.
8. Add a Revit add-in only after the document/review workflow proves value.

## Safety and scope

This repository is research/demo software. It must not be used as a substitute for:

- a licensed architect;
- a code official;
- jurisdiction-specific legal review;
- project-specific engineering;
- final construction documents;
- life-safety certification.

Do not place client models, private project files, licensed code PDFs, credentials, or proprietary firm data in this public proof repository.
