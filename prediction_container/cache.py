import json


class Cache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Cache, cls).__new__(cls)
            cls._instance.cache_data = {}
        return cls._instance

    def _make_key(self, features: dict) -> str:
        return json.dumps(features, sort_keys=True)

    def get(self, features: dict):
        return self.cache_data.get(self._make_key(features))

    def set(self, features: dict, prediction: str):
        self.cache_data[self._make_key(features)] = prediction

    def clear(self):
        print("Cache cleared.")
        self.cache_data = {}