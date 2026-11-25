"""The eval code is code too: test the scoring with a fake chain."""
from app.schemas import TriageResult
from evals.run_eval import load_golden, run, score


class FakeRawMessage:
    usage_metadata = {"input_tokens": 100, "output_tokens": 20}


class AlwaysBilling:
    def invoke(self, inputs):
        result = TriageResult(category="billing", urgency="low", summary="s", reply_draft="r")
        return {"parsed": result, "raw": FakeRawMessage(), "parsing_error": None}


def test_golden_set_loads_and_has_labels():
    cases = load_golden()
    assert len(cases) >= 10
    assert all({"id", "message", "category", "urgency"} <= c.keys() for c in cases)


def test_scoring_counts_correct_labels():
    cases = [
        {"id": "a", "message": "m", "category": "billing", "urgency": "low"},
        {"id": "b", "message": "m", "category": "technical", "urgency": "high"},
    ]
    summary = score(run(AlwaysBilling(), cases))
    assert summary["category_accuracy"] == 0.5
    assert summary["urgency_accuracy"] == 0.5
    assert summary["schema_valid_rate"] == 1.0
    assert summary["input_tokens"] == 200
