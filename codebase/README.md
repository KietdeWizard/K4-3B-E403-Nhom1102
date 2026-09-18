# CP2 VLearn AI Glossary Agent Workflow

This folder contains a single static HTML workflow showing how the VLearn AI glossary agent works.

## How to open

Open `index.html` directly in a browser.

## Run the live model

Configure one provider before running:

```powershell
$env:OPENAI_API_KEY = "..."
$env:AI_MODEL = "gpt-4o-mini"
python codebase/ai_decision_module.py --lesson-file lesson.md --query "LLM là gì?"
```

For Gemini, set `AI_PROVIDER=gemini`, `GEMINI_API_KEY`, and `AI_MODEL` instead.
The command sends the supplied query and lesson context to the configured model and
prints the normalized output contract.

## Run the golden set

```powershell
python scripts/run_golden_eval.py --limit 5
python scripts/run_golden_eval.py --context-file lesson.md --output eval/results.json
```

The evaluator calls the live model through `ai_decision_module.decide()` and writes
one audit record per call to `codebase/logs/ai_decision_runs.jsonl`.

## PDF troubleshooting

When both a file and pasted lesson text are present, the uploaded file takes
priority. PDF pages are marked and relevant pages are selected before the prompt
is sent to the model, which keeps long slide decks searchable. If the API says
the PDF has no readable text, it is likely a scanned/image-only PDF; run OCR on
the file first or paste its extracted text into the lesson context field.

After changing Python files, restart Flask:

```powershell
$env:PYTHONPATH = "$PWD\codebase"
python codebase/app.py
```

## What the workflow demonstrates

- User prompt to VLearn AI.
- Context retrieval from current lesson.
- AI decision point for grounding and confidence.
- Happy path, low-confidence, no-grounding, and correction branches.
- Output contract for glossary terms, related keywords, and learning order.

This is only a workflow artifact, not the final product UI.
