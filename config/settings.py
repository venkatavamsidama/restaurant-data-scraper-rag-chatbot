import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
STRUCTURED_DIR = os.path.join(BASE_DIR, 'data', 'structured')
META_FILE = os.path.join(RAW_DIR, 'metadata.json')

# Proxy rotation
PROXIES = os.getenv('PROXY_LIST', '').split(',')  # comma-separated in .env

# Cache expiration (seconds)
CACHE_EXPIRE = 30 * 24 * 3600

# FAISS index paths
INDEX_FILE = os.path.join(BASE_DIR, 'knowledge_base', 'index.faiss')
META_JSON = os.path.join(BASE_DIR, 'knowledge_base', 'meta.json')