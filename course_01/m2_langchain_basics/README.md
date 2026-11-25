# Course 1, Module 2: LangChain basics, rebuilt locally

The IBM lab *"Build Smarter AI Apps: Empower LLMs with LangChain"* has two exercises I rebuilt with current tools, adding the measurement the lab leaves out:

- **Exercise 1:** compare models and settings. The lab compares temperatures by eye.
- **Exercise 2:** get structured JSON from an LLM. The lab checks one movie by eye.

Here, both are driven by a written spec with success criteria decided before building, a golden set of expected answers, and automated scoring.

## Files

| File | What it is |
|---|---|
| [`SPEC.md`](SPEC.md) | The spec: goal, scope, success criteria, test cases, failure handling, and every decision made along the way |
| [`m2_exercises.ipynb`](m2_exercises.ipynb) | Setup, offline tests, extraction and the Exercise 1 pre-check |
| [`data/golden_movies.json`](data/golden_movies.json) | 21 movies with expected director and year: 18 scored, 2 ambiguous titles, 1 fake movie |
| [`REVIEW_NOTES.md`](REVIEW_NOTES.md) | Mistakes caught in AI-written work, good patterns, decisions, lessons |

## What was built

**Exercise 2: JSON extraction and its eval**
- `extract_movie`: prompt → Claude Haiku 5.5 → `JsonOutputParser`, with the parser kept *outside* the chain so the raw text survives a parse failure. Records a **strict** parse (`json.loads`) and a **lenient** one (LangChain's parser, which repairs broken JSON), plus `stop_reason`.
- `validate_movie`: a hand-written schema check (exactly 4 keys, `year` a real int, so not `"1999"` or `True`). Pydantic was avoided on purpose: it would silently convert `"1999"` to `1999` and hide the errors being counted.
- `score_movie`: correctness against the golden set (exact year; surname as a whole word, with an optional plural "s").
- The golden set includes a **fake movie** (hallucination check), **ambiguous titles** (*Crash*, *Little Women*) and a **sequel** (*The Godfather Part II*, where only the year catches a mix-up).

**Exercise 1: reframed.** Current Claude models rejected `temperature` in this stack, so the experiment became **run-to-run consistency at the default setting** (Claude Haiku 5.5 vs GPT), with temperature tested on GPT only if it accepts the parameter.

## Status

| Item | Status |
|---|---|
| Offline tests for scoring and validation (11) | ✅ Pass, no API calls |
| Extraction smoke test (*The Matrix*) | ✅ Plain JSON, strict parse OK, schema-valid, correct |
| Full Exercise 2 eval (21 movies) | ⏸ Not run yet |
| Exercise 1 consistency run (18 calls) | ⏸ Not run yet |
| GPT temperature pre-check (1 call) | ⏸ In the notebook; result not recorded yet |
| Forced-timeout retry test | ⏸ Not run yet |

I paused here on purpose. The aim of this module was to learn **how to build and evaluate an exercise like this**; the full runs are left for later.

## Key findings

1. **Temperature was rejected.** `claude-haiku-5-5` and `claude-haiku-4-5` both returned `400 "temperature: Extra inputs are not permitted"` via langchain-anthropic and Anthropic SDK 2.x. The course teaches temperature as a core setting. Whether the cause is the model, the API or the SDK wasn't determined; I time-boxed the investigation and recorded it as unknown.
2. **A forgiving parser inflates parse rates.** `JsonOutputParser` turns `'{"a": 1'` into `{'a': 1}`, so strict and lenient parse rates are reported separately.
3. **Matching rules trade false passes for false fails.** Substring matching let "Bongo" pass for "Bong"; whole-word matching then failed "The Wachowskis"; "Frank Miller" still passes for "Miller" and is kept as a documented false pass.
4. **Small samples:** with about 20 items, one item is 5 percentage points, so differences of fewer than 3 movies are treated as inconclusive.
5. **Notebook hidden state:** after the assistant edited the file, the kernel still ran the old code. Always **Restart Kernel → Run All** before trusting results.

## Course code vs this build

| IBM lab (LangChain 0.2.x) | This build (LangChain 1.x) |
|---|---|
| `WatsonxLLM` + `ModelInference` (IBM SDK) | `ChatAnthropic` (langchain-anthropic) |
| `GenParams.TEMPERATURE` | Not sent: rejected by current Claude models in this stack |
| `langchain_core.pydantic_v1` | Pydantic v2 (and a hand-written validator) |
| `prompt \| llm \| parser`, checked by eye | Parser outside the chain, strict + lenient parse, golden-set scoring |

## Run it

Open `m2_exercises.ipynb` in VS Code with the project's `.venv` kernel, then **Restart Kernel → Run All**. That makes **2 API calls**: the GPT temperature check and the *Matrix* smoke test.
