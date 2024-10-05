# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.identity_list_item import IdentityListItem

class TestIdentityListItem(unittest.TestCase):
    """IdentityListItem unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IdentityListItem:
        """Test IdentityListItem
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `IdentityListItem`
        """
        model = IdentityListItem()
        if include_optional:
            return IdentityListItem(
                id = 'bc693f07e7b645539626c25954c58554',
                display_name = 'Adam Zampa',
                first_name = 'Adam',
                last_name = 'Zampa',
                active = True,
                deleted_date = '2007-03-01T13:00:00.000Z'
            )
        else:
            return IdentityListItem(
        )
        """

    def testIdentityListItem(self):
        """Test IdentityListItem"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
