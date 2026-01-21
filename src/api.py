from fastapi import FastAPI, HTTPException
import os
import sys

# Ensure proper path visibility
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_core import RAGCore

app = FastAPI(title="RAG Q&A API")

# Initialize RAG System
rag = RAGCore()

@app.post("/ask")
def ask(payload: dict):
    question = payload.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    try:
        # Check if resources need loading
        if not rag.index:
             # Try refreshing in case it was just created
             if not rag._load_resources():
                 raise HTTPException(status_code=503, detail="Vector store not ready. Document not processed.")

        contexts = rag.retrieve(question, k=3)
        answer = rag.answer(question)
        
        return {
            "question": question,
            "answer": answer,
            "sources": contexts
        }
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=503, detail=f"Service error: {str(e)}")
