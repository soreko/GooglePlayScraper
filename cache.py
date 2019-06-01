

class ICache(object):
    def get(self, key, lock):
        """
        gets a value from cache if exists, otherwise None
        :param key: string
        :param lock: Lock object
        :return: value ot None
        """
        raise NotImplementedError()

    def set(self, key, value, lock):
        """

        :param key: string
        :param value: any
        :param lock: Lock object
        :return: True if succeeded, False otherwise
        """
        raise NotImplementedError()


class SimpleCache(ICache):

    _size = 0
    _cache = {}

    def __init__(self, size=1000):

        self._size = size
        self._cache = {}

    def get(self, key, lock=None):
        value = None

        try:
            if lock:
                lock.acquire(timeout=2)

            value = self._cache.get(key, None)

        finally:
            if lock:
                lock.release()

        return value

    def set(self, key, value, lock=None):

        result = False

        try:
            if lock:
                lock.acquire(timeout=2)

            if len(self._cache) >= self._size:
                self._cache.popitem()

            self._cache[key] = value

            result = True

        finally:
            if lock:
                lock.release()

        return result





