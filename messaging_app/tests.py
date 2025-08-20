import pytest
from django.test import TestCase

class SimpleTest(TestCase):
    def test_example(self):
        """Simple test to verify pipeline works"""
        assert 1 + 1 == 2
        
    def test_django_setup(self):
        """Test Django is properly configured"""
        from django.conf import settings
        assert settings.DEBUG is not None