"""API tests with a fake chain: fast, free, no API key needed."""
from fastapi.testclient import TestClient

from app.main import app, get_chain
from app.schemas import TriageResult


class FakeChain:
    """Stands in for prompt | Claude. Records what it was sent."""

    def __init__(self, result=None, error=None):
        self.result, self.error, self.calls = result, error, []

    def invoke(self, inputs):
        self.calls.append(inputs)
        if self.error:
            raise self.error
        return self.result


GOOD = TriageResult(category="billing", urgency="high",
                    summary="Customer was charged twice.", reply_draft="Sorry about that!")


def client_with(fake):
    app.dependency_overrides[get_chain] = lambda: fake
    return TestClient(app)


def teardown_function():
    app.dependency_overrides.clear()


def test_valid_ticket_returns_triage():
    fake = FakeChain(result=GOOD)
    r = client_with(fake).post("/triage", json={"message": "Charged twice"})
    assert r.status_code == 200
    assert r.json()["category"] == "billing"
    assert fake.calls == [{"message": "Charged twice"}]


def test_empty_message_rejected_before_model_call():
    fake = FakeChain(result=GOOD)
    r = client_with(fake).post("/triage", json={"message": ""})
    assert r.status_code == 422
    assert fake.calls == []  # we never paid for a model call


def test_missing_field_rejected():
    r = client_with(FakeChain(result=GOOD)).post("/triage", json={})
    assert r.status_code == 422


def test_too_long_message_rejected():
    r = client_with(FakeChain(result=GOOD)).post("/triage", json={"message": "x" * 2001})
    assert r.status_code == 422


def test_model_failure_returns_502_without_leaking_details():
    fake = FakeChain(error=RuntimeError("secret internal detail"))
    r = client_with(fake).post("/triage", json={"message": "Help"})
    assert r.status_code == 502
    assert "secret" not in r.text
