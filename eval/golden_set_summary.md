# Tóm Tắt Bộ Dữ Liệu Kiểm Thử Chuẩn (Golden Set Summary) — VLearn AI Glossary

**Tổng số test cases**: 22 cases

---

## 1. Phân Theo Nguồn Nguồn Gốc Dữ Liệu (Origin)

| Nguồn gốc | Số lượng | Tỉ lệ % |
|---|---:|---:|
| `real_chatlog` (Trích xuất từ chatlog thật) | 16 | 72.7% |
| `synthetic_hard_test` (Case tạo thêm để thử thách hệ thống) | 6 | 27.3% |

*Ghi chú: Theo đúng nguyên tắc chỉ đạo, hơn 70% các case được lấy trực tiếp từ câu hỏi thực tế của học viên trong `vlearn-pack/chatlog/tutor_turns.csv`.*

---

## 2. Phân Theo Hành Vi Kỳ Vọng (Expected Behavior)

| Hành vi kỳ vọng | Ý nghĩa | Số lượng | Tỉ lệ % |
|---|---|---:|---:|
| `resolve` | Đủ bằng chứng để map chính xác khái niệm | 15 | 68.2% |
| `clarify` | Câu hỏi mơ hồ hoặc thiếu ngữ cảnh; cần AI hỏi lại học viên | 4 | 18.2% |
| `unsupported` | Khái niệm ngoài phạm vi bài học hoặc chứa prompt injection | 2 | 9.1% |
| `manual_review` | Xung đột nguồn thông tin hoặc cần con người duyệt | 1 | 4.5% |

---

## 3. Phân Theo Nhóm Ý Định & Phân Loại (Category)

| Nhóm ý định | Mô tả | Câu hỏi thật | Case tự tạo | Tổng |
|---|---|---:|---:|---:|
| `define_concept` | Hỏi định nghĩa khái niệm trực tiếp | 4 | 0 | 4 |
| `compare_concepts` | So sánh sự khác nhau giữa 2 khái niệm | 3 | 0 | 3 |
| `explain_mechanism` | Hỏi cơ chế / nguyên lý vận hành bên trong | 3 | 0 | 3 |
| `concept_relationship` | Hỏi mối quan hệ / thứ cấp giữa các thuật ngữ | 1 | 0 | 1 |
| `concept_application` | Hỏi ứng dụng thực tế và khi nào nên dùng | 1 | 0 | 1 |
| `alias` | Tên gọi thay thế / từ tiếng Việt tương đương | 2 | 0 | 2 |
| `acronym` | Viết tắt thuật ngữ chuẩn | 1 | 0 | 1 |
| `lowercase` | Kiểm thử chuẩn hóa chữ thường | 1 | 0 | 1 |
| `ambiguous` | Nhập từ khóa mơ hồ (chỉ nhập 1 từ) | 1 | 0 | 1 |
| `deictic` | Câu hỏi phụ thuộc đoạn văn bôi đen | 1 | 0 | 1 |
| `prompt_injection` | Mẫu câu đè hệ thống từ chatlog thật | 1 | 0 | 1 |
| `typo` | Kiểm thử gõ sai chính tả | 0 | 1 | 1 |
| `unsupported_concept` | Khái niệm không có trong bài giảng (VD: Mamba SSM) | 0 | 1 | 1 |
| `wrong_assumption` | Câu hỏi chứa giả định kỹ thuật sai | 0 | 1 | 1 |
| `multi_concept` | Hỏi liên kết >3 khái niệm cùng lúc | 0 | 1 | 1 |
| `missing_context` | Câu hỏi thiếu hẳn ngữ cảnh bài học | 0 | 1 | 1 |
| `conflicting_source` | Mâu thuẫn giữa slide và transcript | 0 | 1 | 1 |

---

## 4. Tính Trung Thực Và Nguồn Bằng Chứng (Citation Integrity)
- **100%** các test case hỗ trợ (`supported=true`) đều dẫn mã trích dẫn đoạn bài giảng thực tế dạng `[Txx-NNN]` (ví dụ `[T04-003]`, `[T04-015]`, `[T04-040]`).
- **Không** sử dụng câu trả lời cũ của Tutor (`tutor_reply`) làm căn cứ đúng.
- **Không** tạo mã trích dẫn giả đối với các trường hợp không được hỗ trợ (`unsupported`).
