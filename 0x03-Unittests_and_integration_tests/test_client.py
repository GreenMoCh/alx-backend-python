#!/usr/bin/env python3
"""
    4. Parameterize and patch as decorators
    5. Mocking a property
    6. More patching
    7. Parameterize
    8. Integration test: fixtures
"""

import unittest
import requests
import fixtures
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    """Test case for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test the org method of GithubOrgClient
        """
        client = GithubOrgClient(org_name)
        result = client.org()

        mock_get_json.assert_called_once_with("https://api.github.com/orgs/{}".format(org_name))

        self.assertEqual(result, mock_get_json.return_value)

    def test_public_repos_url(self):
        """
        Test that the test_public_repos_url property returns the expected url
        """
        mock_org_payload = {"repos_url": "https://api.githubcom/orgs/google/repos"}

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = mock_org_payload
            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, mock_org_payload["repos_url"])

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that the public_repos method returns the expected list of repos
        """
        mock_repos_payload = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]

        mock_get_json.return_value = mock_repos_payload
        mock_repos_url = "https://api.github.com/orgs.google/repos"

        with patch('client.GithubOrgClient._public_repos_url', new_callable=Mock) as mock_public_repos_url:
            mock_public_repos_url.return_value = mock_repos_url
            client = GithubOrgClient("google")
            repos = client.public_repos()

            self.assertEqual(repos, ["repo1", "repo2"])

            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(mock_repos_url)
    
    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    @patch('client.GithubOrgClient.public_repos', new_callable=patch.PropretyMock)
    def test_has_license(self, repo, license_key, expected, mock_public_repos):
        """
        Test the GithubOrgClient.has_license method with various inputs and expected outputs
        """
        mock_public_repos.return_value = [repo]

        client = GithubOrgClient("org_name")
        result = client.has_license(repo["name"], license)

        self.assertEqual(result, expected)

@parameterized_class(('org_payload', 'repos_payload', 'apache2_repos'), [
    fixtures.org_payload, fixtures.repos_payload, fixtures.expected_repos, fixtures.apache2_repos
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Setup the class by patching requests.get to return mock payloads"""
        def side_effect(url, *args, **kwargs):
            if 'orgs/' in url:
                return Mock(json=lambda: cls.org_payload)
            elif 'repos' in url:
                return Mock(json=lambda: cls.repos_payload)
            raise ValueError("Unhandled URL")

        cls.get_patcher = patch('requests.get', side_effect=side_effect)
        cls.mocked_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """Stop the patcher"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test th public_repos method for correctness"""
        client = GithubOrgClient("fake_org")
        self.assertEqual(client.public_repos, self.expected_repos)
