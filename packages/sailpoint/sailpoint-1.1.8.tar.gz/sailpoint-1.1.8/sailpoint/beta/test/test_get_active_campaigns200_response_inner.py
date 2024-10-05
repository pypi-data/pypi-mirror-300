# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.get_active_campaigns200_response_inner import GetActiveCampaigns200ResponseInner

class TestGetActiveCampaigns200ResponseInner(unittest.TestCase):
    """GetActiveCampaigns200ResponseInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetActiveCampaigns200ResponseInner:
        """Test GetActiveCampaigns200ResponseInner
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetActiveCampaigns200ResponseInner`
        """
        model = GetActiveCampaigns200ResponseInner()
        if include_optional:
            return GetActiveCampaigns200ResponseInner(
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
                    ],
                modified = '2020-03-03T22:20:12.674Z',
                filter = sailpoint.beta.models.fullcampaign_all_of_filter.fullcampaign_allOf_filter(
                    id = '0fbe863c063c4c88a35fd7f17e8a3df5', 
                    type = 'CAMPAIGN_FILTER', 
                    name = 'Test Filter', ),
                sunset_comments_required = True,
                source_owner_campaign_info = sailpoint.beta.models.fullcampaign_all_of_source_owner_campaign_info.fullcampaign_allOf_sourceOwnerCampaignInfo(
                    source_ids = [0fbe863c063c4c88a35fd7f17e8a3df5], ),
                search_campaign_info = sailpoint.beta.models.fullcampaign_all_of_search_campaign_info.fullcampaign_allOf_searchCampaignInfo(
                    type = 'ACCESS', 
                    description = 'Search Campaign description', 
                    reviewer = sailpoint.beta.models.fullcampaign_all_of_search_campaign_info_reviewer.fullcampaign_allOf_searchCampaignInfo_reviewer(
                        type = 'IDENTITY', 
                        id = '2c91808568c529c60168cca6f90c1313', 
                        name = 'William Wilson', ), 
                    query = 'Search Campaign query description', 
                    identity_ids = [0fbe863c063c4c88a35fd7f17e8a3df5], 
                    access_constraints = [
                        sailpoint.beta.models.access_constraint.AccessConstraint(
                            type = 'ENTITLEMENT', 
                            ids = [2c90ad2a70ace7d50170acf22ca90010], 
                            operator = 'SELECTED', )
                        ], ),
                role_composition_campaign_info = sailpoint.beta.models.fullcampaign_all_of_role_composition_campaign_info.fullcampaign_allOf_roleCompositionCampaignInfo(
                    reviewer = sailpoint.beta.models.fullcampaign_all_of_search_campaign_info_reviewer.fullcampaign_allOf_searchCampaignInfo_reviewer(
                        type = 'IDENTITY', 
                        id = '2c91808568c529c60168cca6f90c1313', 
                        name = 'William Wilson', ), 
                    role_ids = [2c90ad2a70ace7d50170acf22ca90010], 
                    remediator_ref = sailpoint.beta.models.fullcampaign_all_of_role_composition_campaign_info_remediator_ref.fullcampaign_allOf_roleCompositionCampaignInfo_remediatorRef(
                        type = 'IDENTITY', 
                        id = '2c90ad2a70ace7d50170acf22ca90010', 
                        name = 'Role Admin', ), 
                    query = 'Search Query', 
                    description = 'Role Composition Description', ),
                sources_with_orphan_entitlements = [
                    sailpoint.beta.models.fullcampaign_all_of_sources_with_orphan_entitlements.fullcampaign_allOf_sourcesWithOrphanEntitlements(
                        id = '2c90ad2a70ace7d50170acf22ca90010', 
                        type = 'SOURCE', 
                        name = 'Source with orphan entitlements', )
                    ],
                mandatory_comment_requirement = 'NO_DECISIONS'
            )
        else:
            return GetActiveCampaigns200ResponseInner(
                name = 'Manager Campaign',
                description = 'Everyone needs to be reviewed by their manager',
                type = 'MANAGER',
        )
        """

    def testGetActiveCampaigns200ResponseInner(self):
        """Test GetActiveCampaigns200ResponseInner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
