from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index

documents = load_knowledge_base("data")

all_chunks = []

for doc in documents:
    all_chunks.extend(chunk_by_sections(doc))

texts = [chunk["content"] for chunk in all_chunks]

embeddings = embed_texts(texts)

index = build_faiss_index(embeddings)

print("Chunks:", len(all_chunks))
print("Vectors stored:", index.ntotal)


# Chunks:  ...
# Vectors stored: same number
# A searchable vector index is basically a database optimized for finding text with similar meaning, not just matching exact words.