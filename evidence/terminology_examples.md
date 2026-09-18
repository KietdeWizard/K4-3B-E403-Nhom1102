# Ví Dụ Thực Tế Câu Hỏi Thuật Ngữ Của Học Viên

Các câu hỏi tiêu biểu trích xuất trực tiếp từ chatlog thật (`vlearn-pack/chatlog/tutor_turns.csv`), phân loại theo taxonomy ý định.

## Định nghĩa khái niệm (define_concept)

### Mã lượt `Turn T00006`
- **Mã học viên**: `S0674`
- **Bài giảng**: `D01 - day01-llm-foundation`
- **Câu hỏi đã làm sạch**: "Giải thích đoạn bôi đen ở Trang 5."
- **Lý do phân loại**: Khớp quy tắc nhận dạng `preset_explain_selection`.

### Mã lượt `Turn T00007`
- **Mã học viên**: `S0674`
- **Bài giảng**: `D01 - day01-llm-foundation`
- **Câu hỏi đã làm sạch**: "2. Tính được chi phí API call dựa trên token economy
3. Gọi được API từ 3 providers: Anthropic, OpenAI, Google Gemini
4. Xây dựng chatb")
Giải thích đoạn bôi đen ở Trang 5."
- **Lý do phân loại**: Khớp quy tắc nhận dạng `preset_explain_selection`.

### Mã lượt `Turn T00009`
- **Mã học viên**: `S0140`
- **Bài giảng**: `D01 - day01-llm-foundation`
- **Câu hỏi đã làm sạch**: "Hãy giải thích ngắn gọn LLM là gì và trích dẫn slide."
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:là gì`.

### Mã lượt `Turn T00012`
- **Mã học viên**: `S0674`
- **Bài giảng**: `D02 - day02-xac-dinh-bai-toan-kinh-doanh-cho-ai`
- **Câu hỏi đã làm sạch**: "Giải thích đoạn bôi đen ở Trang 1: "i Toán Kinh Doan""
- **Lý do phân loại**: Khớp quy tắc nhận dạng `preset_explain_selection`.

### Mã lượt `Turn T00022`
- **Mã học viên**: `S0295`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "Giải thích đoạn bôi đen ở Trang 1: "VLearn Lecture Material""
- **Lý do phân loại**: Khớp quy tắc nhận dạng `preset_explain_selection`.

---

## So sánh khái niệm (compare_concepts)

### Mã lượt `Turn T00017`
- **Mã học viên**: `S0674`
- **Bài giảng**: `D01 - day01-llm-foundation`
- **Câu hỏi đã làm sạch**: "bạn hãy giải thích giúp tôi sự giống và khác nhau của các tầng trí tuệ nhân tạo."
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:khác\s+(?:với|như|sao|nhau|gì)`.

### Mã lượt `Turn T00197`
- **Mã học viên**: `S0595`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "Deep Learning khác gì so với Machine Learning truyền thống?"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:khác\s+(?:với|như|sao|nhau|gì)`.

### Mã lượt `Turn T00198`
- **Mã học viên**: `S0595`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "qua mạng nhiều tầng  B Yêu cầu ít dữ liệu huấn luyện hơn hẳn  C Chỉ chạy được trên các CPU cấu hình thấp")
Deep Learning khác gì so với Machine Learning truyền thống?  A Tự động trích xuất đặc trưng (Feature Extraction) qua mạng nhiều tầng  B Yêu cầu ít dữ liệu huấn luyện hơn hẳn  C Chỉ chạy được trên các CPU cấu hình thấp"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:khác\s+(?:với|như|sao|nhau|gì)`.

### Mã lượt `Turn T00200`
- **Mã học viên**: `S0595`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "qua mạng nhiều tầng  B Yêu cầu ít dữ liệu huấn luyện hơn hẳn  C Chỉ chạy được trên các CPU cấu hình thấp")
Deep Learning khác gì so với Machine Learning truyền thống?  A Tự động trích xuất đặc trưng (Feature Extraction) qua mạng nhiều tầng  B Yêu cầu ít dữ liệu huấn luyện hơn hẳn  C Chỉ chạy được trên các CPU cấu hình thấp"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:khác\s+(?:với|như|sao|nhau|gì)`.

### Mã lượt `Turn T00205`
- **Mã học viên**: `S0235`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "RNN và transformer khác nhau ơqr đâu"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:khác\s+(?:với|như|sao|nhau|gì)`.

---

## Giải thích cơ chế (explain_mechanism)

### Mã lượt `Turn T00245`
- **Mã học viên**: `S0546`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "về mặt toán học nó hoạt động như thế nào ?"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:hoạt động như`.

### Mã lượt `Turn T00382`
- **Mã học viên**: `S0597`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "giair thích cơ chế attention, mutilhead"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:cơ chế`.

### Mã lượt `Turn T00672`
- **Mã học viên**: `S0659`
- **Bài giảng**: `D02 - Day02`
- **Câu hỏi đã làm sạch**: "và vận hành hệ thống AI thực tế.
Product Thinking Inspired)
Xác định đúng bài toán, thấu hiểu người dùng,
tránh xây dựng những tính năng không mang lại
giá trị.
Design Thinking Everyday Things)
Thiết kế dựa trên mô hình tư duy Mental
")
bạn hãy tóm tắt ý chính trong tài liệu này"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:vận hành`.

