# SPEC: Course 1, Module 2 — Exercises 1 & 2, rebuilt locally

**Folder:** `course_01/m2_langchain_basics/`
**Author:** Shailesh (first draft written with tutor as a worked example) · **Date:** 2026-11-07

## 1. Goal
Rebuild IBM lab Exercises 1 and 2 with current LangChain (1.x) on my own machine, and **measure** the results instead of eyeballing them.
- **Exercise 1:** How consistent is each model run-to-run at its **default** setting, and how do two models differ in style? Temperature is tested on GPT only, and only if `OPENAI_MODEL` accepts it (current Claude models reject it via our stack; see Section 5).
- **Exercise 2:** How reliably can an LLM return structured JSON, and how often is that JSON actually *correct*?

Afterwards I should be able to explain: what temperature is meant to change and why I couldn't test it on current models, how consistent each model is at its default, why parseable ≠ schema-valid ≠ correct, and what my pass rates say (and don't say).

## 2. Scope
- **In scope:** Exercise 1 (run-to-run consistency of two models at their defaults), Exercise 2 (JSON extraction with an eval over 21 movies), a short "IBM lab code vs current code" note.
- **Out of scope:** RAG, memory, chains, agents (later builds); any UI; retries to improve pass rates (we measure raw behaviour first).

## 3. Building blocks and data flow
- **Ex 1:** `prompt string → chat model (Claude Haiku 5.5 or GPT, model default) → text` → repeated 3× per prompt per model → compare outputs.
- **Ex 2:** `{"movie_name": ...} → prompt template (+ format instructions) → Claude Haiku → JsonOutputParser → dict → validator → compare with golden answers`.

## 4. Inputs and outputs
| Step | Input | Output |
|---|---|---|
| `run_prompt(model, prompt)` | model name, str (no temperature: always the model default) | `{"text": str, "seconds": float}` |
| `extract_movie(movie_name)` | `"The Matrix"` | raw text + parsed dict, e.g. `{"title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski", "year": 1999, "genre": "Science fiction"}`, or a recorded parse failure |
| `validate_movie(d)` | parsed dict | `True/False` + reason (schema check: exactly the 4 keys `title`, `director`, `year`, `genre`; a 5th key is invalid; `year` must be a real int, not a string like `"1999"` and not a bool) |
| `score_movie(d, golden)` | parsed dict + golden row | `director_ok`, `year_ok` (bools) |

**Unknown values:** if the model doesn't know a movie, it must return `null` for unknown fields (the prompt must say this). Inventing values is a failure. For the fake movie, `title` may echo the input.

## 5. Constraints
- **Models:** Claude Haiku 5.5 (`claude-haiku-5-5`) for both exercises, always called with **no `temperature`** (model default). Exercise 1 compares it with OpenAI (`OPENAI_MODEL` from `.env`).
- **Claude temperature:** rejected for `claude-haiku-5-5` and `claude-haiku-4-5` via langchain-anthropic + SDK 2.x (400 "Extra inputs are not permitted"); cause (model vs API vs SDK routing) not determined; not investigated further. (Observed 2026-11-25.)
- **Libraries:** `langchain-core`, `langchain-anthropic`, `langchain-openai` (1.x). No legacy classes (`WatsonxLLM`, `LLMChain`, `pydantic_v1`). Use plain `pydantic`.
- **Keys:** from `.env` via python-dotenv only. Never printed.
- **Budget:** Ex 1 main = 3 prompts × 2 models × 3 runs at default = **18 calls**; Ex 1 GPT temperature section (only if accepted) = 3 prompts × 2 temperatures × 3 runs = **+18 calls**. Ex 2 = **21 calls** (+21 for the stretch goal). Max ~78 calls per full run (a few cents). One-off checks: 1 GPT temperature check, 1 Matrix extraction smoke test (done), 1 forced-timeout test (2 attempts).
- **Format:** one Jupyter notebook for the exercises; results shown as tables (pandas allowed).

