from django.core.cache import caches
from django.test import TestCase


class YatubeCacheTests(TestCase):
    """The class checks if caching is working."""
    def test_cache_object_exist(self):
        """The function checks that the LocMemCache object exists."""
        self.assertIsNotNone(caches['default'])
