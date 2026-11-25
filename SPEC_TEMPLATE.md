# SPEC: <name of the build>

> Copy this file into the build's folder as `SPEC.md` and fill it in **before** asking Claude Code for any code.
> Write it yourself. Aim for 1 page; short bullet points are fine. Delete the guidance lines (starting with >) when done.

## 1. Goal
> One or two sentences: what this build does and why. What should I understand or be able to show afterwards?

## 2. Scope
- **In scope:**
- **Out of scope (explicitly not doing):**
> Saying what's out is as important as what's in. It stops the AI from adding things you didn't ask for.

## 3. Building blocks and data flow
> Which components, in order, and what passes between them. A one-line flow is enough, e.g.:
> `input dict → prompt template → Claude Haiku → JSON parser → validated dict`

## 4. Inputs and outputs
| Step / function | Input (type, example) | Output (type, example) |
|---|---|---|
| | | |
> Be concrete: `{"movie_name": "The Matrix"}` → `{"title": str, "director": str, "year": int, "genre": str}`

## 5. Constraints
- Models: Claude Haiku 5.5 by default; OpenAI only for: <reason, or "not used">
- Libraries: LangChain 1.x current APIs; no legacy classes (unless shown for comparison)
- Keys from `.env` only
- Budget: max ~<N> API calls per full run (estimate: calls × runs)
- Other: <e.g., runs in under 2 minutes; notebook vs script>

## 6. Success criteria (decide these BEFORE building)
> How will you know it works? Use numbers where you can.
- e.g., JSON parses successfully on ≥ 19/20 inputs
- e.g., `year` is an integer in every parsed result

## 7. Evals and test cases
| # | Input | Expected result | What it checks |
|---|---|---|---|
| 1 | normal case | | happy path |
| 2 | edge case | | |
| 3 | bad / unusual input | | failure handling |
> Include at least one input that should fail or be refused. Write the expected results yourself; don't let the AI write them.

## 8. Failure handling
> What should happen when a step fails (unparseable output, API error, empty result)? Retry? Fail loudly with a clear message?
> Never: silently skip or swallow the error.

## 9. Deliverables
- Files: <e.g., `lab.ipynb`, `evals.py`, `REVIEW_NOTES.md`>
- What the final output shows: <e.g., a results table with pass rates>

## 10. Open questions
> Anything you're unsure about. Better to list it than let the AI guess.
