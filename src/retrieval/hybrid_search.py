# Why: vector search understands meaning, while BM25 is good at exact words like invoice, 2FA, or GitHub. Combining both often improves retrieval.
#Why: FAISS and BM25 scores use different numeric ranges, so we normalize them before combining.


from rank_bm25 import BM25Okapi
import numpy as np

from src.embeddings.embedder import embed_texts


def build_bm25(chunks):
    tokenized = [
    f"{chunk['title']} {chunk['content']}".lower().split()
    for chunk in chunks
]

    return BM25Okapi(tokenized)


def normalize_scores(scores):
    scores = np.array(scores, dtype="float32")

    min_score = scores.min()
    max_score = scores.max()

    if max_score == min_score:
        return np.ones_like(scores)

    return (scores - min_score) / (max_score - min_score)


def hybrid_search(
    query,
    index,
    bm25,
    chunks,
    top_k=10,
    vector_weight=0.8,
    bm25_weight=0.2,
):
    # Vector search
    query_vector = np.array(
        embed_texts([query]),
        dtype="float32"
    )

    vector_scores, vector_indices = index.search(
        query_vector,
        len(chunks)
    )

    vector_score_map = {
        idx: score
        for idx, score in zip(
            vector_indices[0],
            vector_scores[0]
        )
        if idx != -1
    }

    # BM25 search
    tokenized_query = query.lower().split()
    bm25_scores = bm25.get_scores(tokenized_query)

    # Put vector scores in same order as chunks
    ordered_vector_scores = np.array(
        [
            vector_score_map.get(i, 0.0)
            for i in range(len(chunks))
        ],
        dtype="float32"
    )

    # Normalize both score types
    vector_normalized = normalize_scores(ordered_vector_scores)
    bm25_normalized = normalize_scores(bm25_scores)

    # Combine scores
    combined_scores = (
        vector_weight * vector_normalized
        + bm25_weight * bm25_normalized
    )

    ranked_indices = np.argsort(combined_scores)[::-1][:top_k]

    results = []

    for idx in ranked_indices:
        results.append({
            "chunk": chunks[idx],
            "score": float(combined_scores[idx]),
            "vector_score": float(vector_normalized[idx]),
            "bm25_score": float(bm25_normalized[idx]),
        })

    return results
    # for idx, vector_score in zip(
    #     vector_indices[0],
    #     vector_scores[0]
    # ):
    #     combined_score = (
    #         float(vector_score) +
    #         float(bm25_scores[idx])
    #     )
       
    #     combined.append({
    #         "score": combined_score,
    #         "chunk": chunks[idx]
    #     })
   

    # combined.sort(
    #     key=lambda x: x["score"],
    #     reverse=True
    # )

    # return combined[:top_k]


