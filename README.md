# IBM RAG & Agentic AI: learning workspace

I'm working through IBM's [RAG and Agentic AI Professional Certificate](https://www.coursera.org/professional-certificates/ibm-rag-and-agentic-ai) on Coursera, on my way to an **AI Product Manager / Forward Deployed Engineer** role.

This repository is where I rebuild the course exercises **locally with current tools**, and practise two skills the course doesn't emphasise:

1. **Evaluation:** deciding what "working" means before building, then measuring it instead of eyeballing outputs.
2. **Directing AI coding assistants:** writing the spec myself, letting Claude Code draft the code, and reviewing every change.

## How I work

Every exercise follows the same loop:

| Step | Who | What |
|---|---|---|
| 1. Spec | Me | `SPEC.md`: goal, scope, inputs/outputs, success criteria and test cases, decided **before** any code |
| 2. Plan | Claude Code (Plan mode) | Plans from the spec and lists ambiguities; I check the plan against the spec |
| 3. Build | Claude Code (Manual mode) | Small diffs; I review each one before accepting |
| 4. Run | Me | Restart kernel, run everything, read errors before asking for fixes |
| 5. Evaluate | Me | Compare results with the success criteria and my predictions; read the failures |
| 6. Record | Me | `REVIEW_NOTES.md`: mistakes caught, good patterns, what I learned |

The rules the coding assistant must follow are in [`CLAUDE.md`](CLAUDE.md) (spec first, never edit tests to make them pass, no swallowed errors, current APIs, keys only from `.env`). New exercises start from [`SPEC_TEMPLATE.md`](SPEC_TEMPLATE.md).

## Progress

| Course | Module | Course work | Local build |
|---|---|---|---|
| 1. Develop Generative AI Applications | M2: Introduction to LangChain | Graded quiz: 100% | [`course_01/m2_langchain_basics`](course_01/m2_langchain_basics/): spec, 21-movie golden set, schema check and scoring with 11 offline tests, extraction smoke test passed. Full eval runs pending. |
| 2. Build RAG Applications | — | Next | — |

Course completion and demonstrated skill are tracked separately: a passed quiz isn't proof I can build or evaluate the thing.

## What I've learned so far

From the Module 2 build ([full review notes](course_01/m2_langchain_basics/REVIEW_NOTES.md)):

- **Parseable ≠ schema-valid ≠ correct.** A forgiving parser even repairs cut-off JSON, so I report strict and lenient parse rates separately.
- **Every matching rule trades false passes for false fails.** Fixing "Bongo" matching "Bong" broke "The Wachowskis"; documenting known false passes keeps the eval honest.
- **The spec is the source of truth.** Every decision goes back into `SPEC.md`, or the spec stops being trustworthy.
- **Course material goes stale.** The course teaches temperature as a core setting; current Claude models rejected it in my stack. One cheap test call before the full run caught it.
- **Verify the assistant's claims.** It was confidently wrong about the git history, and "tested" sometimes meant "tested outside the notebook".

## Repository map

```
.
├── CLAUDE.md                  rules for Claude Code in this repo
├── SPEC_TEMPLATE.md           starting point for every exercise spec
├── hello.py                   setup check: one call to Claude and one to GPT
├── .env.example               the settings you need (copy to .env)
├── course_01/
│   └── m2_langchain_basics/   C1 M2 exercises rebuilt locally (see its README)
└── experiments/
    └── triage-api/            practice project: FastAPI + Claude ticket triage with an eval harness
```

## Run it yourself

You need [uv](https://docs.astral.sh/uv/), an Anthropic API key (workspace-scoped) and, only for model comparisons, an OpenAI key.

```bash
git clone https://github.com/Shailesh0105/ibm-rag-agentic.git
cd ibm-rag-agentic
uv sync                  # creates .venv with the exact versions in uv.lock
cp .env.example .env     # then add your keys
uv run python hello.py   # one call to each provider
```

Notebooks: open them in VS Code, select the project's `.venv` kernel, then **Restart Kernel → Run All**. Each notebook says how many API calls it makes.

## Stack

Python 3.12 · uv · LangChain 1.x (the course pins 0.2.x) · Claude Haiku 5.5 by default · OpenAI only when two models are compared · pandas · Jupyter in VS Code · Claude Code.

---
Course content belongs to IBM and Coursera; this repo contains only my own specs, code and notes. API keys are never committed.
