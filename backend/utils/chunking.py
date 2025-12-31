def chunk_text(text: str, chunk_size=800, overlap=100):
    """
    Splits text into overlapping chunks
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap  # overlap helps with context continuity

    return chunks
