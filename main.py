from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import requests

app = FastAPI()

# CORS setup
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

# REQUIRED for Render health checks
@app.get("/")
def root():
    return {"status": "online"}

# OPTIONAL wake endpoint
@app.get("/wake")
def wake():
    return {"wakeup": "ok"}

@app.post("/chat")
def chat(req: ChatReq):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    
    payload = {
        "model": "llama3-8b-8192",
        "messages": [{"role": "user", "content": req.message}]
    }

    res = requests.post(url, json=payload, headers=headers)
    data = res.json()

    return {"reply": data["choices"][0]["message"]["content"]}
