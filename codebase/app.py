from __future__ import annotations

import os
import tempfile
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from ai_decision_module import decide, extract_lesson_context

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 15 * 1024 * 1024


def get_lesson_context() -> str:
    lesson_text = request.form.get("lesson_context", "").strip()
    upload = request.files.get("lesson_file")

    if upload and upload.filename:
        suffix = Path(upload.filename).suffix.lower()
        if suffix not in {".pdf", ".pptx", ".txt", ".md"}:
            raise ValueError("Chỉ hỗ trợ PDF, PowerPoint, TXT hoặc Markdown.")
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temporary_file:
            upload.save(temporary_file)
            temporary_path = temporary_file.name
        try:
            extracted_text = extract_lesson_context(temporary_path)
        finally:
            Path(temporary_path).unlink(missing_ok=True)
        if not extracted_text.strip():
            raise ValueError(
                "Không đọc được chữ từ tài liệu. PDF này có thể là bản scan/ảnh; "
                "hãy dùng PDF có text hoặc OCR trước khi upload."
            )
        return extracted_text
    if lesson_text:
        return lesson_text
    return ""


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/api/decide")
def api_decide():
    try:
        lesson_context = get_lesson_context()
        user_query = request.form.get("user_query", "").strip()
        topic_history = request.form.get("topic_history", "").strip()
        if not lesson_context:
            return jsonify({"error": "Hãy nhập lesson context hoặc upload tài liệu."}), 400
        if not user_query:
            return jsonify({"error": "Hãy nhập câu hỏi của học viên."}), 400
        result = decide(lesson_context, user_query, topic_history)
        return jsonify(result)
    except (OSError, RuntimeError, ValueError) as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        app.logger.exception("Unexpected webapp error")
        return jsonify({"error": "Có lỗi máy chủ. Kiểm tra log để biết chi tiết."}), 500


@app.errorhandler(413)
def request_too_large(_error):
    return jsonify({"error": "Tệp quá lớn. Giới hạn là 15 MB."}), 413


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=False)
