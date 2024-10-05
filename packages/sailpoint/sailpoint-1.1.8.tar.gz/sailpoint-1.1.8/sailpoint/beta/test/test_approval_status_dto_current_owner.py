# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.approval_status_dto_current_owner import ApprovalStatusDtoCurrentOwner

class TestApprovalStatusDtoCurrentOwner(unittest.TestCase):
    """ApprovalStatusDtoCurrentOwner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ApprovalStatusDtoCurrentOwner:
        """Test ApprovalStatusDtoCurrentOwner
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ApprovalStatusDtoCurrentOwner`
        """
        model = ApprovalStatusDtoCurrentOwner()
        if include_optional:
            return ApprovalStatusDtoCurrentOwner(
                type = 'IDENTITY',
                id = '2c3780a46faadee4016fb4e018c20652',
                name = 'Allen Albertson'
            )
        else:
            return ApprovalStatusDtoCurrentOwner(
        )
        """

    def testApprovalStatusDtoCurrentOwner(self):
        """Test ApprovalStatusDtoCurrentOwner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
