from ai_engine import Summarizer
from utils import extract_text_from_pdf

if __name__ == "__main__":
    summarizer = Summarizer()

    file_path = "data/sample.pdf"  # change as needed

    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    if len(text.strip()) < 50:
        print("Input too short")
    else:
        summary = summarizer.summarize(text)
        print(summary)

