from data_sanitization.cleaner import cleaned_text_without_headers_footers
from data_sanitization.utils import extract_clean_text
from chunking.chunker import chunk_text
from embedding.embedding import embed_chunks, build_faiss_index

import pickle
import faiss
import os
from dotenv import load_dotenv

load_dotenv()


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PDF_PATH = os.path.join(os.path.dirname(BASE_DIR), "file", "data.pdf")
OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "output")
CLEANED_TEXT_PATH = os.path.join(OUTPUT_DIR, "cleaned.txt")
INDEX_PATH = os.path.join(OUTPUT_DIR, "index.faiss")
METADATA_PATH = os.path.join(OUTPUT_DIR, "metadata.pkl")

HEADER_PATTERN = r"^Chapter\s+\d+"
FOOTER_PATTERN = r"^\d+$"


def run_pipeline(pdf_path=PDF_PATH):
    print(f"🚀 Starting Pipeline for {pdf_path}...")

    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found at {pdf_path}")

    print("📄 Extracting text...")
    clean_text = extract_clean_text(pdf_path)

    clean_lines = clean_text.splitlines()
    final_text = cleaned_text_without_headers_footers(
        clean_lines, header_pattern=HEADER_PATTERN, footer_pattern=FOOTER_PATTERN
    )

    with open(CLEANED_TEXT_PATH, "w", encoding="utf-8") as f:
        f.write(final_text)

    print("🔪 Chunking text...")
    chunks = chunk_text(final_text, chunk_size=800, overlap=100)
    print(f"   Created {len(chunks)} chunks.")

    print("🧠 Generating embeddings...")
    embeddings = embed_chunks(chunks)

    print("🏗️ Building Index...")
    index = build_faiss_index(embeddings)
    faiss.write_index(index, INDEX_PATH)

    metadata = [{"chunk_id": i, "text": t} for i, t in enumerate(chunks)]
    with open(METADATA_PATH, "wb") as f:
        pickle.dump(metadata, f)

    print("✅ Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
