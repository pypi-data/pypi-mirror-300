# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.bulk_add_tagged_object import BulkAddTaggedObject

class TestBulkAddTaggedObject(unittest.TestCase):
    """BulkAddTaggedObject unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BulkAddTaggedObject:
        """Test BulkAddTaggedObject
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BulkAddTaggedObject`
        """
        model = BulkAddTaggedObject()
        if include_optional:
            return BulkAddTaggedObject(
                object_refs = [
                    sailpoint.v3.models.tagged_object_dto.TaggedObjectDto(
                        type = 'IDENTITY', 
                        id = '2c91808568c529c60168cca6f90c1313', 
                        name = 'William Wilson', )
                    ],
                tags = [BU_FINANCE, PCI],
                operation = 'APPEND'
            )
        else:
            return BulkAddTaggedObject(
        )
        """

    def testBulkAddTaggedObject(self):
        """Test BulkAddTaggedObject"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
