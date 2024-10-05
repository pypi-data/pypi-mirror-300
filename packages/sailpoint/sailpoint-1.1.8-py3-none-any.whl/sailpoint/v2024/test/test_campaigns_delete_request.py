# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.campaigns_delete_request import CampaignsDeleteRequest

class TestCampaignsDeleteRequest(unittest.TestCase):
    """CampaignsDeleteRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CampaignsDeleteRequest:
        """Test CampaignsDeleteRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CampaignsDeleteRequest`
        """
        model = CampaignsDeleteRequest()
        if include_optional:
            return CampaignsDeleteRequest(
                ids = [2c9180887335cee10173490db1776c26, 2c9180836a712436016a7125a90c0021]
            )
        else:
            return CampaignsDeleteRequest(
        )
        """

    def testCampaignsDeleteRequest(self):
        """Test CampaignsDeleteRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
