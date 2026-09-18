# Bảng Ghi Nhận Validation Trực Tiếp Với Người Dùng (User Testing Log)

> **Phương pháp áp dụng**: Stanford CS177 (Jim Morris) / Sean Ellis Disappointment Metric / PAIR 5.1 Behavior Digest  
> **Thời gian thực hiện**: 18/09/2026  
> **Thành phần tham gia quan sát**: Trần Hoàng Duy Anh, Phạm Thanh Sơn (Nhóm 1102)

---

## 1. Danh Sách & Nhật Ký Người Thử (User Test Log)

| Người thử (Tên/Mã — Willing User?) | Task đã giao | Quan sát hành vi (PAIR 5.1 Signals) | Quote nguyên văn | Mức nghiêm trọng |
|---|---|---|---|---|
| **Võ Đức Tài** <br>`2A202603007`<br>*(Willing User CP1, Học viên K4)* | **Task 1:** Dùng prototype tra cứu thuật ngữ "LLM là gì và trích dẫn slide" trong bài học Day 1. | • Mở app bấm ngay nút tải demo mà không ngõ text.<br>• Khi thẻ Glossary hiển thị, di chuột 3s rà soát mã `T04-003`.<br>• Do dự 2s tìm cách nhấp vào mã `T04-003` để mở slide PDF.<br>• Không bấm Regenerate do kết quả đúng ngữ cảnh. | *"Cái thẻ card có trích dẫn T04-003 khá yên tâm vì đúng slide thầy giảng, nhưng nãy tui tưởng bấm vô cái chữ T04-003 đó là nó tự nhảy tới trang slide PDF luôn chớ!"* | **Medium**<br>*(UX: Cần hỗ trợ click jump tới trang slide)* |
| **Đỗ Đình Long** <br>`2A202602673`<br>*(Willing User CP1, Học viên K4)* | **Task 2:** Thử thách AI bằng câu hỏi ngoài bài: "Mamba State Space Model là gì và khác gì Transformer?" | • Đặt câu hỏi nâng cao ngoài bài học.<br>• Hệ thống trả về `unsupported` (Out of scope).<br>• Do dự 4s tưởng AI bị đơ, sau khi đọc thông báo từ chối liền gật đầu hiểu ra.<br>• Thử gõ câu hỏi thứ 2 về "Attention Mechanism" thì nhận `resolve` ngay. | *"Mới đầu tui tưởng nó bị ngu khi từ chối trả lời Mamba, nhưng đọc kỹ lại thấy nó ghi rõ không có trong slide thì chuẩn đấy! Thà từ chối còn hơn bịa linh tinh làm tui học sai."* | **Low**<br>*(Cần làm rõ thêm UI badge an toàn để user không tưởng nhầm là lỗi)* |

---

## 2. Kịch Bản 5 Nhịp Đã Thực Hiện

1. **Comfort (~1')**: *"Tụi mình đang đánh giá sản phẩm, không đánh giá bạn; không có câu trả lời đúng/sai — cứ nói to suy nghĩ của bạn."*
2. **Context (~1')**: *"Kể lần gần nhất bạn gặp hàng loạt thuật ngữ mới khi xem slide VLearn, bạn đã làm gì?"*  
   *Trả lời từ Võ Đức Tài*: *"Tui phải mở Google với ChatGPT sang 2 tab khác, vừa học vừa tra đuối muốn chết."*
3. **Task (~1')**: Giao task theo Outcome (không chỉ nút):  
   - Task 1: *"Hãy dùng công cụ này để làm rõ thuật ngữ LLM cùng trích dẫn trong bài học."*
   - Task 2: *"Hãy tra thử một khái niệm bạn thắc mắc xem hệ thống xử lý thế nào."*
4. **Observe (~5')**: Im lặng quan sát hành vi PAIR (do dự, di chuột, sửa prompt, thử nghiệm). Chỉ dùng câu hỏi trung tính khi người thử bị kẹt: *"Bạn nghĩ nó nên hoạt động thế nào?"*
5. **Hỏi sau khi dùng (~2')**:  
   - **Disappointment Question (Sean Ellis)**: *"Nếu từ mai không được dùng cái này nữa, bạn cảm thấy thế nào?"*  
     - *Võ Đức Tài*: **Rất tiếc** (nếu nhấp được trực tiếp vào trang slide).  
     - *Đỗ Đình Long*: **Rất tiếc** (vì tiết kiệm thời gian vừa học vừa mở tab ChatGPT ngoài).

---

## 3. Tổng Hợp 4 Dòng Tín Hiệu (Validation Synthesis)

1. **Chủ đề lặp nhiều nhất**: Người dùng rất thích việc trích dẫn đúng nguồn `source_ids` (`T04-003`), nhưng mong muốn mã nguồn này nhấp được (`clickable link`) để nhảy trực tiếp tới trang slide PDF tương ứng.
2. **1-2 thay đổi làm trước demo (→ Đã cập nhật vào Changelog Spec §9)**:
   - Thêm tooltip giải thích định dạng mã `T04-003` (`[Tập slide 04 - Trang 003]`).
   - Cập nhật màu sắc UI cho badge trạng thái `unsupported` để người dùng nhận diện ngay đây là cơ chế an toàn (chống bịa tri thức), tránh hiểu nhầm là hệ thống bị lỗi.
3. **Giữ nguyên có lý do**: Giữ nguyên cơ chế kiên quyết từ chối (`unsupported` / `clarify`) khi bài học không có căn cứ. Phản hồi thực tế từ Đỗ Đình Long khẳng định việc AI từ chối giúp xây dựng độ tin cậy (`grounding trust`) cao hơn nhiều so với việc cố trả lời linh tinh.
4. **Đưa vào backlog (Cho Slide 6 / Phiên bản tiếp theo)**:
   - **Interactive PDF Viewer**: Click vào `source_id` sẽ mở ngay viewer đọc file PDF và highlight dòng tương ứng.
   - **Submit Correction Button**: Cho phép học viên gửi đánh giá/gắn cờ nếu phát hiện thẻ thuật ngữ chưa đầy đủ.
