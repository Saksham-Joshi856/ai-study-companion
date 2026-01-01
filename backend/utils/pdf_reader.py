from PyPDF2 import PdfReader

def extract_text_from_pdf(file):
    reader = PdfReader(file.file)  # 👈 THIS IS CRITICAL
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text
