import os
from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
STRUCTURED_DIR = os.path.join(BASE_DIR, 'data', 'structured')
META_RAW = os.path.join(RAW_DIR, 'metadata.json')
META_STRUCT = os.path.join(STRUCTURED_DIR, 'metadata.json')

# Proxy rotation
PROXIES = os.getenv('PROXY_LIST', '').split(',')  # comma-separated in .env

# Cache expiration (seconds)
CACHE_EXPIRE = 30 * 24 * 3600

# LLM Config
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'gemini') 
OPENAI_API_KEY = os.getenv('GEMINI_API_KEY', '')
LLM_MODEL = os.getenv('LLM_MODEL', 'gemini-pro')

# FAISS index paths
INDEX_FILE = os.path.join(BASE_DIR, 'knowledge_base', 'index.faiss')
META_JSON = os.path.join(BASE_DIR, 'knowledge_base', 'meta.json')