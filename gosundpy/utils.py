import functools
import time

class _timed_cache(object):

    def __init__(self):
        self.reset()

    def set(self, last_call, value):
        self.last_call = last_call
        self.value = value

    def reset(self):
        self.last_call = 0
        self.value = None

def cache_response(hours=0, minutes=0, seconds=0):
    seconds += 60 * 60 * hours + 60 * minutes
    def _rate_limit(fn):
        @functools.wraps(fn)
        def _call(*args, **kwargs):
            now = time.time()
            if now - cache.last_call < seconds:
                return cache.value
            cache.set(now, fn(*args, **kwargs))
            return cache.value
        cache = _timed_cache()
        _call.clear_cache = cache.reset
        return _call
    return _rate_limit
