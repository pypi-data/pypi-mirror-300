# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.campaign_ended_campaign import CampaignEndedCampaign

class TestCampaignEndedCampaign(unittest.TestCase):
    """CampaignEndedCampaign unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> CampaignEndedCampaign:
        """Test CampaignEndedCampaign
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `CampaignEndedCampaign`
        """
        model = CampaignEndedCampaign()
        if include_optional:
            return CampaignEndedCampaign(
                id = '2c91808576f886190176f88cac5a0010',
                name = 'Manager Access Campaign',
                description = 'Audit access for all employees.',
                created = '2021-02-16T03:04:45.815Z',
                modified = '2021-03-16T03:06:45.815Z',
                deadline = '2021-03-16T03:04:45.815Z',
                type = MANAGER,
                campaign_owner = sailpoint.v2024.models.campaign_activated_campaign_campaign_owner.CampaignActivated_campaign_campaignOwner(
                    id = '37f080867702c1910177031320c40n27', 
                    display_name = 'John Snow', 
                    email = 'john.snow@example.com', ),
                status = COMPLETED
            )
        else:
            return CampaignEndedCampaign(
                id = '2c91808576f886190176f88cac5a0010',
                name = 'Manager Access Campaign',
                description = 'Audit access for all employees.',
                created = '2021-02-16T03:04:45.815Z',
                deadline = '2021-03-16T03:04:45.815Z',
                type = MANAGER,
                campaign_owner = sailpoint.v2024.models.campaign_activated_campaign_campaign_owner.CampaignActivated_campaign_campaignOwner(
                    id = '37f080867702c1910177031320c40n27', 
                    display_name = 'John Snow', 
                    email = 'john.snow@example.com', ),
                status = COMPLETED,
        )
        """

    def testCampaignEndedCampaign(self):
        """Test CampaignEndedCampaign"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
