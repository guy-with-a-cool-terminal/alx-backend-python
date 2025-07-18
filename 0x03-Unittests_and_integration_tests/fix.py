from parameterized import parameterized_class  # Add this at the top

# Add this decorator to enable class-level parameterization
@parameterized_class([
    {
        "org_payload": payload[0],
        "repos_payload": payload[1],
        "expected_repos": [repo["name"] for repo in payload[1]],
        "apache2_repos": [
            repo["name"]
            for repo in payload[1]
            if repo.get("license", {}).get("key") == "apache-2.0"
        ],
    }
    for payload in TEST_PAYLOAD
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests for GithubOrgClient"""

    def setUp(self):
        """Patch requests.get using instance attributes from parameterized class"""
        self.get_patcher = patch("requests.get")
        mock_get = self.get_patcher.start()

        def side_effect(url):
            class MockResponse:
                def __init__(self, json_data):
                    self._json = json_data

                def json(self):
                    return self._json

            if url == "https://api.github.com/orgs/google":
                return MockResponse(self.org_payload)  # ✅ now using instance attribute
            elif url == self.org_payload["repos_url"]:
                return MockResponse(self.repos_payload)
            return MockResponse(None)

        mock_get.side_effect = side_effect

    def tearDown(self):
        self.get_patcher.stop()

    def test_public_repos(self):
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)

    def test_public_repos_with_license(self):
        client = GithubOrgClient("google")
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos
        )
