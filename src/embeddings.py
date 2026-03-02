import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

MODEL_NAME = "all-MiniLM-L6-v2"
DATA_PATH = "data/raw_catalog.json"
INDEX_PATH = "data/faiss.index"
META_PATH = "data/catalog_metadata.npy"

def build_index():
    print("Loading catalog...")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    model = SentenceTransformer(MODEL_NAME)

    texts = [
    f"""
    This is a {item['test_type']} type assessment.
    It is used for hiring and evaluating candidates.
    Title: {item['title']}.
    Description: {item.get('description', '')}
    """
    for item in catalog
    ]

    print("Generating embeddings...")
    embeddings = model.encode(texts, show_progress_bar=True)

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(embeddings))

    faiss.write_index(index, INDEX_PATH)
    np.save(META_PATH, catalog)

    print("FAISS index built and saved.")


if __name__ == "__main__":
    build_index()