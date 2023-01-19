#!/usr/bin/env python3
"""
Redis basic.
"""
from typing import Union, Callable, Optional
import redis
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Creates and returns function that increments the count \
        for that key every time the method is called and returns \
        the value returned by the original method"""
    method_key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        self._redis.incr(method_key)
        return method(self, *args, **kwargs)
    return wrapper

class Cache:
    """Cache class to handle redis operations."""
    def __init__(self):
        """stores an instance of the Redis client."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Takes and stores a data argument and returns a string."""
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self,
            key: str, fn: Optional[Callable] = None) -> str:
        """Takes a key string argument and an optional.
        Callable argument named fn. This callable will be used to\
            convertthe data back to a desired format."""
        data = self._redis.get(key)
        return fn(data) if fn is not None else data

    def get_str(self, data: str) -> str:
        """Returns str value of decoded byte """
        return data.decode('utf-8', 'strict')

    def get_int(self, data: str) -> int:
        """Returns int value of decoded byte """
        return int(data)
