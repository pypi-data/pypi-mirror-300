# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.completed_approval_reviewer_comment import CompletedApprovalReviewerComment

class TestCompletedApprovalReviewerComment(unittest.TestCase):
    """CompletedApprovalReviewerComment unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CompletedApprovalReviewerComment:
        """Test CompletedApprovalReviewerComment
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CompletedApprovalReviewerComment`
        """
        model = CompletedApprovalReviewerComment()
        if include_optional:
            return CompletedApprovalReviewerComment(
                comment = 'This is a comment.',
                created = '2017-07-11T18:45:37.098Z',
                author = sailpoint.v3.models.comment_dto_author.CommentDto_author(
                    type = 'IDENTITY', 
                    id = '2c9180847e25f377017e2ae8cae4650b', 
                    name = 'john.doe', )
            )
        else:
            return CompletedApprovalReviewerComment(
        )
        """

    def testCompletedApprovalReviewerComment(self):
        """Test CompletedApprovalReviewerComment"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
