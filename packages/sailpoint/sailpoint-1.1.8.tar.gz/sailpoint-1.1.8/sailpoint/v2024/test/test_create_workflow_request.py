# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.create_workflow_request import CreateWorkflowRequest

class TestCreateWorkflowRequest(unittest.TestCase):
    """CreateWorkflowRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CreateWorkflowRequest:
        """Test CreateWorkflowRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CreateWorkflowRequest`
        """
        model = CreateWorkflowRequest()
        if include_optional:
            return CreateWorkflowRequest(
                name = 'Send Email',
                owner = sailpoint.v2024.models.workflow_body_owner.WorkflowBody_owner(
                    type = 'IDENTITY', 
                    id = '2c91808568c529c60168cca6f90c1313', 
                    name = 'William Wilson', ),
                description = 'Send an email to the identity who's attributes changed.',
                definition = sailpoint.v2024.models.workflow_definition.WorkflowDefinition(
                    start = 'Send Email Test', 
                    steps = {Send Email={actionId=sp:send-email, attributes={body=This is a test, from=sailpoint@sailpoint.com, recipientId.$=$.identity.id, subject=test}, nextStep=success, selectResult=null, type=ACTION}, success={type=success}}, ),
                enabled = False,
                trigger = sailpoint.v2024.models.workflow_trigger.WorkflowTrigger(
                    type = 'EVENT', 
                    display_name = '', 
                    attributes = null, )
            )
        else:
            return CreateWorkflowRequest(
                name = 'Send Email',
                owner = sailpoint.v2024.models.workflow_body_owner.WorkflowBody_owner(
                    type = 'IDENTITY', 
                    id = '2c91808568c529c60168cca6f90c1313', 
                    name = 'William Wilson', ),
        )
        """

    def testCreateWorkflowRequest(self):
        """Test CreateWorkflowRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
