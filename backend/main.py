from fastapi import FastAPI, UploadFile, File
from backend.ai_engine import Summarizer
from backend.utils import extract_text_from_pdf

app = FastAPI(title="AI Study Companion")

summarizer = Summarizer()

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/summarize-text")
def summarize_text(text: str):
    summary = summarizer.summarize(text)
    return {"summary": summary}

@app.post("/summarize-pdf")
def summarize_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)
    summary = summarizer.summarize(text)
    return {"summary": summary}
