# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.account_attributes_changed import AccountAttributesChanged

class TestAccountAttributesChanged(unittest.TestCase):
    """AccountAttributesChanged unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccountAttributesChanged:
        """Test AccountAttributesChanged
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccountAttributesChanged`
        """
        model = AccountAttributesChanged()
        if include_optional:
            return AccountAttributesChanged(
                identity = sailpoint.beta.models.account_attributes_changed_identity.AccountAttributesChanged_identity(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20642', 
                    name = 'Michael Michaels', ),
                source = sailpoint.beta.models.account_attributes_changed_source.AccountAttributesChanged_source(
                    id = '4e4d982dddff4267ab12f0f1e72b5a6d', 
                    type = 'SOURCE', 
                    name = 'Corporate Active Directory', ),
                account = sailpoint.beta.models.account_attributes_changed_account.AccountAttributesChanged_account(
                    id = '52170a74-ca89-11ea-87d0-0242ac130003', 
                    uuid = '1cb1f07d-3e5a-4431-becd-234fa4306108', 
                    name = 'john.doe', 
                    native_identity = 'cn=john.doe,ou=users,dc=acme,dc=com', 
                    type = ACCOUNT, ),
                changes = [
                    sailpoint.beta.models.account_attributes_changed_changes_inner.AccountAttributesChanged_changes_inner(
                        attribute = 'sn', 
                        old_value = doe, 
                        new_value = ryans, )
                    ]
            )
        else:
            return AccountAttributesChanged(
                identity = sailpoint.beta.models.account_attributes_changed_identity.AccountAttributesChanged_identity(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20642', 
                    name = 'Michael Michaels', ),
                source = sailpoint.beta.models.account_attributes_changed_source.AccountAttributesChanged_source(
                    id = '4e4d982dddff4267ab12f0f1e72b5a6d', 
                    type = 'SOURCE', 
                    name = 'Corporate Active Directory', ),
                account = sailpoint.beta.models.account_attributes_changed_account.AccountAttributesChanged_account(
                    id = '52170a74-ca89-11ea-87d0-0242ac130003', 
                    uuid = '1cb1f07d-3e5a-4431-becd-234fa4306108', 
                    name = 'john.doe', 
                    native_identity = 'cn=john.doe,ou=users,dc=acme,dc=com', 
                    type = ACCOUNT, ),
                changes = [
                    sailpoint.beta.models.account_attributes_changed_changes_inner.AccountAttributesChanged_changes_inner(
                        attribute = 'sn', 
                        old_value = doe, 
                        new_value = ryans, )
                    ],
        )
        """

    def testAccountAttributesChanged(self):
        """Test AccountAttributesChanged"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
