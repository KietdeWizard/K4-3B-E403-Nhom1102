# AI Spec - VLearn Contextual Glossary Layer - Nhom 1102

Huong: A - VLearn  
Loai: Tinh nang moi tren trai nghiem hoc hien co

## §1. User & Job

- **Job executor + workflow:** Hoc vien dang xem slide/video tren VLearn. Khi gap nhieu thuat ngu moi trong cung mot topic, hoc vien phai dung bai hoc de hoi tung cau rieng le, sau do tu ghep cac cau tra loi lai voi nhau.

- **Core JTBD:** Khi dang hoc mot bai co nhieu thuat ngu moi, hoc vien muon thay nhanh dinh nghia, vi du trong dung bai hoc, nguon/trang va quan he giua cac khai niem, de tiep tuc hoc ma khong bi dut mach.

- **Problem statement khong chua chu AI:** Dinh nghia thuat ngu hien nam rai rac trong tung luot hoi-dap, khien hoc vien ton thoi gian hoi lap lai, kho kiem tra nguon trong slide, va kho hinh dung quan he giua cac khai niem trong cung mot topic.

- **Evidence A/B:**
  - Data pack co `13.494` luot hoi-dap cua `1617` hoc vien. Nguon: `data/vlearn-pack/chatlog/DATA_DICTIONARY.md` va cac file mining trong `eval/`.
  - Truong `misconceptions` rong `28%`; chi `22.7%` luot co tutor tra loi. Nguon: `eval/evidence/terminology_stats.md`.
  - Phong van nhanh `09` hoc vien: `09/09` noi viec hoi lai cac dinh nghia lam ton thoi gian va dut mach hoc. Raw verbatim interview quotes chua duoc dua vao repo, day la gap can bo sung neu con thoi gian.
  - Quote chatlog that tu `eval/evidence/terminology_examples.md`:
    1. `T00009`: "Hay giai thich ngan gon LLM la gi va trich dan slide."
    2. `T00197`: "Deep Learning khac gi so voi Machine Learning truyen thong?"
    3. `T00205`: "RNN va transformer khac nhau o dau"
    4. `T00382`: "giai thich co che attention, mutilhead"
    5. `T00212`: "Co phai la mot cau hoi co 4 cau thi transformer se xu ly dong loat 4 cau do thay vi xu ly tung cau dung k?"
    6. `T00431`: "vay no lien quan gi den diamond?"

## §2. Impact & Quyết Định Chọn

| Ung vien | Ai bi anh huong | Tan suat | Ton gi moi lan | Ket luan |
|---|---:|---:|---|---|
| Contextual glossary layer | `09/09` hoc vien phong van; chatlog co nhieu cau hoi dinh nghia/so sanh/lien quan | Nhieu lan trong mot bai co nhieu thuat ngu | Dut mach hoc, hoi lap lai, kho trace ve slide | Chon |
| Tom tat toan bo bai hoc | Hoc vien can on lai sau buoi | Sau moi buoi | De giong summary tool chung, khong danh dung pain dang hoc | Loai |
| Ban do lo hong kien thuc ca nhan | Hoc vien co nhieu log hoc | Sau nhieu buoi | Cost-of-error cao vi co the gan nhan sai nang luc hoc vien | Loai |
| Dashboard cho kho cua ca lop | Giang vien/TA | Sau moi buoi | Doi user chinh sang giang vien, can xu ly noise va an danh | Loai |

- **Ly do chon:** VLearn AI hien tai da co the giai thich mot khai niem rieng le. Diem moi cua nhom la lop glossary theo bai/topic: gom cac thuat ngu quan trong, vi du theo noi dung bai, nguon trang va quan he khai niem de hoc vien khong phai hoi tung cau roi tu ghep lai.

## §3. Giải Pháp Tương Tự Đã Nghiên Cứu

| San pham | Flow cua ho | Dang hoc | Dang ne | Minh khac gi |
|---|---|---|---|---|
| Khan Academy Khanmigo | Hoc vien hoi trong luc hoc, chatbot giai thich theo ngu canh | Tra loi gan thoi diem hoc giup giam dut mach | De tro thanh chatbot chung neu khong gioi han nguon | Nhom tap trung vao glossary cards co source/page va concept connections |
| Coursera/edX transcript search & glossary | Hoc vien tim keyword trong transcript/glossary | Tim nhanh noi dung co trong khoa hoc | Thuong tinh, khong xu ly alias/typo/cau hoi tu nhien | Dung model de chon thuat ngu, tao vi du theo bai va noi quan he |
| VLearn AI hien tai | Hoc vien hoi mot cau va nhan giai thich | Da giai quyet nhu cau "X la gi?" | Cau tra loi nam rai rac trong chat, it thay quan he/nguon trang | Feature moi la lop glossary tong hop trong cung topic/slide |

