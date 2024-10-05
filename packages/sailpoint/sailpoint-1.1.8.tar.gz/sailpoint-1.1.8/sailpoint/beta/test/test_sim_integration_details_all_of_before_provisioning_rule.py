# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.sim_integration_details_all_of_before_provisioning_rule import SimIntegrationDetailsAllOfBeforeProvisioningRule

class TestSimIntegrationDetailsAllOfBeforeProvisioningRule(unittest.TestCase):
    """SimIntegrationDetailsAllOfBeforeProvisioningRule unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SimIntegrationDetailsAllOfBeforeProvisioningRule:
        """Test SimIntegrationDetailsAllOfBeforeProvisioningRule
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SimIntegrationDetailsAllOfBeforeProvisioningRule`
        """
        model = SimIntegrationDetailsAllOfBeforeProvisioningRule()
        if include_optional:
            return SimIntegrationDetailsAllOfBeforeProvisioningRule(
                type = 'IDENTITY',
                id = '2c918085708c274401708c2a8a760001',
                name = 'Example Rule'
            )
        else:
            return SimIntegrationDetailsAllOfBeforeProvisioningRule(
        )
        """

    def testSimIntegrationDetailsAllOfBeforeProvisioningRule(self):
        """Test SimIntegrationDetailsAllOfBeforeProvisioningRule"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
