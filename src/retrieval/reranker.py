# Why: hybrid search finds likely candidates; the reranker compares the query and each chunk more carefully and reorders them.
from sentence_transformers import CrossEncoder


model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank_results(query, results, top_k=3):
    pairs = [
        [query, result["chunk"]["content"]]
        for result in results
    ]

    scores = model.predict(pairs)

    for result, score in zip(results, scores):
        result["rerank_score"] = float(score)

    results.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return results[:top_k]