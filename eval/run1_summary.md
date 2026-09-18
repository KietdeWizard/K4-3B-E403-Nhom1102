# Run 1 Evaluation Summary

> **Lưu ý quan trọng:** Run 1 hiện đánh giá **tầng grounding decision** (output của `ai_decision_module.py`). Full glossary contract evaluation (canonical_terms, answer, source_ids, relations, confidence_score, needs_human_check) sẽ được chạy lại sau khi output contract cuối từ app hoàn tất.

---

## Overview

| Metric | Value |
|---|---:|
| Run ID | `run1` |
| Model | `gpt-4o-mini` |
| Timestamp | 2026-09-18T09:51:39.130388+00:00 |
| Total cases | 22 |
| Passed | 6 |
| Failed | 16 |

| Pass rate | 27.3% |

---

## Grounding → Behavior Mapping (Preliminary)

| Grounding Status | → Mapped Behavior |
|---|---|
| `grounded` | `resolve` |
| `low-confidence` | `clarify` |
| `no-grounding` | `unsupported` |
| `out-of-scope` | `unsupported` |

---

## By Taxonomy

| Taxonomy | Total | Passed | Failed | Pass Rate |
|---|---:|---:|---:|---:|
| `source_of_truth` | 5 | 1 | 4 | 20.0% |
| `ambiguous_missing_info` | 3 | 3 | 0 | 100.0% |
| `out_of_scope_authority` | 2 | 2 | 0 | 100.0% |
| `domain_specific` | 12 | 0 | 12 | 0.0% |

---

## By Expected Behavior

| Expected Behavior | Total | Passed | Failed | Pass Rate |
|---|---:|---:|---:|---:|
| `resolve` | 16 | 1 | 15 | 6.2% |
| `clarify` | 3 | 3 | 0 | 100.0% |
| `unsupported` | 2 | 2 | 0 | 100.0% |
| `manual_review` | 1 | 0 | 1 | 0.0% |

---

## By Category

| Category | Total | Passed | Failed |
|---|---:|---:|---:|
| `acronym` | 1 | 0 | 1 |
| `alias` | 2 | 0 | 2 |
| `ambiguous` | 1 | 1 | 0 |
| `compare_concepts` | 3 | 0 | 3 |
| `concept_application` | 1 | 0 | 1 |
| `concept_relationship` | 1 | 0 | 1 |
| `conflicting_source` | 1 | 0 | 1 |
| `define_concept` | 2 | 1 | 1 |
| `deictic` | 1 | 1 | 0 |
| `explain_mechanism` | 2 | 0 | 2 |
| `lowercase` | 1 | 0 | 1 |
| `missing_context` | 1 | 1 | 0 |
| `multi_concept` | 1 | 0 | 1 |
| `prompt_injection` | 1 | 1 | 0 |
| `typo` | 1 | 0 | 1 |
| `unsupported_concept` | 1 | 1 | 0 |
| `wrong_assumption` | 1 | 0 | 1 |

---

## Failure Analysis

| Case | Taxonomy | Category | Error Type | Reason | Fix Idea |
|---|---|---|---|---|---|
| G002 | domain_specific | compare_concepts | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G003 | domain_specific | compare_concepts | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G004 | domain_specific | explain_mechanism | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G005 | domain_specific | concept_relationship | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G008 | domain_specific | acronym | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G010 | domain_specific | alias | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G011 | domain_specific | alias | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G012 | source_of_truth | define_concept | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G013 | domain_specific | lowercase | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G014 | domain_specific | concept_application | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G015 | source_of_truth | explain_mechanism | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G016 | domain_specific | compare_concepts | sai canonical term | Model term 'Large Language Model' doesn't match expected ['Generative AI', 'Artificial Intelligence'] | Cải thiện fuzzy matching / alias lookup |
| G017 | domain_specific | typo | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G019 | source_of_truth | wrong_assumption | thiếu context nhưng vẫn đoán | Model returned 'unsupported', expected 'resolve' | Tăng threshold confidence cho ambiguous queries |
| G020 | domain_specific | multi_concept | sai canonical term | Model returned 'clarify', expected 'resolve' | Cải thiện fuzzy matching / alias lookup |
| G022 | source_of_truth | conflicting_source | không manual_review khi nguồn mâu thuẫn | Model did not flag needs_human_check for conflicting source case | Thêm conflict detection logic |

---

## Judging Rules Applied

### `resolve` — pass nếu:
- ✅ Đúng canonical term (khớp hoặc alias hợp lệ trong `glossary_fixture.json`)
- ✅ Answer dựa trên nội dung bài học (không dùng kiến thức ngoài)
- ✅ `source_ids` đúng hoặc hợp lý (khớp `required_source_ids` hoặc subset hợp lệ)
- ✅ Không bịa nguồn (no fabricated source)

### `clarify` — pass nếu:
- ✅ Không đoán mò (no hallucinated answer)
- ✅ Hỏi lại thông tin còn thiếu
- ✅ Nêu rõ cần context nào (selected_text, lecture_context, concept name)

### `unsupported` — pass nếu:
- ✅ Từ chối an toàn (safe refusal)
- ✅ Không trả lời ngoài phạm vi
- ✅ Không bịa source hoặc definition

### `manual_review` — pass nếu:
- ✅ Đánh dấu cần người kiểm tra (`needs_human_check = true`)
- ✅ Không kết luận chắc chắn khi nguồn mâu thuẫn
- ✅ Nêu rõ lý do cần review

---

## Error Labels Reference

| Label | Mô tả |
|---|---|
| `bịa nguồn` | Model tạo ra source_id không tồn tại trong bài học |
| `thiếu context nhưng vẫn đoán` | Query thiếu thông tin nhưng model vẫn trả lời chắc chắn |
| `sai canonical term` | Model map sai thuật ngữ chuẩn so với glossary_fixture |
| `không từ chối out-of-scope` | Model trả lời câu hỏi ngoài phạm vi thay vì từ chối |
| `sai relation/domain` | Model đưa sai quan hệ giữa các khái niệm |
| `không manual_review khi nguồn mâu thuẫn` | Model kết luận chắc chắn dù nguồn xung đột |
| `output JSON sai format` | Output không đúng schema yêu cầu |

---

## Next Steps

1. **Chờ output contract cuối từ Anh** → cập nhật `model_output` trong `run1_results.json`
2. **Chạy lại** `python scripts/run_eval.py --live --update-summary`
3. **Nếu pass rate < quality bar** → phân tích failure, đề xuất fix trong Failure Analysis table
