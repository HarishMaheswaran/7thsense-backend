from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# 🔥 FIXED CORS SECTION — MUST BE HERE AND EXACTLY LIKE THIS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

class ChatReq(BaseModel):
    message: str

@app.get("/")
def root():
    return {"status": "online"}

@app.post("/chat")
def chat(req: ChatReq):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "user", "content": req.message}
        ]
    }

    r = requests.post("https://api.groq.com/openai/v1/chat/completions",
                       headers=headers,
                       json=payload)

    if r.status_code != 200:
        return {"reply": "API Error", "error": r.text}

    resp = r.json()
    reply = resp["choices"][0]["message"]["content"]
    return {"reply": reply}

