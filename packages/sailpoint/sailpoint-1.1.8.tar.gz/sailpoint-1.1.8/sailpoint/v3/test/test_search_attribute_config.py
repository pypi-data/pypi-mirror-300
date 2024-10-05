# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.search_attribute_config import SearchAttributeConfig

class TestSearchAttributeConfig(unittest.TestCase):
    """SearchAttributeConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SearchAttributeConfig:
        """Test SearchAttributeConfig
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SearchAttributeConfig`
        """
        model = SearchAttributeConfig()
        if include_optional:
            return SearchAttributeConfig(
                name = 'newMailAttribute',
                display_name = 'New Mail Attribute',
                application_attributes = {2c91808b79fd2422017a0b35d30f3968=employeeNumber, 2c91808b79fd2422017a0b36008f396b=employeeNumber}
            )
        else:
            return SearchAttributeConfig(
        )
        """

    def testSearchAttributeConfig(self):
        """Test SearchAttributeConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
