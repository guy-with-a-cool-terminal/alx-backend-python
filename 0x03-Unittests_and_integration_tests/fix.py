from parameterized import parameterized
import unittest
from client import GithubOrgClient

class TestHasLicense(unittest.TestCase):
    """TestCase for GithubOrgClient.has_license"""

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test has_license method directly with real input."""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)
