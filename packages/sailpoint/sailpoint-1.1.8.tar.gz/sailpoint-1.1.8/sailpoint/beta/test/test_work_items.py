# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.work_items import WorkItems

class TestWorkItems(unittest.TestCase):
    """WorkItems unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> WorkItems:
        """Test WorkItems
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `WorkItems`
        """
        model = WorkItems()
        if include_optional:
            return WorkItems(
                id = '2c9180835d2e5168015d32f890ca1581',
                requester_id = '2c9180835d2e5168015d32f890ca1581',
                requester_display_name = 'John Smith',
                owner_id = '2c9180835d2e5168015d32f890ca1581',
                owner_name = 'Jason Smith',
                created = '2017-07-11T18:45:37.098Z',
                modified = '2018-06-25T20:22:28.104Z',
                description = 'Create account on source 'AD'',
                state = 'Pending',
                type = 'Generic',
                remediation_items = [
                    sailpoint.beta.models.remediation_item_details.RemediationItemDetails(
                        id = '2c9180835d2e5168015d32f890ca1581', 
                        target_id = '2c9180835d2e5168015d32f890ca1581', 
                        target_name = 'john.smith', 
                        target_display_name = 'emailAddress', 
                        application_name = 'Active Directory', 
                        attribute_name = 'phoneNumber', 
                        attribute_operation = 'update', 
                        attribute_value = '512-555-1212', 
                        native_identity = 'jason.smith2', )
                    ],
                approval_items = [
                    sailpoint.beta.models.approval_item_details.ApprovalItemDetails(
                        id = '2c9180835d2e5168015d32f890ca1581', 
                        account = 'john.smith', 
                        application = 'Active Directory', 
                        name = 'emailAddress', 
                        operation = 'update', 
                        value = 'a@b.com', 
                        state = 'Pending', )
                    ],
                name = 'Account Create',
                completed = '2018-10-19T13:49:37.385Z',
                num_items = 19,
                errors = [The work item ID that was specified was not found.],
                form = sailpoint.beta.models.form_details.FormDetails(
                    id = '2c9180835d2e5168015d32f890ca1581', 
                    name = 'AccountSelection Form', 
                    title = 'Account Selection for John.Doe', 
                    subtitle = 'Please select from the following', 
                    target_user = 'Jane.Doe', 
                    sections = [
                        sailpoint.beta.models.section_details.SectionDetails()
                        ], )
            )
        else:
            return WorkItems(
        )
        """

    def testWorkItems(self):
        """Test WorkItems"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
