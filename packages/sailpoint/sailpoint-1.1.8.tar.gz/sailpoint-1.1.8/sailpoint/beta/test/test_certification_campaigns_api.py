# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.certification_campaigns_api import CertificationCampaignsApi


class TestCertificationCampaignsApi(unittest.TestCase):
    """CertificationCampaignsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = CertificationCampaignsApi()

    def tearDown(self) -> None:
        pass

    def test_complete_campaign(self) -> None:
        """Test case for complete_campaign

        Complete a Campaign
        """
        pass

    def test_create_campaign(self) -> None:
        """Test case for create_campaign

        Create Campaign
        """
        pass

    def test_create_campaign_template(self) -> None:
        """Test case for create_campaign_template

        Create a Campaign Template
        """
        pass

    def test_delete_campaign_template(self) -> None:
        """Test case for delete_campaign_template

        Delete a Campaign Template
        """
        pass

    def test_delete_campaign_template_schedule(self) -> None:
        """Test case for delete_campaign_template_schedule

        Delete Campaign Template Schedule
        """
        pass

    def test_delete_campaigns(self) -> None:
        """Test case for delete_campaigns

        Delete Campaigns
        """
        pass

    def test_get_active_campaigns(self) -> None:
        """Test case for get_active_campaigns

        List Campaigns
        """
        pass

    def test_get_campaign(self) -> None:
        """Test case for get_campaign

        Get Campaign
        """
        pass

    def test_get_campaign_reports(self) -> None:
        """Test case for get_campaign_reports

        Get Campaign Reports
        """
        pass

    def test_get_campaign_reports_config(self) -> None:
        """Test case for get_campaign_reports_config

        Get Campaign Reports Configuration
        """
        pass

    def test_get_campaign_template(self) -> None:
        """Test case for get_campaign_template

        Get a Campaign Template
        """
        pass

    def test_get_campaign_template_schedule(self) -> None:
        """Test case for get_campaign_template_schedule

        Get Campaign Template Schedule
        """
        pass

    def test_get_campaign_templates(self) -> None:
        """Test case for get_campaign_templates

        List Campaign Templates
        """
        pass

    def test_move(self) -> None:
        """Test case for move

        Reassign Certifications
        """
        pass

    def test_patch_campaign_template(self) -> None:
        """Test case for patch_campaign_template

        Update a Campaign Template
        """
        pass

    def test_set_campaign_reports_config(self) -> None:
        """Test case for set_campaign_reports_config

        Set Campaign Reports Configuration
        """
        pass

    def test_set_campaign_template_schedule(self) -> None:
        """Test case for set_campaign_template_schedule

        Set Campaign Template Schedule
        """
        pass

    def test_start_campaign(self) -> None:
        """Test case for start_campaign

        Activate a Campaign
        """
        pass

    def test_start_campaign_remediation_scan(self) -> None:
        """Test case for start_campaign_remediation_scan

        Run Campaign Remediation Scan
        """
        pass

    def test_start_campaign_report(self) -> None:
        """Test case for start_campaign_report

        Run Campaign Report
        """
        pass

    def test_start_generate_campaign_template(self) -> None:
        """Test case for start_generate_campaign_template

        Generate a Campaign from Template
        """
        pass

    def test_update_campaign(self) -> None:
        """Test case for update_campaign

        Update a Campaign
        """
        pass


if __name__ == '__main__':
    unittest.main()
