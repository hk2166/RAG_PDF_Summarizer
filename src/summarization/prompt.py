with open('../../output/chunks.txt', 'r') as f:
    chunks = f.read()
    
SUMMARY_PROMPT = """
You are summarizing a technical document.

Rules:
- Be concise and factual
- Do NOT add new information
- Preserve important technical details
- Use bullet points where appropriate

Text:
{chunk}
"""
