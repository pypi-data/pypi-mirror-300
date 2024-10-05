# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.app_account_details_source_account import AppAccountDetailsSourceAccount

class TestAppAccountDetailsSourceAccount(unittest.TestCase):
    """AppAccountDetailsSourceAccount unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AppAccountDetailsSourceAccount:
        """Test AppAccountDetailsSourceAccount
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AppAccountDetailsSourceAccount`
        """
        model = AppAccountDetailsSourceAccount()
        if include_optional:
            return AppAccountDetailsSourceAccount(
                id = 'fbf4f72280304f1a8bc808fc2a3bcf7b',
                native_identity = 'CN=Abby Smith,OU=Austin,OU=Americas,OU=Demo,DC=seri,DC=acme,DC=com',
                display_name = 'Abby Smith',
                source_id = '10efa58ea3954883b52bf74f489ce8f9',
                source_display_name = 'ODS-AD-SOURCE'
            )
        else:
            return AppAccountDetailsSourceAccount(
        )
        """

    def testAppAccountDetailsSourceAccount(self):
        """Test AppAccountDetailsSourceAccount"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
