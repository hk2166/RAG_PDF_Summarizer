from provider import (
    openai_provider,
    deepseek_provider,
    gemini_provider,
    ollama_provider
)
import re

PROVIDERS = {
    "gemini": gemini_provider,
    "ollama": ollama_provider,
    "openai": openai_provider,
    "deepseek": deepseek_provider
}

MODEL_PRIORITY = ["gemini", "ollama", "openai", "deepseek"]


def summarize_with_fallback(chunk, model_priority):
    last_error = None

    for model_name in model_priority:
        try:
            print(f"→ Trying {model_name}")
            summary = PROVIDERS[model_name].summarize(chunk)

            if summary and len(summary) > 20:
                return summary, model_name

        except Exception as e:
            print(f"✗ {model_name} failed: {e}")
            last_error = e

    raise RuntimeError(f"All models failed. Last error: {last_error}")


def parse_chunks_file(chunks_file_path):
    """Read and parse chunks from chunks.txt file."""
    with open(chunks_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by chunk markers and extract content
    # Format: --- CHUNK 1 ---\ncontent\n--- CHUNK 2 ---\ncontent
    chunk_pattern = r'--- CHUNK \d+ ---\n(.*?)(?=\n--- CHUNK \d+ ---|$)'
    matches = re.findall(chunk_pattern, content, re.DOTALL)
    
    return [chunk.strip() for chunk in matches if chunk.strip()]


def process_chunks(chunks_file_path):
    """Process all chunks and generate summaries."""
    chunks = parse_chunks_file(chunks_file_path)
    
    chunk_summaries = []
    
    for i, chunk in enumerate(chunks):
        print(f"\nSummarizing chunk {i+1}/{len(chunks)}")

        summary, used_model = summarize_with_fallback(
            chunk,
            MODEL_PRIORITY
        )

        chunk_summaries.append({
            "chunk_id": i,
            "model": used_model,
            "summary": summary
        })
    
    return chunk_summaries


if __name__ == "__main__":
    CHUNKS_PATH = "../../output/chunks.txt"
    OUTPUT_PATH = "../../output/chunk_summaries.txt"
    
    print("Starting summarization...")
    chunk_summaries = process_chunks(CHUNKS_PATH)
    
    # Save summaries to file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for item in chunk_summaries:
            f.write(f"\n--- CHUNK {item['chunk_id']} ({item['model']}) ---\n")
            f.write(item["summary"])
            f.write("\n")
    
    print(f"\n✅ Completed {len(chunk_summaries)} summaries")
    print(f"✅ Saved to {OUTPUT_PATH}")
    
    for s in chunk_summaries:
        print(f"\nChunk {s['chunk_id']} ({s['model']}):")
        print(s['summary'][:100] + "...")
