# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.base_access import BaseAccess

class TestBaseAccess(unittest.TestCase):
    """BaseAccess unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> BaseAccess:
        """Test BaseAccess
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `BaseAccess`
        """
        model = BaseAccess()
        if include_optional:
            return BaseAccess(
                id = '2c91808568c529c60168cca6f90c1313',
                name = 'John Doe',
                description = 'The admin role',
                created = '2018-06-25T20:22:28.104Z',
                modified = '2018-06-25T20:22:28.104Z',
                synced = '2018-06-25T20:22:33.104Z',
                enabled = True,
                requestable = True,
                request_comments_required = False,
                owner = sailpoint.v3.models.base_access_all_of_owner.BaseAccess_allOf_owner(
                    type = 'IDENTITY', 
                    id = '2c9180a46faadee4016fb4e018c20639', 
                    name = 'Support', 
                    email = 'cloud-support@sailpoint.com', )
            )
        else:
            return BaseAccess(
        )
        """

    def testBaseAccess(self):
        """Test BaseAccess"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
