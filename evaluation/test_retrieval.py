
# Why: this checks whether the correct document appears in the top 3 retrieved results.import json
import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.hybrid_search import build_bm25, hybrid_search
from src.retrieval.reranker import rerank_results

documents = load_knowledge_base("data")
 
chunks = []

for doc in documents:
    chunks.extend(chunk_by_sections(doc))

texts =[
    f"{chunk['title']}\n{chunk['content']}"
    for chunk in chunks
]

embeddings = embed_texts(texts)
index = build_faiss_index(embeddings)
bm25 = build_bm25(chunks)

with open("evaluation/questions.json", "r") as file:
    questions = json.load(file)


correct = 0

for item in questions:
    results = hybrid_search(
        item["question"],
        index,
        bm25,
        chunks,
        top_k=10
    )

    results = rerank_results(
        item["question"],
        results,
        top_k=3
    )

    sources = [
        result["chunk"]["source_path"]
        for result in results
    ]

    found = any(
        item["expected_source"] in source
        for source in sources
    )

    if found:
        correct += 1

    print()
    print("Question:", item["question"])
    print("Expected:", item["expected_source"])
    print("Found:", found)


print()
print("Accuracy:", correct, "/", len(questions))