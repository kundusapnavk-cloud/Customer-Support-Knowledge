# # Why: search gives us raw results; this converts them into clean context that we can later send to an LLM.
# from src.retrieval.search import search_index


# def retrieve_context(query, index, chunks, top_k=3):
#     results = search_index(query, index, chunks, top_k)

#     context_parts = []

#     for result in results:
#         chunk = result["chunk"]

#         context_parts.append(
#             f"Title: {chunk['title']}\n"
#             f"Category: {chunk['category']}\n"
#             f"Source: {chunk['source_path']}\n"
#             f"Content:\n{chunk['content']}"
#         )

#     return "\n\n---\n\n".join(context_parts)
#-----------------------------------------------------------------------------------------------------------------------#

# # Why: now retrieval returns both the text for the LLM and the original source files for citations.
# from src.retrieval.search import search_index


# def retrieve_context(query, index, chunks, top_k=3):
#     results = search_index(query, index, chunks, top_k)

#     context_parts = []
#     sources = []

#     for result in results:
#         chunk = result["chunk"]

#         context_parts.append(
#             f"Title: {chunk['title']}\n"
#             f"Category: {chunk['category']}\n"
#             f"Content:\n{chunk['content']}"
#         )

#         sources.append({
#             "title": chunk["title"],
#             "source_path": chunk["source_path"],
#             "score": result["score"]
#         })

#     context = "\n\n---\n\n".join(context_parts)

#     return context, sources

# #--------------------------------------------------------------------------------------------------------------#


# Why: your main RAG pipeline will now use hybrid search + reranking, not the older FAISS-only search.
from src.retrieval.hybrid_search import hybrid_search
from src.retrieval.reranker import rerank_results


def retrieve_context(query, index, bm25, chunks):
    results = hybrid_search(
        query,
        index,
        bm25,
        chunks,
        top_k=10
    )

    results = rerank_results(
        query,
        results,
        top_k=3
    )

    context_parts = []
    sources = []

    for result in results:
        chunk = result["chunk"]

        context_parts.append(
            f"Title: {chunk['title']}\n"
            f"Category: {chunk['category']}\n"
            f"Content:\n{chunk['content']}"
        )

        sources.append({
            "title": chunk["title"],
            "source_path": chunk["source_path"],
            "score": result["rerank_score"]
        })

    context = "\n\n---\n\n".join(context_parts)

    return context, sources, results