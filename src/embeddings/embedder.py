# Why: we are using a local embedding model, so there is no embedding API cost.
from sentence_transformers import SentenceTransformer


model = SentenceTransformer("BAAI/bge-small-en-v1.5")


def embed_texts(texts: list[str]):
    return model.encode(texts, normalize_embeddings=True)