# # Why: before answering, we want to check whether retrieval found something strong enough.
# def is_confident(results, threshold=0.5):
#     if not results:
#         return False

#     best_score = results[0].get("rerank_score")

#     if best_score is None:
#         return False

#     return best_score >= threshold

# # Supported → 4.34 to 8.45
# # Unsupported → -5.25 to -1.68
# # Provisional threshold → 1.0

def _get_score(result):
    if "rerank_score" in result:
        return float(result["rerank_score"])

    return float(result.get("score", -999.0))


def _get_source(result):
    chunk = result.get("chunk", {})

    if isinstance(chunk, dict):
        return chunk.get("source_path", "")

    return getattr(chunk, "source_path", "")


def is_confident(
    results,
    strong_threshold=0.5,
    weak_threshold=-5.0,
    min_margin=2.0,
):
    if not results:
        return False

    # Keep only the best score from each document
    best_by_source = {}

    for result in results:
        source = _get_source(result)
        score = _get_score(result)

        if source not in best_by_source or score > best_by_source[source]:
            best_by_source[source] = score

    scores = sorted(
        best_by_source.values(),
        reverse=True,
    )

    if not scores:
        return False

    top_score = scores[0]

    # Strong absolute confidence
    if top_score >= strong_threshold:
        return True

    if len(scores) < 2:
        return False

    second_score = scores[1]
    margin = top_score - second_score

    # Weaker absolute score, but clearly better than other documents
    return (
        top_score >= weak_threshold
        and margin >= min_margin
    )