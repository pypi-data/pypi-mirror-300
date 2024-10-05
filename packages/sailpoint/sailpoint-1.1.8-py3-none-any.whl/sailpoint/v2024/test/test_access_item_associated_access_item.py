# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.access_item_associated_access_item import AccessItemAssociatedAccessItem

class TestAccessItemAssociatedAccessItem(unittest.TestCase):
    """AccessItemAssociatedAccessItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessItemAssociatedAccessItem:
        """Test AccessItemAssociatedAccessItem
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessItemAssociatedAccessItem`
        """
        model = AccessItemAssociatedAccessItem()
        if include_optional:
            return AccessItemAssociatedAccessItem(
                access_type = 'role',
                id = '2c918087763e69d901763e72e97f006f',
                name = 'sample',
                source_name = 'Source Name',
                source_id = '2793o32dwd',
                description = 'Role - Workday/Citizenship access',
                display_name = 'sample',
                entitlement_count = '12',
                app_display_name = 'AppName',
                remove_date = '2024-07-01T06:00:00.00Z',
                standalone = True,
                revocable = True,
                native_identity = 'dr.arden.ogahn.d',
                app_role_id = '2c918087763e69d901763e72e97f006f',
                attribute = 'groups',
                value = 'Upward mobility access',
                entitlement_type = 'entitlement',
                privileged = False,
                cloud_governed = True
            )
        else:
            return AccessItemAssociatedAccessItem(
                standalone = True,
                revocable = True,
                privileged = False,
                cloud_governed = True,
        )
        """

    def testAccessItemAssociatedAccessItem(self):
        """Test AccessItemAssociatedAccessItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
