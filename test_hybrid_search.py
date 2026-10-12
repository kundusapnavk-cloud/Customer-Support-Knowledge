# Why: this lets us test whether exact keywords and semantic meaning work together.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search

documents = load_knowledge_base("data")

chunks = []

for doc in documents:
    chunks.extend(chunk_by_sections(doc))

texts = [
    f"{chunk['title']}\n{chunk['content']}"
    for chunk in chunks
]

embeddings = embed_texts(texts)
index = build_faiss_index(embeddings)

bm25 = build_bm25(chunks)

query = "Where can I download my invoice?"

results = hybrid_search(
    query,
    index,
    bm25,
    chunks
)

for result in results:
    print()
    print("Score:", result["score"])
    print("Title:", result["chunk"]["title"])
    print("Content:", result["chunk"]["content"])