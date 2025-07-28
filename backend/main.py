
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os
import requests

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class AgentRequest(Base):
    __tablename__ = "agent_requests"
    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(50), index=True)
    prompt = Column(Text)
    response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class RequestPayload(BaseModel):
    agent: str
    prompt: str

class ResponsePayload(BaseModel):
    agent: str
    prompt: str
    response: str

@app.post("/agent/prompt", response_model=ResponsePayload)
def handle_prompt(payload: RequestPayload):
    # Интеграция с реальным Claude API (аналогичная функция)
    response = f"Simulated Claude API response to: {payload.prompt}"
    db = SessionLocal()
    try:
        req = AgentRequest(agent_name=payload.agent, prompt=payload.prompt, response=response)
        db.add(req)
        db.commit()
        db.refresh(req)
    finally:
        db.close()
    return ResponsePayload(agent=payload.agent, prompt=payload.prompt, response=response)

@app.get("/agent/history/{agent_name}")
def get_agent_history(agent_name: str):
    db = SessionLocal()
    try:
        results = db.query(AgentRequest).filter_by(agent_name=agent_name).all()
        return [{"prompt": r.prompt, "response": r.response, "created_at": r.created_at.isoformat()} for r in results]
    finally:
        db.close()
