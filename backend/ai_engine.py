from transformers import pipeline

class Summarizer:
    def __init__(self):
        self.summarizer = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    def summarize_chunk(self, text):
        return self.summarizer(
            text,
            max_length=120,
            min_length=40,
            do_sample=False,
            truncation=True
        )[0]["summary_text"]

    def summarize_final(self, text):
        return self.summarizer(
            text,
            max_length=150,
            min_length=60,
            do_sample=False,
            truncation=True
        )[0]["summary_text"]
