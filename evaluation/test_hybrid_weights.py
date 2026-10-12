import sys
import json
from pathlib import Path
 
# This automatically tests all three candidate weight combinations against the same evaluation dataset.This step is about deciding how much we should trust semantic search vs exact keyword search.
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search


DATA_PATH = "data"
QUESTIONS_PATH = "evaluation/questions.json"


def load_questions():
    with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def get_source_path(result):
    chunk = result["chunk"]

    if isinstance(chunk, dict):
        return chunk.get("source_path", "")

    return getattr(chunk, "source_path", "")


def evaluate_weight(
    questions,
    index,
    bm25,
    chunks,
    vector_weight,
    bm25_weight,
):
    recall_at_1 = 0
    recall_at_3 = 0

    for item in questions:
        query = item["question"]
        expected_source = item["expected_source"]

        results = hybrid_search(
            query=query,
            index=index,
            bm25=bm25,
            chunks=chunks,
            top_k=3,
            vector_weight=vector_weight,
            bm25_weight=bm25_weight,
        )

        sources = [
            get_source_path(result)
            for result in results
        ]

        if sources and expected_source in sources[0]:
            recall_at_1 += 1

        if any(expected_source in source for source in sources[:3]):
            recall_at_3 += 1

    total = len(questions)

    return {
        "Recall@1": recall_at_1 / total,
        "Recall@3": recall_at_3 / total,
    }


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

    questions = load_questions()

    weights = [
        (0.5, 0.5),
        (0.6, 0.4),
        (0.7, 0.3),
    ]

    print("\nHybrid Retrieval Weight Evaluation\n")

    for vector_weight, bm25_weight in weights:
        scores = evaluate_weight(
            questions,
            index,
            bm25,
            chunks,
            vector_weight,
            bm25_weight,
        )

        print(
            f"Vector {vector_weight:.1f} / BM25 {bm25_weight:.1f}"
        )
        print(f"Recall@1: {scores['Recall@1']:.2%}")
        print(f"Recall@3: {scores['Recall@3']:.2%}")
        print("-" * 40)


if __name__ == "__main__":
    main()