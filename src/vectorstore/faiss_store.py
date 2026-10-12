# FAISS will store the embedding vectors and let us search for the most similar chunks.
import faiss
import numpy as np

def build_faiss_index(embeddings):
    vectors = np.array(embeddings, dtype="float32")

    dimension = vectors.shape[1]
    
# Why: we normalized the embeddings earlier, so IndexFlatIP can be used for cosine-style similarity search.

    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    return index