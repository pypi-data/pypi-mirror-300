# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.entitlement_request_config import EntitlementRequestConfig

class TestEntitlementRequestConfig(unittest.TestCase):
    """EntitlementRequestConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> EntitlementRequestConfig:
        """Test EntitlementRequestConfig
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EntitlementRequestConfig`
        """
        model = EntitlementRequestConfig()
        if include_optional:
            return EntitlementRequestConfig(
                access_request_config = sailpoint.v2024.models.entitlement_access_request_config.EntitlementAccessRequestConfig(
                    approval_schemes = [
                        sailpoint.v2024.models.entitlement_approval_scheme.EntitlementApprovalScheme(
                            approver_type = 'GOVERNANCE_GROUP', 
                            approver_id = 'e3eab852-8315-467f-9de7-70eda97f63c8', )
                        ], 
                    request_comment_required = True, 
                    denial_comment_required = False, )
            )
        else:
            return EntitlementRequestConfig(
        )
        """

    def testEntitlementRequestConfig(self):
        """Test EntitlementRequestConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
