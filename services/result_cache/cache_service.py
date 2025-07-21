class Cache:

    instance = None
    def __init__(self):
        self.cache = {}

    def try_predict(self, key):
        return self.cache.get(key)

    def add_to_cache(self, key, value):
        self.cache[key] = value


    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = Cache()
        return cls.instance