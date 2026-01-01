from transformers import pipeline

SUMMARY_MODES = {
    "quick": {
        "prompt": """
You are an expert assistant.
Give a VERY short and crisp summary.
Focus only on the core idea.
Avoid details.

Notes:
{text}
""",
        "max_length": 120,
        "min_length": 50
    },

    "study": {
        "prompt": """
You are a study assistant.
Create well-structured study notes.
Focus on key concepts and clarity.
Avoid repetition.

Format:
OVERVIEW:
KEY CONCEPTS:
FINAL TAKEAWAY:

Notes:
{text}
""",
        "max_length": 250,
        "min_length": 120
    },

    "deep": {
        "prompt": """
You are a teacher explaining to a student.
Explain concepts clearly and in detail.
Use simple language and examples.

Notes:
{text}
""",
        "max_length": 400,
        "min_length": 200
    }
}


FINAL_PROMPT = """
You are an expert study assistant.

Using the notes below, produce a high-quality final summary.

Strict rules:
- DO NOT repeat ideas
- Combine similar points into one
- Remove redundancy completely
- Use clear, simple language
- Focus only on important concepts

Format:
OVERVIEW:
<2-3 lines>

KEY CONCEPTS:
- Point 1
- Point 2
- Point 3

FINAL TAKEAWAY:
<1-2 lines>

Notes:
{text}
"""



class Summarizer:
    def __init__(self):
        self.model = pipeline(
            "summarization",
            model="facebook/bart-large-cnn"
        )

    
    def summarize_chunk(self, text: str) -> str:
        if not text or len(text.strip()) < 200:
            return text  # 🔥 skip model call

        return self.model(
            text,
            max_length=80,
            min_length=30,
            do_sample=False,
            truncation=True
        )[0]["summary_text"]


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
        if mode not in SUMMARY_MODES:
            mode = "study"

        unique_summaries = self.remove_duplicates(chunk_summaries)
        combined_text = "\n".join(unique_summaries)

        mode_config = SUMMARY_MODES[mode]
        prompt = mode_config["prompt"].format(text=combined_text)

        result = self.model(
            prompt,
            max_length=mode_config["max_length"],
            min_length=mode_config["min_length"],
            do_sample=False,
            truncation=True
        )

        return result[0]["summary_text"]

