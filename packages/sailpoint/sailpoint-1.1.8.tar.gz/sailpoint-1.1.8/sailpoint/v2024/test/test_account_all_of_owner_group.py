# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.account_all_of_owner_group import AccountAllOfOwnerGroup

class TestAccountAllOfOwnerGroup(unittest.TestCase):
    """AccountAllOfOwnerGroup unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccountAllOfOwnerGroup:
        """Test AccountAllOfOwnerGroup
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccountAllOfOwnerGroup`
        """
        model = AccountAllOfOwnerGroup()
        if include_optional:
            return AccountAllOfOwnerGroup(
                type = 'GOVERNANCE_GROUP',
                id = '8d3e0094e99445de98eef6c75e25jc04',
                name = 'GovGroup AX17Z'
            )
        else:
            return AccountAllOfOwnerGroup(
        )
        """

    def testAccountAllOfOwnerGroup(self):
        """Test AccountAllOfOwnerGroup"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
