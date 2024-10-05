# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.completed_approval_pre_approval_trigger_result import CompletedApprovalPreApprovalTriggerResult

class TestCompletedApprovalPreApprovalTriggerResult(unittest.TestCase):
    """CompletedApprovalPreApprovalTriggerResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CompletedApprovalPreApprovalTriggerResult:
        """Test CompletedApprovalPreApprovalTriggerResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CompletedApprovalPreApprovalTriggerResult`
        """
        model = CompletedApprovalPreApprovalTriggerResult()
        if include_optional:
            return CompletedApprovalPreApprovalTriggerResult(
                comment = 'This request was autoapproved by our automated ETS subscriber',
                decision = 'APPROVED',
                reviewer = 'Automated AR Approval',
                var_date = '2022-06-07T19:18:40.748Z'
            )
        else:
            return CompletedApprovalPreApprovalTriggerResult(
        )
        """

    def testCompletedApprovalPreApprovalTriggerResult(self):
        """Test CompletedApprovalPreApprovalTriggerResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
