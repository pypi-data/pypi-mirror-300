# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.slimcampaign import Slimcampaign

class TestSlimcampaign(unittest.TestCase):
    """Slimcampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Slimcampaign:
        """Test Slimcampaign
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Slimcampaign`
        """
        model = Slimcampaign()
        if include_optional:
            return Slimcampaign(
                id = '2c9079b270a266a60170a2779fcb0007',
                name = 'Manager Campaign',
                description = 'Everyone needs to be reviewed by their manager',
                deadline = '2020-03-15T10:00:01.456Z',
                type = 'MANAGER',
                email_notification_enabled = False,
                auto_revoke_allowed = False,
                recommendations_enabled = True,
                status = 'ACTIVE',
                correlated_status = 'CORRELATED',
                created = '2020-03-03T22:15:13.611Z',
                total_certifications = 100,
                completed_certifications = 10,
                alerts = [
                    sailpoint.beta.models.campaign_alert.CampaignAlert(
                        level = 'ERROR', 
                        localizations = [
                            sailpoint.beta.models.error_message_dto.ErrorMessageDto(
                                locale = 'en-US', 
                                locale_origin = 'DEFAULT', 
                                text = 'The request was syntactically correct but its content is semantically invalid.', )
                            ], )
                    ]
            )
        else:
            return Slimcampaign(
                name = 'Manager Campaign',
                description = 'Everyone needs to be reviewed by their manager',
                type = 'MANAGER',
        )
        """

    def testSlimcampaign(self):
        """Test Slimcampaign"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
