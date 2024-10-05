# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.public_identity_config import PublicIdentityConfig

class TestPublicIdentityConfig(unittest.TestCase):
    """PublicIdentityConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> PublicIdentityConfig:
        """Test PublicIdentityConfig
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `PublicIdentityConfig`
        """
        model = PublicIdentityConfig()
        if include_optional:
            return PublicIdentityConfig(
                attributes = [
                    sailpoint.v2024.models.public_identity_attribute_config.PublicIdentityAttributeConfig(
                        key = 'country', 
                        name = 'Country', )
                    ],
                modified = '2018-06-25T20:22:28.104Z',
                modified_by = sailpoint.v2024.models.identity_reference.IdentityReference(
                    type = 'IDENTITY', 
                    id = '2c9180a46faadee4016fb4e018c20639', 
                    name = 'Thomas Edison', )
            )
        else:
            return PublicIdentityConfig(
        )
        """

    def testPublicIdentityConfig(self):
        """Test PublicIdentityConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
