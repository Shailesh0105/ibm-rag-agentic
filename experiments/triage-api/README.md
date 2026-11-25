# Ticket Triage API (practice project)

A small FastAPI service that sends a customer support ticket to Claude and returns a **category** (billing, technical, account, other) and an **urgency** (high, medium, low), plus an eval harness that scores it against a golden set.

It's a first practice project in the current stack: FastAPI instead of the course's Flask, LangChain 1.x, and Claude Haiku.

## Structure

```
app/main.py         web layer: POST /triage, GET /health; errors are logged in full and returned to callers as a generic 502
app/triage.py       the LLM step: prompt (ticket treated as data, not instructions) → Claude → TriageResult
app/schemas.py      request and response models (Pydantic v2)
evals/golden.jsonl  12 tickets with expected category and urgency
evals/run_eval.py   runs the golden set through the real chain and scores it (12 API calls)
tests/              offline tests: schemas, API with a fake chain, eval scoring
```

## Run

```bash
cd experiments/triage-api
uv sync
cp .env.example .env              # add your Anthropic key and model
uv run pytest -q                  # offline tests, no API calls
uv run fastapi dev app/main.py    # local server at http://127.0.0.1:8000/docs
uv run python -m evals.run_eval   # real eval: 12 API calls
```

Status: tests written and passing offline; the eval with a real key hasn't been run yet.
