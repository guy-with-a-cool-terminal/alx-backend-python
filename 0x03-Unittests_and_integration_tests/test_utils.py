#!/usr/bin/env python3
"""

unit tests for the access_nested_map function

"""
import unittest
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch, Mock


class TestAccessNestedMap(unittest.TestCase):
    ''' parameterized testcase for the function '''
    @parameterized.expand([
        # structure: each tuple->>>nested_map,path,expected_result
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """

        test access_nested_map returns correct value for valid nested paths

        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Tests that access_nested_map raises keyerror when path is invalid

        """
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)
        self.assertEqual(str(cm.exception), f"'{path[-1]}'")


class TestGetJson(unittest.TestCase):
    """ Tests get_json function """
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """

        test the function returns correct payload from a mocked response

        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)

            # check our mocked get() was called with the url
            mock_get.assert_called_once_with(test_url)

            # check get_json returns what we expect
            self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """ Tests the memoize decorator  """

    def test_memoize(self):
        """

        Test that a method wrapped with the decorator is called only once

        """
        class TestClass:
            def a_method(self) -> int:
                return 42

            @memoize
            def a_property(self) -> int:
                return self.a_method()

        with patch.object(
                TestClass, 'a_method', return_value=42) as mock_method:
            test_obj = TestClass()

            # access memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # check value is correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # ensure we called the method once
            mock_method.assert_called_once()
