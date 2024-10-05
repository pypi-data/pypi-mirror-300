# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.task_definition_summary import TaskDefinitionSummary

class TestTaskDefinitionSummary(unittest.TestCase):
    """TaskDefinitionSummary unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TaskDefinitionSummary:
        """Test TaskDefinitionSummary
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TaskDefinitionSummary`
        """
        model = TaskDefinitionSummary()
        if include_optional:
            return TaskDefinitionSummary(
                id = '2c91808475b4334b0175e1dff64b63c5',
                unique_name = 'Cloud Account Aggregation',
                description = 'Aggregates from the specified application.',
                parent_name = 'Cloud Account Aggregation',
                executor = 'sailpoint.task.ServiceTaskExecutor',
                arguments = { }
            )
        else:
            return TaskDefinitionSummary(
                id = '2c91808475b4334b0175e1dff64b63c5',
                unique_name = 'Cloud Account Aggregation',
                description = 'Aggregates from the specified application.',
                parent_name = 'Cloud Account Aggregation',
                executor = 'sailpoint.task.ServiceTaskExecutor',
                arguments = { },
        )
        """

    def testTaskDefinitionSummary(self):
        """Test TaskDefinitionSummary"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
