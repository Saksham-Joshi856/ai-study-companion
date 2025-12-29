from fastapi import FastAPI, UploadFile, File
from backend.ai_engine import Summarizer
from backend.schemas import TextRequest, SummaryResponse
from pypdf import PdfReader

app = FastAPI(title="AI Study Companion")

summarizer = Summarizer()

@app.get("/")
def root():
    return {"status": "AI Study Companion running 🚀"}

@app.post("/summarize-text", response_model=SummaryResponse)
def summarize_text(request: TextRequest):
    summary = summarizer.summarize(request.text)
    return {"summary": summary}

@app.post("/summarize-pdf", response_model=SummaryResponse)
def summarize_pdf(file: UploadFile = File(...)):
    reader = PdfReader(file.file)
    text = " ".join(page.extract_text() for page in reader.pages)
    summary = summarizer.summarize(text)
    return {"summary": summary}
