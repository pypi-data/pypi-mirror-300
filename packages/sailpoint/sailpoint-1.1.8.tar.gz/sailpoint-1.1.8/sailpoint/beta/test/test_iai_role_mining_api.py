# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.iai_role_mining_api import IAIRoleMiningApi


class TestIAIRoleMiningApi(unittest.TestCase):
    """IAIRoleMiningApi unit test stubs"""

    def setUp(self) -> None:
        self.api = IAIRoleMiningApi()

    def tearDown(self) -> None:
        pass

    def test_create_potential_role_provision_request(self) -> None:
        """Test case for create_potential_role_provision_request

        Create request to provision a potential role into an actual role.
        """
        pass

    def test_create_role_mining_sessions(self) -> None:
        """Test case for create_role_mining_sessions

        Create a role mining session
        """
        pass

    def test_download_role_mining_potential_role_zip(self) -> None:
        """Test case for download_role_mining_potential_role_zip

        Export (download) details for a potential role in a role mining session
        """
        pass

    def test_export_role_mining_potential_role(self) -> None:
        """Test case for export_role_mining_potential_role

        Export (download) details for a potential role in a role mining session
        """
        pass

    def test_export_role_mining_potential_role_async(self) -> None:
        """Test case for export_role_mining_potential_role_async

        Asynchronously export details for a potential role in a role mining session and upload to S3
        """
        pass

    def test_export_role_mining_potential_role_status(self) -> None:
        """Test case for export_role_mining_potential_role_status

        Retrieve status of a potential role export job
        """
        pass

    def test_get_all_potential_role_summaries(self) -> None:
        """Test case for get_all_potential_role_summaries

        Retrieves all potential role summaries
        """
        pass

    def test_get_entitlement_distribution_potential_role(self) -> None:
        """Test case for get_entitlement_distribution_potential_role

        Retrieves entitlement popularity distribution for a potential role in a role mining session
        """
        pass

    def test_get_entitlements_potential_role(self) -> None:
        """Test case for get_entitlements_potential_role

        Retrieves entitlements for a potential role in a role mining session
        """
        pass

    def test_get_excluded_entitlements_potential_role(self) -> None:
        """Test case for get_excluded_entitlements_potential_role

        Retrieves excluded entitlements for a potential role in a role mining session
        """
        pass

    def test_get_identities_potential_role(self) -> None:
        """Test case for get_identities_potential_role

        Retrieves identities for a potential role in a role mining session
        """
        pass

    def test_get_potential_role(self) -> None:
        """Test case for get_potential_role

        Retrieve potential role in session
        """
        pass

    def test_get_potential_role_applications(self) -> None:
        """Test case for get_potential_role_applications

        Retrieves the applications of a potential role for a role mining session
        """
        pass

    def test_get_potential_role_source_identity_usage(self) -> None:
        """Test case for get_potential_role_source_identity_usage

        Retrieves potential role source usage
        """
        pass

    def test_get_potential_role_summaries(self) -> None:
        """Test case for get_potential_role_summaries

        Retrieve session's potential role summaries
        """
        pass

    def test_get_role_mining_potential_role(self) -> None:
        """Test case for get_role_mining_potential_role

        Retrieves a specific potential role
        """
        pass

    def test_get_role_mining_session(self) -> None:
        """Test case for get_role_mining_session

        Get a role mining session
        """
        pass

    def test_get_role_mining_session_status(self) -> None:
        """Test case for get_role_mining_session_status

        Get role mining session status state
        """
        pass

    def test_get_role_mining_sessions(self) -> None:
        """Test case for get_role_mining_sessions

        Retrieves all role mining sessions
        """
        pass

    def test_get_saved_potential_roles(self) -> None:
        """Test case for get_saved_potential_roles

        Retrieves all saved potential roles
        """
        pass

    def test_patch_potential_role(self) -> None:
        """Test case for patch_potential_role

        Update a potential role in session
        """
        pass

    def test_patch_role_mining_potential_role(self) -> None:
        """Test case for patch_role_mining_potential_role

        Update a potential role
        """
        pass

    def test_patch_role_mining_session(self) -> None:
        """Test case for patch_role_mining_session

        Patch a role mining session
        """
        pass

    def test_update_entitlements_potential_role(self) -> None:
        """Test case for update_entitlements_potential_role

        Edit entitlements for a potential role to exclude some entitlements
        """
        pass


if __name__ == '__main__':
    unittest.main()
