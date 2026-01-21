from pypdf import PdfReader
import fitz


def extract_text_best_per_page(pdf_path):
    doc = fitz.open(pdf_path)
    reader = PdfReader(pdf_path)

    final_text = []

    for i, page in enumerate(doc):
        try:
            pymupdf_text = page.get_text() or ""
        except Exception:
            pymupdf_text = ""

        try:
            if i < len(reader.pages):
                pypdf_text = reader.pages[i].extract_text() or ""
            else:
                pypdf_text = ""
        except Exception:
            pypdf_text = ""

        best_text = pymupdf_text if len(pymupdf_text) >= len(pypdf_text) else pypdf_text
        final_text.append(best_text)

    doc.close()
    return "\n".join(final_text)


if __name__ == "__main__":
    pdf_path = "../file/data.pdf"
