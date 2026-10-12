import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search
from src.retrieval.reranker import rerank


DATA_PATH = "data"


SUPPORTED = [
    "Can I get a refund after cancelling?",
    "How do I reset my password?",
    "Where can I download my invoice?",
    "How do I connect Slack?",
]

UNSUPPORTED = [
    "Does TaskFlow offer cryptocurrency payments?",
    "Can TaskFlow book flights for me?",
    "Does TaskFlow support medical records?",
    "Can I use TaskFlow to order food?",
]


def build_pipeline():
    documents = load_knowledge_base(DATA_PATH)

    chunks = []

    for doc in documents:
        chunks.extend(chunk_by_sections(doc))

    texts = [chunk["content"] for chunk in chunks]
    embeddings = embed_texts(texts)

    index = build_faiss_index(embeddings)
    bm25 = build_bm25(chunks)

    return index, bm25, chunks


def test_question(question, index, bm25, chunks):
    results = hybrid_search(
        query=question,
        index=index,
        bm25=bm25,
        chunks=chunks,
        top_k=10,
        vector_weight=0.8,
        bm25_weight=0.2,
    )

    reranked = rerank(
        question,
        results,
        top_k=3,
    )

    top = reranked[0]

    print("\nQuestion:", question)
    print("Top score:", top["rerank_score"])
    print("Source:", top["chunk"]["source_path"])


def main():
    index, bm25, chunks = build_pipeline()

    print("\nSUPPORTED QUESTIONS")

    for question in SUPPORTED:
        test_question(question, index, bm25, chunks)

    print("\nUNSUPPORTED QUESTIONS")

    for question in UNSUPPORTED:
        test_question(question, index, bm25, chunks)


if __name__ == "__main__":
    main()