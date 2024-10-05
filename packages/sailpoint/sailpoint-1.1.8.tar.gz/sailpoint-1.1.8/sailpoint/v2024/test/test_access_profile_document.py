# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.access_profile_document import AccessProfileDocument

class TestAccessProfileDocument(unittest.TestCase):
    """AccessProfileDocument unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessProfileDocument:
        """Test AccessProfileDocument
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessProfileDocument`
        """
        model = AccessProfileDocument()
        if include_optional:
            return AccessProfileDocument(
                id = '2c9180825a6c1adc015a71c9023f0818',
                name = 'Cloud Eng',
                description = 'The admin role',
                created = '2018-06-25T20:22:28.104Z',
                modified = '2018-06-25T20:22:28.104Z',
                synced = '2018-06-25T20:22:33.104Z',
                enabled = True,
                requestable = True,
                request_comments_required = False,
                owner = sailpoint.v2024.models.base_access_all_of_owner.BaseAccess_allOf_owner(
                    type = 'IDENTITY', 
                    id = '2c9180a46faadee4016fb4e018c20639', 
                    name = 'Support', 
                    email = 'cloud-support@sailpoint.com', ),
                type = 'accessprofile',
                source = sailpoint.v2024.models.access_profile_document_all_of_source.AccessProfileDocument_allOf_source(
                    id = 'ff8081815757d4fb0157588f3d9d008f', 
                    name = 'Employees', ),
                entitlements = [
                    sailpoint.v2024.models.base_entitlement.BaseEntitlement(
                        has_permissions = False, 
                        description = 'Cloud engineering', 
                        attribute = 'memberOf', 
                        value = 'CN=Cloud Engineering,DC=sailpoint,DC=COM', 
                        schema = 'group', 
                        privileged = False, 
                        id = '2c918084575812550157589064f33b89', 
                        name = 'CN=Cloud Engineering,DC=sailpoint,DC=COM', )
                    ],
                entitlement_count = 5,
                tags = [TAG_1, TAG_2]
            )
        else:
            return AccessProfileDocument(
                id = '2c9180825a6c1adc015a71c9023f0818',
                name = 'Cloud Eng',
                type = 'accessprofile',
        )
        """

    def testAccessProfileDocument(self):
        """Test AccessProfileDocument"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
