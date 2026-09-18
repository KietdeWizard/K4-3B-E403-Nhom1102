#!/usr/bin/env python3
"""
scripts/mine_glossary_inputs.py

Đọc file vlearn-pack/chatlog/tutor_turns.csv, làm sạch câu hỏi của học viên,
phân loại intent theo taxonomy thuật ngữ và tạo các file báo cáo:
  - eval/processed_student_questions.csv
  - eval/terminology_candidates.csv
  - evidence/terminology_stats.md
  - evidence/terminology_examples.md
"""

import os
import csv
import re
from collections import defaultdict

def clean_question(raw_q):
    if not raw_q:
        return ""
    q = raw_q.strip()
    # Loại bỏ tiền tố ngữ cảnh như (Trang N, đoạn được chọn: "...") hoặc (Đang học phần "...")
    q_cleaned = re.sub(r'^\s*\((?:Trang\s+\d+|Đang học phần|Đoạn được chọn)[^)]*\)\s*', '', q, flags=re.IGNORECASE)
    # Loại bỏ tiền tố Đoạn được chọn: "..."
    q_cleaned = re.sub(r'^\s*Đoạn được chọn:\s*".*?"\s*', '', q_cleaned, flags=re.IGNORECASE)
    q_cleaned = q_cleaned.strip()
    return q_cleaned if q_cleaned else q.strip()

def classify_intent(clean_q, is_preset_val):
    is_preset = (str(is_preset_val).lower() in ['true', '1', 't'])
    q_lower = clean_q.lower().strip()
    
    # Câu hỏi hành chính / nộp bài / sửa lỗi code / thao tác giao diện
    non_glossary_patterns = [
        r'nộp bài', r'dowload', r'tải slide', r'điểm danh', r'lịch học', r'deadline',
        r'tạo essay', r'viết bài luận', r'sửa lỗi code', r'chạy code', r'lỗi syntax',
        r'cho em xin link', r'đăng ký tài khoản', r'không bấm được'
    ]
    for p in non_glossary_patterns:
        if re.search(p, q_lower):
            return 'non_glossary', 'admin_or_tooling_query'

    # Xử lý preset
    if is_preset:
        if 'giải thích đoạn bôi đen' in q_lower or 'giải thích rõ đoạn này' in q_lower:
            return 'define_concept', 'preset_explain_selection'
        if 'tóm tắt' in q_lower:
            return 'non_glossary', 'preset_summary'
        return 'define_concept', 'preset_generic'

    # Quy tắc phân loại taxonomy
    # B. Comparison
    compare_patterns = [
        r'khác\s+(?:với|như|sao|nhau|gì)', r'so sánh', r'phân biệt', r'\bvs\b', r'sự khác nhau'
    ]
    for p in compare_patterns:
        if re.search(p, q_lower):
            return 'compare_concepts', f'rule:{p}'

    # A. Definition
    define_patterns = [
        r'là gì', r'nghĩa là gì', r'định nghĩa', r'giải thích', r'what is', r'nói rõ hơn về',
        r'khái niệm', r'được hiểu là', r'hiểu thế nào'
    ]
    for p in define_patterns:
        if re.search(p, q_lower):
            return 'define_concept', f'rule:{p}'

    # C. Mechanism
    mechanism_patterns = [
        r'hoạt động như', r'hoạt động sao', r'cơ chế', r'nguyên lý', r'vận hành', r'tại sao lại',
        r'cách hoạt động', r'how it works'
    ]
    for p in mechanism_patterns:
        if re.search(p, q_lower):
            return 'explain_mechanism', f'rule:{p}'

    # D. Relationship
    relationship_patterns = [
        r'liên quan', r'có phải', r'nằm trong', r'thuộc', r'tập con', r'quan hệ', r'liên kết'
    ]
    for p in relationship_patterns:
        if re.search(p, q_lower):
            return 'concept_relationship', f'rule:{p}'

    # E. Application
    application_patterns = [
        r'khi nào (?:dùng|sử dụng|áp dụng)', r'dùng để làm gì', r'ứng dụng', r'trường hợp nào', r'sử dụng khi nào'
    ]
    for p in application_patterns:
        if re.search(p, q_lower):
            return 'concept_application', f'rule:{p}'

    # F. Ambiguous / Short concept query
    if len(q_lower.split()) <= 4 and ('?' in q_lower or len(q_lower.split()) <= 2):
        ai_terms = ['attention', 'transformer', 'llm', 'embedding', 'prompt', 'top-k', 'top-p', 'agent', 'rag', 'fine-tuning', 'fine tuning', 'temperature']
        for term in ai_terms:
            if term in q_lower:
                return 'ambiguous', 'short_concept_query'
        if q_lower in ['cái này là gì?', 'là sao?', 'giải thích?']:
            return 'ambiguous', 'deictic_short_query'

    return 'non_glossary', 'no_terminology_match'

