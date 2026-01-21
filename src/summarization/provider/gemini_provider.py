import os
import sys
from dotenv import load_dotenv
from google import genai

try:
    from prompt import SUMMARY_PROMPT
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from prompt import SUMMARY_PROMPT


load_dotenv()


if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client()


def summarize(chunk):
    response = client.models.generate_content(
        model="gemini-2.5-flash", contents=SUMMARY_PROMPT.format(chunk=chunk)
    )

    return response.text.strip() if response.text else ""
