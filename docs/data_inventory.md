# Danh Mục & Kiểm Kê Dữ Liệu (Data Inventory)

## 1. Dữ Liệu Chatlog (Nhật Ký Hội Thoại)
- **Đường dẫn**: `vlearn-pack/chatlog/tutor_turns.csv`
- **Số dòng lượt hỏi-đáp**: 13.494 dòng (từ 22/07/2026 đến 15/09/2026)
- **Số học viên duy nhất**: 1.617 mã học viên đã ẩn danh (`S####`)
- **Dữ liệu Khóa K4**: 3.097 lượt (448 học viên, từ ngày 09/09/2026)
- **Các cột dữ liệu quan trọng**:
  - `turn_id`: Mã định danh lượt hỏi-đáp (`T00001` đến `T13494`).
  - `period`: Kỳ dữ liệu (`history` trước đợt làm lại hạ tầng 03/08 vs `live`).
  - `cohort_hint`: Nhãn khóa học (`K3` hoặc `K4`).
  - `asked_at_vn`: Thời điểm hỏi theo giờ Việt Nam (`YYYY-MM-DD HH:MM`).
  - `student`: Mã học viên đã mã hóa (`S####`).
  - `lecture_code`: Mã bài giảng (`D01`, `D02`, ...).
  - `lecture_title`: Tên bài giảng hiển thị trên hệ thống.
  - `course_id`: Mã khóa học (`K4P1`, `L2-L3-K4P1`, `COMP2010`, ...).
  - `is_preset`: Cờ đánh dấu câu hỏi mẫu bấm sẵn từ giao diện (chiếm 22.7%).
  - `q_len`: Độ dài câu hỏi tính theo số ký tự.
  - `student_question`: Câu hỏi nguyên văn của học viên (đã mask ẩn danh).
  - `tutor_reply`: Câu trả lời của AI Tutor cũ (đã mask ẩn danh).
  - `move_used`: Nước đi sư phạm (`review_concept`, `give_direct_answer`, `give_example`, ...).
  - `has_citation`: Cờ đánh dấu câu trả lời có trích dẫn tài liệu hay không (28% False).
  - `rating`: Đánh giá của học viên (`up` / `down` / rỗng).

## 2. Dữ Liệu Transcript Bài Giảng
- **Đường dẫn**:
  - `vlearn-pack/transcript/transcript-01-clean.md` (Day 2 sáng: Xác định bài toán kinh doanh)
  - `vlearn-pack/transcript/transcript-02-clean.md` (Day 2: Chỉ số thành công & tự động hóa)
  - `vlearn-pack/transcript/transcript-03-clean.md` (Day 2 chiều: Ràng buộc bài toán các nhóm)
  - `vlearn-pack/transcript/transcript-04-clean.md` (Day 1: Foundation - cách LLM hoạt động)
  - `vlearn-pack/transcript/transcript-05-clean.md` (Đánh giá bài toán & dữ liệu)
  - `vlearn-pack/transcript/transcript-06-clean.md` (Buổi Foundation: Transformer & Attention)
- **Định dạng**: Văn bản Markdown đã được làm sạch giọng nói ASR.
- **Mã trích dẫn nguồn**: Khoảng ~700 đoạn bài giảng được gắn mã định vị trích dẫn dạng `[Txx-NNN]` (ví dụ `[T04-015]`, `[T06-040]`).

## 3. Dữ Liệu Slide Bài Giảng
- **Đường dẫn**:
  - `vlearn-pack/slides/d1-slide-hackathon.pdf` (Slide Day 1 AI & LLM Foundation, 29 trang)
  - `vlearn-pack/slides/d2-slide-hackathon.pdf` (Slide Day 2 Xác định bài toán kinh doanh, 29 trang)

## 4. Ghi Chú & Giới Hạn Dữ Liệu Cần Lưu Ý
1. **Bất thường ngày 30/07/2026**: Có 2.579 lượt hỏi (do một hoạt động diễn ra trên lớp). Mọi báo cáo thống kê chính bắt buộc phải báo cáo theo 3 phiên bản: **Toàn bộ dữ liệu**, **Loại trừ 30/07**, và **Chỉ riêng Khóa K4**.
2. **Câu hỏi mẫu bấm sẵn (`is_preset`)**: Chiếm 22.7% tổng số lượt hỏi. Cần tách biệt phần này khi phân tích hành vi đặt câu hỏi tự nhiên của học viên.
3. **`tutor_reply` KHÔNG phải Ground Truth**: Câu trả lời cũ của Tutor chỉ dùng để tham khảo ngữ cảnh. Kiến thức chuẩn bắt buộc phải trích từ transcript/slide hoặc đánh dấu `manual_review_required: true`.
4. **Nhãn ẩn danh**: Tên người được chuyển thành `[HV]`, email thành `[EMAIL]`, số điện thoại thành `[PHONE]`, mã sinh viên thành `[MSSV]`.
