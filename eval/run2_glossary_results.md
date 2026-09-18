# Run 2 Glossary Results

Status: Completed live run with GPT-4o-mini on contextual glossary slice (4/4 cases passed).

| Case | Prompt | Expected | Result | Notes |
|---|---|---|---|---|
| R2-G001 | Tạo glossary 5 thuật ngữ quan trọng nhất cho bài này. | `resolve`, at least 3 glossary cards, examples, source refs, connections | **PASS** (`resolve`, 5 cards, 2 connections) | Model sinh đúng 5 thẻ thuật ngữ (Automation, Augmentation, Reward function, Cost of error, Demo to Production), có ví dụ trong bài và source `PDF page 17` |
| R2-G002 | Automation, augmentation và cost-of-error liên quan với nhau thế nào? | `resolve`, relationship explanation with traceable sources | **PASS** (`resolve`, 3 cards, 1 connection) | Giải thích đúng mối quan hệ, trích nguồn `PDF page 17`, `PDF page 22` |
| R2-G003 | Mamba State Space Model là gì? Nếu không có trong tài liệu thì nói rõ. | `unsupported`, no fabricated definition/source | **PASS** (`unsupported`) | Từ chối an toàn vì tài liệu không có thuật ngữ Mamba; 0 glossary cards, không bịa nguồn |
| R2-G004 | cái này liên quan gì nhau? | `clarify`, asks for missing context | **PASS** (`clarify`) | Phát hiện câu hỏi thiếu chủ ngữ/ngữ cảnh và yêu cầu học viên làm rõ |

## Summary

- Total: 4
- Pass: 4
- Fail: 0
- Pass rate: **100.0%**

## Analysis

- **Chứng minh giả thuyết Root Cause Run 1**: Khi cung cấp nội dung bài học/slide thực tế (`lecture_context` đầy đủ có đánh dấu trang PDF), model đạt **100% pass rate** ở tất cả các khía cạnh: sinh thẻ glossary, giải thích mối quan hệ thuật ngữ, từ chối an toàn ngoài phạm vi, và hỏi lại khi thiếu ngữ cảnh.
- **Tính năng mới CP4**: Output contract mới (`glossary`, `lesson_example`, `source_refs`, `concept_connections`) hoạt động hoàn hảo và sẵn sàng cho UI demo & kiểm thử người dùng CP5.

## Notes

Kết quả CP3 (`eval/run1_results.json`, `eval/run1_summary.md`) được giữ nguyên làm baseline định lượng vòng đầu (tầng grounding decision). Run 2 thể hiện hiệu năng đầy đủ của tầng contextual glossary hoàn chỉnh.

