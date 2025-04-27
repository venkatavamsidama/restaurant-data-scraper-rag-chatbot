import os
import json
import faiss
import numpy as np
import sys

# ⚡ Fix for Streamlit + Torch issue: delete buggy torch.classes early
if "torch.classes" in sys.modules:
    del sys.modules["torch.classes"]

from sentence_transformers import SentenceTransformer
from pipeline.preprocessor import clean_text, chunk_text
from config.settings import STRUCTURED_DIR, INDEX_FILE, META_JSON

MODEL = SentenceTransformer('all-MiniLM-L6-v2')

def build_index():
    passages, meta = [], []
    
    for fname in os.listdir(STRUCTURED_DIR):
        if not fname.endswith('.json') or fname == 'metadata.json':
            continue
        path = os.path.join(STRUCTURED_DIR, fname)
        try:
            with open(path, encoding='utf8') as f:
                r = json.load(f)
            if not isinstance(r, dict):
                print(f"[SKIP] {fname} is not a dict.")
                continue
            if 'menu' not in r or not isinstance(r['menu'], list):
                print(f"[SKIP] {fname} has no valid 'menu'.")
                continue

            for item in r['menu']:
                if not isinstance(item, dict):
                    continue
                desc = clean_text(item.get('description', '') or item.get('desc', '') or '')
                if not desc.strip():
                    continue
                for chunk in chunk_text(desc):
                    passages.append(chunk)
                    meta.append({**item, 'restaurant': r.get('name', fname.replace('.json', ''))})

        except Exception as e:
            print(f"[ERROR] Failed to process {fname}: {e}")

    if not passages:
        print("[WARN] No valid passages found. Skipping index creation.")
        return

    emb = np.array(MODEL.encode(passages))
    idx = faiss.IndexFlatL2(emb.shape[1])
    idx.add(emb)

    os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
    faiss.write_index(idx, INDEX_FILE)

    with open(META_JSON, 'w', encoding='utf8') as f:
        json.dump(meta, f, indent=2)

    print(f"[INFO] Index created at {INDEX_FILE} with {len(passages)} passages.")
    print(f"[INFO] Indexed {len(meta)} chunks from {len(meta)} menu items.")

if __name__ == '__main__':
    build_index()
