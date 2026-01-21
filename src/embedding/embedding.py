import os
import numpy as np
import faiss
import pickle
import re
import warnings

# Suppress warnings from google libraries
warnings.filterwarnings("ignore", category=FutureWarning)

from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not set in .env file")

genai.configure(api_key=API_KEY)

EMBEDDING_MODEL = "models/text-embedding-004"

def embed_text(text: str):
    """
    generate embedding for the text of gemini model (for documents/chunks)
    """
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=text,
        task_type="retrieval_document"
    )
    return result['embedding']


def embed_query(query: str) -> list[float]:
    """
    Generate embedding for a query using specific task type for better retrieval
    """
    result = genai.embed_content(
        model=EMBEDDING_MODEL,
        content=query,
        task_type="retrieval_query"
    )
    return result["embedding"]


def embed_chunks(chunks: list[str]) -> np.ndarray:
    embeddings = []

    for i, chunk in enumerate(chunks):
        print(f"Embedding chunk {i+1}/{len(chunks)}")
        vector = embed_text(chunk)
        embeddings.append(vector)

    return np.array(embeddings).astype("float32")


def build_faiss_index(embeddings: np.ndarray):
    """
    Builds a FAISS index from the given embeddings.
    """
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    return index


def parse_chunks_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    chunk_pattern = r'--- CHUNK \d+ ---\n(.*?)(?=\n--- CHUNK \d+ ---|$)'
    matches = re.findall(chunk_pattern, content, re.DOTALL)
    return [c.strip() for c in matches if c.strip()]


if __name__ == "__main__":
    # Script to build the index
    CHUNKS_PATH = "../../output/chunks.txt"
    INDEX_PATH = "../../output/index.faiss"
    METADATA_PATH = "../../output/metadata.pkl"

    if not os.path.exists(CHUNKS_PATH):
        print(f"❌ Error: Chunks file not found at {CHUNKS_PATH}")
        print("   Run src/chunking/chunker.py first.")
        exit(1)

    print(f"📖 Reading chunks from {CHUNKS_PATH}...")
    chunks = parse_chunks_file(CHUNKS_PATH)
    print(f"   Found {len(chunks)} chunks.")

    print("🧠 Generating embeddings (this may take a while)...")
    embeddings = embed_chunks(chunks)

    print("🏗️ Building FAISS index...")
    index = build_faiss_index(embeddings)
    
    print(f"💾 Saving index to {INDEX_PATH}...")
    faiss.write_index(index, INDEX_PATH)
    
    # Save metadata (text lookup)
    with open(METADATA_PATH, "wb") as f:
        pickle.dump([{"chunk_id": i, "text": t} for i, t in enumerate(chunks)], f)
    
    print("✅ Indexing complete!")


