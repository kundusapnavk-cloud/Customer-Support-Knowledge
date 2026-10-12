import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search


DATA_PATH = "data"
QUESTIONS_PATH = "evaluation/hard_questions.json"


def main():
    documents = load_knowledge_base(DATA_PATH)

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

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    supported_questions = [
        q for q in questions
        if q["supported"]
    ]

    weights = [
        (0.5, 0.5),
        (0.6, 0.4),
        (0.7, 0.3),
        (0.8, 0.2),
    ]

    for vector_weight, bm25_weight in weights:

        recall_1 = 0
        recall_3 = 0
        recall_10 = 0

        for item in supported_questions:

            results = hybrid_search(
                query=item["question"],
                index=index,
                bm25=bm25,
                chunks=chunks,
                top_k=10,
                vector_weight=vector_weight,
                bm25_weight=bm25_weight,
            )

            sources = [
                result["chunk"]["source_path"]
                for result in results
            ]

            expected = item["expected_source"]

            if expected in sources[0]:
                recall_1 += 1

            if any(expected in source for source in sources[:3]):
                recall_3 += 1

            if any(expected in source for source in sources[:10]):
                recall_10 += 1

        total = len(supported_questions)

        print(
            f"\nVector {vector_weight} / BM25 {bm25_weight}"
        )
        print(f"Recall@1: {recall_1}/{total} = {recall_1/total:.2%}")
        print(f"Recall@3: {recall_3}/{total} = {recall_3/total:.2%}")
        print(f"Recall@10: {recall_10}/{total} = {recall_10/total:.2%}")


if __name__ == "__main__":
    main()