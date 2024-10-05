# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.non_employee_approval_item_base import NonEmployeeApprovalItemBase

class TestNonEmployeeApprovalItemBase(unittest.TestCase):
    """NonEmployeeApprovalItemBase unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NonEmployeeApprovalItemBase:
        """Test NonEmployeeApprovalItemBase
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NonEmployeeApprovalItemBase`
        """
        model = NonEmployeeApprovalItemBase()
        if include_optional:
            return NonEmployeeApprovalItemBase(
                id = '2c1e388b-1e55-4b0a-ab5c-897f1204159c',
                approver = sailpoint.beta.models.identity_reference_with_id.IdentityReferenceWithId(
                    type = 'IDENTITY', 
                    id = '5168015d32f890ca15812c9180835d2e', ),
                account_name = 'test.account',
                approval_status = 'APPROVED',
                approval_order = 1,
                comment = '',
                modified = '2019-08-23T18:52:59.162Z',
                created = '2019-08-23T18:40:35.772Z'
            )
        else:
            return NonEmployeeApprovalItemBase(
        )
        """

    def testNonEmployeeApprovalItemBase(self):
        """Test NonEmployeeApprovalItemBase"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
