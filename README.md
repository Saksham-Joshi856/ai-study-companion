#  AI Study Companion

AI Study Companion is a backend-focused project that provides "AI-powered text and PDF summarization" using modern NLP models.  
It is designed to help students quickly understand large study materials such as notes, articles, and PDFs.

---

##  Features

- Upload and summarize large PDF documents
- Chunk-based processing for long texts
- Hierarchical AI summarization for concise outputs
- FastAPI backend with interactive Swagger UI
- Built using HuggingFace Transformers (BART)

---

##  Tech Stack

- Language: Python
- Backend Framework: FastAPI
- AI Model: `facebook/bart-large-cnn` (Hugging Face Transformers)
- PDF Processing: pypdf
- Server: Uvicorn
- Version Control: Git & GitHub

---

## 🧠 How it Works

1. Extracts text from uploaded PDF
2. Splits text into overlapping chunks
3. Summarizes each chunk using an NLP model
4. Generates a final concise summary

##  Project Structure

