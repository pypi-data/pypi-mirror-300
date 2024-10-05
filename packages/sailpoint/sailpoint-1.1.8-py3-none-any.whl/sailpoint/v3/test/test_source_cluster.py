# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.source_cluster import SourceCluster

class TestSourceCluster(unittest.TestCase):
    """SourceCluster unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SourceCluster:
        """Test SourceCluster
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SourceCluster`
        """
        model = SourceCluster()
        if include_optional:
            return SourceCluster(
                type = 'CLUSTER',
                id = '2c9180866166b5b0016167c32ef31a66',
                name = 'Corporate Cluster'
            )
        else:
            return SourceCluster(
                type = 'CLUSTER',
                id = '2c9180866166b5b0016167c32ef31a66',
                name = 'Corporate Cluster',
        )
        """

    def testSourceCluster(self):
        """Test SourceCluster"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
