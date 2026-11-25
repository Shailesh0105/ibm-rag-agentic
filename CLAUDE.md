# CLAUDE.md — ibm-rag-agentic (learning workspace)

I am learning RAG and agentic AI to become an AI PM / Forward Deployed Engineer.
My goal is to learn to **direct and review** AI-written code, not to collect code I can't explain.

## Workflow rules
1. **No code without a spec.** Before implementing anything, check that a `SPEC.md` exists in the
   relevant folder. If it doesn't, or it's missing inputs/outputs, constraints or test cases,
   ask me to write or complete it. Do not write it for me.
2. **Implement only what the spec says.** If something in the spec is ambiguous or seems wrong,
   ask before choosing. List any assumptions you made at the end of your reply.
3. **Small, reviewable changes.** Prefer several small diffs over one large one.
4. **Explain non-obvious decisions** (library choice, parameters, error handling) in 1–2 lines each,
   so I can review them. Do not explain obvious syntax.
5. **Never change tests, eval datasets or eval scripts to make them pass.** If a test fails,
   report it and propose a fix to the code, not to the test.
6. **Errors must be visible.** No bare `except:` or silently swallowed exceptions; no blanket
   warning suppression. Fail loudly with a clear message.

## Technical defaults
- Python 3.12, managed with `uv` (`uv add <pkg>`, `uv run python <file>`). Do not use pip directly.
- LangChain 1.x current APIs (LCEL, `langchain_core`). Do not use legacy classes such as
  LLMChain, SequentialChain, ConversationChain or RetrievalQA unless I ask for a course comparison.
- **Default LLM: Anthropic Claude** (`claude-haiku-5-5`; `claude-sonnet-5-5` for harder tasks).
  Use OpenAI (model from `OPENAI_MODEL` in `.env`) only when a task needs a second model.
- Embeddings: a local sentence-transformers model unless the spec says otherwise.
- Keys come only from `.env` via python-dotenv. Never hard-code, print or log keys.
- Before using any library API you are not certain is current, say so and suggest how to verify it.

## When you finish a task
Summarise: files changed, how to run it, what you tested (and what you did **not** test).
