"""Run the golden set through the real chain and score it.

Usage:  uv run python -m evals.run_eval
Costs:  one model call per golden ticket (12 calls).
"""
import json
import statistics
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from app.triage import build_chain

GOLDEN = Path(__file__).parent / "golden.jsonl"
RESULTS_DIR = Path(__file__).parent / "results"

# Fill these in from the Anthropic pricing page for the model you use (USD per million tokens).
PRICE_IN_PER_MTOK = None
PRICE_OUT_PER_MTOK = None


def load_golden(path=GOLDEN):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def run(chain, cases):
    """Call the chain on every case and record what happened. No scoring here."""
    rows = []
    for case in cases:
        start = time.perf_counter()
        out = chain.invoke({"message": case["message"]})
        seconds = time.perf_counter() - start
        parsed, raw = out["parsed"], out["raw"]
        usage = getattr(raw, "usage_metadata", None) or {}
        rows.append({
            "id": case["id"],
            "expected_category": case["category"],
            "expected_urgency": case["urgency"],
            "category": parsed.category if parsed else None,
            "urgency": parsed.urgency if parsed else None,
            "parse_error": str(out["parsing_error"]) if out["parsing_error"] else None,
            "seconds": round(seconds, 2),
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
        })
    return rows


def score(rows):
    n = len(rows)
    tokens_in = sum(r["input_tokens"] for r in rows)
    tokens_out = sum(r["output_tokens"] for r in rows)
    cost = None
    if PRICE_IN_PER_MTOK is not None and PRICE_OUT_PER_MTOK is not None:
        cost = round((tokens_in * PRICE_IN_PER_MTOK + tokens_out * PRICE_OUT_PER_MTOK) / 1e6, 5)
    return {
        "cases": n,
        "schema_valid_rate": sum(r["parse_error"] is None for r in rows) / n,
        "category_accuracy": sum(r["category"] == r["expected_category"] for r in rows) / n,
        "urgency_accuracy": sum(r["urgency"] == r["expected_urgency"] for r in rows) / n,
        "latency_median_s": statistics.median(r["seconds"] for r in rows),
        "latency_max_s": max(r["seconds"] for r in rows),
        "input_tokens": tokens_in,
        "output_tokens": tokens_out,
        "cost_usd": cost,
    }


def main():
    load_dotenv()
    rows = run(build_chain(include_raw=True), load_golden())
    summary = score(rows)

    print(json.dumps(summary, indent=2))
    misses = [r for r in rows if r["category"] != r["expected_category"] or r["urgency"] != r["expected_urgency"]]
    print(f"\n{len(misses)} case(s) with a wrong label:")
    for r in misses:
        print(f"  {r['id']}: got {r['category']}/{r['urgency']}, "
              f"expected {r['expected_category']}/{r['expected_urgency']}")

    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / f"{datetime.now():%Y%m%d-%H%M%S}.json"
    out.write_text(json.dumps({"summary": summary, "rows": rows}, indent=2))
    print(f"\nSaved {out}")


if __name__ == "__main__":
    main()
