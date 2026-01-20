from data_sanitization.cleaner import cleaned_text_without_headers_footers
from data_sanitization.utils import extract_clean_text
from chunking.chunker import chunk_text
from summarizer import summarize_with_fallback
from dotenv import load_dotenv
load_dotenv()


MODEL_PRIORITY = ["openai", "deepseek", "gemini", "ollama"]
chunk_summaries = []

PDF_PATH = "../file/data.pdf"
OUTPUT_PATH = "../output/cleaned.txt"

HEADER_PATTERN = r'^Chapter\s+\d+'
FOOTER_PATTERN = r'^\d+$'


def run_pipeline():
    # 1. Extract and clean text (removes gibberish)
    clean_text = extract_clean_text(PDF_PATH)
    
    # 2. Split into lines
    clean_lines = clean_text.splitlines()
    
    # 3. Remove headers/footers
    final_text = cleaned_text_without_headers_footers(
        clean_lines,
        header_pattern=HEADER_PATTERN,
        footer_pattern=FOOTER_PATTERN
    )

    # 4. Save result
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_text)

    # 5. Chunk the text
    chunks = chunk_text(final_text, chunk_size=800, overlap=100)

    print("✅ Pipeline completed")
    print(f"✅ Created {len(chunks)} chunks")
    print(chunks)


if __name__ == "__main__":
    run_pipeline()
