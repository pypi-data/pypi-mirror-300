# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.requestability_for_role import RequestabilityForRole

class TestRequestabilityForRole(unittest.TestCase):
    """RequestabilityForRole unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RequestabilityForRole:
        """Test RequestabilityForRole
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RequestabilityForRole`
        """
        model = RequestabilityForRole()
        if include_optional:
            return RequestabilityForRole(
                comments_required = True,
                denial_comments_required = True,
                approval_schemes = [
                    sailpoint.beta.models.approval_scheme_for_role.ApprovalSchemeForRole(
                        approver_type = 'GOVERNANCE_GROUP', 
                        approver_id = '46c79819-a69f-49a2-becb-12c971ae66c6', )
                    ]
            )
        else:
            return RequestabilityForRole(
        )
        """

    def testRequestabilityForRole(self):
        """Test RequestabilityForRole"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
