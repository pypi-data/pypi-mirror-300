# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.access_profile_details import AccessProfileDetails

class TestAccessProfileDetails(unittest.TestCase):
    """AccessProfileDetails unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessProfileDetails:
        """Test AccessProfileDetails
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessProfileDetails`
        """
        model = AccessProfileDetails()
        if include_optional:
            return AccessProfileDetails(
                id = '2c91808a7190d06e01719938fcd20792',
                name = 'Employee-database-read-write',
                description = 'Collection of entitlements to read/write the employee database',
                created = '2021-03-01T22:32:58.104Z',
                modified = '2021-03-02T20:22:28.104Z',
                disabled = True,
                requestable = True,
                protected = False,
                owner_id = '9870808a7190d06e01719938fcd20792',
                source_id = 10360661,
                source_name = 'AD Source',
                app_id = 10360661,
                app_name = 'mail app',
                application_id = 'edcb0951812949d085b60cd8bf35bc78',
                type = 'source',
                entitlements = [2c9180857725c14301772a93bb77242d, c9dc28e148a24d65b3ccb5fb8ca5ddd9],
                entitlement_count = 12,
                segments = [f7b1b8a3-5fed-4fd4-ad29-82014e137e19, 29cb6c06-1da8-43ea-8be4-b3125f248f2a],
                approval_schemes = 'accessProfileOwner',
                revoke_request_approval_schemes = 'accessProfileOwner',
                request_comments_required = True,
                denied_comments_required = True,
                account_selector = sailpoint.v2024.models.access_profile_details_account_selector.AccessProfileDetails_accountSelector(
                    selectors = [
                        sailpoint.v2024.models.selector.selector(
                            application_id = '2c91808874ff91550175097daaec161c"', 
                            account_match_config = sailpoint.v2024.models.selector_account_match_config.selector_accountMatchConfig(
                                match_expression = sailpoint.v2024.models.selector_account_match_config_match_expression.selector_accountMatchConfig_matchExpression(
                                    match_terms = [{name=, value=, op=null, container=true, and=false, children=[{name=businessCategory, value=Service, op=eq, container=false, and=false, children=null}]}], 
                                    and = True, ), ), )
                        ], )
            )
        else:
            return AccessProfileDetails(
        )
        """

    def testAccessProfileDetails(self):
        """Test AccessProfileDetails"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
