from fastapi import FastAPI, UploadFile, File
from backend.ai_engine.summarizer import Summarizer
from backend.utils.pdf_reader import extract_text_from_pdf
from backend.utils.chunking import chunk_text
import tempfile
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="AI Study Companion")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
summarizer = Summarizer()

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/summarize-pdf")
async def summarize_pdf(file: UploadFile = File(...)):
    text = extract_text_from_pdf(file)

    chunks = chunk_text(text)

    chunk_summaries = []
    for chunk in chunks:
        summary = summarizer.summarize_chunk(chunk)
        chunk_summaries.append(summary)

    combined_summary = " ".join(chunk_summaries)

    final_summary = summarizer.summarize_final(combined_summary)

    return {
        "status": "success",
        "chunks_processed": len(chunks),
        "summary": final_summary
    }
