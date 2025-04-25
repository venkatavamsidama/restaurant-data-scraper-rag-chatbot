import re


def clean_text(text: str) -> str:
    text = re.sub(r'<[^>]+>', '', text)
    return re.sub(r'\s+', ' ', text).strip().lower()


def chunk_text(text: str, max_len: int = 512) -> list[str]:
    words = text.split()
    chunks, curr = [], []
    length = 0
    for w in words:
        if length + len(w) + 1 > max_len:
            chunks.append(' '.join(curr))
            curr, length = [w], len(w)
        else:
            curr.append(w)
            length += len(w) + 1
    if curr:
        chunks.append(' '.join(curr))
    return chunks