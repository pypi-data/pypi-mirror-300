# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.approval_comment2 import ApprovalComment2

class TestApprovalComment2(unittest.TestCase):
    """ApprovalComment2 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ApprovalComment2:
        """Test ApprovalComment2
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ApprovalComment2`
        """
        model = ApprovalComment2()
        if include_optional:
            return ApprovalComment2(
                comment = 'This request was autoapproved by our automated ETS subscriber.',
                commenter = 'Automated AR Approval',
                var_date = '2018-06-25T20:22:28.104Z'
            )
        else:
            return ApprovalComment2(
        )
        """

    def testApprovalComment2(self):
        """Test ApprovalComment2"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
