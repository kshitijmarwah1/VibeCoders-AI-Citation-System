def merge_texts(texts: list[str]) -> str:
    return "\n\n".join(t for t in texts if t.strip())
