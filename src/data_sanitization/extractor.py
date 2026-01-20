from pypdf import PdfReader
import fitz



def extract_text_best_per_page(pdf_path):
    doc = fitz.open(pdf_path)
    reader = PdfReader(pdf_path)

    final_text = []

    for i, page in enumerate(doc):
        pymupdf_text = page.get_text() or ""
        pypdf_text = reader.pages[i].extract_text() or ""

        
        best_text = pymupdf_text if len(pymupdf_text) >= len(pypdf_text) else pypdf_text
        final_text.append(best_text)

    doc.close()
    return "\n".join(final_text)


pdf_path = "../file/data.pdf"