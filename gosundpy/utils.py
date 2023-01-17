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

    class _cache_response(object):

        def __init__(self, fn):
            # wraps class instance methods only
            self.fn = fn
            self.cache_key = f'_{fn.__name__}_cache'

        def call(self, instance, *args, **kwargs):
            now = time.time()
            cache = getattr(instance, self.cache_key)
            if now - cache.last_call < seconds:
                return cache.value
            cache.set(now, self.fn(instance, *args, **kwargs))
            return cache.value

        def __get__(self, instance, owner):
            @functools.wraps(self.fn)
            def _call(*args, **kwargs):
                return self.call(instance, *args, **kwargs)
            if not hasattr(instance, self.cache_key):
                setattr(instance, self.cache_key, _timed_cache())
            _call.clear_cache = getattr(instance, self.cache_key).reset
            return _call

    return _cache_response
