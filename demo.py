"""Run the offline synthetic architecture review demo."""
import argparse
import json
from pathlib import Path

from architecture_ai_rag import ReviewEngine, chunk_code_document, load_model


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--code", default="data/sample_building_code.txt")
    parser.add_argument("--model", default="data/sample_revit_model.json")
    parser.add_argument("--question", default="What accessibility and egress requirements should be reviewed?")
    args = parser.parse_args()
    chunks = chunk_code_document(Path(args.code).read_text(encoding="utf-8"), Path(args.code).name)
    reviews = ReviewEngine(chunks).review_model(load_model(Path(args.model)), args.question)
    print(json.dumps([review.to_dict() for review in reviews], indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
