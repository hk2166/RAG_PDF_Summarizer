
import os
from dotenv import load_dotenv
import requests
from prompt import SUMMARY_PROMPT

# Load environment variables
load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
if not OLLAMA_API_KEY:
    raise ValueError("OLLAMA_API_KEY not found in .env file")

def summarize(chunk):
    response = requests.post(
        "http://localhost:11434/api/generate",
        headers={
            "Authorization": f"Bearer {OLLAMA_API_KEY}"
        },
        json={
            "model": "llama3",
            "prompt": SUMMARY_PROMPT.format(chunk=chunk),
            "stream": False
        },
        timeout=60
    )

    response.raise_for_status()
    return response.json()["response"].strip()
