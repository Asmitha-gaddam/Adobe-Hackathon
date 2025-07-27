import fitz  # PyMuPDF
import os

def extract_pages(pdf_path):
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({
            "page_number": i + 1,
            "text": text,
            "document": os.path.basename(pdf_path)
        })
    return pages