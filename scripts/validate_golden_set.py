#!/usr/bin/env python3
"""
scripts/validate_golden_set.py

Validates eval/golden_set.json against project constraints:
  1. JSON parseable.
  2. Total test cases >= 20.
  3. Unique case_id strings.
      4. Required fields present in each case, including 4-class risk taxonomy.
  5. expected_behavior strictly in ['resolve', 'clarify', 'unsupported', 'manual_review'].
  6. Real chatlog cases specify a non-empty turn_id.
  7. Supported cases with 'resolve' behavior specify canonical_terms.
  8. Unsupported cases do not require fake citation source_ids.
  9. Source IDs conform to [Txx-NNN] pattern if provided.

Returns exit code 0 on success, exit code 1 on failure.
"""

import os
import sys
import json
import re

ALLOWED_BEHAVIORS = {'resolve', 'clarify', 'unsupported', 'manual_review'}
ALLOWED_TAXONOMY = {
    'source_of_truth',
    'ambiguous_missing_info',
    'out_of_scope_authority',
    'domain_specific',
}
SOURCE_ID_PATTERN = re.compile(r'^T\d{2}-\d{3}$')

def validate():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    golden_path = os.path.join(repo_root, 'eval', 'golden_set.json')

    if not os.path.exists(golden_path):
        print(f"[ERROR] File not found: {golden_path}")
        sys.exit(1)

    try:
        with open(golden_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"[ERROR] Failed to parse JSON: {e}")
        sys.exit(1)

    errors = []

    if not isinstance(data, dict):
        errors.append("Root JSON must be an object.")
        data = {}

    dataset_version = data.get("dataset_version")
    if not dataset_version:
        errors.append("Missing 'dataset_version' root field.")

    cases = data.get("cases", [])
    if not isinstance(cases, list):
        errors.append("'cases' field must be a list.")
        cases = []

    total_cases = len(cases)
    print(f"[*] Found {total_cases} test cases in {golden_path}")

    if total_cases < 20:
        errors.append(f"Golden set must contain at least 20 cases, found {total_cases}.")

    seen_case_ids = set()

    for idx, c in enumerate(cases, start=1):
        c_prefix = f"Case #{idx}"
        if not isinstance(c, dict):
            errors.append(f"{c_prefix} is not a valid JSON object.")
            continue

        case_id = c.get("case_id")
        if not case_id:
            errors.append(f"{c_prefix} missing 'case_id'.")
        else:
            c_prefix = f"Case '{case_id}'"
            if case_id in seen_case_ids:
                errors.append(f"Duplicate case_id found: '{case_id}'.")
            seen_case_ids.add(case_id)

        # Check required root fields in case
        for req_field in ["source", "input", "category", "taxonomy", "expected", "manual_review_required", "notes"]:
            if req_field not in c:
                errors.append(f"{c_prefix} missing required field '{req_field}'.")

        taxonomy = c.get("taxonomy")
        if taxonomy not in ALLOWED_TAXONOMY:
            errors.append(f"{c_prefix} has invalid taxonomy '{taxonomy}'. Allowed: {ALLOWED_TAXONOMY}")

        source = c.get("source", {})
        if isinstance(source, dict):
            src_type = source.get("type")
            turn_id = source.get("turn_id")
            if src_type == "real_chatlog" and not turn_id:
                errors.append(f"{c_prefix} has type 'real_chatlog' but missing 'turn_id'.")
        else:
            errors.append(f"{c_prefix} 'source' must be an object.")

        expected = c.get("expected", {})
        if isinstance(expected, dict):
            exp_behavior = expected.get("expected_behavior")
            if exp_behavior not in ALLOWED_BEHAVIORS:
                errors.append(f"{c_prefix} has invalid expected_behavior '{exp_behavior}'. Allowed: {ALLOWED_BEHAVIORS}")

            supported = expected.get("supported")
            canonical_terms = expected.get("canonical_terms", [])
            required_source_ids = expected.get("required_source_ids", [])

            if exp_behavior == "resolve" and supported and not canonical_terms:
                errors.append(f"{c_prefix} behavior is 'resolve' but 'canonical_terms' is empty.")

            if not supported and required_source_ids:
                errors.append(f"{c_prefix} is unsupported (supported=False) but contains required_source_ids: {required_source_ids}")

            for sid in required_source_ids:
                if not SOURCE_ID_PATTERN.match(sid):
                    errors.append(f"{c_prefix} has malformed source ID '{sid}'. Expected format 'Txx-NNN'.")
        else:
            errors.append(f"{c_prefix} 'expected' must be an object.")

    if errors:
        print("\n[FAIL] Golden Set Validation Errors Found:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("\n[SUCCESS] All Golden Set validation checks passed cleanly!")
        sys.exit(0)

if __name__ == '__main__':
    validate()
