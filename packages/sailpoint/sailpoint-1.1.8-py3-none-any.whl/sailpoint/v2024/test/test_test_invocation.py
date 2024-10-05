# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.test_invocation import TestInvocation

class TestTestInvocation(unittest.TestCase):
    """TestInvocation unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TestInvocation:
        """Test TestInvocation
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TestInvocation`
        """
        model = TestInvocation()
        if include_optional:
            return TestInvocation(
                trigger_id = 'idn:access-request-post-approval',
                input = {identityId=201327fda1c44704ac01181e963d463c},
                content_json = {workflowId=1234},
                subscription_ids = [0f11f2a4-7c94-4bf3-a2bd-742580fe3bde]
            )
        else:
            return TestInvocation(
                trigger_id = 'idn:access-request-post-approval',
                content_json = {workflowId=1234},
        )
        """

    def testTestInvocation(self):
        """Test TestInvocation"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
