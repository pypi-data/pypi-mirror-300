import multiprocessing


class SharedMemory(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._instance._manager = multiprocessing.Manager()
            cls._instance._shared_memory = cls._instance._manager.dict()

        return cls._instance

    def __getitem__(self, item):
        if item not in self._shared_memory:
            raise KeyError(f'Key «{item}» not found in memory')

        return self._shared_memory[item]

    def __setitem__(self, key, value):
        self._shared_memory[key] = value

    def __delitem__(self, key):
        del self._shared_memory[key]

    def __contains__(self, item):
        return item in self._shared_memory

    def __str__(self):
        return str(self._shared_memory)

    def __del__(self):
        self._manager.shutdown()
