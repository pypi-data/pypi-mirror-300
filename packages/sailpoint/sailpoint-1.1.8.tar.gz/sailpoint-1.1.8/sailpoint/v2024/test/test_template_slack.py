# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.template_slack import TemplateSlack

class TestTemplateSlack(unittest.TestCase):
    """TemplateSlack unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> TemplateSlack:
        """Test TemplateSlack
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `TemplateSlack`
        """
        model = TemplateSlack()
        if include_optional:
            return TemplateSlack(
                key = '',
                text = '',
                blocks = '',
                attachments = '',
                notification_type = '',
                approval_id = '',
                request_id = '',
                requested_by_id = '',
                is_subscription = True,
                auto_approval_data = sailpoint.v2024.models.template_slack_auto_approval_data.TemplateSlack_autoApprovalData(
                    is_auto_approved = '', 
                    item_id = '', 
                    item_type = '', 
                    auto_approval_message_json = '', 
                    auto_approval_title = '', ),
                custom_fields = sailpoint.v2024.models.template_slack_custom_fields.TemplateSlack_customFields(
                    request_type = '', 
                    contains_deny = '', 
                    campaign_id = '', 
                    campaign_status = '', )
            )
        else:
            return TemplateSlack(
        )
        """

    def testTemplateSlack(self):
        """Test TemplateSlack"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
