from datetime import datetime, timezone

from fastapi import FastAPI

from app.ai import generate
from app.schemas import (ChatRequest, ChatResponse, HealthResponse, QuizQuestion,
                         QuizRequest, QuizResponse, SummariseRequest, SummariseResponse)

VERSION = "1.0.0"
app = FastAPI(title="Learning Assistant API", version=VERSION)


# --- Health (never calls the AI model) ---
@app.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(status="ok", version=VERSION, timestamp=datetime.now(timezone.utc))


# --- Chat ---
@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    return ChatResponse(answer=generate(req.message))


# --- Quiz ---
@app.post("/quiz", response_model=QuizResponse)
def quiz(req: QuizRequest):
    prompt = (f"Write {req.num_questions} multiple-choice questions about '{req.topic}'. "
              "Each has 4 options, the 0-based index of the correct one, and a short explanation.")
    questions = generate(prompt, schema=list[QuizQuestion])[: req.num_questions]
    return QuizResponse(topic=req.topic, questions=questions)


# --- Summarise ---
@app.post("/summarise", response_model=SummariseResponse)
def summarise(req: SummariseRequest):
    prompt = (f"Summarise the text below in at most {req.max_bullets} short bullet points. "
              f"Return a JSON list of strings.\n\n{req.text}")
    bullets = generate(prompt, schema=list[str])[: req.max_bullets]
    return SummariseResponse(bullets=bullets, bullet_count=len(bullets))
