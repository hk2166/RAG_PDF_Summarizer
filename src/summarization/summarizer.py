# Summarizer Module (Gemini Only)
try:
    from provider import gemini_provider
except ImportError:
    from .provider import gemini_provider

import time

def summarize_chunk(chunk):
    """
    Summarize a single chunk using Gemini.
    """
    try:
        return gemini_provider.summarize(chunk)
    except Exception as e:
        print(f"Error summarizing chunk: {e}")
        return None

def summarize_all(chunks):
    """
    Summarize a list of chunks.
    """
    summaries = []
    print(f"Summarizing {len(chunks)} chunks using Gemini...")
    for i, chunk in enumerate(chunks):
        print(f"  Processing chunk {i+1}/{len(chunks)}...")
        summary = summarize_chunk(chunk)
        if summary:
            summaries.append(summary)
        else:
            summaries.append(f"[Error summarizing chunk {i+1}]")
        # Gentle rate limiting
        time.sleep(1) 
    return summaries
