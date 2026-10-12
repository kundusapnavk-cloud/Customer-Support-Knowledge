# Why: this turns your full RAG pipeline into one reusable /chat endpoint.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25
from src.retrieval.retriever import retrieve_context
from src.generation.generator import generate_answer
from src.retrieval.confidence import is_confident

documents = load_knowledge_base("data")

chunks = []

for doc in documents:
    chunks.extend(chunk_by_sections(doc))

texts = [chunk["content"] for chunk in chunks]

embeddings = embed_texts(texts)

index = build_faiss_index(embeddings)

bm25 = build_bm25(chunks)

query = " After I close my TaskFlow account, what happens to my stored data?"

context, sources, results = retrieve_context(
    query,
    index,
    bm25,
    chunks
)
if is_confident(results):
    answer = generate_answer(query, context)
else:
    answer = "I could not find enough reliable information in the support knowledge base."
# answer = generate_answer(query, context)

print("\nQUESTION:")
print(query)

print("\nANSWER:")
print(answer)

print("\nSOURCES:")

for source in sources:
    print(
        f"- {source['title']} "
        f"({source['source_path']})"
    )