import time
from functools import wraps


def rate_limit(delay: float = 1.0):
    """Decorator to enforce a delay between function calls."""
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            time.sleep(delay)
            return fn(*args, **kwargs)
        return wrapped
    return decorator