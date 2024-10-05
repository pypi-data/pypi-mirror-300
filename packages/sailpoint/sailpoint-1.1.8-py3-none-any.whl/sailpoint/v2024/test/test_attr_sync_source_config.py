# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.attr_sync_source_config import AttrSyncSourceConfig

class TestAttrSyncSourceConfig(unittest.TestCase):
    """AttrSyncSourceConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AttrSyncSourceConfig:
        """Test AttrSyncSourceConfig
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AttrSyncSourceConfig`
        """
        model = AttrSyncSourceConfig()
        if include_optional:
            return AttrSyncSourceConfig(
                source = sailpoint.v2024.models.attr_sync_source.AttrSyncSource(
                    type = 'SOURCE', 
                    id = '2c9180835d191a86015d28455b4b232a', 
                    name = 'HR Active Directory', ),
                attributes = [{name=email, displayName=Email, enabled=true, target=mail}, {name=firstname, displayName=First Name, enabled=false, target=givenName}]
            )
        else:
            return AttrSyncSourceConfig(
                source = sailpoint.v2024.models.attr_sync_source.AttrSyncSource(
                    type = 'SOURCE', 
                    id = '2c9180835d191a86015d28455b4b232a', 
                    name = 'HR Active Directory', ),
                attributes = [{name=email, displayName=Email, enabled=true, target=mail}, {name=firstname, displayName=First Name, enabled=false, target=givenName}],
        )
        """

    def testAttrSyncSourceConfig(self):
        """Test AttrSyncSourceConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
