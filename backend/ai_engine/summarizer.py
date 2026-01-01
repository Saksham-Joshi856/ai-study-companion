from transformers import pipeline


class Summarizer:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    def summarize_text(self, text: str) -> str:
        if not text or len(text.strip()) < 50:
            return text

        input_words = len(text.split())

        max_len = min(120, input_words)
        min_len = min(40, max_len - 10) if max_len > 50 else max_len - 5

        result = self.summarizer(
            text,
            max_length=max_len,
            min_length=min_len,
            do_sample=False
        )

        return result[0]["summary_text"]
