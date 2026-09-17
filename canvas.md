


1. **Track + đề:** A2 · VLearn — tính năng mới: *Glossary theo bài học, có liên kết khái niệm*, bản đồ review glossary định nghĩa của chương/topic/video 
2. **Job executor:** Hoc vien đang xem slide lecture
3. **Pain:** 
Khi học một bài có nhiều thuật ngữ mới, học viên phải dừng đọc nhiều lần để hỏi nghĩa từng thuật ngữ. Các câu trả lời nằm rải rác trong cuộc hội thoại, khiến họ khó hình dung quan hệ guyawx các khái niệm và tiếp tục theo dõi bài học.

4. **Bằng chứng đầu:**
   - Data pack có `13.494` lượt hỏi–đáp của `1617` học viên — đủ signal để khảo sát. Trường `misconceptions` rỗng `28%`; chỉ `22.7%` lượt tutor trả lời. *Nguồn:* `data/vlearn-pack/chatlog/DATA_DICTIONARY.md`, ghép theo `turn_id`.
   - Phỏng vấn `09` học viên: `09/09` cần tốn thười gian hỏi đi hỏi lại các định nghĩa
5. **Lát cắt:** Học viên đang xem một slide/video trong VLearn · gặp nhiều thuật ngữ chưa rõ trong cùng topic · AI quyết định các thuật ngữ quan trọng nhất cần giải thích dựa trên nội dung bài học và lịch sử câu hỏi cùng topic · tạo một glossary ngắn gồm định nghĩa dễ hiểu, ví dụ theo ngữ cảnh bài học, và link/trang nguồn để học viên tra nhanh mà không phải hỏi lặp lại nhiều lần.

6. **AI tự làm đến đâu:** *Có điều kiện:* AI tự đề xuất glossary khi có đủ nguồn chính thức từ slide/video/topic và có signal rằng học viên hay hỏi định nghĩa trong phần đó; mỗi thuật ngữ phải kèm căn cứ từ nội dung bài học hoặc log câu hỏi. Khi không đủ nguồn hoặc thuật ngữ mơ hồ, AI ghi "chưa đủ căn cứ để định nghĩa chắc chắn" và gợi ý học viên hỏi giảng viên/tutor. *Lý do:* định nghĩa sai hoặc ngoài ngữ cảnh có thể làm học viên hiểu lệch kiến thức nền, nên AI chỉ hỗ trợ tra cứu và tổng hợp, không tự bịa thuật ngữ, không kết luận học viên yếu phần nào. **Willing users:** `[Tên 1]`, `[Tên 2]`, `[Tên 3]`.

7. **Phân công:** `Nguyễn Minh Kiệt` — product lead, canvas/spec, pain statement, lát cắt, user flow, safety rule · `Trần Hoàng Duy Anh` — prototype AI glossary, prompt, output JSON/format, kiểm tra hallucination · `Đào Minh Hiếu — thiết kế logic lấy thuật ngữ từ slide/topic, mapping thuật ngữ với nguồn, hard-test cases · `Phạm Thanh Sơn` — mining data câu hỏi định nghĩa, bằng chứng pain, ví dụ thực tế, khảo sát/phỏng vấn học viên.
