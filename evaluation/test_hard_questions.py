import sys
import json
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search
from src.retrieval.reranker import rerank_results


DATA_PATH = "data"
QUESTIONS_PATH = "evaluation/hard_questions.json"
THRESHOLD = 0.5


def main():
    documents = load_knowledge_base(DATA_PATH)

    chunks = []

    for doc in documents:
        chunks.extend(chunk_by_sections(doc))

    embeddings = embed_texts(
    [
        f"{chunk['title']}\n{chunk['content']}"
        for chunk in chunks
    ]
)

    index = build_faiss_index(embeddings)
    bm25 = build_bm25(chunks)

    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        questions = json.load(f)

    for item in questions:
        results = hybrid_search(
            query=item["question"],
            index=index,
            bm25=bm25,
            chunks=chunks,
            top_k=10,
            vector_weight=0.8,
            bm25_weight=0.2,
        )

        print("\nHYBRID TOP 10:")

        for result in results:
            print(
                round(result["score"], 3),
                result["chunk"]["source_path"]
            )

        reranked = rerank_results(
            item["question"],
            results,
            top_k=3,
        )

        print("\nRERANKED TOP 3:")

        for result in reranked:
            print(
                round(result["rerank_score"], 3),
                result["chunk"]["source_path"]
            )

        top = reranked[0]
        score = top["rerank_score"]
        source = top["chunk"]["source_path"]

        predicted_supported = score >= THRESHOLD

        print("\nQuestion:", item["question"])
        print("Expected supported:", item["supported"])
        print("Predicted supported:", predicted_supported)
        print("Score:", round(score, 3))
        print("Top source:", source)

        if item["expected_source"]:
            print(
                "Correct source:",
                item["expected_source"] in source
            )


if __name__ == "__main__":
    main()