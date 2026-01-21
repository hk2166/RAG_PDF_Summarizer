def chunk_text(text, chunk_size=800, overlap=100):
    chunks = []
    current_chunk = ""
    paragraphs = text.split("\n\n")

    for para in paragraphs:
        para = para.strip()

        if not para:
            continue

        if len(current_chunk) + len(para) > chunk_size:
            if current_chunk.strip():
                chunks.append(current_chunk.strip())

            # Create new chunk with overlap
            # If current_chunk is empty, overlap logic might be weird, but python handles slice gracefully
            current_chunk = current_chunk[-overlap:] + "\n" + para
        else:
            current_chunk += "\n" + para

    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks


if __name__ == "__main__":
    CLEANED_TEXT_PATH = "../../output/cleaned.txt"
    OUTPUT_PATH = "../../output/chunks.txt"

    # Read the file first
    with open(CLEANED_TEXT_PATH, "r", encoding="utf-8") as f:
        cleaned_text = f.read()
    
    # Chunk the text
    chunks = chunk_text(cleaned_text)
    
    # Write chunks to output file
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        for i, chunk in enumerate(chunks):
            f.write(f"\n--- CHUNK {i+1} ---\n")
            f.write(chunk)
            f.write("\n")
    
    print(f"✅ Created {len(chunks)} chunks")
    print(f"✅ Saved to {OUTPUT_PATH}")








