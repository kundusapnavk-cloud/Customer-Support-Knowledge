
# Why: FAISS still searches by meaning, but now we can reject results from unrelated categories.
import numpy as np

from src.embeddings.embedder import embed_texts
from src.retrieval.filters import detect_category


def search_index(query, index, chunks, top_k=3):
    query_vector = embed_texts([query])
    query_vector = np.array(query_vector, dtype="float32")

    category = detect_category(query)

    search_k = min(len(chunks), top_k * 5)

    scores, indices = index.search(query_vector, search_k)

    results = []

    for score, idx in zip(scores[0], indices[0]):
        chunk = chunks[idx]

        if category and chunk["category"] != category:
            continue

        results.append({
            "score": float(score),
            "chunk": chunk
        })

        if len(results) == top_k:
            break

    return results


# # Why: this converts the user question into a vector and asks FAISS for the most similar chunks.
# import numpy as np #numpy converts the query embedding into the numeric format FAISS expects.

# from src.embeddings.embedder import embed_texts #embed_texts converts the user's question into an embedding.

# # query → user's question
# # index → FAISS vector index
# # chunks → your stored text chunks
# # top_k=3 → return the 3 most similar chunks
# def search_index(query, index, chunks, top_k=3):
#     query_vector = embed_texts([query]) #Turns the question into a vector.
#     query_vector = np.array(query_vector, dtype="float32") #Converts it to a NumPy array using float32, because FAISS expects that format.

# # This is the actual vector search.
# # FAISS compares the query vector with all stored chunk vectors and returns:
# # scores  → how similar each result is
# # indices → which chunks matched
#     scores, indices = index.search(query_vector, top_k)

#     results = []

# # Pairs each similarity score with the matching chunk position.
#     for score, idx in zip(scores[0], indices[0]):
#         results.append({
#             "score": float(score), #This retrieves the actual chunk and stores it together with its score.
#             "chunk": chunks[idx]
#         })

#     return results
