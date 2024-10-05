# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.approval_status_dto import ApprovalStatusDto

class TestApprovalStatusDto(unittest.TestCase):
    """ApprovalStatusDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ApprovalStatusDto:
        """Test ApprovalStatusDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ApprovalStatusDto`
        """
        model = ApprovalStatusDto()
        if include_optional:
            return ApprovalStatusDto(
                forwarded = False,
                original_owner = sailpoint.beta.models.approval_status_dto_original_owner.ApprovalStatusDto_originalOwner(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20642', 
                    name = 'Michael Michaels', ),
                current_owner = None,
                modified = '2019-08-23T18:52:57.398Z',
                status = 'PENDING',
                scheme = 'MANAGER',
                error_messages = [
                    sailpoint.beta.models.error_message_dto.ErrorMessageDto(
                        locale = 'en-US', 
                        locale_origin = 'DEFAULT', 
                        text = 'The request was syntactically correct but its content is semantically invalid.', )
                    ],
                comment = 'I approve this request',
                remove_date = '2020-07-11T00:00Z'
            )
        else:
            return ApprovalStatusDto(
        )
        """

    def testApprovalStatusDto(self):
        """Test ApprovalStatusDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
