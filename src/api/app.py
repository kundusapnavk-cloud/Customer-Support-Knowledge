from fastapi import FastAPI
from pydantic import BaseModel

from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25
from src.retrieval.retriever import retrieve_context
from src.retrieval.confidence import is_confident
from src.generation.generator import generate_answer
from src.conversation.context import build_contextual_query


app = FastAPI(
    title="TaskFlow Support RAG",
    version="1.0.0",
)


class ChatRequest(BaseModel):
    question: str
    history: list[dict] = []


# Build RAG pipeline once when API starts
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


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": "TaskFlow Support RAG"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    retrieval_query = build_contextual_query(
        request.question,
        request.history,
    )

    context, sources, results = retrieve_context(
        retrieval_query,
        index,
        bm25,
        chunks,
    )

    if is_confident(results):
        answer = generate_answer(
            retrieval_query,
            context,
        )
    else:
        answer = (
            "I could not find enough reliable information "
            "in the support knowledge base."
        )

    # Remove duplicate sources
    unique_sources = []
    seen = set()

    for source in sources:
        path = source["source_path"]

        if path not in seen:
            seen.add(path)
            unique_sources.append(source)

    return {
        "answer": answer,
        "sources": unique_sources,
    }