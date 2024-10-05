# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.sim_integrations_api import SIMIntegrationsApi


class TestSIMIntegrationsApi(unittest.TestCase):
    """SIMIntegrationsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SIMIntegrationsApi()

    def tearDown(self) -> None:
        pass

    def test_create_sim_integration(self) -> None:
        """Test case for create_sim_integration

        Create new SIM integration
        """
        pass

    def test_delete_sim_integration(self) -> None:
        """Test case for delete_sim_integration

        Delete a SIM integration
        """
        pass

    def test_get_sim_integration(self) -> None:
        """Test case for get_sim_integration

        Get a SIM integration details.
        """
        pass

    def test_get_sim_integrations(self) -> None:
        """Test case for get_sim_integrations

        List the existing SIM integrations.
        """
        pass

    def test_patch_before_provisioning_rule(self) -> None:
        """Test case for patch_before_provisioning_rule

        Patch a SIM beforeProvisioningRule attribute.
        """
        pass

    def test_patch_sim_attributes(self) -> None:
        """Test case for patch_sim_attributes

        Patch a SIM attribute.
        """
        pass

    def test_put_sim_integration(self) -> None:
        """Test case for put_sim_integration

        Update an existing SIM integration
        """
        pass


if __name__ == '__main__':
    unittest.main()
