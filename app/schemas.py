from datetime import datetime

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str
    version: str
    timestamp: datetime


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)


class ChatResponse(BaseModel):
    answer: str


class QuizRequest(BaseModel):
    topic: str = Field(min_length=2, max_length=100)
    num_questions: int = Field(ge=1, le=10)


class QuizQuestion(BaseModel):
    question: str
    options: list[str]
    answer_index: int
    explanation: str


class QuizResponse(BaseModel):
    topic: str
    questions: list[QuizQuestion]


class SummariseRequest(BaseModel):
    text: str = Field(min_length=20, max_length=10000)
    max_bullets: int = Field(ge=1, le=10)


class SummariseResponse(BaseModel):
    bullets: list[str]
    bullet_count: int
