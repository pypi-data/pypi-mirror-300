# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.account_attributes_changed_account import AccountAttributesChangedAccount

class TestAccountAttributesChangedAccount(unittest.TestCase):
    """AccountAttributesChangedAccount unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccountAttributesChangedAccount:
        """Test AccountAttributesChangedAccount
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccountAttributesChangedAccount`
        """
        model = AccountAttributesChangedAccount()
        if include_optional:
            return AccountAttributesChangedAccount(
                id = '52170a74-ca89-11ea-87d0-0242ac130003',
                uuid = '1cb1f07d-3e5a-4431-becd-234fa4306108',
                name = 'john.doe',
                native_identity = 'cn=john.doe,ou=users,dc=acme,dc=com',
                type = ACCOUNT
            )
        else:
            return AccountAttributesChangedAccount(
                id = '52170a74-ca89-11ea-87d0-0242ac130003',
                uuid = '1cb1f07d-3e5a-4431-becd-234fa4306108',
                name = 'john.doe',
                native_identity = 'cn=john.doe,ou=users,dc=acme,dc=com',
                type = ACCOUNT,
        )
        """

    def testAccountAttributesChangedAccount(self):
        """Test AccountAttributesChangedAccount"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