## 6. Success criteria (decided before building)
**Exercise 1 — these are predictions to test, not pass/fail:**
- P1: At the model default, the factual prompt gives identical output in ≥ 2 of 3 runs (per model).
- P2: At the model default, the creative prompt gives 3 different outputs (per model).
- Record per setting: number of distinct outputs (out of 3), average length (words), average latency.
- GPT temperature section (if run): same three metrics per prompt × temperature; descriptive only, no predictions. If `OPENAI_MODEL` rejects `temperature`, the results say temperature is "not testable on current models".

**Exercise 2 — pass/fail:**
- Parse rate ≥ 20/21 (output turns into a dict). Reported two ways:
  - **Lenient:** `JsonOutputParser` succeeds. It strips code fences and repairs truncated JSON (e.g. `{"a": 1` → `{'a': 1}`). The ≥ 20/21 threshold applies to this rate.
  - **Strict:** plain `json.loads` on the raw text succeeds (no fence stripping, no repair). Reported alongside, not pass/fail.
- Schema-valid rate ≥ 20/21 (all 4 keys present; `year` is an int between 1888 and 2026, or null; strings non-empty or null).
- Correctness ≥ 16/18 on the unambiguous real movies (rows 1–17 and 21): director and year both match.
- Fake movie (row 20): **no invented director or year**. Pass = `director is None` AND `year is None`. `title` may echo the input. If `genre` is not null, record "partial invention" (this does not fail the test). Pass/fail on its own; this is the hallucination check.
- Ambiguous titles (rows 18–19): not scored; record which film the model chose, inferred from the returned year/director. (The 4-key schema has no field for flagging ambiguity, so flagging is not measured.)
- **Denominators:** if any API errors occur, show both counts, e.g. "19/20 (1 api_error)", i.e. out of the attempts that got a response, plus the api_error count.

## 7. Evals and test cases

**Exercise 1 prompts** (from the IBM lab):
1. Creative: "Write a short poem about artificial intelligence."
2. Factual: "What are the key components of a neural network?"
3. Instruction-following: "List 5 tips for effective time management."
Main experiment: each prompt × 3 runs at the model default (no `temperature`), for `claude-haiku-5-5` and `OPENAI_MODEL`.
GPT temperature section (only if the test call accepts `temperature=0`): each prompt × temperatures 0 and 1 × 3 runs, GPT only. Note: temperature 0 is close to deterministic but not guaranteed identical. "Identical" = exact string match after stripping whitespace.

**Exercise 2 golden set** (expected answers written by me, not by the AI):
| # | Movie | Expected director (match on surname) | Expected year |
|---|---|---|---|
| 1 | The Matrix | Wachowski | 1999 |
| 2 | Inception | Nolan | 2010 |
| 3 | Parasite | Bong | 2019 |
| 4 | Titanic | Cameron | 1997 |
| 5 | Spirited Away | Miyazaki | 2001 |
| 6 | The Godfather | Coppola | 1972 |
| 7 | Pulp Fiction | Tarantino | 1994 |
| 8 | Jurassic Park | Spielberg | 1993 |
| 9 | The Shawshank Redemption | Darabont | 1994 |
| 10 | Get Out | Peele | 2017 |
| 11 | Amélie | Jeunet | 2001 |
| 12 | Mad Max: Fury Road | Miller | 2015 |
| 13 | The Dark Knight | Nolan | 2008 |
| 14 | Toy Story | Lasseter | 1995 |
| 15 | Everything Everywhere All at Once | Kwan | 2022 |
| 16 | Dangal | Tiwari | 2016 |
| 17 | 3 Idiots | Hirani | 2009 |
| 18 | Crash *(ambiguous: 1996 Cronenberg / 2004 Haggis)* | not scored | not scored |
| 19 | Little Women *(ambiguous: 1994 Armstrong / 2019 Gerwig)* | not scored | not scored |
| 20 | The Glass Orchard of Mars *(fake)* | null | null |
| 21 | The Godfather Part II *(sequel)* | Coppola | 1974 |

Row 21 checks that the model doesn't confuse a sequel with the original: Coppola is right either way, so only the year (1974, not 1972) catches the mistake. Rows 1–17 and 21 are scored for correctness.

