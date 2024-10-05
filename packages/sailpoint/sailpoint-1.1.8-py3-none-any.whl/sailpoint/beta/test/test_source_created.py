# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.source_created import SourceCreated

class TestSourceCreated(unittest.TestCase):
    """SourceCreated unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SourceCreated:
        """Test SourceCreated
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SourceCreated`
        """
        model = SourceCreated()
        if include_optional:
            return SourceCreated(
                id = '2c9180866166b5b0016167c32ef31a66',
                name = 'Test source',
                type = 'DIRECT_CONNECT',
                created = '2021-03-29T22:01:50.474Z',
                connector = 'active-directory',
                actor = sailpoint.beta.models.source_created_actor.SourceCreated_actor(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20648', 
                    name = 'William Wilson', )
            )
        else:
            return SourceCreated(
                id = '2c9180866166b5b0016167c32ef31a66',
                name = 'Test source',
                type = 'DIRECT_CONNECT',
                created = '2021-03-29T22:01:50.474Z',
                connector = 'active-directory',
                actor = sailpoint.beta.models.source_created_actor.SourceCreated_actor(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20648', 
                    name = 'William Wilson', ),
        )
        """

    def testSourceCreated(self):
        """Test SourceCreated"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
