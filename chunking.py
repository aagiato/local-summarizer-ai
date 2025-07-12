def chunk_text_by_words(text: str, max_words: int = 375, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_words
        chunk = words[start:end]
        chunks.append(" ".join(chunk))
        start += max_words - overlap
    return chunks
