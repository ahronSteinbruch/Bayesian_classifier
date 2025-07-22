import unittest

from services.result_cache.cache_service import Cache

class TestCache(unittest.TestCase):
    def setUp(self):
        # Reset the singleton's internal cache before each test
        self.cache = Cache.get_instance()
        self.cache.cache = {}

    def test_add_and_retrieve_prediction(self):
        features = {"x": 1, "y": 2}
        prediction = "class_A"

        self.cache.add_to_cache(features, prediction)
        result = self.cache.try_predict(features)

        self.assertEqual(result, prediction)

    def test_cache_key_consistency(self):
        features1 = {"x": 1, "y": 2}
        features2 = {"y": 2, "x": 1}  # Same keys, different order

        prediction = "class_B"
        self.cache.add_to_cache(features1, prediction)

        # Should retrieve the same value since keys are logically the same
        self.assertEqual(self.cache.try_predict(features2), prediction)

    def test_singleton_instance(self):
        another_cache = Cache.get_instance()
        self.assertIs(self.cache, another_cache)

    def test_try_predict_nonexistent(self):
        self.assertIsNone(self.cache.try_predict({"unknown": 123}))


if __name__ == '__main__':
    unittest.main()
