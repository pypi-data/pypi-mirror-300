# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.access_item_role_response import AccessItemRoleResponse

class TestAccessItemRoleResponse(unittest.TestCase):
    """AccessItemRoleResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessItemRoleResponse:
        """Test AccessItemRoleResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessItemRoleResponse`
        """
        model = AccessItemRoleResponse()
        if include_optional:
            return AccessItemRoleResponse(
                access_type = 'role',
                id = '2c918087763e69d901763e72e97f006f',
                display_name = 'sample',
                description = 'Role - Workday/Citizenship access',
                source_name = 'Source Name',
                remove_date = '2024-07-01T06:00:00.00Z',
                revocable = True
            )
        else:
            return AccessItemRoleResponse(
                revocable = True,
        )
        """

    def testAccessItemRoleResponse(self):
        """Test AccessItemRoleResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
