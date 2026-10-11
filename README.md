# Learning Assistant API

FastAPI backend (Gemini via Google AI Studio) with `/health`, `/chat`, `/quiz`, `/summarise`.

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # put your key from https://aistudio.google.com/apikey
fastapi dev app/main.py
```
Swagger UI: http://127.0.0.1:8000/docs

## Endpoints
| Method | Path | Body | Response |
|---|---|---|---|
| GET | /health | – | `{status, version, timestamp}` (no AI call) |
| POST | /chat | `{message}` (1–2000 chars) | `{answer}` |
| POST | /quiz | `{topic, num_questions}` (1–10) | `{topic, questions:[{question, options, answer_index, explanation}]}` |
| POST | /summarise | `{text, max_bullets}` (text 20–10000 chars, 1–10) | `{bullets, bullet_count}` |

## Manual tests in Swagger UI (`/docs` → *Try it out*)
1. **Valid** – `POST /quiz` with `{"topic": "Python", "num_questions": 3}` → `200` with 3 questions.
2. **Invalid** – `POST /quiz` with `{"topic": "Python", "num_questions": 99}` → `422` ("less than or equal to 10").

## Automated tests
```bash
pytest
```
The AI call is mocked, so tests need no API key. See [docs/api-test-report.md](docs/api-test-report.md).
