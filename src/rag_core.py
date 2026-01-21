import os
import pickle
import faiss
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv


import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from QA_Prompt import RAG_PROMPT
from embedding.embedding import embed_query
from main import run_pipeline


class RAGCore:
    def __init__(self, api_key=None):
        load_dotenv()
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY not set")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel("gemini-2.5-flash")

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_dir = os.path.join(os.path.dirname(self.base_dir), "output")
        self.index_path = os.path.join(self.output_dir, "index.faiss")
        self.metadata_path = os.path.join(self.output_dir, "metadata.pkl")

        self.index = None
        self.metadata = None
        self._load_resources()

    def _load_resources(self):
        """Attempts to load the index and metadata. Returns True if successful."""
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            try:
                self.index = faiss.read_index(self.index_path)
                with open(self.metadata_path, "rb") as f:
                    self.metadata = pickle.load(f)
                return True
            except Exception as e:
                print(f"Error loading resources: {e}")
                return False
        return False

    def process_document(self, pdf_path=None):
        """Runs the pipeline on the given PDF (or default if None)."""
        print(f"Running pipeline via RAGCore on {pdf_path or 'default'}...")
        if pdf_path:
            run_pipeline(pdf_path)
        else:
            run_pipeline()
        return self._load_resources()

    def retrieve(self, query: str, k: int = 3):
        if not self.index or not self.metadata:
            if not self._load_resources():
                raise RuntimeError("Index not processed. Please run the pipeline.")

        query_vector = embed_query(query)
        query_vector = np.array([query_vector]).astype("float32")

        _, indices = self.index.search(query_vector, k)

        valid_indices = [i for i in indices[0] if 0 <= i < len(self.metadata)]

        return [self.metadata[i]["text"] for i in valid_indices]

    def answer(self, question: str):
        contexts = self.retrieve(question)
        if not contexts:
            return "I couldn't find relevant information in the document."

        context_text = "\n\n".join(contexts)
        prompt = RAG_PROMPT.format(context=context_text, question=question)

        response = self.model.generate_content(prompt)
        return response.text.strip()
