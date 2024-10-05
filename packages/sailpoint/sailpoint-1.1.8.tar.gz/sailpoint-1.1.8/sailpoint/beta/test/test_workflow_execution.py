# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.workflow_execution import WorkflowExecution

class TestWorkflowExecution(unittest.TestCase):
    """WorkflowExecution unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WorkflowExecution:
        """Test WorkflowExecution
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WorkflowExecution`
        """
        model = WorkflowExecution()
        if include_optional:
            return WorkflowExecution(
                id = 'b393f4e2-4785-4d7f-ab27-3a6b8ded4c81',
                workflow_id = 'd201c5d9-d37b-4a2f-af14-66414f39d568',
                request_id = '41e12a74fa7b4a6a98ae47887b64acdb',
                start_time = '2022-02-07T20:13:29.356648026Z',
                close_time = '2022-02-07T20:13:31.682410165Z',
                status = 'Completed'
            )
        else:
            return WorkflowExecution(
        )
        """

    def testWorkflowExecution(self):
        """Test WorkflowExecution"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
