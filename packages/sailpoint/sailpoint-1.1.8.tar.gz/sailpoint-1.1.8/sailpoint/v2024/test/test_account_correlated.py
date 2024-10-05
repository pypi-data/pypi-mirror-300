# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.account_correlated import AccountCorrelated

class TestAccountCorrelated(unittest.TestCase):
    """AccountCorrelated unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccountCorrelated:
        """Test AccountCorrelated
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccountCorrelated`
        """
        model = AccountCorrelated()
        if include_optional:
            return AccountCorrelated(
                identity = sailpoint.v2024.models.account_correlated_identity.AccountCorrelated_identity(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20642', 
                    name = 'Michael Michaels', ),
                source = sailpoint.v2024.models.account_correlated_source.AccountCorrelated_source(
                    type = 'SOURCE', 
                    id = '2c9180835d191a86015d28455b4b232a', 
                    name = 'HR Active Directory', ),
                account = sailpoint.v2024.models.account_correlated_account.AccountCorrelated_account(
                    type = 'ACCOUNT', 
                    id = '98da47c31df444558c211f9b205184f6', 
                    name = 'Brian Mendoza', 
                    native_identity = 'cn=john.doe,ou=users,dc=acme,dc=com', 
                    uuid = '1cb1f07d-3e5a-4431-becd-234fa4306108', ),
                attributes = {sn=doe, givenName=john, memberOf=[cn=g1,ou=groups,dc=acme,dc=com, cn=g2,ou=groups,dc=acme,dc=com, cn=g3,ou=groups,dc=acme,dc=com]},
                entitlement_count = 0
            )
        else:
            return AccountCorrelated(
                identity = sailpoint.v2024.models.account_correlated_identity.AccountCorrelated_identity(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20642', 
                    name = 'Michael Michaels', ),
                source = sailpoint.v2024.models.account_correlated_source.AccountCorrelated_source(
                    type = 'SOURCE', 
                    id = '2c9180835d191a86015d28455b4b232a', 
                    name = 'HR Active Directory', ),
                account = sailpoint.v2024.models.account_correlated_account.AccountCorrelated_account(
                    type = 'ACCOUNT', 
                    id = '98da47c31df444558c211f9b205184f6', 
                    name = 'Brian Mendoza', 
                    native_identity = 'cn=john.doe,ou=users,dc=acme,dc=com', 
                    uuid = '1cb1f07d-3e5a-4431-becd-234fa4306108', ),
                attributes = {sn=doe, givenName=john, memberOf=[cn=g1,ou=groups,dc=acme,dc=com, cn=g2,ou=groups,dc=acme,dc=com, cn=g3,ou=groups,dc=acme,dc=com]},
        )
        """

    def testAccountCorrelated(self):
        """Test AccountCorrelated"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
