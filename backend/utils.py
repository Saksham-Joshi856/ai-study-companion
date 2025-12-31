from pypdf import PdfReader

def extract_text_from_pdf(file) -> str:
    reader = PdfReader(file.file)
    text = " ".join(page.extract_text() or "" for page in reader.pages)
    return text


def chunk_text(text: str, max_words: int = 300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)

    return chunks