def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    chatlog_path = os.path.join(repo_root, 'vlearn-pack', 'chatlog', 'tutor_turns.csv')
    
    eval_dir = os.path.join(repo_root, 'eval')
    evidence_dir = os.path.join(repo_root, 'evidence')
    os.makedirs(eval_dir, exist_ok=True)
    os.makedirs(evidence_dir, exist_ok=True)

    rows = []
    with open(chatlog_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    processed = []
    candidates = []

    stats = {
        'all': {'turns': 0, 'students': set(), 'preset_turns': 0, 'term_turns': 0, 'term_students': set(), 'by_intent': defaultdict(int), 'by_intent_students': defaultdict(set), 'student_term_counts': defaultdict(int)},
        'no_spike': {'turns': 0, 'students': set(), 'preset_turns': 0, 'term_turns': 0, 'term_students': set(), 'by_intent': defaultdict(int), 'by_intent_students': defaultdict(set), 'student_term_counts': defaultdict(int)},
        'k4_only': {'turns': 0, 'students': set(), 'preset_turns': 0, 'term_turns': 0, 'term_students': set(), 'by_intent': defaultdict(int), 'by_intent_students': defaultdict(set), 'student_term_counts': defaultdict(int)}
    }

    examples_by_intent = defaultdict(list)

    for r in rows:
        turn_id = r['turn_id']
        student = r['student']
        cohort = r['cohort_hint']
        course_id = r['course_id']
        lecture_code = r['lecture_code']
        lecture_title = r['lecture_title']
        asked_at = r['asked_at_vn']
        is_preset_str = r['is_preset']
        is_preset = (str(is_preset_str).lower() in ['true', '1', 't'])
        raw_q = r['student_question']

        clean_q = clean_question(raw_q)
        q_len = len(clean_q)

        intent, rule_matched = classify_intent(clean_q, is_preset_str)

        proc_row = {
            'turn_id': turn_id,
            'student': student,
            'cohort_hint': cohort,
            'course_id': course_id,
            'lecture_code': lecture_code,
            'lecture_title': lecture_title,
            'asked_at_vn': asked_at,
            'is_preset': is_preset_str,
            'raw_student_question': raw_q,
            'clean_student_question': clean_q,
            'question_length': q_len,
            'classified_intent': intent
        }
        processed.append(proc_row)

        is_term = (intent != 'non_glossary')
        if is_term:
            cand_row = {
                'turn_id': turn_id,
                'student': student,
                'lecture': f"{lecture_code} - {lecture_title}",
                'clean_question': clean_q,
                'matched_rule': rule_matched,
                'proposed_label': intent,
                'review_label': intent,
                'review_notes': 'Phân loại tự động qua script khai phá'
            }
            candidates.append(cand_row)

            if len(examples_by_intent[intent]) < 10:
                examples_by_intent[intent].append({
                    'turn_id': turn_id,
                    'student': student,
                    'lecture': f"{lecture_code} - {lecture_title}",
                    'raw_q': raw_q,
                    'clean_q': clean_q,
                    'rule': rule_matched
                })

        date_str = asked_at.split(' ')[0] if asked_at else ''
        is_spike = (date_str == '2026-07-30')
        is_k4 = (cohort == 'K4')

        scopes_to_update = ['all']
        if not is_spike:
            scopes_to_update.append('no_spike')
        if is_k4:
            scopes_to_update.append('k4_only')

        for s_key in scopes_to_update:
            st = stats[s_key]
            st['turns'] += 1
            st['students'].add(student)
            if is_preset:
                st['preset_turns'] += 1
            if is_term:
                st['term_turns'] += 1
                st['term_students'].add(student)
                st['by_intent'][intent] += 1
                st['by_intent_students'][intent].add(student)
                st['student_term_counts'][student] += 1

    proc_csv_path = os.path.join(eval_dir, 'processed_student_questions.csv')
    with open(proc_csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['turn_id', 'student', 'cohort_hint', 'course_id', 'lecture_code', 'lecture_title', 'asked_at_vn', 'is_preset', 'raw_student_question', 'clean_student_question', 'question_length', 'classified_intent']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(processed)

    cand_csv_path = os.path.join(eval_dir, 'terminology_candidates.csv')
    with open(cand_csv_path, 'w', encoding='utf-8', newline='') as f:
        fieldnames = ['turn_id', 'student', 'lecture', 'clean_question', 'matched_rule', 'proposed_label', 'review_label', 'review_notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(candidates)

    stats_md_path = os.path.join(evidence_dir, 'terminology_stats.md')
    with open(stats_md_path, 'w', encoding='utf-8') as f:
        f.write('# Thống Kê Nhu Cầu Tra Cứu Thuật Ngữ (Terminology & Glossary)\n\n')
        f.write('Báo cáo thống kê thực nghiệm khai phá trực tiếp từ chatlog thật (`vlearn-pack/chatlog/tutor_turns.csv`).\n')
        f.write('Số liệu được phân tách theo 3 phạm vi nhằm loại bỏ thiên lệch do hoạt động bất thường ngày `2026-07-30`.\n\n')

        f.write('## 1. Tổng Quan Chỉ Số\n\n')
        f.write('| Chỉ số | Toàn bộ dữ liệu | Loại trừ 2026-07-30 | Chỉ Khóa K4 |\n')
        f.write('|---|---:|---:|---:|\n')
        f.write(f"| Tổng số lượt hỏi (`turns`) | {stats['all']['turns']:,} | {stats['no_spike']['turns']:,} | {stats['k4_only']['turns']:,} |\n")
        f.write(f"| Số học viên duy nhất (`unique students`) | {len(stats['all']['students']):,} | {len(stats['no_spike']['students']):,} | {len(stats['k4_only']['students']):,} |\n")
        f.write(f"| Lượt hỏi mẫu (`is_preset=true`) | {stats['all']['preset_turns']:,} ({stats['all']['preset_turns']/stats['all']['turns']*100:.1f}%) | {stats['no_spike']['preset_turns']:,} ({stats['no_spike']['preset_turns']/stats['no_spike']['turns']*100:.1f}%) | {stats['k4_only']['preset_turns']:,} ({stats['k4_only']['preset_turns']/stats['k4_only']['turns']*100:.1f}%) |\n")
        f.write(f"| Lượt hỏi về thuật ngữ | {stats['all']['term_turns']:,} ({stats['all']['term_turns']/stats['all']['turns']*100:.1f}%) | {stats['no_spike']['term_turns']:,} ({stats['no_spike']['term_turns']/stats['no_spike']['turns']*100:.1f}%) | {stats['k4_only']['term_turns']:,} ({stats['k4_only']['term_turns']/stats['k4_only']['turns']*100:.1f}%) |\n")
        f.write(f"| Số học viên có hỏi về thuật ngữ | {len(stats['all']['term_students']):,} ({len(stats['all']['term_students'])/len(stats['all']['students'])*100:.1f}%) | {len(stats['no_spike']['term_students']):,} ({len(stats['no_spike']['term_students'])/len(stats['no_spike']['students'])*100:.1f}%) | {len(stats['k4_only']['term_students']):,} ({len(stats['k4_only']['term_students'])/len(stats['k4_only']['students'])*100:.1f}%) |\n\n")

        f.write('## 2. Phân Tích Theo Ý Định Hỏi (Toàn Bộ Dữ Liệu)\n\n')
        f.write('| Nhóm ý định (Intent) | Số lượt | % Tổng lượt | Số học viên | % Tổng học viên |\n')
        f.write('|---|---:|---:|---:|---:|\n')
        intents_order = ['define_concept', 'compare_concepts', 'explain_mechanism', 'concept_relationship', 'concept_application', 'ambiguous', 'non_glossary']
        intent_names = {
            'define_concept': 'Định nghĩa thuật ngữ (`define_concept`)',
            'compare_concepts': 'So sánh khái niệm (`compare_concepts`)',
            'explain_mechanism': 'Giải thích cơ chế (`explain_mechanism`)',
            'concept_relationship': 'Quan hệ giữa các khái niệm (`concept_relationship`)',
            'concept_application': 'Ứng dụng & Khi nào dùng (`concept_application`)',
            'ambiguous': 'Từ khóa nhập mơ hồ (`ambiguous`)',
            'non_glossary': 'Không thuộc glossary (`non_glossary`)'
        }
        for i_cat in intents_order:
            t_cnt = stats['all']['by_intent'][i_cat] if i_cat != 'non_glossary' else (stats['all']['turns'] - stats['all']['term_turns'])
            s_cnt = len(stats['all']['by_intent_students'][i_cat]) if i_cat != 'non_glossary' else len(stats['all']['students'] - stats['all']['term_students'])
            t_pct = t_cnt / stats['all']['turns'] * 100
            s_pct = s_cnt / len(stats['all']['students']) * 100
            f.write(f"| {intent_names[i_cat]} | {t_cnt:,} | {t_pct:.1f}% | {s_cnt:,} | {s_pct:.1f}% |\n")

        f.write('\n## 3. Phân Tích Theo Ý Định Hỏi (Riêng Khóa K4)\n\n')
        f.write('| Nhóm ý định (Intent) | Số lượt | % Lượt K4 | Số học viên | % Học viên K4 |\n')
        f.write('|---|---:|---:|---:|---:|\n')
        for i_cat in intents_order:
            t_cnt = stats['k4_only']['by_intent'][i_cat] if i_cat != 'non_glossary' else (stats['k4_only']['turns'] - stats['k4_only']['term_turns'])
            s_cnt = len(stats['k4_only']['by_intent_students'][i_cat]) if i_cat != 'non_glossary' else len(stats['k4_only']['students'] - stats['k4_only']['term_students'])
            t_pct = t_cnt / stats['k4_only']['turns'] * 100 if stats['k4_only']['turns'] else 0
            s_pct = s_cnt / len(stats['k4_only']['students']) * 100 if stats['k4_only']['students'] else 0
            f.write(f"| {intent_names[i_cat]} | {t_cnt:,} | {t_pct:.1f}% | {s_cnt:,} | {s_pct:.1f}% |\n")

        f.write('\n## 4. Phân Tích Tần Suất Tra Cứu Lặp Lại Nối Tiếp\n\n')
        f.write('Nhằm kiểm tra giả thuyết bài toán: học viên có phải tra cứu nhiều thuật ngữ riêng lẻ trong cùng bài học hay không:\n\n')

        for s_name, s_key in [('Toàn bộ dữ liệu', 'all'), ('Loại trừ 2026-07-30', 'no_spike'), ('Khóa K4', 'k4_only')]:
            st = stats[s_key]
            counts = st['student_term_counts']
            st_ge1 = len(st['term_students'])
            st_ge2 = sum(1 for s, c in counts.items() if c >= 2)
            st_ge3 = sum(1 for s, c in counts.items() if c >= 3)
            st_ge5 = sum(1 for s, c in counts.items() if c >= 5)
            f.write(f"### {s_name}\n")
            f.write(f"- Học viên hỏi ≥1 câu hỏi thuật ngữ: **{st_ge1:,}** ({st_ge1/len(st['students'])*100:.1f}% tổng số học viên)\n")
            f.write(f"- Học viên hỏi ≥2 câu hỏi thuật ngữ: **{st_ge2:,}** ({st_ge2/st_ge1*100:.1f}% học viên có hỏi thuật ngữ)\n")
            f.write(f"- Học viên hỏi ≥3 câu hỏi thuật ngữ: **{st_ge3:,}** ({st_ge3/st_ge1*100:.1f}% học viên có hỏi thuật ngữ)\n")
            f.write(f"- Học viên hỏi ≥5 câu hỏi thuật ngữ: **{st_ge5:,}** ({st_ge5/st_ge1*100:.1f}% học viên có hỏi thuật ngữ)\n\n")

    examples_md_path = os.path.join(evidence_dir, 'terminology_examples.md')
    with open(examples_md_path, 'w', encoding='utf-8') as f:
        f.write('# Ví Dụ Thực Tế Câu Hỏi Thuật Ngữ Của Học Viên\n\n')
        f.write('Các câu hỏi tiêu biểu trích xuất trực tiếp từ chatlog thật (`vlearn-pack/chatlog/tutor_turns.csv`), phân loại theo taxonomy ý định.\n\n')

        intent_titles = {
            'define_concept': 'Định nghĩa khái niệm (define_concept)',
            'compare_concepts': 'So sánh khái niệm (compare_concepts)',
            'explain_mechanism': 'Giải thích cơ chế (explain_mechanism)',
            'concept_relationship': 'Quan hệ khái niệm (concept_relationship)',
            'concept_application': 'Ứng dụng thực tế (concept_application)',
            'ambiguous': 'Từ khóa mơ hồ (ambiguous)'
        }

        for intent in ['define_concept', 'compare_concepts', 'explain_mechanism', 'concept_relationship', 'concept_application', 'ambiguous']:
            f.write(f"## {intent_titles[intent]}\n\n")
            ex_list = examples_by_intent[intent]
            if not ex_list:
                f.write("*Không tìm thấy ví dụ phù hợp.*\n\n")
                continue
            for ex in ex_list[:5]:
                f.write(f"### Mã lượt `Turn {ex['turn_id']}`\n")
                f.write(f"- **Mã học viên**: `{ex['student']}`\n")
                f.write(f"- **Bài giảng**: `{ex['lecture']}`\n")
                f.write(f"- **Câu hỏi đã làm sạch**: \"{ex['clean_q']}\"\n")
                f.write(f"- **Lý do phân loại**: Khớp quy tắc nhận dạng `{ex['rule']}`.\n\n")
            f.write('---\n\n')

    print("Mining and evidence generation complete!")
    print(f"- Processed questions: {len(processed):,}")
    print(f"- Terminology candidates: {len(candidates):,}")

if __name__ == '__main__':
    main()
