# This code is testing the full retrieval pipeline end-to-end.
from src.ingestion.loader import load_knowledge_base
from src.chunking.section_chunker import chunk_by_sections
from src.embeddings.embedder import embed_texts
from src.vectorstore.faiss_store import build_faiss_index
from src.retrieval.retriever import retrieve_context

#Loads all support Markdown files.
documents = load_knowledge_base("data") 

#Splits every document into smaller chunks and stores them in one list.
all_chunks = []

for doc in documents:
    all_chunks.extend(chunk_by_sections(doc))

#Extracts only the chunk text.
texts = [chunk["content"] for chunk in all_chunks]

#Converts every chunk into an embedding vector.
embeddings = embed_texts(texts)
#Stores those vectors inside a FAISS index so they can be searched.
index = build_faiss_index(embeddings)

query = "How do I stop my subscription and get a refund?"

context = retrieve_context(query, index, all_chunks)

print(context)