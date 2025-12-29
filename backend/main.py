from ai_engine import Summarizer

if __name__ == "__main__":
    text = """
    Artificial Intelligence is a branch of computer science
    that aims to create intelligent machines that work and
    react like humans. Some of the activities computers with
    artificial intelligence are designed for include speech
    recognition, learning, planning, and problem solving.
    """

    summarizer = Summarizer()
    print(summarizer.summarize(text))
