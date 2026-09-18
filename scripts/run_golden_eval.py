#!/usr/bin/env python3
"""Run the live glossary decision module against eval/golden_set.json.

Examples:
    python scripts/run_golden_eval.py --limit 5
    python scripts/run_golden_eval.py --context-file lesson.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from codebase.ai_decision_module import decide


def load_cases(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as data_file:
        payload = json.load(data_file)
    return payload["cases"]


def evaluate_case(case: dict[str, Any], context: str | None) -> dict[str, Any]:
    expected = case["expected"]
    case_context = context if context is not None else case["input"].get("lecture_context") or ""
    actual = decide(case_context, case["input"]["student_question"])
    actual_terms = set(actual["canonical_terms"])
    expected_terms = set(expected.get("canonical_terms", []))
    required_sources = set(expected.get("required_source_ids", []))
    return {
        "case_id": case["case_id"],
        "expected_behavior": expected["expected_behavior"],
        "actual_behavior": actual["behavior"],
        "behavior_ok": actual["behavior"] == expected["expected_behavior"],
        "terms_ok": expected_terms.issubset(actual_terms),
        "sources_ok": required_sources.issubset(set(actual["source_ids"])),
        "result": actual,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--golden", type=Path, default=REPO_ROOT / "eval" / "golden_set.json")
    parser.add_argument("--context-file", type=Path, help="Use one real lesson context for every case")
    parser.add_argument("--limit", type=int, help="Run only the first N cases")
    parser.add_argument("--output", type=Path, help="Write detailed JSON results to this path")
    args = parser.parse_args()

    context = args.context_file.read_text(encoding="utf-8") if args.context_file else None
    cases = load_cases(args.golden)
    if args.limit is not None:
        cases = cases[: args.limit]

    results = [evaluate_case(case, context) for case in cases]
    behavior_pass = sum(result["behavior_ok"] for result in results)
    term_pass = sum(result["terms_ok"] for result in results)
    source_pass = sum(result["sources_ok"] for result in results)
    print(f"Cases: {len(results)}")
    print(f"Behavior: {behavior_pass}/{len(results)}")
    print(f"Canonical terms: {term_pass}/{len(results)}")
    print(f"Required sources: {source_pass}/{len(results)}")
    for result in results:
        if not (result["behavior_ok"] and result["terms_ok"] and result["sources_ok"]):
            print(
                f"{result['case_id']}: expected={result['expected_behavior']} "
                f"actual={result['actual_behavior']} terms_ok={result['terms_ok']} "
                f"sources_ok={result['sources_ok']}"
            )

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if behavior_pass == len(results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
