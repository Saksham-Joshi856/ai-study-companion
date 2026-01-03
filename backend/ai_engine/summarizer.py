from transformers import pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np


MODE_CONFIG = {
    "quick": {
        "max_length": 120,
        "min_length": 60
    },
    "study": {
        "max_length": 280,
        "min_length": 150
    },
    "deep": {
        "max_length": 450,
        "min_length": 300
    }
}






class Summarizer:
    def __init__(self):
        self.chunk_model = pipeline(
            "summarization",
            model="sshleifer/distilbart-cnn-12-6",  # 🚀 2x faster
            device=-1
        )

        self.final_model = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1
        )

    
    
    def summarize_chunks(self, chunks: list[str]) -> list[str]:
        selected = []

        for chunk in chunks[:15]:
            sentences = [s.strip() for s in chunk.split(". ") if len(s.split()) > 6]

            if len(sentences) <= 3:
                selected.extend(sentences)
                continue

            vectorizer = TfidfVectorizer(stop_words="english")
            X = vectorizer.fit_transform(sentences)

            scores = np.asarray(X.sum(axis=1)).ravel()
            top_ids = scores.argsort()[-3:]

            for i in sorted(top_ids):
                selected.append(sentences[i])

        return selected

    def enforce_structure(self, text: str) -> str:
        overview = []
        key_concepts = []
        takeaway = []

        for line in text.split("\n"):
            line = line.strip()

            if not line:
                continue
            if line.upper().startswith("OVERVIEW"):
                continue
            elif line.upper().startswith("KEY"):
                continue
            elif line.upper().startswith("FINAL"):
                continue

            if len(overview) < 2:
                overview.append(line)
            elif len(key_concepts) < 6:
                key_concepts.append(line)
            else:
                takeaway.append(line)

        if not key_concepts:
            key_concepts = self.bulletize(text).split("\n")

        return f"""OVERVIEW:
    {' '.join(overview)}

    KEY CONCEPTS:
    {chr(10).join(f"- {c.lstrip('- ').strip()}" for c in key_concepts)}

    FINAL TAKEAWAY:
    {' '.join(takeaway[:2])}
    """.strip()


    def bulletize(self, text: str) -> str:
        sentences = [s.strip() for s in text.split(".") if len(s.split()) > 6]

        bullets = []
        for s in sentences[:6]:
            bullets.append(f"- {s}.")

        return "\n".join(bullets)



    def clean_language(self, text: str) -> str:
        junk_phrases = [
            "this summary",
            "in conclusion",
            "overall",
            "it is important to note",
            "the document discusses"
        ]

        for phrase in junk_phrases:
            text = text.replace(phrase, "")

        return text.strip()


    def remove_duplicates(self, summaries: list[str]) -> list[str]:
        unique = []
        seen = set()

        for s in summaries:
            key = s.lower().strip()
            if key not in seen:
                seen.add(key)
                unique.append(s)

        return unique

    
    def final_summary(self, chunk_summaries: list[str], mode: str = "study") -> str:
        if not chunk_summaries:
            return "No content found to summarize."

        if mode not in MODE_CONFIG:
            mode = "study"

        # Deduplicate + clean
        seen = set()
        cleaned = []
        for s in chunk_summaries:
            s = s.strip()
            if s and s.lower() not in seen:
                cleaned.append(s)
                seen.add(s.lower())

        cleaned = cleaned[:8]
        
        combined_text = " ".join(cleaned)

        cfg = MODE_CONFIG[mode]

        result = self.final_model(
            combined_text,
            max_length=cfg["max_length"],
            min_length=cfg["min_length"],
            do_sample=False,
            truncation=True
        )

        summary = result[0]["summary_text"]

        # 🔥 Post-processing (THIS is where quality comes from)
        summary = self.clean_language(summary)
        if mode == "study":
            summary = self.enforce_structure(summary)

        return summary






    def rank_chunks(self, summaries: list[str]) -> list[str]:
        """
        Rank summaries based on information density.
        Longer + richer summaries are usually more important.
        """
        return sorted(
            summaries,
            key=lambda x: len(x.split()),
            reverse=True
        )

    