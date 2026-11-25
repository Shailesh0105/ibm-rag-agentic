# CLAUDE.md
- SPEC.md is the source of truth. If code and spec disagree, ask; don't guess.
- Never edit tests or evals/golden.jsonl to make them pass.
- No swallowed errors: log the full error, return a generic message to callers.
- Current APIs only: langchain 1.x, langchain-anthropic, FastAPI, Pydantic v2.
- Model: Claude Haiku via ANTHROPIC_MODEL. Keys only from .env.
- Run tests with: uv run pytest -q
