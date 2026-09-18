# Thống Kê Nhu Cầu Tra Cứu Thuật Ngữ (Terminology & Glossary)

Báo cáo thống kê thực nghiệm khai phá trực tiếp từ chatlog thật (`vlearn-pack/chatlog/tutor_turns.csv`).
Số liệu được phân tách theo 3 phạm vi nhằm loại bỏ thiên lệch do hoạt động bất thường ngày `2026-07-30`.

## 1. Tổng Quan Chỉ Số

| Chỉ số | Toàn bộ dữ liệu | Loại trừ 2026-07-30 | Chỉ Khóa K4 |
|---|---:|---:|---:|
| Tổng số lượt hỏi (`turns`) | 13,494 | 10,915 | 3,097 |
| Số học viên duy nhất (`unique students`) | 1,617 | 1,414 | 448 |
| Lượt hỏi mẫu (`is_preset=true`) | 3,067 (22.7%) | 2,648 (24.3%) | 542 (17.5%) |
| Lượt hỏi về thuật ngữ | 6,101 (45.2%) | 5,089 (46.6%) | 1,329 (42.9%) |
| Số học viên có hỏi về thuật ngữ | 1,249 (77.2%) | 1,050 (74.3%) | 333 (74.3%) |

## 2. Phân Tích Theo Ý Định Hỏi (Toàn Bộ Dữ Liệu)

| Nhóm ý định (Intent) | Số lượt | % Tổng lượt | Số học viên | % Tổng học viên |
|---|---:|---:|---:|---:|
| Định nghĩa thuật ngữ (`define_concept`) | 5,544 | 41.1% | 1,206 | 74.6% |
| So sánh khái niệm (`compare_concepts`) | 335 | 2.5% | 227 | 14.0% |
| Giải thích cơ chế (`explain_mechanism`) | 61 | 0.5% | 50 | 3.1% |
| Quan hệ giữa các khái niệm (`concept_relationship`) | 111 | 0.8% | 91 | 5.6% |
| Ứng dụng & Khi nào dùng (`concept_application`) | 37 | 0.3% | 32 | 2.0% |
| Từ khóa nhập mơ hồ (`ambiguous`) | 13 | 0.1% | 11 | 0.7% |
| Không thuộc glossary (`non_glossary`) | 7,393 | 54.8% | 368 | 22.8% |

## 3. Phân Tích Theo Ý Định Hỏi (Riêng Khóa K4)

| Nhóm ý định (Intent) | Số lượt | % Lượt K4 | Số học viên | % Học viên K4 |
|---|---:|---:|---:|---:|
| Định nghĩa thuật ngữ (`define_concept`) | 1,123 | 36.3% | 317 | 70.8% |
| So sánh khái niệm (`compare_concepts`) | 125 | 4.0% | 80 | 17.9% |
| Giải thích cơ chế (`explain_mechanism`) | 17 | 0.5% | 15 | 3.3% |
| Quan hệ giữa các khái niệm (`concept_relationship`) | 44 | 1.4% | 33 | 7.4% |
| Ứng dụng & Khi nào dùng (`concept_application`) | 18 | 0.6% | 15 | 3.3% |
| Từ khóa nhập mơ hồ (`ambiguous`) | 2 | 0.1% | 1 | 0.2% |
| Không thuộc glossary (`non_glossary`) | 1,768 | 57.1% | 115 | 25.7% |

## 4. Phân Tích Tần Suất Tra Cứu Lặp Lại Nối Tiếp

Nhằm kiểm tra giả thuyết bài toán: học viên có phải tra cứu nhiều thuật ngữ riêng lẻ trong cùng bài học hay không:

### Toàn bộ dữ liệu
- Học viên hỏi ≥1 câu hỏi thuật ngữ: **1,249** (77.2% tổng số học viên)
- Học viên hỏi ≥2 câu hỏi thuật ngữ: **838** (67.1% học viên có hỏi thuật ngữ)
- Học viên hỏi ≥3 câu hỏi thuật ngữ: **610** (48.8% học viên có hỏi thuật ngữ)
- Học viên hỏi ≥5 câu hỏi thuật ngữ: **346** (27.7% học viên có hỏi thuật ngữ)

### Loại trừ 2026-07-30
- Học viên hỏi ≥1 câu hỏi thuật ngữ: **1,050** (74.3% tổng số học viên)
- Học viên hỏi ≥2 câu hỏi thuật ngữ: **669** (63.7% học viên có hỏi thuật ngữ)
- Học viên hỏi ≥3 câu hỏi thuật ngữ: **482** (45.9% học viên có hỏi thuật ngữ)
- Học viên hỏi ≥5 câu hỏi thuật ngữ: **272** (25.9% học viên có hỏi thuật ngữ)

### Khóa K4
- Học viên hỏi ≥1 câu hỏi thuật ngữ: **333** (74.3% tổng số học viên)
- Học viên hỏi ≥2 câu hỏi thuật ngữ: **211** (63.4% học viên có hỏi thuật ngữ)
- Học viên hỏi ≥3 câu hỏi thuật ngữ: **148** (44.4% học viên có hỏi thuật ngữ)
- Học viên hỏi ≥5 câu hỏi thuật ngữ: **87** (26.1% học viên có hỏi thuật ngữ)

