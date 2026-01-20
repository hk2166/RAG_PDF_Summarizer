from data_sanitization.extractor import extract_text_best_per_page

def is_gibberish(text, threshold=0.3):
    if not text.strip():
        return True

    junk = sum(1 for c in text if not c.isalnum() and not c.isspace())
    return (junk / len(text)) > threshold


def extract_clean_text(pdf_path):
    raw_text = extract_text_best_per_page(pdf_path)
    lines = raw_text.splitlines()
    clean_lines = [line for line in lines if not is_gibberish(line)]
    return "\n".join(clean_lines)

pdf_path = "../file/data.pdf"