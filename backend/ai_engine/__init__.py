import torch
from transformers import pipeline

class Summarizer:
    def __init__(self):
        device = 0 if torch.cuda.is_available() else -1

        self.model = pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=device
        )
