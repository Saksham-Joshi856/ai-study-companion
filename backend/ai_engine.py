from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    def summarize(self, text):
        if not text or len(text.strip()) < 50:
            return "Text too short to summarize."

        # BART max input tokens ≈ 1024 → safe char limit ~3500
        max_chars = 3500
        chunks = [text[i:i+max_chars] for i in range(0, len(text), max_chars)]

        summaries = []
        for chunk in chunks:
            out = self.summarizer(
                chunk,
                max_length=120,
                min_length=30,
                do_sample=False
            )
            summaries.append(out[0]["summary_text"])

        return " ".join(summaries)
