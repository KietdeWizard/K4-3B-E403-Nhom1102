# Run 2 Glossary Results

Run 2 is a corrective smoke test after Run 1 showed that many golden-set cases used topic-title context instead of real slide/transcript text. It does not replace the 22-case CP3 golden set. It checks whether the visible glossary flow works when the model receives real lesson context.

## Summary

- Total: 2 lesson-context smoke cases
- Pass: 2
- Fail: 0
- Pass rate: 100%
- Scope: contextual glossary output with real lesson context from two lessons
- Model: `gpt-4o-mini`

## Results

| Case | Lesson | Prompt | Expected | Result | Notes |
|---|---|---|---|---|---|
| R2-D1-G001 | Day 1: AI & LLM Foundation | `Tao glossary 5 thuat ngu quan trong nhat cho bai nay.` | `resolve`, at least 3 glossary cards, examples, source refs, connections | Pass | Live log produced 5 glossary cards: Large Language Model, Generative AI, Transformer, Attention Mechanism, Token. Source refs included PDF pages from the lesson context. |
| R2-D2-G001 | Day 2: Automation vs Augmentation | `Automation, augmentation va cost-of-error lien quan voi nhau the nao?` | `resolve`, relationship explanation with traceable sources | Pass | Direct live model call returned `behavior=resolve`, 3 glossary cards, `source_refs=["PDF page 17","PDF page 22"]`, and concept connections. |

## Interpretation

Run 2 supports the failure analysis from Run 1: the app performs better when the evaluation context resembles the product flow, where users upload or paste real lesson material. The result is not comparable to the full 22-case golden set because it is a 2-case smoke test, but it is useful for CP5 demo readiness.

## Remaining Risk

- Run 2 is small and should not be used to claim production accuracy.
- The full 22-case golden set still needs a future rerun with real slide/transcript context for each `resolve` case.
- Source refs are page-level, not exact text highlight links yet.
