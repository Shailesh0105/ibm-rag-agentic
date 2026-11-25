# Review notes — Course 1, Module 2

## Issues I caught (mistakes in AI-written work)
| # | Issue | Found by | Lesson |
|---|---|---|---|
| 1 | Claude Code said the repo had no commits; `git log` showed commit f11b5d2. | Tutor (checked git) | Verify confident claims about the project's state. |
| 2 | The plan's question numbers (Q5, Q6, Q7) didn't match its own list. | Tutor | Answer by topic, not by number; small inconsistencies cause confusion. |
| 3 | "Tested" meant run outside Jupyter with no API calls; the notebook itself hadn't been run. | Tutor | Read "What I tested / didn't test" carefully; run it yourself. |
| 4 | The surname check matched part of a word: "Bongo Smith" passed for "Bong". | Tutor (tried extra inputs) | Probe edge cases beyond the spec's test list. |
| 5 | The whole-word fix created a false fail: "The Wachowskis" failed for "Wachowski". | Claude Code (flagged its own side effect) | Every matching rule trades false passes against false fails. |
| 6 | The spec asked Claude Haiku 5.5 for temperature 0/1; the model rejects non-default temperature (400 error). | Claude Code's planned test call | The spec (written by tutor) used an outdated assumption; one cheap test call before the full run caught it. |
| 7 | `JsonOutputParser` repairs broken JSON (`'{"a": 1'` → `{'a': 1}`), so "parse rate" looks better than it is. | Claude Code | A forgiving parser hides failures; report strict and lenient parse rates. |
| 8 | The retry path for API errors had never run, so nobody knew it worked. | Claude Code | Untested error handling is unverified; force a cheap failure to test it. |
| 9 | `.claude/settings.local.json` allowed `uv add *` without asking. | Tutor | Every new dependency should be reviewed; don't click "always allow". |
| 10 | macOS `.DS_Store` files were committed to git. | Tutor | Check `git status` before committing; add `.DS_Store` to `.gitignore`. |
| 11 | Assumed Claude Haiku 4.5 would still accept temperature (spec written by tutor). It returned the same 400 error. | Claude Code's test call | Two models, identical error: the cause may not be the model. Time-boxed and recorded as unknown. |
| 12 | Notebook hidden state: after Claude Code edited the file, my kernel and editor still ran the old code (with temperature). | **Me** | Always Restart Kernel → Run All before trusting results. |

## Good patterns in the AI's code (to reuse)
- `validate_movie` checks types by hand because pydantic would silently turn "1999" into 1999 and hide the errors being counted.
- Its own visible retry loop (exactly one retry) instead of the library's invisible one.
- `_is_real_int` rejects `True`/`False`, because in Python a bool counts as an int.
- The setup cell checks the golden file itself (21 rows, ids in order, 18/2/1 categories), so a typo fails early instead of skewing scores.
- A control test (a valid input that must pass), so a validator that rejects everything can't pass the suite.
- `score_movie` raises an error on unscored rows instead of quietly returning False.
- Missing keys are reported by name only, never by value.
- It lists what it did and didn't test, and flags APIs it isn't sure are current.

## Changes I asked for
- Spec: test 21 (*The Godfather Part II*, 1974); temperatures 0 and 1; "fewer than 3 movies = inconclusive" rule.
- Plan decisions: ambiguous titles record the chosen film; fake movie passes if director and year are null (genre = "partial invention"); show both denominators; golden JSON format; offline unit tests; 5th key = invalid; REVIEW_NOTES.md headings.
- Scoring: whole-word surname match, plus "Bongo" test and ValueError tests for fake/ambiguous rows.
- Scoring: optional plural "s" plus "Wachowskis" test; SPEC Section 7 updated to match.
- After the temperature error: Ex 2 at default temperature; Ex 1 Claude side on claude-haiku-4-5 (after one test call); strict + lenient parse rates; one forced-timeout retry test.
- After Haiku 4.5 also rejected temperature: Ex 1 reframed to run-to-run consistency at the default (Claude Haiku 5.5 vs GPT), with a GPT-only temperature section if GPT accepts it. SPEC records the cause as undetermined.

## Things I learned
- Parseable ≠ schema-valid ≠ correct (an all-null answer is schema-valid but wrong).
- If the spec and the code disagree, the spec stops being the source of truth; update it with every decision.
- Adding one test case changed six numbers in the spec; check every number an edit affects.
- With ~20 test items, one item ≈ 5 percentage points; small differences can be chance.
- Newer models (Claude 5.x, possibly newer GPT) remove temperature; the course teaches it as a core setting.
- Notebooks keep hidden state: the file and the kernel's memory can disagree.
- Time-box investigations: record what's unknown and move on when the concept is already covered.

## Open questions
- Why keep a test that passes on a wrong answer (Frank Miller)? *(to answer in my own words)*
- Is the temperature rejection caused by the models, the API or the SDK?
