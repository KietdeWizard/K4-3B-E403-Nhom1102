# Run 2 Glossary Eval Plan

Run 2 measures the visible product slice after CP3: contextual glossary cards.

## Dataset

- File: `eval/glossary_demo_cases.json`
- Current size: 4 smoke-test cases for demo readiness.
- Existing CP3 golden set remains in `eval/golden_set.json` with 22 behavior/grounding cases.

## Pass Criteria

A glossary case passes when:

- `behavior` matches the expected behavior.
- For `resolve`, the output includes at least the required number of glossary terms.
- Each glossary card has `term`, `definition`, `lesson_example`, and at least one traceable `source_ref`.
- `source_ref` must appear in the supplied lesson context, for example `PDF page 17`.
- The answer does not invent outside concepts.
- The output includes at least one useful `concept_connections` item when the case asks for relationships.
- For `unsupported`, the system refuses safely and does not fabricate a definition or source.
- For `clarify`, the system asks what context or term is missing instead of guessing.

## Manual Run

Use the app with the sample context or an uploaded slide:

1. Run `python codebase\app.py`.
2. Open `http://localhost:5000`.
3. Click `Nạp lesson mẫu`.
4. Run the three suggestion prompts:
   - Generate glossary
   - Concept connection
   - Out of scope
5. Record pass/fail and failure reason in `eval/run2_glossary_results.md`.

## Relationship To Run 1

Run 1 measured the central decision/grounding layer on 22 cases and produced `6/22` pass. Run 2 is not a replacement for Run 1; it measures the visible glossary layer: examples, page/source refs, and concept connections.
