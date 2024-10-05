# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.api.global_tenant_security_settings_api import GlobalTenantSecuritySettingsApi


class TestGlobalTenantSecuritySettingsApi(unittest.TestCase):
    """GlobalTenantSecuritySettingsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = GlobalTenantSecuritySettingsApi()

    def tearDown(self) -> None:
        pass

    def test_create_auth_org_network_config(self) -> None:
        """Test case for create_auth_org_network_config

        Create security network configuration.
        """
        pass

    def test_get_auth_org_lockout_config(self) -> None:
        """Test case for get_auth_org_lockout_config

        Get Auth Org Lockout Configuration.
        """
        pass

    def test_get_auth_org_network_config(self) -> None:
        """Test case for get_auth_org_network_config

        Get security network configuration.
        """
        pass

    def test_get_auth_org_service_provider_config(self) -> None:
        """Test case for get_auth_org_service_provider_config

        Get Service Provider Configuration.
        """
        pass

    def test_get_auth_org_session_config(self) -> None:
        """Test case for get_auth_org_session_config

        Get Auth Org Session Configuration.
        """
        pass

    def test_patch_auth_org_lockout_config(self) -> None:
        """Test case for patch_auth_org_lockout_config

        Update Auth Org Lockout Configuration
        """
        pass

    def test_patch_auth_org_network_config(self) -> None:
        """Test case for patch_auth_org_network_config

        Update security network configuration.
        """
        pass

    def test_patch_auth_org_service_provider_config(self) -> None:
        """Test case for patch_auth_org_service_provider_config

        Update Service Provider Configuration
        """
        pass

    def test_patch_auth_org_session_config(self) -> None:
        """Test case for patch_auth_org_session_config

        Update Auth Org Session Configuration
        """
        pass


if __name__ == '__main__':
    unittest.main()
