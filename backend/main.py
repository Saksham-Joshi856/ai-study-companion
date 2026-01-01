from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from backend.ai_engine.summarizer import Summarizer
from backend.utils.pdf_reader import extract_text_from_pdf
from backend.utils.chunking import chunk_text

app = FastAPI(title="AI Study Companion")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

summarizer = Summarizer()


@app.get("/")
def root():
    return {"status": "running"}


@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)

    if not text:
        return {"error": "No text found in PDF"}

    chunks = chunk_text(text)

    summaries = []
    for chunk in chunks:
        summary = summarizer.summarize_text(chunk)
        summaries.append(summary)

    final_summary = " ".join(summaries)

    return {
        "summary": final_summary
    }