**Matching rules:** year = exact integer match. Director = expected surname appears in the output as a **whole word** (case-insensitive), with an optional trailing "s" so plurals match (e.g. "The Wachowskis" matches "Wachowski"; "Bongo" does not match "Bong"). Genre is not scored (subjective); it only has to be a non-empty string or null.

**Exercise 2 model settings:** `claude-haiku-5-5`, no `temperature` (model default; see Section 5), `max_tokens` 1024.

**Retry-path test (1 forced error, makes real requests):** call with a very small timeout so the request times out. Expected: exactly 2 attempts (1 retry), then `status = "api_error"`. No other forced errors.

**Offline tests (no API calls)** for `validate_movie` and `score_movie`:
| Input | Expected |
|---|---|
| `{"title":"X","director":"Y","year":"1999","genre":"Z"}` | invalid (year is a string) |
| `{"title":"X","director":"Y","year":True,"genre":"Z"}` | invalid (year is a bool) |
| valid 4 keys + a 5th key | invalid |
| year 1850 | invalid |
| director "George Miller" vs expected "Miller" | `director_ok` True |
| director "Frank Miller" vs expected "Miller" | `director_ok` True — documents a known **false pass** of the surname rule (see Section 10) |
| director "Bongo Smith" vs expected "Bong" | `director_ok` False (whole-word rule) |
| director "The Wachowskis" vs expected "Wachowski" | `director_ok` True (optional plural "s") |
| `score_movie` on a `fake` row | raises `ValueError` |
| `score_movie` on an `ambiguous` row | raises `ValueError` |

## 8. Failure handling
- **Parse failure:** do not retry. Record it as a failure, keep the raw model output, and show it in the results table. Each row records both `strict_parse_ok` (plain `json.loads`) and the lenient `JsonOutputParser` result; a row that parses only leniently is kept and flagged.
- **API error** (timeout, rate limit): retry once, then record as `api_error` and continue with the next item. API errors are counted and reported separately, not mixed into the parse rate.
- Nothing is skipped silently. Every one of the 21 movies and every Ex 1 call (18, or 36 with the GPT temperature section) appears in the results.
- **If `OPENAI_MODEL` rejects `temperature=0`** in the one test call: skip the GPT temperature section and record temperature as "not testable on current models" in the results. GPT stays in the main (default) comparison.
- **Claude and `temperature`:** never passed (see Section 5).
- **A non-retryable error** (e.g. a 400 bad request, bad key, unknown model) stops the run with the original error. It is not retried and not counted as `api_error`.

## 9. Deliverables
- `m2_exercises.ipynb`: Ex 1 and Ex 2, with results tables, plus the offline test cell from Section 7.
- `data/golden_movies.json`: the golden table above, copied exactly. Each row: `{"id", "movie", "expected_director_surname", "expected_year", "category": "scored" | "ambiguous" | "fake", "note"}`; "not scored" cells and the fake movie's expected values are `null`.
- `REVIEW_NOTES.md`: issues I caught when reviewing the AI-written code. Created with headings only; I fill it in.
- A final markdown cell in the notebook: results vs success criteria, a placeholder for "What surprised me" (I write this), and a 4-row "IBM lab code → current code" table.

**Stretch (only after the above works):** run Ex 2 a second way, with `ChatAnthropic(...).with_structured_output(Movie)` instead of prompt + JsonOutputParser, and compare parse/schema-valid rates (apply the "fewer than 3 movies = inconclusive" rule from Section 10).

## 10. Open questions
- Is exact string match too strict for "identical"? (A single changed comma counts as different.) Keep it for now and note the limitation.
- Should a director match need the full name? Surname is a simpler first rule; are there films where it could give a false pass?
- ~~20 movies is a small sample: what difference between two approaches would I actually trust?~~
  **My answer:** with ~20 movies, one movie is about 5 percentage points, and re-running the same approach can easily change one or two results by chance. So I won't trust a difference of only 1–2 movies. Rule for the stretch comparison: a difference of fewer than 3 movies is "inconclusive"; I'll also list exactly which movies changed result, and if it matters, re-run or grow the test set.
