# API Test Report

Automated: `pytest` → 6 passed (AI layer mocked). Validation/health outputs below come from real calls to the app without an API key. **Live Gemini responses have not been tested yet**; do the Swagger tests with a real key.

| # | Endpoint | Request | Expected | Observed |
|---|---|---|---|---|
| 1 | GET /health | – | 200 `{status, version, timestamp}` | 200 `{"status":"ok","version":"1.0.0","timestamp":"2026-10-11T17:14:20Z"}` |
| 2 | POST /chat | `{"message":"What is an API?"}` | 200 `{answer}` | 200 (mocked, pytest) |
| 3 | POST /quiz | `{"topic":"Python","num_questions":2}` | 200, 2 questions | 200, 2 questions (mocked, pytest) |
| 4 | POST /summarise | `{"text":"x"*50,"max_bullets":2}` | 200, `bullet_count` 2 | 200 (mocked, pytest) |

## Validation errors (all `422`)
| Endpoint | Request | Error |
|---|---|---|
| POST /chat | `{"message":""}` | `string_too_short` – at least 1 character |
| POST /quiz | `{"topic":"Python","num_questions":99}` | `less_than_equal` – must be ≤ 10 |
| POST /summarise | `{"text":"short","max_bullets":0}` | `string_too_short` (text ≥ 20) and `greater_than_equal` (max_bullets ≥ 1) |

## Other errors
- Missing `GEMINI_API_KEY` on an AI endpoint → `503 {"detail":"GEMINI_API_KEY is not configured"}`.
- Provider failure → `502 {"detail":"AI provider error: ..."}`.

## Manual Swagger tests
- Valid: `POST /quiz` `{"topic":"Python","num_questions":3}` → 200.
- Invalid: `POST /quiz` `{"topic":"Python","num_questions":99}` → 422.
