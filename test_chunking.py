#We need to confirm every document is actually being converted into chunks before adding embeddings.from src.ingestion.loader import load_knowledge_base
from src.ingestion.loader import load_knowledge_base
from src.chunking.chunker import chunk_document

documents = load_knowledge_base("data")

all_chunks = []

for doc in documents:
    chunks = chunk_document(doc)
    all_chunks.extend(chunks)

# print("Documents:", len(documents))
# print("Chunks:", len(all_chunks))

# print("\nFirst chunk:")
# print(all_chunks[0])
for i, chunk in enumerate(all_chunks[:10], start=1):
    print(f"\nChunk {i}")
    print("Source:", chunk["source_path"])
    print("Title:", chunk["title"])
    print("Category:", chunk["category"])
    print("Content:", chunk["content"][:200])