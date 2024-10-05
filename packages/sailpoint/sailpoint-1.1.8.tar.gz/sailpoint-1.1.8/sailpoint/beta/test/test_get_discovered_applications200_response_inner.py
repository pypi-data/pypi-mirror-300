# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.get_discovered_applications200_response_inner import GetDiscoveredApplications200ResponseInner

class TestGetDiscoveredApplications200ResponseInner(unittest.TestCase):
    """GetDiscoveredApplications200ResponseInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetDiscoveredApplications200ResponseInner:
        """Test GetDiscoveredApplications200ResponseInner
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetDiscoveredApplications200ResponseInner`
        """
        model = GetDiscoveredApplications200ResponseInner()
        if include_optional:
            return GetDiscoveredApplications200ResponseInner(
                id = '',
                name = 'ExampleApp',
                discovery_source = 'csv',
                discovered_vendor = 'ExampleVendor',
                description = 'An application for managing examples.',
                recommended_connectors = [ConnectorA, ConnectorB],
                discovered_at = '2023-01-01T12:00Z',
                created_at = '2023-01-01T12:00Z',
                status = 'ACTIVE',
                associated_sources = [e0cc5d7d-bf7f-4f81-b2af-8885b09d9923, a0303682-5e4a-44f7-bdc2-6ce6112549c1]
            )
        else:
            return GetDiscoveredApplications200ResponseInner(
        )
        """

    def testGetDiscoveredApplications200ResponseInner(self):
        """Test GetDiscoveredApplications200ResponseInner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