### Mã lượt `Turn T00725`
- **Mã học viên**: `S0053`
- **Bài giảng**: `D12 - day03-tu-chatbot-den-agentic-agent-react`
- **Câu hỏi đã làm sạch**: "đề tài này thì sao tại sao lại có điểm cao hơn FAQ nội bộ HR"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:tại sao lại`.

### Mã lượt `Turn T01092`
- **Mã học viên**: `S0597`
- **Bài giảng**: `D14 - day04-prompt-engineering-tool-calling`
- **Câu hỏi đã làm sạch**: "kỹ thuật tối ưu prompt, cơ chế gọi tool và cách xử lý ngữ cảnh"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:cơ chế`.

---

## Quan hệ khái niệm (concept_relationship)

### Mã lượt `Turn T00136`
- **Mã học viên**: `S0408`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "• 2025 Thongtincuuho.org Co-founder)
• 2025 FPT Software AI Center PM · AI Agent)
• 2021  2025 Xantus PM · On-chain Analytics, AI Agent)
• 2016  2021 DY")
đây có phải là thông tin chính xác hay không ?"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:có phải`.

### Mã lượt `Turn T00194`
- **Mã học viên**: `S0235`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "LLM của google vậy bạn có phải dựa trên moo hình gemini không"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:có phải`.

### Mã lượt `Turn T00212`
- **Mã học viên**: `S0445`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "Có phải là một câu hỏi có 4 câu thì transformer sẽ xử lý đồng loạt 4 câu đó thay vì xử lý từng câu đúng k ?"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:có phải`.

### Mã lượt `Turn T00261`
- **Mã học viên**: `S1614`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "dựa vào tài liệu này bạn hãy cho tôi bộ quizz liên quan"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:liên quan`.

### Mã lượt `Turn T00431`
- **Mã học viên**: `S0546`
- **Bài giảng**: `D07 - day02-slide-blue`
- **Câu hỏi đã làm sạch**: "vậy nó liên quan gì đến diamond ?"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:liên quan`.

---

## Ứng dụng thực tế (concept_application)

### Mã lượt `Turn T01168`
- **Mã học viên**: `S1084`
- **Bài giảng**: `D15 - day05-lecture-slides-batch03`
- **Câu hỏi đã làm sạch**: "bằng các ứng dụng đọc PDF chuyên dụng trên máy tính để có thể tùy chỉnh mức độ zoom theo ý muốn.")
Bạn có thể mở trực tiếp tệp PDF của bài giảng (thường được đính kèm trong mục tài liệu của khóa học) bằng các ứng dụng đọc PDF chuyên dụng trên máy tính để có thể tùy chỉnh mức độ zoom theo ý muốn."
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:ứng dụng`.

### Mã lượt `Turn T01217`
- **Mã học viên**: `S0955`
- **Bài giảng**: `D16 - day05-slide-batch03-C401`
- **Câu hỏi đã làm sạch**: "hay chỉ cung cấp một lộ trình cố định cho tất cả mọi người?")
Ứng dụng có tự động phân tích điểm yếu của người dùng thông qua kết quả bài tập để liên tục tái định hình lộ trình học theo thời gian thực (real-time adaptation) hay chỉ cung cấp một lộ trình cố định cho tất cả mọi người?"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:ứng dụng`.

### Mã lượt `Turn T01856`
- **Mã học viên**: `S0460`
- **Bài giảng**: `D15 - day05-lecture-slides-batch03`
- **Câu hỏi đã làm sạch**: ", ví dụ với promise và intent 2 ứng dụng thực tế")
Trong slide 29 (trang 39), ví dụ với promise và intent 2 ứng dụng thực tế"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:ứng dụng`.

### Mã lượt `Turn T02126`
- **Mã học viên**: `S0025`
- **Bài giảng**: `D05 - Day05`
- **Câu hỏi đã làm sạch**: "tôi là 1 BA khách hàng muốn tôi thiết kế 1 ứng dụng giáo dục đơn giản tôi cần làm gì đầu tiên"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:ứng dụng`.

### Mã lượt `Turn T02328`
- **Mã học viên**: `S0460`
- **Bài giảng**: `D15 - day05-lecture-slides-batch03`
- **Câu hỏi đã làm sạch**: ", ví dụ với promise và intent 2 ứng dụng thực tế")
Trong slide 29 (trang 29), ví dụ với promise và intent 2 ứng dụng thực tế"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `rule:ứng dụng`.

---

## Từ khóa mơ hồ (ambiguous)

### Mã lượt `Turn T00343`
- **Mã học viên**: `S0049`
- **Bài giảng**: `D17 - 5-day02-lecture-slides-v2`
- **Câu hỏi đã làm sạch**: "AI agent"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `short_concept_query`.

### Mã lượt `Turn T00956`
- **Mã học viên**: `S1497`
- **Bài giảng**: `D04 - Day04`
- **Câu hỏi đã làm sạch**: "viết prompt"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `short_concept_query`.

### Mã lượt `Turn T02654`
- **Mã học viên**: `S0701`
- **Bài giảng**: `D05 - Day05`
- **Câu hỏi đã làm sạch**: "prompt engineering"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `short_concept_query`.

### Mã lượt `Turn T02740`
- **Mã học viên**: `S1403`
- **Bài giảng**: `D01 - Day01`
- **Câu hỏi đã làm sạch**: "LLM API"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `short_concept_query`.

### Mã lượt `Turn T03104`
- **Mã học viên**: `S1320`
- **Bài giảng**: `D05 - Day05`
- **Câu hỏi đã làm sạch**: "agent"
- **Lý do phân loại**: Khớp quy tắc nhận dạng `short_concept_query`.

---

