"""Live AI grounding decision module for the glossary prototype.

The module accepts lesson text plus a learner query. Configure one provider:

OpenAI-compatible:
    set OPENAI_API_KEY=...
    set AI_MODEL=gpt-4o-mini

Gemini:
    set AI_PROVIDER=gemini
    set GEMINI_API_KEY=...
    set AI_MODEL=gemini-2.0-flash

Run:
    python codebase/ai_decision_module.py
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ALLOWED_STATUSES = {
    "grounded",
    "low-confidence",
    "no-grounding",
    "out-of-scope",
}
DEFAULT_LOG_PATH = Path(__file__).with_name("logs") / "ai_decision_runs.jsonl"

SYSTEM_INSTRUCTIONS = """You are the grounding decision system for a lesson glossary prototype.
Use only the supplied lesson_context and topic_history. Do not use outside knowledge.
The lesson_context is the primary source; topic_history is only supporting context.
Do not evaluate the learner's ability.

Choose exactly one status:
- grounded: direct, sufficient evidence in lesson_context and the query is in scope.
- low-confidence: related evidence exists but is incomplete, ambiguous, or multi-meaning.
- no-grounding: the requested term or answer has no evidence in lesson_context.
- out-of-scope: the query asks for something beyond glossary support for this lesson,
  such as solving an exercise, predicting an exam, or unrelated knowledge.

Return only valid JSON. Do not use Markdown fences or add text outside the JSON.
The JSON must have exactly these fields:
{
  "status": "grounded | low-confidence | no-grounding | out-of-scope",
  "confidence_score": 0.0,
  "reason": "brief evidence-based explanation",
  "term": "main term or null",
  "evidence_found": true,
  "needs_human_check": true
}
"""


def build_prompt(
    lesson_context: str,
    user_query: str,
    topic_history: str | list[str] | None = None,
) -> str:
    """Build the user prompt sent to the model."""
    history = topic_history or "(none provided)"
    if isinstance(history, list):
        history = "\n".join(f"- {item}" for item in history)

    return f"""{SYSTEM_INSTRUCTIONS}

lesson_context:
---
{lesson_context.strip()}
---

user_query:
---
{user_query.strip()}
---

topic_history:
---
{history}
---

Classify the query now and return only the required JSON object."""


def extract_lesson_context(file_path: str | Path) -> str:
    """Extract lesson text from a PDF, PPTX, TXT, or Markdown file.

    PDF and PPTX support use optional packages so the core API client stays
    dependency-light. Install `pypdf` and `python-pptx` for those formats.
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")
    if suffix == ".pdf":
        try:
            from pypdf import PdfReader
        except ImportError as exc:
            raise RuntimeError("Install pypdf to read PDF lesson files") from exc
        return "\n\n".join(page.extract_text() or "" for page in PdfReader(path).pages).strip()
    if suffix == ".pptx":
        try:
            from pptx import Presentation
        except ImportError as exc:
            raise RuntimeError("Install python-pptx to read PowerPoint lesson files") from exc
        text_blocks = []
        for slide in Presentation(path).slides:
            slide_text = [shape.text for shape in slide.shapes if hasattr(shape, "text")]
            if slide_text:
                text_blocks.append("\n".join(slide_text))
        return "\n\n".join(text_blocks).strip()
    raise ValueError("Supported lesson files: .pdf, .pptx, .txt, .md")


def _request_json(url: str, payload: dict[str, Any], headers: dict[str, str]) -> str:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return response.read().decode("utf-8")


def call_model(prompt: str) -> str:
    """Call the configured live model and return its raw response text."""
    provider = os.getenv("AI_PROVIDER", "openai").lower()
    model = os.getenv("AI_MODEL")

    if provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")
        model = model or "gemini-2.0-flash"
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.0, "responseMimeType": "application/json"},
        }
        raw = _request_json(url, payload, {})
        response = json.loads(raw)
        return response["candidates"][0]["content"]["parts"][0]["text"]

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not configured")
    model = model or "gpt-4o-mini"
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    payload = {
        "model": model,
        "temperature": 0.0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": prompt},
        ],
    }
    raw = _request_json(
        f"{base_url}/chat/completions",
        payload,
        {"Authorization": f"Bearer {api_key}"},
    )
    response = json.loads(raw)
    return response["choices"][0]["message"]["content"]


