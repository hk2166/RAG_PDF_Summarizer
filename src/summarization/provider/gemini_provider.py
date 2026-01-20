import os
import sys
from dotenv import load_dotenv
from google import genai  # Requires: pip install google-genai

# Handle imports whether running as a script or a module
try:
    from prompt import SUMMARY_PROMPT
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from prompt import SUMMARY_PROMPT

# Load environment variables from .env
load_dotenv()

# The new SDK automatically looks for "GEMINI_API_KEY" or "GOOGLE_API_KEY"
# in your environment, so you can just initialize the client directly.
# However, checking for the key's existence first is still good practice.
if not os.getenv("GEMINI_API_KEY"):
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client()

def summarize(chunk):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=SUMMARY_PROMPT.format(chunk=chunk)
    )
    # The new SDK returns an object where .text is a property, not a method.
    return response.text.strip() if response.text else ""