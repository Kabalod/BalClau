
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
CLAUDE_ENDPOINT = "https://api.anthropic.com/v1/messages"
CLAUDE_MODEL = "claude-3-opus-20240229"

class ClaudeRequest(BaseModel):
    user_message: str
    max_tokens: int = 1024

@app.post("/claude")
def ask_claude(payload: ClaudeRequest):
    headers = {
        "x-api-key": CLAUDE_API_KEY,
        "anthropic-version": "2023-06-01",
        "Content-Type": "application/json"
    }
    data = {
        "model": CLAUDE_MODEL,
        "max_tokens": payload.max_tokens,
        "messages": [
            {"role": "user", "content": payload.user_message}
        ]
    }
    response = requests.post(CLAUDE_ENDPOINT, headers=headers, json=data)
    return response.json()