def _extract_json(raw_response: str) -> dict[str, Any]:
    cleaned = raw_response.strip()
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.IGNORECASE)
    parsed = json.loads(cleaned)
    if not isinstance(parsed, dict):
        raise ValueError("Model response is not a JSON object")
    return parsed


def validate_output(result: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize the model output against the required schema."""
    required = {
        "status",
        "confidence_score",
        "reason",
        "term",
        "evidence_found",
        "needs_human_check",
    }
    missing = required - result.keys()
    if missing:
        raise ValueError(f"Missing output fields: {sorted(missing)}")
    if result["status"] not in ALLOWED_STATUSES:
        raise ValueError(f"Invalid status: {result['status']}")
    if not isinstance(result["confidence_score"], (int, float)):
        raise ValueError("confidence_score must be numeric")
    if not 0 <= float(result["confidence_score"]) <= 1:
        raise ValueError("confidence_score must be between 0 and 1")
    if not isinstance(result["reason"], str) or not result["reason"].strip():
        raise ValueError("reason must be a non-empty string")
    if result["term"] is not None and not isinstance(result["term"], str):
        raise ValueError("term must be a string or null")
    if not isinstance(result["evidence_found"], bool):
        raise ValueError("evidence_found must be boolean")
    if not isinstance(result["needs_human_check"], bool):
        raise ValueError("needs_human_check must be boolean")

    return {
        "status": result["status"],
        "confidence_score": round(float(result["confidence_score"]), 3),
        "reason": result["reason"].strip(),
        "term": result["term"].strip() if isinstance(result["term"], str) else None,
        "evidence_found": result["evidence_found"],
        "needs_human_check": result["needs_human_check"],
    }


def parse_response(raw_response: str) -> dict[str, Any]:
    """Parse and validate a raw model response."""
    return validate_output(_extract_json(raw_response))


def log_request(
    prompt: str,
    raw_response: str | None,
    result: dict[str, Any],
    *,
    log_path: str | Path = DEFAULT_LOG_PATH,
    error: str | None = None,
) -> None:
    """Append prompt, raw response, result, and error details to a JSONL log."""
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "prompt": prompt,
        "raw_response": raw_response,
        "result": result,
        "error": error,
    }
    with path.open("a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(record, ensure_ascii=False) + "\n")


def fallback_result(reason: str) -> dict[str, Any]:
    """Return a safe result when the model call or response validation fails."""
    return {
        "status": "low-confidence",
        "confidence_score": 0.0,
        "reason": reason,
        "term": None,
        "evidence_found": False,
        "needs_human_check": True,
    }


def decide(
    lesson_context: str,
    user_query: str,
    topic_history: str | list[str] | None = None,
    *,
    log_path: str | Path = DEFAULT_LOG_PATH,
) -> dict[str, Any]:
    """Build a prompt, call the live model, validate it, and write an audit log."""
    prompt = build_prompt(lesson_context, user_query, topic_history)
    raw_response: str | None = None
    error: str | None = None

    try:
        if not lesson_context.strip():
            raise ValueError("lesson_context is empty")
        if not user_query.strip():
            raise ValueError("user_query is empty")
        raw_response = call_model(prompt)
        result = parse_response(raw_response)
    except (ValueError, RuntimeError, KeyError, TypeError, json.JSONDecodeError, urllib.error.URLError) as exc:
        error = str(exc)
        result = fallback_result(f"Không thể xác minh bằng model: {error}")

    log_request(prompt, raw_response, result, log_path=log_path, error=error)
    return result


def main() -> int:
    sample = {
        "lesson_context": (
            "Slide 7: Attention allows the model to focus on relevant tokens. "
            "Each token is mapped into an embedding."
        ),
        "user_query": "Attention là gì?",
        "topic_history": "Học viên từng hỏi về token và embedding.",
    }
    result = decide(**sample)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["confidence_score"] == 0.0 and result["needs_human_check"]:
        print(f"\nAudit log: {DEFAULT_LOG_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
