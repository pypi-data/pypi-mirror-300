# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.load_uncorrelated_accounts_task_task_attributes import LoadUncorrelatedAccountsTaskTaskAttributes

class TestLoadUncorrelatedAccountsTaskTaskAttributes(unittest.TestCase):
    """LoadUncorrelatedAccountsTaskTaskAttributes unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> LoadUncorrelatedAccountsTaskTaskAttributes:
        """Test LoadUncorrelatedAccountsTaskTaskAttributes
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LoadUncorrelatedAccountsTaskTaskAttributes`
        """
        model = LoadUncorrelatedAccountsTaskTaskAttributes()
        if include_optional:
            return LoadUncorrelatedAccountsTaskTaskAttributes(
                qpoc_job_id = '5d303d46-fc51-48cd-9c6d-4e211e3ab63c',
                task_start_delay = sailpoint.v2024.models.task_start_delay.taskStartDelay()
            )
        else:
            return LoadUncorrelatedAccountsTaskTaskAttributes(
        )
        """

    def testLoadUncorrelatedAccountsTaskTaskAttributes(self):
        """Test LoadUncorrelatedAccountsTaskTaskAttributes"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
