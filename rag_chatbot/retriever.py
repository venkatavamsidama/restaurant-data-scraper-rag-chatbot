import json
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Define file paths
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
INDEX_FILE = os.path.join(BASE_DIR, 'knowledge_base', 'index.faiss')
META_JSON = os.path.join(BASE_DIR, 'knowledge_base', 'meta.json')

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

class Retriever:
    def __init__(self):
        # Ensure the index file exists
        if not os.path.exists(INDEX_FILE):
            raise FileNotFoundError(f"Index file not found at {INDEX_FILE}. Please generate the index first.")
        
        # Ensure the metadata file exists
        if not os.path.exists(META_JSON):
            raise FileNotFoundError(f"Metadata file not found at {META_JSON}. Please provide the metadata file.")
        
        try:
            # Read the index from the file
            self.index = faiss.read_index(INDEX_FILE)
        except Exception as e:
            raise RuntimeError(f"Failed to read the index from {INDEX_FILE}: {str(e)}")
        
        try:
            # Load the metadata from the JSON file
            with open(META_JSON, encoding='utf8') as f:
                self.metadata = json.load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to read the metadata from {META_JSON}: {str(e)}")

    def retrieve(self, query: str, top_k: int = 5):
        # Encode the query into embeddings
        q_emb = np.array(MODEL.encode([query]))
        
        # Perform the search on the index
        _, idxs = self.index.search(q_emb, top_k)
        
        # Return the corresponding metadata for the top K results
        return [self.metadata[i] for i in idxs[0]]

