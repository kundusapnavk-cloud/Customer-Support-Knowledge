#Why: this confirms every chunk now has a semantic vector representation.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts

#Loads all Markdown files from the data/ folder into SupportDocument objects.
documents = load_knowledge_base("data")

#Creates an empty list where all chunks from all documents will be stored.
all_chunks = []

# For each document:
# chunk_by_sections(doc) splits it into smaller chunks.
# extend(...) adds all those chunks into one big all_chunks list.
for doc in documents:
    all_chunks.extend(chunk_by_sections(doc))

#This extracts only the text from each chunk.
texts = [chunk["content"] for chunk in all_chunks]

#This converts each text chunk into a numeric vector.
embeddings = embed_texts(texts)

print("Chunks:", len(all_chunks))
print("Embeddings:", len(embeddings)) #Shows the number of embedding vectors generated.
print("Vector size:", len(embeddings[0])) #Shows how many numbers are inside one embedding vector.