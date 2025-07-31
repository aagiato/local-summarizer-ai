import os
from PyPDF2 import PdfReader
from chunking import chunk_text_by_words

def load_and_chunk_document(path: str, max_words: int = 375) -> list[str]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    if path.lower().endswith(".pdf"):
        reader = PdfReader(path)
        text = "".join(page.extract_text() or "" for page in reader.pages)
    elif path.lower().endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        raise ValueError("Unsupported file type, only PDF or TXT.")

    return chunk_text_by_words(text, max_words=max_words)
