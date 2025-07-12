from chunking import chunk_text_by_words
import os
import fitz  # pymupdf

def load_file(path):
    if path.endswith(".txt"):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    elif path.endswith(".pdf"):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    else:
        raise ValueError("Unsupported file type")

def main():
    file_path = r"C:\Users\aagia\Desktop\7455eba6-bb80-41d3-96b7-12111eae648c.pdf"  # <--- Replace this

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return

    text = load_file(file_path)
    chunks = chunk_text_by_words(text)

    print(f"Loaded and chunked {len(chunks)} chunks.")
    print("First chunk:\n")
    print(chunks[0][:1000].encode('ascii', errors='ignore').decode())  # Print first 1000 characters of first chunk

if __name__ == "__main__":
    main()
