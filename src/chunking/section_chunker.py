import re
from src.ingestion.models import SupportDocument

# #instead of cutting every 500 characters, this splits on Markdown section headings like ## Steps or ## Important.

# def chunk_by_sections(doc: SupportDocument) -> list[dict]:
#     parts = re.split(r'(?=^##\s)', doc.content, flags=re.MULTILINE)

#     chunks = []

#     for part in parts:
#         text = part.strip()

#         if not text:
#             continue

#         chunks.append({
#             "content": text,
#             "title": doc.title,
#             "category": doc.category,
#             "product": doc.product,
#             "plan": doc.plan,
#             "source_type": doc.source_type,
#             "source_path": doc.source_path,
#         })

#     return chunks

#----------------------------------------------------------------------------------------------------------------------------#
#Why: now long sections are split by sentences instead of being cut randomly.

def split_long_text(text: str, max_chars: int = 700) -> list[str]:
    if len(text) <= max_chars:
        return [text]

    sentences = re.split(r'(?<=[.!?])\s+', text)

    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current += (" " if current else "") + sentence
        else:
            if current:
                chunks.append(current.strip())
            current = sentence

    if current:
        chunks.append(current.strip())

    return chunks


def chunk_by_sections(doc: SupportDocument) -> list[dict]:
    sections = re.split(r'(?=^##\s)', doc.content, flags=re.MULTILINE)

    chunks = []

    for section in sections:
        section = section.strip()

        if not section:
            continue

        smaller_chunks = split_long_text(section)

        for text in smaller_chunks:
            chunks.append({
                "content": text,
                "title": doc.title,
                "category": doc.category,
                "product": doc.product,
                "plan": doc.plan,
                "source_type": doc.source_type,
                "source_path": doc.source_path,
            })

    return chunks