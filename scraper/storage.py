import json
import os
from diskcache import Cache
from config.settings import RAW_DIR, META_RAW, CACHE_EXPIRE

cache = Cache(os.path.join(RAW_DIR, '.cache'))


def save_page(filename: str, html: str) -> None:
    path = os.path.join(RAW_DIR, filename)
    os.makedirs(RAW_DIR, exist_ok=True)
    with open(path, 'w', encoding='utf8') as f:
        f.write(html)
    cache.set(path, True, expire=CACHE_EXPIRE)


def append_raw_metadata(entry: dict) -> None:
    os.makedirs(os.path.dirname(META_RAW), exist_ok=True)
    with open(META_RAW, 'a+', encoding='utf8') as f:
        f.write(json.dumps(entry) + '\n')