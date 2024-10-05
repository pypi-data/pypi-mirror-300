# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.review_reassign import ReviewReassign

class TestReviewReassign(unittest.TestCase):
    """ReviewReassign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ReviewReassign:
        """Test ReviewReassign
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ReviewReassign`
        """
        model = ReviewReassign()
        if include_optional:
            return ReviewReassign(
                reassign = [
                    sailpoint.beta.models.reassign_reference.ReassignReference(
                        id = 'ef38f94347e94562b5bb8424a56397d8', 
                        type = 'ITEM', )
                    ],
                reassign_to = 'ef38f94347e94562b5bb8424a56397d8',
                reason = 'reassigned for some reason'
            )
        else:
            return ReviewReassign(
                reassign = [
                    sailpoint.beta.models.reassign_reference.ReassignReference(
                        id = 'ef38f94347e94562b5bb8424a56397d8', 
                        type = 'ITEM', )
                    ],
                reassign_to = 'ef38f94347e94562b5bb8424a56397d8',
                reason = 'reassigned for some reason',
        )
        """

    def testReviewReassign(self):
        """Test ReviewReassign"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
