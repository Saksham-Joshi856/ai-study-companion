from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.model = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=-1  # CPU
        )

    def summarize_chunk(self, text: str) -> str:
        if len(text.strip()) < 50:
            return ""

        result = self.model(
            text,
            max_length=130,
            min_length=40,
            do_sample=False,
            truncation=True
        )

        return result[0]["summary_text"]
