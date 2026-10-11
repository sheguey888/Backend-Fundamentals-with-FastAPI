import os

from dotenv import load_dotenv
from fastapi import HTTPException
from google import genai
from google.genai import types

load_dotenv()
MODEL = "gemini-flash-lite-latest"
SYSTEM_PROMPT = "You are a helpful learning assistant. Be simple and accurate; if unsure, say so."


def generate(prompt: str, schema=None):
    """Call Gemini. Returns text, or a parsed object when `schema` is given."""
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise HTTPException(503, "GEMINI_API_KEY is not configured")
    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT)
    if schema:
        config.response_mime_type = "application/json"
        config.response_schema = schema
    try:
        resp = genai.Client(api_key=key).models.generate_content(
            model=MODEL, contents=prompt, config=config
        )
    except Exception as e:
        raise HTTPException(502, f"AI provider error: {e}")
    return resp.parsed if schema else resp.text
