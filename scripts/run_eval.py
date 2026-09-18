"""Evaluation runner for CP3 golden set.

Usage:
    python scripts/run_eval.py                          # dry run (no API call)
    python scripts/run_eval.py --live                   # call ai_decision_module for each case
    python scripts/run_eval.py --live --update-summary  # run + update run1_summary.md

The script:
1. Loads golden_set.json and glossary_fixture.json
2. For each case, either calls ai_decision_module.decide() (--live) or reads
   existing model_output from run1_results.json
3. Judges each case using the judging rules
4. Writes updated run1_results.json
5. Optionally regenerates run1_summary.md with real numbers
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = ROOT / "eval"
DATA_DIR = ROOT / "data"

GOLDEN_SET_PATH = EVAL_DIR / "golden_set.json"
GLOSSARY_PATH = DATA_DIR / "glossary_fixture.json"
RESULTS_PATH = EVAL_DIR / "run1_results.json"
SUMMARY_PATH = EVAL_DIR / "run1_summary.md"

# Mapping from ai_decision_module grounding status → expected_behavior
GROUNDING_TO_BEHAVIOR = {
    "grounded": "resolve",
    "low-confidence": "clarify",
    "no-grounding": "unsupported",
    "out-of-scope": "unsupported",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def build_glossary_index(glossary: list[dict]) -> dict[str, dict]:
    """Build lookup: canonical_term (lowercased) → entry, plus aliases."""
    index: dict[str, dict] = {}
    for entry in glossary:
        key = entry["canonical_term"].lower()
        index[key] = entry
        for alias in entry.get("aliases", []):
            index[alias.lower()] = entry
    return index


def judge_resolve(
    case: dict,
    model_output: dict,
    glossary_index: dict[str, dict],
) -> tuple[str, str | None, str | None]:
    """Judge a case whose expected behavior is 'resolve'.

    Returns: (judge_result, failure_reason, error_type)
    """
    # Check 1: model_behavior must be 'resolve'
    mapped_behavior = GROUNDING_TO_BEHAVIOR.get(
        model_output.get("status", ""), ""
    )
    if mapped_behavior != "resolve":
        return (
            "fail",
            f"Model returned '{model_output.get('status')}' → '{mapped_behavior}', expected 'resolve'",
            "sai canonical term" if mapped_behavior == "clarify" else "thiếu context nhưng vẫn đoán",
        )

    # Check 2: term matches expected canonical terms
    model_term = (model_output.get("term") or "").strip().lower()
    expected_terms = [t.lower() for t in case.get("expected_canonical_terms", [])]

    if expected_terms and model_term:
        # Check direct match or alias match
        term_matched = False
        for et in expected_terms:
            if model_term == et:
                term_matched = True
                break
            # Check if model_term is a known alias for the expected term
            if model_term in glossary_index:
                entry = glossary_index[model_term]
                if entry["canonical_term"].lower() == et:
                    term_matched = True
                    break
            # Check if expected term is an alias entry for model_term
            if et in glossary_index:
                entry = glossary_index[et]
                if entry["canonical_term"].lower() == model_term:
                    term_matched = True
                    break
        if not term_matched:
            return (
                "fail",
                f"Model term '{model_output.get('term')}' doesn't match expected {case.get('expected_canonical_terms')}",
                "sai canonical term",
            )

    # Check 3: evidence_found should be True
    if not model_output.get("evidence_found", False):
        return (
            "fail",
            "Model reports evidence_found=false for a case that should resolve",
            "bịa nguồn",
        )

    return ("pass", None, None)


def judge_clarify(
    case: dict,
    model_output: dict,
) -> tuple[str, str | None, str | None]:
    """Judge a case whose expected behavior is 'clarify'."""
    mapped_behavior = GROUNDING_TO_BEHAVIOR.get(
        model_output.get("status", ""), ""
    )

    # Acceptable: clarify (low-confidence) or unsupported (no-grounding)
    if mapped_behavior not in ("clarify", "unsupported"):
        if mapped_behavior == "resolve":
            return (
                "fail",
                "Model resolved confidently instead of asking for clarification",
                "thiếu context nhưng vẫn đoán",
            )
        return (
            "fail",
            f"Model returned '{model_output.get('status')}' → '{mapped_behavior}', expected 'clarify'",
            "thiếu context nhưng vẫn đoán",
        )

    # Check that confidence is not too high for ambiguous queries
    confidence = model_output.get("confidence_score", 1.0)
    if confidence > 0.8 and mapped_behavior == "resolve":
        return (
            "fail",
            f"Confidence {confidence} too high for ambiguous query",
            "thiếu context nhưng vẫn đoán",
        )

    return ("pass", None, None)


def judge_unsupported(
    case: dict,
    model_output: dict,
) -> tuple[str, str | None, str | None]:
    """Judge a case whose expected behavior is 'unsupported'."""
    mapped_behavior = GROUNDING_TO_BEHAVIOR.get(
        model_output.get("status", ""), ""
    )

    if mapped_behavior not in ("unsupported",):
        if mapped_behavior == "resolve":
            return (
                "fail",
                "Model resolved a query that should be unsupported/out-of-scope",
                "không từ chối out-of-scope",
            )
        if mapped_behavior == "clarify":
            # Clarify is acceptable as a partial pass for unsupported
            # (asking for more info rather than fabricating)
            return ("pass", None, None)
        return (
            "fail",
            f"Model returned '{model_output.get('status')}' → '{mapped_behavior}', expected 'unsupported'",
            "không từ chối out-of-scope",
        )

    # Check that model didn't fabricate sources
    if model_output.get("evidence_found", False):
        return (
            "fail",
            "Model claims evidence_found=true for unsupported concept",
            "bịa nguồn",
        )

    return ("pass", None, None)


def judge_manual_review(
    case: dict,
    model_output: dict,
) -> tuple[str, str | None, str | None]:
    """Judge a case whose expected behavior is 'manual_review'."""
    # Must flag needs_human_check
    if not model_output.get("needs_human_check", False):
        return (
            "fail",
            "Model did not flag needs_human_check for conflicting source case",
            "không manual_review khi nguồn mâu thuẫn",
        )

    # Should not be fully confident
    confidence = model_output.get("confidence_score", 1.0)
    if confidence > 0.9:
        return (
            "fail",
            f"Model is too confident ({confidence}) for conflicting source",
            "không manual_review khi nguồn mâu thuẫn",
        )

    return ("pass", None, None)


JUDGES = {
    "resolve": judge_resolve,
    "clarify": judge_clarify,
    "unsupported": judge_unsupported,
    "manual_review": judge_manual_review,
}


def judge_case(
    case: dict,
    model_output: dict,
    glossary_index: dict[str, dict],
) -> tuple[str, str | None, str | None]:
    """Dispatch to the appropriate judge function."""
    expected = case.get("expected_behavior", "")
    judge_fn = JUDGES.get(expected)
    if judge_fn is None:
        return ("fail", f"Unknown expected_behavior: {expected}", "output JSON sai format")

    if expected == "resolve":
        return judge_fn(case, model_output, glossary_index)
    return judge_fn(case, model_output)


def run_live_eval(golden_cases: list[dict]) -> list[dict]:
    """Call ai_decision_module.decide() for each golden case."""
    sys.path.insert(0, str(ROOT / "codebase"))
    from ai_decision_module import decide

    outputs = []
    for case in golden_cases:
        lecture_ctx = case.get("input", {}).get("lecture_context", "") or ""
        question = case.get("input", {}).get("student_question", "")

        print(f"  -> Running {case['case_id']}: {question[:50]}...")
        result = decide(
            lesson_context=lecture_ctx,
            user_query=question,
        )
        outputs.append(result)
        print(f"    status={result.get('status')}, confidence={result.get('confidence_score')}")

    return outputs


def generate_summary(results_data: dict) -> str:
    """Generate run1_summary.md content from results data."""
    results = results_data.get("results", [])
    total = len(results)

    passed = sum(1 for r in results if r.get("judge_result") == "pass")
    failed = sum(1 for r in results if r.get("judge_result") == "fail")
    pending = total - passed - failed
    pass_rate = f"{passed / total * 100:.1f}" if total > 0 else "0.0"

    # By taxonomy
    tax_counter: dict[str, dict] = {}
    for r in results:
        t = r.get("taxonomy", "unknown")
        if t not in tax_counter:
            tax_counter[t] = {"total": 0, "passed": 0, "failed": 0}
        tax_counter[t]["total"] += 1
        if r.get("judge_result") == "pass":
            tax_counter[t]["passed"] += 1
        elif r.get("judge_result") == "fail":
            tax_counter[t]["failed"] += 1

    # By expected behavior
    beh_counter: dict[str, dict] = {}
    for r in results:
        b = r.get("expected_behavior", "unknown")
        if b not in beh_counter:
            beh_counter[b] = {"total": 0, "passed": 0, "failed": 0}
        beh_counter[b]["total"] += 1
        if r.get("judge_result") == "pass":
            beh_counter[b]["passed"] += 1
        elif r.get("judge_result") == "fail":
            beh_counter[b]["failed"] += 1

    # By category
    cat_counter: dict[str, dict] = {}
    for r in results:
        c = r.get("category", "unknown")
        if c not in cat_counter:
            cat_counter[c] = {"total": 0, "passed": 0, "failed": 0}
        cat_counter[c]["total"] += 1
        if r.get("judge_result") == "pass":
            cat_counter[c]["passed"] += 1
        elif r.get("judge_result") == "fail":
            cat_counter[c]["failed"] += 1

    # Failures
    failures = [r for r in results if r.get("judge_result") == "fail"]

    lines = [
        "# Run 1 Evaluation Summary",
        "",
        "> **Lưu ý quan trọng:** Run 1 hiện đánh giá **tầng grounding decision** (output của `ai_decision_module.py`). Full glossary contract evaluation (canonical_terms, answer, source_ids, relations, confidence_score, needs_human_check) sẽ được chạy lại sau khi output contract cuối từ app hoàn tất.",
        "",
        "---",
        "",
        "## Overview",
        "",
        "| Metric | Value |",
        "|---|---:|",
        f"| Run ID | `{results_data.get('run_id', 'run1')}` |",
        f"| Model | `{results_data.get('model', 'gpt-4o-mini')}` |",
        f"| Timestamp | {results_data.get('timestamp', 'N/A')} |",
        f"| Total cases | {total} |",
        f"| Passed | {passed} |",
        f"| Failed | {failed} |",
        f"| Pending | {pending} |" if pending > 0 else "",
        f"| Pass rate | {pass_rate}% |",
        "",
        "---",
        "",
        "## Grounding → Behavior Mapping (Preliminary)",
        "",
        "| Grounding Status | → Mapped Behavior |",
        "|---|---|",
        "| `grounded` | `resolve` |",
        "| `low-confidence` | `clarify` |",
        "| `no-grounding` | `unsupported` |",
        "| `out-of-scope` | `unsupported` |",
        "",
        "---",
        "",
        "## By Taxonomy",
        "",
        "| Taxonomy | Total | Passed | Failed | Pass Rate |",
        "|---|---:|---:|---:|---:|",
    ]

    tax_order = ["source_of_truth", "ambiguous_missing_info", "out_of_scope_authority", "domain_specific"]
    for t in tax_order:
        if t in tax_counter:
            d = tax_counter[t]
            pr = f"{d['passed'] / d['total'] * 100:.1f}" if d["total"] > 0 else "0.0"
            lines.append(f"| `{t}` | {d['total']} | {d['passed']} | {d['failed']} | {pr}% |")

    lines += [
        "",
        "---",
        "",
        "## By Expected Behavior",
        "",
        "| Expected Behavior | Total | Passed | Failed | Pass Rate |",
        "|---|---:|---:|---:|---:|",
    ]

    beh_order = ["resolve", "clarify", "unsupported", "manual_review"]
    for b in beh_order:
        if b in beh_counter:
            d = beh_counter[b]
            pr = f"{d['passed'] / d['total'] * 100:.1f}" if d["total"] > 0 else "0.0"
            lines.append(f"| `{b}` | {d['total']} | {d['passed']} | {d['failed']} | {pr}% |")

    lines += [
        "",
        "---",
        "",
        "## By Category",
        "",
        "| Category | Total | Passed | Failed |",
        "|---|---:|---:|---:|",
    ]

    for c in sorted(cat_counter.keys()):
        d = cat_counter[c]
        lines.append(f"| `{c}` | {d['total']} | {d['passed']} | {d['failed']} |")

    lines += [
        "",
        "---",
        "",
        "## Failure Analysis",
        "",
        "| Case | Taxonomy | Category | Error Type | Reason | Fix Idea |",
        "|---|---|---|---|---|---|",
    ]

    if failures:
        for f in failures:
            fix_idea = ""
            et = f.get("error_type", "")
            if et == "bịa nguồn":
                fix_idea = "Thêm validation source_ids trước khi output"
            elif et == "thiếu context nhưng vẫn đoán":
                fix_idea = "Tăng threshold confidence cho ambiguous queries"
            elif et == "sai canonical term":
                fix_idea = "Cải thiện fuzzy matching / alias lookup"
            elif et == "không từ chối out-of-scope":
                fix_idea = "Thêm explicit out-of-scope check trong prompt"
            elif et == "sai relation/domain":
                fix_idea = "Cross-check relations với glossary_fixture"
            elif et == "không manual_review khi nguồn mâu thuẫn":
                fix_idea = "Thêm conflict detection logic"
            elif et == "output JSON sai format":
                fix_idea = "Thêm stricter JSON schema validation"

            lines.append(
                f"| {f['case_id']} | {f.get('taxonomy', '')} | {f.get('category', '')} "
                f"| {et} | {f.get('failure_reason', '')} | {fix_idea} |"
            )
    else:
        lines.append("| _(no failures)_ | | | | | |")

    lines += [
        "",
        "---",
        "",
        "## Judging Rules Applied",
        "",
        "### `resolve` — pass nếu:",
        "- ✅ Đúng canonical term (khớp hoặc alias hợp lệ trong `glossary_fixture.json`)",
        "- ✅ Answer dựa trên nội dung bài học (không dùng kiến thức ngoài)",
        "- ✅ `source_ids` đúng hoặc hợp lý (khớp `required_source_ids` hoặc subset hợp lệ)",
        "- ✅ Không bịa nguồn (no fabricated source)",
        "",
        "### `clarify` — pass nếu:",
        "- ✅ Không đoán mò (no hallucinated answer)",
        "- ✅ Hỏi lại thông tin còn thiếu",
        "- ✅ Nêu rõ cần context nào (selected_text, lecture_context, concept name)",
        "",
        "### `unsupported` — pass nếu:",
        "- ✅ Từ chối an toàn (safe refusal)",
        "- ✅ Không trả lời ngoài phạm vi",
        "- ✅ Không bịa source hoặc definition",
        "",
        "### `manual_review` — pass nếu:",
        "- ✅ Đánh dấu cần người kiểm tra (`needs_human_check = true`)",
        "- ✅ Không kết luận chắc chắn khi nguồn mâu thuẫn",
        "- ✅ Nêu rõ lý do cần review",
        "",
        "---",
        "",
        "## Error Labels Reference",
        "",
        "| Label | Mô tả |",
        "|---|---|",
        "| `bịa nguồn` | Model tạo ra source_id không tồn tại trong bài học |",
        "| `thiếu context nhưng vẫn đoán` | Query thiếu thông tin nhưng model vẫn trả lời chắc chắn |",
        "| `sai canonical term` | Model map sai thuật ngữ chuẩn so với glossary_fixture |",
        "| `không từ chối out-of-scope` | Model trả lời câu hỏi ngoài phạm vi thay vì từ chối |",
        "| `sai relation/domain` | Model đưa sai quan hệ giữa các khái niệm |",
        "| `không manual_review khi nguồn mâu thuẫn` | Model kết luận chắc chắn dù nguồn xung đột |",
        "| `output JSON sai format` | Output không đúng schema yêu cầu |",
        "",
        "---",
        "",
        "## Next Steps",
        "",
        "1. **Chờ output contract cuối từ Anh** → cập nhật `model_output` trong `run1_results.json`",
        "2. **Chạy lại** `python scripts/run_eval.py --live --update-summary`",
        "3. **Nếu pass rate < quality bar** → phân tích failure, đề xuất fix trong Failure Analysis table",
    ]

    return "\n".join(line for line in lines if line is not None) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run CP3 golden set evaluation")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Call ai_decision_module.decide() for each case (requires API key)",
    )
    parser.add_argument(
        "--update-summary",
        action="store_true",
        help="Regenerate run1_summary.md with computed numbers",
    )
    args = parser.parse_args()

    # Load data
    print("Loading golden set...")
    golden = load_json(GOLDEN_SET_PATH)
    golden_cases = golden["cases"]
    print(f"  {len(golden_cases)} cases loaded")

    print("Loading glossary fixture...")
    glossary = load_json(GLOSSARY_PATH)
    glossary_index = build_glossary_index(glossary)
    print(f"  {len(glossary)} terms indexed ({len(glossary_index)} total keys)")

    print("Loading existing results...")
    results_data = load_json(RESULTS_PATH)
    results = results_data["results"]

    # Build case lookup
    results_by_id = {r["case_id"]: r for r in results}

    # Run live evaluation if requested
    if args.live:
        print("\n=== LIVE EVALUATION ===")
        outputs = run_live_eval(golden_cases)
        for case, output in zip(golden_cases, outputs):
            cid = case["case_id"]
            if cid in results_by_id:
                results_by_id[cid]["model_output"] = output
                results_by_id[cid]["model_behavior"] = GROUNDING_TO_BEHAVIOR.get(
                    output.get("status", ""), "unknown"
                )

    # Judge all cases that have model_output
    print("\n=== JUDGING ===")
    judged = 0
    for r in results:
        model_output = r.get("model_output", {})
        if not model_output:
            print(f"  [SKIP] {r['case_id']}: no model_output yet, skipping")
            continue

        judge_result, failure_reason, error_type = judge_case(
            r, model_output, glossary_index
        )
        r["judge_result"] = judge_result
        r["failure_reason"] = failure_reason
        r["error_type"] = error_type
        judged += 1

        icon = "[PASS]" if judge_result == "pass" else "[FAIL]"
        print(f"  {icon} {r['case_id']}: {judge_result}", end="")
        if failure_reason:
            print(f" — {failure_reason}", end="")
        print()

    print(f"\n  Judged {judged}/{len(results)} cases")

    # Update timestamp
    results_data["timestamp"] = datetime.now(timezone.utc).isoformat()

    # Save results
    print(f"\nSaving results to {RESULTS_PATH}...")
    save_json(RESULTS_PATH, results_data)

    # Generate summary if requested
    if args.update_summary:
        print(f"Generating summary to {SUMMARY_PATH}...")
        summary_content = generate_summary(results_data)
        SUMMARY_PATH.write_text(summary_content, encoding="utf-8")

    # Print quick stats
    passed = sum(1 for r in results if r.get("judge_result") == "pass")
    failed = sum(1 for r in results if r.get("judge_result") == "fail")
    pending = len(results) - passed - failed
    print(f"\n{'='*40}")
    print(f"  PASS: {passed}  |  FAIL: {failed}  |  PENDING: {pending}")
    if passed + failed > 0:
        print(f"  Pass rate: {passed / (passed + failed) * 100:.1f}%")
    print(f"{'='*40}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
