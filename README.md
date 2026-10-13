# Architecture AI RAG Proof of Concept

Offline proof of concept for architecture-model data and building-code retrieval.

The demo reads a synthetic Revit-style model and a synthetic building-code excerpt that live in this repository. It splits the code text into sections, finds the sections that share words with the question and the model, and prints each match with its source. A qualified architect still has to review every finding. This demo does not certify code compliance.

## What you will see

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

## Clone and run

Python 3.9 or newer is enough. There are no packages to install.

```bash
git clone https://github.com/yellowlotuscg/architecture-ai-rag-poc.git
cd architecture-ai-rag-poc
PYTHONPATH=src python3 demo.py
```

The script reads `data/sample_building_code.txt` and `data/sample_revit_model.json`, then prints JSON. Pass `--code`, `--model`, or `--question` to point at different local files or ask a different question.

## Tests

The tests use the Python standard library. From the repository root:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -v
```

GitHub Actions runs that same command on pull requests and on pushes to `main`. The workflow checks out the code without saved credentials and does not use secrets.

## Public scope

This repository is a small example you can read through. It leaves out firm-specific controls, private document handling, production connectors, and deployment infrastructure.

A later version could add the following. This repository stops at the offline demo.

1. PDF ingestion with page and section metadata.
2. Firm-scoped document collections.
3. Embeddings behind the same explainable retrieval contract.
4. IFC and Revit export adapters, before a live Revit plugin.
5. A review queue with architect comments and decisions.
6. Code-edition and jurisdiction validation.
7. A private FastAPI and SQLite pilot, with storage chosen during that work.
8. A Revit add-in only after the document and review workflow proves useful.

## Safety and scope

This is research and demo software. It is not a substitute for:

- a licensed architect
- a code official
- jurisdiction-specific legal review
- project-specific engineering
- final construction documents
- life-safety certification

Keep client models, private project files, licensed code PDFs, credentials, and proprietary firm data out of this public repository.

## License

[MIT](LICENSE). Copyright (c) 2026 Matthew Coggins.
