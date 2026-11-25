# SPEC: Course 1, Module 2 — Exercises 1 & 2, rebuilt locally

**Folder:** `course_01/m2_langchain_basics/`
**Author:** Shailesh (first draft written with tutor as a worked example) · **Date:** 2026-11-07

## 1. Goal
Rebuild IBM lab Exercises 1 and 2 with current LangChain (1.x) on my own machine, and **measure** the results instead of eyeballing them.
- **Exercise 1:** How do model choice and temperature affect consistency and style of outputs?
- **Exercise 2:** How reliably can an LLM return structured JSON, and how often is that JSON actually *correct*?

Afterwards I should be able to explain: what temperature changes, why parseable ≠ schema-valid ≠ correct, and what my pass rates say (and don't say).

## 2. Scope
- **In scope:** Exercise 1 (model × temperature comparison), Exercise 2 (JSON extraction with an eval over 20 movies), a short "IBM lab code vs current code" note.
- **Out of scope:** RAG, memory, chains, agents (later builds); any UI; retries to improve pass rates (we measure raw behaviour first).

## 3. Building blocks and data flow
- **Ex 1:** `prompt string → chat model (Claude Haiku or GPT, temperature T) → text` → repeated 3× per setting → compare outputs.
- **Ex 2:** `{"movie_name": ...} → prompt template (+ format instructions) → Claude Haiku → JsonOutputParser → dict → validator → compare with golden answers`.

## 4. Inputs and outputs
| Step | Input | Output |
|---|---|---|
| `run_prompt(model, temperature, prompt)` | model name, float, str | `{"text": str, "seconds": float}` |
| `extract_movie(movie_name)` | `"The Matrix"` | raw text + parsed dict, e.g. `{"title": "The Matrix", "director": "Lana Wachowski, Lilly Wachowski", "year": 1999, "genre": "Science fiction"}`, or a recorded parse failure |
| `validate_movie(d)` | parsed dict | `True/False` + reason (schema check) |
| `score_movie(d, golden)` | parsed dict + golden row | `director_ok`, `year_ok` (bools) |

**Unknown values:** if the model doesn't know a movie, it must return `null` for unknown fields (the prompt must say this). Inventing values is a failure.

## 5. Constraints
- **Models:** Claude Haiku 5.5 (`claude-haiku-5-5`) for Exercise 2. Exercise 1 compares two models, so it uses Claude Haiku **and** OpenAI (`OPENAI_MODEL` from `.env`).
- **Libraries:** `langchain-core`, `langchain-anthropic`, `langchain-openai` (1.x). No legacy classes (`WatsonxLLM`, `LLMChain`, `pydantic_v1`). Use plain `pydantic`.
- **Keys:** from `.env` via python-dotenv only. Never printed.
- **Budget:** Ex 1 = 3 prompts × 2 models × 2 temperatures × 3 runs = **36 calls**. Ex 2 = **20 calls** (+20 for the stretch goal). Max ~76 calls per full run (a few cents).
- **Format:** one Jupyter notebook for the exercises; results shown as tables (pandas allowed).

## 6. Success criteria (decided before building)
**Exercise 1 — these are predictions to test, not pass/fail:**
- P1: At temperature 0.1, the factual prompt gives identical output in ≥ 2 of 3 runs (per model).
- P2: At temperature 0.9, the creative prompt gives 3 different outputs (per model).
- Record per setting: number of distinct outputs (out of 3), average length (words), average latency.

**Exercise 2 — pass/fail:**
- Parse rate ≥ 19/20 (output turns into a dict).
- Schema-valid rate ≥ 19/20 (all 4 keys present; `year` is an int between 1888 and 2026, or null; strings non-empty or null).
- Correctness ≥ 15/17 on the unambiguous real movies (rows 1–17): director and year both match.
- Fake movie (row 20): **no invented director or year** (all null). Pass/fail on its own; this is the hallucination check.
- Ambiguous titles (rows 18–19): not scored; record which film the model chose and whether it flagged the ambiguity.

## 7. Evals and test cases

**Exercise 1 prompts** (from the IBM lab):
1. Creative: "Write a short poem about artificial intelligence."
2. Factual: "What are the key components of a neural network?"
3. Instruction-following: "List 5 tips for effective time management."
Temperatures: 0.1 and 0.9. "Identical" = exact string match after stripping whitespace.

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

**Matching rules:** year = exact integer match. Director = expected surname appears in the output (case-insensitive). Genre is not scored (subjective); it only has to be a non-empty string or null.

## 8. Failure handling
- **Parse failure:** do not retry. Record it as a failure, keep the raw model output, and show it in the results table.
- **API error** (timeout, rate limit): retry once, then record as `api_error` and continue with the next item. API errors are counted and reported separately, not mixed into the parse rate.
- Nothing is skipped silently. Every one of the 20 movies and 36 Ex 1 calls appears in the results.
- **If `OPENAI_MODEL` rejects the `temperature` parameter** (some newer models do): record that, run GPT at its default setting, and note it in the results. Don't remove GPT from the comparison silently.

## 9. Deliverables
- `m2_exercises.ipynb`: Ex 1 and Ex 2, with results tables.
- `data/golden_movies.json`: the golden table above, copied exactly.
- `REVIEW_NOTES.md`: issues I caught when reviewing the AI-written code.
- A final markdown cell in the notebook: results vs success criteria, what surprised me, and a 4-row "IBM lab code → current code" table.

**Stretch (only after the above works):** run Ex 2 a second way, with `ChatAnthropic(...).with_structured_output(Movie)` instead of prompt + JsonOutputParser, and compare parse/schema-valid rates.

## 10. Open questions
- Is exact string match too strict for "identical"? (A single changed comma counts as different.) Keep it for now and note the limitation.
- Should a director match need the full name? Surname is a simpler first rule; are there films where it could give a false pass?
- 20 movies is a small sample: what difference between two approaches would I actually trust?
