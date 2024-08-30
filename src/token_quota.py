import tiktoken # OpenAI's tokenizer

def estimate_tokens(text: str) -> int:
    """
    Estimates the number of tokens required for the given text using OpenAI's tokenizer.
     cl100k_base is a common tokenizer for GPT-3.5-turbo
    """
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)