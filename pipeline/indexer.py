import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from pipeline.preprocessor import clean_text, chunk_text
from config.settings import STRUCTURED_DIR, INDEX_FILE, META_JSON

MODEL = SentenceTransformer('all-MiniLM-L6-v2')


def build_index():
    passages, meta = [], []
    for fname in os.listdir(STRUCTURED_DIR):
        if not fname.endswith('.json'): continue
        r = json.load(open(os.path.join(STRUCTURED_DIR, fname), encoding='utf8'))
        for item in r.get('menu', []):
            desc = clean_text(item.get('description',''))
            for chunk in chunk_text(desc):
                passages.append(chunk)
                meta.append({**item, 'restaurant': r['name']})

    emb = np.array(MODEL.encode(passages))
    idx = faiss.IndexFlatL2(emb.shape[1])
    idx.add(emb)
    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    faiss.write_index(idx, INDEX_FILE)
    with open(META_JSON, 'w', encoding='utf8') as f:
        json.dump(meta, f, indent=2)

if __name__ == '__main__':
    build_index()