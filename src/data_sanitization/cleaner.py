from data_sanitization.utils import extract_clean_text
import re


def cleaned_text_without_headers_footers(
    clean_lines, header_pattern=None, footer_pattern=None
):
    cleaned_lines = []
    for line in clean_lines:
        line = line.strip()

        if not line:
            continue

        if header_pattern and re.search(header_pattern, line):
            continue

        if footer_pattern and re.search(footer_pattern, line):
            continue

        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


if __name__ == "__main__":
    pdf_path = "../file/data.pdf"
    raw_clean_text = extract_clean_text(pdf_path)
    clean_lines = raw_clean_text.splitlines()
    final_text = cleaned_text_without_headers_footers(clean_lines)
    print(final_text)
