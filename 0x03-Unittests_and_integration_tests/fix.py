from unittest.mock import patch
from parameterized import parameterized
import unittest
from client import GithubOrgClient

class TestHasLicense(unittest.TestCase):
    """TestCase for GithubOrgClient.has_license"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    @patch("client.access_nested_map")  # Correct path based on import
    def test_has_license(self, repo, license_key, expected, mock_access):
        """Test the has_license static method with patched access_nested_map."""
        mock_access.return_value = repo["license"]["key"]
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
