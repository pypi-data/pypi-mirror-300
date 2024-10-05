# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.iai_recommendations_api import IAIRecommendationsApi


class TestIAIRecommendationsApi(unittest.TestCase):
    """IAIRecommendationsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = IAIRecommendationsApi()

    def tearDown(self) -> None:
        pass

    def test_get_recommendations(self) -> None:
        """Test case for get_recommendations

        Returns a Recommendation Based on Object
        """
        pass

    def test_get_recommendations_config(self) -> None:
        """Test case for get_recommendations_config

        Get certification recommendation config values
        """
        pass

    def test_update_recommendations_config(self) -> None:
        """Test case for update_recommendations_config

        Update certification recommendation config values
        """
        pass


if __name__ == '__main__':
    unittest.main()
