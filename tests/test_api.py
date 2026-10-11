import pytest
from fastapi.testclient import TestClient

from app import main
from app.schemas import QuizQuestion

client = TestClient(main.app)


@pytest.fixture(autouse=True)
def fake_ai(monkeypatch):
    def fake(prompt, schema=None):
        if schema == list[str]:
            return ["point one", "point two", "point three"]
        if schema:
            return [QuizQuestion(question="Q?", options=["a", "b", "c", "d"], answer_index=0, explanation="e")] * 5
        return "hello"
    monkeypatch.setattr(main, "generate", fake)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert set(r.json()) == {"status", "version", "timestamp"}


def test_chat_valid():
    r = client.post("/chat", json={"message": "What is an API?"})
    assert r.status_code == 200 and r.json() == {"answer": "hello"}


def test_chat_empty_message_rejected():
    assert client.post("/chat", json={"message": ""}).status_code == 422


def test_quiz_respects_count():
    r = client.post("/quiz", json={"topic": "Python", "num_questions": 2})
    assert r.status_code == 200 and len(r.json()["questions"]) == 2


def test_quiz_too_many_questions_rejected():
    assert client.post("/quiz", json={"topic": "Python", "num_questions": 99}).status_code == 422


def test_summarise_respects_max_bullets():
    r = client.post("/summarise", json={"text": "x" * 50, "max_bullets": 2})
    assert r.status_code == 200 and r.json()["bullet_count"] == 2
