from fastapi import FastAPI, UploadFile, File , Form
from fastapi.middleware.cors import CORSMiddleware


from ai_engine.summarizer import Summarizer
from utils.pdf_reader import extract_text_from_pdf
from utils.chunking import chunk_text

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
async def summarize_pdf(
    file: UploadFile = File(...),
    mode: str = Form("default")
):
    text = extract_text_from_pdf(file)
    chunks = chunk_text(text)

    chunk_summaries = []
    for chunk in chunks:
        chunk_summaries.append(
            summarizer.summarize_chunk(chunk)
        )

    final_summary = summarizer.final_summary(chunk_summaries, mode)

    return {
        "mode": mode,
        "summary": final_summary
    }