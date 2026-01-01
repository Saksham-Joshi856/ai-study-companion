from transformers import pipeline

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
        if not text or len(text.strip()) < 50:
            return ""

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

    
    def final_summary(self, chunk_summaries: list[str]) -> str:
        """
        Takes list of chunk summaries and produces one final summary
        """
        unique_summaries = self.remove_duplicates(chunk_summaries)

        combined_text = "\n".join(unique_summaries)

        prompt = FINAL_PROMPT.format(text=combined_text)

        result = self.model(
            prompt,
            max_length=250,
            min_length=120,
            do_sample=False,
            truncation=True
        )

        return result[0]["summary_text"]
