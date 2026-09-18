# Tóm tắt bộ dữ liệu kiểm thử chuẩn (Golden Set Summary) - VLearn AI Glossary

**Tổng số test cases:** 22 cases

---

## 1. Phân theo nguồn gốc dữ liệu

| Nguồn gốc | Số lượng | Tỉ lệ |
|---|---:|---:|
| `real_chatlog` - trích xuất/phát triển từ chatlog thật | 16 | 72.7% |
| `synthetic_hard_test` - case tạo thêm để thử thách hệ thống | 6 | 27.3% |

Ghi chú: bộ này vượt yêu cầu CP3 vì có 16/22 case lấy hoặc phát triển từ chatlog thật trong `data/`, cao hơn mức tối thiểu 10 case.

---

## 2. Phân theo 4 lớp chỗ khó

| Taxonomy | Ý nghĩa | Số lượng |
|---|---|---:|
| `source_of_truth` | Phải dựa trên nguồn bài học, citation/trace đúng, không bịa nguồn | 5 |
| `ambiguous_missing_info` | Câu hỏi mơ hồ, thiếu context, hoặc phụ thuộc đoạn bôi đen | 3 |
| `out_of_scope_authority` | Ngoài phạm vi/thẩm quyền hoặc prompt injection | 2 |
| `domain_specific` | Thuật ngữ/domain AI có alias, typo, quan hệ khái niệm, hoặc nhiều nghĩa | 12 |

Tất cả 4 lớp đều có tối thiểu 2 case.

---

## 3. Phân theo hành vi kỳ vọng

| Expected behavior | Ý nghĩa | Số lượng | Tỉ lệ |
|---|---|---:|---:|
| `resolve` | Đủ bằng chứng để map/giải thích khái niệm | 16 | 72.7% |
| `clarify` | Câu hỏi mơ hồ hoặc thiếu ngữ cảnh; cần hỏi lại | 3 | 13.6% |
| `unsupported` | Khái niệm ngoài phạm vi bài học hoặc prompt injection | 2 | 9.1% |
| `manual_review` | Xung đột nguồn hoặc cần con người duyệt | 1 | 4.5% |

---

## 4. Phân theo nhóm ý định và phân loại

| Category | Câu hỏi thật | Case tự tạo | Tổng |
|---|---:|---:|---:|
| `define_concept` | 2 | 0 | 2 |
| `compare_concepts` | 3 | 0 | 3 |
| `explain_mechanism` | 2 | 0 | 2 |
| `concept_relationship` | 1 | 0 | 1 |
| `concept_application` | 1 | 0 | 1 |
| `alias` | 2 | 0 | 2 |
| `acronym` | 1 | 0 | 1 |
| `lowercase` | 1 | 0 | 1 |
| `ambiguous` | 1 | 0 | 1 |
| `deictic` | 1 | 0 | 1 |
| `prompt_injection` | 1 | 0 | 1 |
| `typo` | 0 | 1 | 1 |
| `unsupported_concept` | 0 | 1 | 1 |
| `wrong_assumption` | 0 | 1 | 1 |
| `multi_concept` | 0 | 1 | 1 |
| `missing_context` | 0 | 1 | 1 |
| `conflicting_source` | 0 | 1 | 1 |

---

## 5. Tính trung thực và nguồn bằng chứng

- 100% case `supported=true` có `required_source_ids` dạng `Txx-NNN`.
- Không dùng câu trả lời cũ của Tutor (`tutor_reply`) làm ground truth.
- Case `unsupported` không gắn citation giả.
- Các case mơ hồ hoặc thiếu context được kỳ vọng `clarify`, không đoán.
- Case xung đột nguồn được đánh dấu `manual_review_required=true`.
