# Why: retrieve broadly first, then keep only the strongest few chunks.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search
from src.retrieval.reranker import rerank_results

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

query = "I cancelled but I was still charged. Can I get my money back?"

results = hybrid_search(
    query,
    index,
    bm25,
    chunks,
    top_k=10
)

reranked = rerank_results(
    query,
    results,
    top_k=3
)

for result in reranked:
    print()
    print("Title:", result["chunk"]["title"])
    print("Rerank score:", result["rerank_score"])
    print("Content:", result["chunk"]["content"])