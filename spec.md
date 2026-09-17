# Template AI Spec *(spec.md — commit trước hạn chốt spec: 21:00 18/9, tại CP4 · quality bar chốt từ thời điểm nộp)*

> Cấu trúc phủ đúng "SPEC 8 phần" của chương trình: Bằng chứng (§1-§2) · Lát cắt (§4) · Canvas (đính kèm CP1) · Augment/Automate (§4) · 4 đường đi của trải nghiệm (§6) · Kiểu lỗi (§5) · Kiểm thử (§7) · Phân công (§8). Hướng dẫn viết từng mục: `02-guide.md`.

```markdown
# AI SPEC — [Tên lát cắt] · Nhóm [XX] · Zone [X]
Hướng: [ ] A — VLearn  [ ] B — Trợ lý Học viên  [ ] C — Làn mở
Loại: [ ] Tối ưu tính năng có sẵn  [ ] Tính năng mới

## §1. User & Job

- Job executor + workflow:
  Học viên đang xem slide/video lecture trên VLearn, gặp nhiều thuật ngữ mới trong cùng một chương/topic. Khi không hiểu một thuật ngữ, học viên phải dừng lại để hỏi tutor/chatbot, sau đó quay lại bài học rồi tiếp tục hỏi thêm các thuật ngữ khác nếu gặp tiếp.

- Core JTBD:
  Khi đang học một bài có nhiều thuật ngữ mới, học viên muốn tra nhanh định nghĩa và mối liên hệ giữa các khái niệm trong đúng ngữ cảnh bài học, để tiếp tục theo dõi nội dung mà không bị ngắt mạch học liên tục.

- Problem statement:
  Các định nghĩa thuật ngữ hiện đang nằm rải rác trong từng lượt hỏi–đáp, khiến học viên mất thời gian hỏi lặp lại, khó nhớ thuật ngữ đã hỏi trước đó, và khó nhìn thấy quan hệ giữa các khái niệm trong cùng một topic/video.

- Evidence:
  - Data pack có `13.494` lượt hỏi–đáp của `1617` học viên, đủ signal để khảo sát hành vi hỏi bài.
  - Trường `misconceptions` rỗng `28%`, cho thấy dữ liệu hiểu sai/khó hiểu chưa luôn được cấu trúc sẵn.
  - Chỉ `22.7%` lượt tutor trả lời, làm tăng nhu cầu có lớp hỗ trợ tra cứu/tổng hợp nhanh từ nguồn bài học.
  - Phỏng vấn `09` học viên: `09/09` nói rằng việc hỏi đi hỏi lại các định nghĩa làm tốn thời gian và ngắt mạch học

## §2. Impact & quyết định chọn

- Bảng impact ≥3 ứng viên:

| Ứng viên | Ai bị ảnh hưởng | Tần suất | Tốn gì mỗi lần | Khả thi trong hackathon |
|---|---:|---:|---|---|
| Glossary theo bài học, có liên kết khái niệm | `09/09` học viên phỏng vấn xác nhận pain; data pack có `13.494` lượt hỏi–đáp | Xảy ra nhiều lần trong một bài có nhiều thuật ngữ mới | Mất thời gian hỏi lại, ngắt mạch học, khó nhớ thuật ngữ trước đó | Cao: có thể prototype bằng slide/topic mẫu + glossary card + concept map nhỏ |
| Tóm tắt toàn bộ bài học sau buổi | Nhiều học viên cần ôn lại sau lớp | Sau mỗi buổi học | Dễ quá rộng, khó chứng minh cá nhân hóa từ data hiện có | Trung bình: dễ làm demo nhưng dễ giống summary tool chung |
| Bản đồ lỗ hổng kiến thức cá nhân | Học viên có nhiều log hỏi bài | Sau nhiều lượt học/tutor | Rủi ro suy luận sai rằng học viên “hổng kiến thức” khi signal yếu | Thấp-Trung bình: cần nhiều dữ liệu cá nhân và kiểm chứng chất lượng |
| Dashboard chỗ khó của cả lớp cho giảng viên | Giảng viên/TA | Sau mỗi buổi học | Cần gom dữ liệu lớp, xử lý noise/preset questions, bảo vệ danh tính | Trung bình: hay nhưng lệch khỏi pain đang chọn của học viên xem slide |

- Ứng viên ĐÃ LOẠI + vì sao:
  - Tóm tắt toàn bộ bài học sau buổi: loại vì quá rộng, không đánh trực tiếp vào pain “đang học bị ngắt vì phải hỏi định nghĩa”.
  - Bản đồ lỗ hổng kiến thức cá nhân: loại vì cost-of-error cao; nếu hệ thống kết luận sai học viên yếu phần nào thì dễ gây mất niềm tin.
  - Dashboard chỗ khó của cả lớp cho giảng viên: loại vì user chính chuyển sang giảng viên, trong khi bằng chứng phỏng vấn hiện tại đang mạnh hơn ở phía học viên.

- Ứng viên CHỌN + vì sao:
  Chọn **Glossary theo bài học, có liên kết khái niệm** vì pain được xác nhận bởi `09/09` học viên phỏng vấn và phù hợp với data pack có `13.494` lượt hỏi–đáp. Tính năng này có lát cắt hẹp, dễ demo trong checkpoint 2: từ một slide/topic, hệ thống tạo danh sách thuật ngữ quan trọng, định nghĩa ngắn theo ngữ cảnh bài học, ví dụ, nguồn/trang liên quan, và mối liên hệ giữa các thuật ngữ. Rủi ro thấp hơn các phương án “đánh giá năng lực” vì AI chỉ hỗ trợ tra cứu/tổng hợp, không kết luận học viên yếu hay giỏi.

## §3. Giải pháp tương tự đã nghiên cứu
- [Sản phẩm 1]: flow / đáng học / đáng né / mình khác gì
- [Sản phẩm 2]: ...

## §4. Thiết kế
- Lát cắt MỘT CÂU (1 user · 1 việc · 1 quyết định AI · 1 kết quả):
- Non-goals (≥3 thứ KHÔNG build):
- Mức prototype nhắm tới: [ ] Sketch [ ] Mock [ ] Working — phần nào mock, phần nào thật:
- Automation: [ ] augment [ ] conditional [ ] automate — lý do theo cost-of-error:
- §4b. Nguyên tắc đã áp dụng (≥4 — HAX/PAIR, xem guide):
  | Nguyên tắc | Áp cụ thể vào đâu trong prototype |
  |---|---|

## §5. Kiểu lỗi — 4 lớp chỗ khó + kịch bản (≥8) [bảng theo guide §2.5]

## §6. Bốn đường đi của trải nghiệm
- Happy path: · Low-confidence (②): · Failure/không căn cứ (①): · Correction (user sửa):
- Khi bị đòi ngoài phạm vi (③): · Case đặc thù domain (④):

## §7. Kiểm thử
- Chiều chất lượng + định nghĩa kiểm chứng được:
- Golden set (≥20 case theo cơ cấu trong guide §2.6, file trong eval/):
- Quality bar (chốt từ hạn chốt spec của khoá, giữ nguyên sau đó): "Đạt khi ≥ ___% qua bộ, và ___"
- Kết quả các lượt chạy (bảng % — cập nhật đến trước CP6):

## §8. Phân công & kế hoạch
- Phân công có tên: spec / evidence / prompt / code / demo
- Willing users (≥2 tên) + kế hoạch vòng validation *(bonus, nếu làm)*:
- Multi-prototype (nếu làm): trục khác biệt của ≥2 phương án + lý do chọn:

## §9. Changelog
| Thời điểm | Đổi gì | Vì sao (trỏ về feedback/case nào) |
```