## §4. Thiết Kế

- **Lat cat mot cau:** Hoc vien dang xem mot slide/video trong VLearn, gap nhieu thuat ngu moi trong cung topic; he thong goi model that de tao 3-5 glossary cards gom dinh nghia ngan, vi du theo ngu canh bai hoc, source/page trace duoc, va concept connections giua cac khai niem.

- **Prototype hien tai:** Flask app trong `codebase/` cho phep paste/upload lesson context, goi model that qua `ai_decision_module.py`, va hien thi glossary cards. CP3 da chung minh decision/grounding layer; ban hien tai them field `glossary`, `lesson_example`, `source_refs`, `concept_connections`.

- **Non-goals:**
  - Khong danh gia hoc vien yeu/manh o khai niem nao.
  - Khong tra loi bang kien thuc ngoai bai khi lesson context khong co can cu.
  - Khong thay the tutor trong cau hoi chuyen sau/tranh luan hoc thuat.
  - Khong tao concept map day du cho toan khoa trong ban demo nay.

- **Automation:** Conditional. He thong tu tao glossary khi co du lesson context va source trace duoc. Khi cau hoi mo ho, thieu context, ngoai pham vi, hoac nguon mau thuan, he thong phai `clarify`, `unsupported`, hoac `manual_review`.

### §4b. Nguyên Tắc HAX/PAIR Áp Dụng

| Nguyen tac | Ap dung trong prototype |
|---|---|
| G2 - Make clear how well the system can do what it can do | UI hien confidence, behavior va human-check khi can |
| G3 - Time services based on context | Glossary xuat hien theo bai/topic dang hoc, khong phai chatbot chung |
| G10 - Scope services when in doubt | Neu khong co can cu/source, he thong hoi lai hoac tu choi |
| G11 - Make clear why the system did what it did | Moi card co source/page va concept connection |
| PAIR cost-of-error | Sai dinh nghia co the lam hoc vien hieu lech, nen khong auto-ket luan khi thieu nguon |

## §5. Kiểu Lỗi - 4 Lớp Chỗ Khó

| Tinh huong | Lop | Hanh vi mong muon | Nguyen tac ap |
|---|---|---|---|
| Hoi "LLM la gi va trich dan slide" | Source of truth | `resolve`, dinh nghia co source/page that | G11 |
| Hoi "Deep Learning khac Machine Learning the nao" | Domain-specific | `resolve`, phan biet dung va neu quan he | G11 |
| Hoi "RNN va Transformer khac nhau o dau" co typo | Domain-specific | map duoc thuat ngu, khong fail vi typo | G2 |
| Hoi "attention" qua rong | Ambiguous/missing info | `clarify`, hoi attention trong ngu canh nao | G10 |
| Hoi "cai nay lien quan gi nhau?" khong co selected text | Ambiguous/missing info | yeu cau bo sung term/selection | G10 |
| Prompt injection yeu cau bo qua quy tac | Out of scope/authority | `unsupported`, khong lam theo injection | G10 |
| Hoi "Mamba State Space Model" khi bai khong co | Out of scope/authority | `unsupported`, khong bia dinh nghia/source | G10 |
| Slide noi Perceptron mau thuan voi transcript | Source of truth | `manual_review`, can human check | PAIR cost-of-error |
| Tao glossary nhung term khong co trong bai | Source of truth | loai term do, khong tao card | G11 |
| Tao connection sai quan he giua automation/augmentation | Domain-specific | sua relation theo source trong slide | G11 |

Case lam nhom so nhat khi demo: model bia `source_ref` hoac dua kien thuc ngoai bai vao glossary card. Vi vay validation loc `source_refs` chi giu nguon xuat hien that trong context.

## §6. Bốn Đường Đi Trải Nghiệm

- **Happy path:** Hoc vien upload slide/paste lesson -> bam Generate glossary -> he thong tra 3-5 cards -> moi card co dinh nghia, vi du trong bai, source/page, related terms -> hoc vien xem concept connections de hieu thu tu/quan he.
- **Low confidence:** Term mo ho hoac thieu signal -> he thong hoi lai can term/selection nao, khong doan.
- **Failure/no grounding:** Term khong co trong bai -> he thong bao ngoai pham vi lesson hien tai, khong tao dinh nghia gia.
- **Correction:** Hoc vien thay card sai/thieu -> ghi chu "can human check"; ban demo chua co nut submit correction day du, dua vao backlog.

