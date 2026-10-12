# Why: this is your first real retrieval test.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.search import search_index

documents = load_knowledge_base("data")

all_chunks = []

for doc in documents:
    all_chunks.extend(chunk_by_sections(doc))

texts = [chunk["content"] for chunk in all_chunks]

embeddings = embed_texts(texts)
index = build_faiss_index(embeddings)

query = "How can I get my money back?"

results = search_index(query, index, all_chunks)

for i, result in enumerate(results, start=1):
    print(f"\nResult {i}")
    print("Score:", result["score"])
    print("Title:", result["chunk"]["title"])
    print("Category:", result["chunk"]["category"])
    print("Content:", result["chunk"]["content"])