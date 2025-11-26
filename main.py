# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # or restrict to your GitHub Pages domain for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatReq(BaseModel):
    message: str

@app.post("/chat")
def chat(req: ChatReq):
    # Example using Groq REST endpoint (adjust to actual Groq client you use)
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
      "model": "llama3-8b-8192",
      "messages": [{"role":"user", "content": req.message}]
    }
    r = requests.post(url, json=payload, headers=headers, timeout=30)
    r.raise_for_status()
    data = r.json()
    reply = data.get("choices", [{}])[0].get("message", {}).get("content", "No reply")
    return {"reply": reply}
