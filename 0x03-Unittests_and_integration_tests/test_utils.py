#!/usr/bin/env python3
"""
    0. Parameterize a unit test
    1. Parameterize a unit test
    2. Mock HTTP calls
    3. Parameterize and patch
"""

import unittest
from unittest.mock import patch, Mock
from parameterized import parameterized
from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """ Test case for access_nested_map function """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected_result):
        """
        Tests access_nested_map function wih various inputs
        """
        self.assertEqual(access_nested_map(nested_map, path), expected_result)

    @parameterized.expand([
        ({}, ("a",), "Key 'a' not found in the nested map"),
        ({"a": 1}, ("a", "b"), "Key 'b' not found in the nested map under 'a'")
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple, expected_exception_msg: str):
        """
        Tests that a KeyError is raised with the expected message
        """
        with self.assertRaises(KeyError) as context:
            access_nested_map(nested_map, path)

        self.assertEqual(str(context.exception), expected_exception_msg)


class TestgetJson(unittest.TestCase):
    """ Test case for get_json function """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    @patch('utils.requests.get')
    def test_get_json(self, test_url, test_payload, mock_get):
        """
        Tests that get_json returns the expected result
        """
        mock_get.return_value = Mock()
        mock_get.return_value.json.return_value = test_payload

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)

        self.assertEqual(result, test_payload)


class TestMemorize(unittest.TestCase):
    """ Test case for the memorize decorator """

    class TestClass:

        def a_method(self):
            return 42

        @memoize
        def a_property(self):
            return self.a_method()

    @patch.object(TestClass, 'a_method')
    def test_memorize(self, mock_a_method):
        """
        Test the memorize decorator
        """
        test_instance = self.TestClass()

        result1 = test_instance.a_property()
        result2 = test_instance.a_property()

        mock_a_method.assert_called_once()

        self.assertEqual(result1, 42)
        self.assertEqual(result2, 42)
        