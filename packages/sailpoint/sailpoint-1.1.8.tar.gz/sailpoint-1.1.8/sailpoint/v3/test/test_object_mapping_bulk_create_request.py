# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.object_mapping_bulk_create_request import ObjectMappingBulkCreateRequest

class TestObjectMappingBulkCreateRequest(unittest.TestCase):
    """ObjectMappingBulkCreateRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ObjectMappingBulkCreateRequest:
        """Test ObjectMappingBulkCreateRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ObjectMappingBulkCreateRequest`
        """
        model = ObjectMappingBulkCreateRequest()
        if include_optional:
            return ObjectMappingBulkCreateRequest(
                new_object_mappings = [
                    sailpoint.v3.models.object_mapping_request.Object Mapping Request(
                        object_type = 'IDENTITY', 
                        json_path = '$.name', 
                        source_value = 'My Governance Group Name', 
                        target_value = 'My New Governance Group Name', 
                        enabled = False, )
                    ]
            )
        else:
            return ObjectMappingBulkCreateRequest(
                new_object_mappings = [
                    sailpoint.v3.models.object_mapping_request.Object Mapping Request(
                        object_type = 'IDENTITY', 
                        json_path = '$.name', 
                        source_value = 'My Governance Group Name', 
                        target_value = 'My New Governance Group Name', 
                        enabled = False, )
                    ],
        )
        """

    def testObjectMappingBulkCreateRequest(self):
        """Test ObjectMappingBulkCreateRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
