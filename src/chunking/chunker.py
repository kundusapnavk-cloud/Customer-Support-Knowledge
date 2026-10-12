from src.ingestion.models import SupportDocument


def chunk_document(doc: SupportDocument, chunk_size: int = 500) -> list[dict]:
    text = doc.content
    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk_text = text[start:start + chunk_size].strip()

        if not chunk_text:
            continue

        chunks.append({
            "content": chunk_text,
            "title": doc.title,
            "category": doc.category,
            "product": doc.product,
            "plan": doc.plan,
            "source_type": doc.source_type,
            "source_path": doc.source_path,
        })

    return chunks