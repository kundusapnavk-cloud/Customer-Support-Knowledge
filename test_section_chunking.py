#Why: this lets you verify that chunks now follow meaningful sections.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections

documents = load_knowledge_base("data")

all_chunks = []

for doc in documents:
    all_chunks.extend(chunk_by_sections(doc))

print("Documents:", len(documents))
print("Chunks:", len(all_chunks))

for i, chunk in enumerate(all_chunks[:5], start=1):
    print(f"\nChunk {i}")
    print("Source:", chunk["source_path"])
    print("Category:", chunk["category"])
    print("Content:", chunk["content"][:300])


