import json

class Cache:
    _instance = None

    def __init__(self):
        self.cache = {}
        print("Cache instance created")

    @staticmethod
    def _make_hashable_key(features: dict) -> str:
        """Converts a dictionary to a sorted, hashable JSON string."""
        return json.dumps(features, sort_keys=True)

    def try_predict(self, key_dict: dict):
        key = self._make_hashable_key(key_dict)
        return self.cache.get(key)

    def add_to_cache(self, key_dict: dict, value: str):
        key = self._make_hashable_key(key_dict)
        self.cache[key] = value
        print(f"Added to cache: {key} -> {value}")

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Cache()
        return cls._instance