## §7. Kiểm Thử

- **Chieu chat luong co the kiem chung:**
  1. Behavior correctness: output dung `resolve/clarify/unsupported/manual_review`.
  2. Grounding faithfulness: khong bia source; source/page phai xuat hien trong context.
  3. Glossary usefulness: case `resolve` co term, definition, lesson_example, source_ref.
  4. Concept connection quality: giai thich duoc quan he giua cac term trong cung topic.
  5. Safety: prompt injection/out-of-scope khong duoc tra loi nhu kien thuc trong bai.

- **Golden set CP3:** `eval/golden_set.json` co 22 case, trong do 16 case phat trien tu chatlog that, phu 4 taxonomy: source_of_truth, ambiguous_missing_info, out_of_scope_authority, domain_specific.

- **Run 2 glossary smoke set:** `eval/glossary_demo_cases.json` co 4 case de test product slice moi: generate glossary, concept connection, out-of-scope, ambiguous query.

- **Quality bar chot CP4:** Dat khi `>=75%` pass tren bo CP3 golden set, va `100%` case `out_of_scope_authority` pass. Voi glossary demo, moi case `resolve` phai co `definition + lesson_example + source_ref` trace duoc ve lesson context; khong chap nhan fabricated source.

- **Ket qua cac luot chay:**

| Run | Model | Bo test | Tong | Pass | Fail | Pass rate | Ghi chu |
|---|---|---:|---:|---:|---:|---:|---|
| run1 | gpt-4o-mini | `eval/golden_set.json` | 22 | 6 | 16 | 27.3% | Decision/grounding layer. Safety out-of-scope dat 2/2. Fail chinh do `lecture_context` qua ngan, chua phai slide/transcript that |
| run2 | pending | `eval/glossary_demo_cases.json` | 4 | pending | pending | pending | Se chay sau khi API/app on dinh voi UI glossary cards |

- **Tu khai han che:** Run 1 chua do day du chat luong glossary cards. Full concept map va tu dong tao glossary cho toan khoa hoc chua lam trong prototype nay.

## §8. Phân Công & Kế Hoạch

| Thanh vien | Trach nhiem |
|---|---|
| Nguyen Minh Kiet | Product lead, organize workflow, review/spec, slide demo, submission CP3/CP4/CP5 |
| Tran Hoang Duy Anh | Prompt, app/code, output JSON contract, live model integration, observe validation |
| Pham Thanh Son | Golden set, chatlog evidence, invite 2 external users cung Anh |
| Dao Minh Hieu | Eval runner, run results, quality dimensions/bar/results, backup demo recording cung Anh |

- **CP5 validation plan:** Son + Anh moi it nhat 2 nguoi ngoai nhom. Moi phien 10 phut, giao task:
  1. Tao glossary cho slide/topic dang xem.
  2. Dung source/page de kiem tra lai mot thuat ngu.
  3. Hoi mot khai niem ngoai bai de xem he thong tu choi.

- **Willing users:**
  - Do Dinh Long - 2A202602673: willing user ngoai nhom, se test task tao glossary va kiem tra source/page.
  - Vo Duc Tai - 2A202603007: willing user ngoai nhom, se test task hoi concept connection va khai niem ngoai bai.

## §9. Changelog

| Thoi diem | Doi gi | Vi sao |
|---|---|---|
| 2026-09-18 13:45 | Hoan thanh 22-case golden set va taxonomy 4 lop | Phuc vu CP3 quantitative eval |
| 2026-09-18 13:54 | Chay run1: 6/22 pass, 27.3% | Do thuc nghiem trung thuc cho decision/grounding layer |
| 2026-09-18 14:30 | Sua loi API key co the lo qua error UI, them `.env.example` va redaction | Bao mat va logging an toan |
| 2026-09-18 16:30 | Dinh huong lai visible product slice thanh contextual glossary layer | VLearn AI da giai thich khai niem rieng le; feature moi can vi du, source/page, connection |
| 2026-09-18 16:45 | Cap nhat app contract voi `glossary`, `lesson_example`, `source_refs`, `concept_connections` | De demo dung lat cat glossary |
| 2026-09-18 16:50 | Them `eval/glossary_demo_cases.json` va `eval/run2_glossary_plan.md` | Chuan bi Run 2 cho glossary layer |
