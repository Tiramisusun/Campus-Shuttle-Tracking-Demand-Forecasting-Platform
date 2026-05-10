import json
import functools
from ..extensions import redis_client
from ..config import Config

def cache(key_prefix, ttl=Config.CACHE_TTL):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            cache_key = f"{key_prefix}:{':'.join(str(a) for a in args)}"
            cached = redis_client.get(cache_key)
            if cached:
                return json.loads(cached)
            result = fn(*args, **kwargs)
            redis_client.setex(cache_key, ttl, json.dumps(result))
            return result
        return wrapper
    return decorator


class DistributedLock:
    def __init__(self, key, timeout=10):
        self.key = f"lock:{key}"
        self.timeout = timeout

    def __enter__(self):
        acquired = redis_client.set(self.key, "1", nx=True, ex=self.timeout)
        if not acquired:
            raise RuntimeError(f"Could not acquire lock for {self.key}")
        return self

    def __exit__(self, *args):
        redis_client.delete(self.key)
