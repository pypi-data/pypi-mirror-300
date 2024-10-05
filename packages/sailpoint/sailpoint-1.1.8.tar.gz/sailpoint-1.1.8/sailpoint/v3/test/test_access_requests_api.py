# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.api.access_requests_api import AccessRequestsApi


class TestAccessRequestsApi(unittest.TestCase):
    """AccessRequestsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = AccessRequestsApi()

    def tearDown(self) -> None:
        pass

    def test_cancel_access_request(self) -> None:
        """Test case for cancel_access_request

        Cancel Access Request
        """
        pass

    def test_create_access_request(self) -> None:
        """Test case for create_access_request

        Submit Access Request
        """
        pass

    def test_get_access_request_config(self) -> None:
        """Test case for get_access_request_config

        Get Access Request Configuration
        """
        pass

    def test_list_access_request_status(self) -> None:
        """Test case for list_access_request_status

        Access Request Status
        """
        pass

    def test_set_access_request_config(self) -> None:
        """Test case for set_access_request_config

        Update Access Request Configuration
        """
        pass


if __name__ == '__main__':
    unittest.main()
