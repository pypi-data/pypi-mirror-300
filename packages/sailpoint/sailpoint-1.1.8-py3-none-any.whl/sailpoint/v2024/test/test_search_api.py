# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.api.search_api import SearchApi


class TestSearchApi(unittest.TestCase):
    """SearchApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SearchApi()

    def tearDown(self) -> None:
        pass

    def test_search_aggregate(self) -> None:
        """Test case for search_aggregate

        Perform a Search Query Aggregation
        """
        pass

    def test_search_count(self) -> None:
        """Test case for search_count

        Count Documents Satisfying a Query
        """
        pass

    def test_search_get(self) -> None:
        """Test case for search_get

        Get a Document by ID
        """
        pass

    def test_search_post(self) -> None:
        """Test case for search_post

        Perform Search
        """
        pass


if __name__ == '__main__':
    unittest.main()
