#!/usr/bin/env python3
"""
Unit && INtergration tests for GithubOrgClient from client.py
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized
from parameterized import parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """TestCase for GithubOrgClient.org method"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns correct data
        and get_json is called exactly once with the right URL.
        """
        expected_result = {"login": org_name}
        mock_get_json.return_value = expected_result

        client = GithubOrgClient(org_name)
        result = client.org

        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")
        self.assertEqual(result, expected_result)

    def test_public_repos_url(self):
        """
        test _public_repos_url returns a correct url

        """
        test_url = "https://api.github.com/orgs/testorg/repos"
        mock_org_payload = {"repos_url": test_url}

        with patch.object(
                GithubOrgClient, "org", new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_org_payload
            client = GithubOrgClient("testorg")
            result = client._public_repos_url

            self.assertEqual(result, test_url)

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns correct names and
        both get_json and _public_repos_url are used correctly.
        """
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"}
        ]
        mock_get_json.return_value = mock_repos_payload

        with patch.object(
                GithubOrgClient,
                "_public_repos_url", new_callable=PropertyMock) as mock_url:
            mock_url.return_value = "https://api.github.com/orgs/testorg/repos"

            client = GithubOrgClient("testorg")
            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2", "repo3"])
            mock_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test the static method has_license"""
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


"""
Integration tests for GithubOrgClient.public_repos

"""


@parameterized_class([
    {
        "org_payload": payload[0],
        "repos_payload": payload[1],
        "expected_repos": [repo["name"] for repo in payload[1]],
        "apache2_repos": [
            repo["name"]
            for repo in payload[1]
            if isinstance(repo.get("license"), dict) and repo["license"].get("key") == "apache-2.0"
        ]

    }
    for payload in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """ tests with fixtures """
    @classmethod
    def setUpClass(cls):
        cls.get_patcher = patch("requests.get")

        # start patcher
        mock_get = cls.get_patcher.start()

        def side_effect(url):
            class MockResponse:
                def __init__(self, json_data):
                    self._json = json_data

                def json(self):
                    return self._json

            if url == f"https://api.github.com/orgs/google":
                return MockResponse(cls.org_payload)
            elif url == cls.org_payload["repos_url"]:
                return MockResponse(cls.repos_payload)
            else:
                return MockResponse(None)
        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test public_repos returns expected repo names"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        """Test public_repos filters by license correctly"""
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"),
                         self.apache2_repos)
