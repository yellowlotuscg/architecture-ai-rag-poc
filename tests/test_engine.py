import json
import tempfile
import unittest
from pathlib import Path

from architecture_ai_rag import ReviewEngine, chunk_code_document, load_model


CODE = """## 1001.2 Accessible Route\n### Clear width\nAccessible route clear width is 36 inches.\n### Exception\nExisting conditions may use 32 inches with authority approval.\n## 1002.4 Bathroom Turning Space\n### Turning diameter\nProvide a 60 inch turning space.\n"""


class ArchitectureRagTests(unittest.TestCase):
    def test_chunking_preserves_section_and_exception(self):
        chunks = chunk_code_document(CODE, "code.txt")
        self.assertEqual([chunk.section for chunk in chunks], ["1001.2 Accessible Route", "1001.2 Accessible Route", "1002.4 Bathroom Turning Space"])
        self.assertIn("authority approval", chunks[1].text)

    def test_retrieval_preserves_citation(self):
        engine = ReviewEngine(chunk_code_document(CODE, "code.txt"))
        results = engine.retrieve("accessible route clear width", limit=1)
        self.assertEqual(results[0][0].source, "code.txt")
        self.assertGreater(results[0][1], 1)

    def test_model_review_is_advisory_and_cited(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "model.json"
            path.write_text(json.dumps({"elements": [{"id": "door-1", "category": "Door", "properties": {"clear_width_inches": 31}}]}), encoding="utf-8")
            review = ReviewEngine(chunk_code_document(CODE, "code.txt")).review_model(load_model(path))[0]
        self.assertEqual(review.model_element, "door-1")
        self.assertTrue(review.findings)
        self.assertIn("qualified architect", review.disclaimer)
        self.assertEqual(review.findings[0]["review_status"], "architect_review_required")


if __name__ == "__main__":
    unittest.main()
