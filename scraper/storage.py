import json
import os
from diskcache import Cache
from config.settings import RAW_DIR, META_FILE, CACHE_EXPIRE

cache = Cache(os.path.join(RAW_DIR, '.cache'))


def save_page(filename: str, html: str) -> None:
    path = os.path.join(RAW_DIR, filename)
    with open(path, 'w', encoding='utf8') as f:
        f.write(html)
    cache.set(path, True, expire=CACHE_EXPIRE)


def append_metadata(entry: dict) -> None:
    os.makedirs(os.path.dirname(META_FILE), exist_ok=True)
    with open(META_FILE, 'a+', encoding='utf8') as f:
        f.write(json.dumps(entry) + '\n')