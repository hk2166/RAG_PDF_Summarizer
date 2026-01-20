import os
from dotenv import load_dotenv
from openai import OpenAI
from prompt import SUMMARY_PROMPT

# Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise ValueError("OPENAI_API_KEY not found in .env file")

client = OpenAI(api_key=API_KEY)

def summarize(chunk):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a precise technical summarizer."},
            {"role": "user", "content": SUMMARY_PROMPT.format(chunk=chunk)}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
