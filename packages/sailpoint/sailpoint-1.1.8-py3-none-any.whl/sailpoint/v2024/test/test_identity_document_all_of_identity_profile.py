# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.identity_document_all_of_identity_profile import IdentityDocumentAllOfIdentityProfile

class TestIdentityDocumentAllOfIdentityProfile(unittest.TestCase):
    """IdentityDocumentAllOfIdentityProfile unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IdentityDocumentAllOfIdentityProfile:
        """Test IdentityDocumentAllOfIdentityProfile
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `IdentityDocumentAllOfIdentityProfile`
        """
        model = IdentityDocumentAllOfIdentityProfile()
        if include_optional:
            return IdentityDocumentAllOfIdentityProfile(
                id = '3bc8ad26b8664945866b31339d1ff7d2',
                name = 'HR Employees'
            )
        else:
            return IdentityDocumentAllOfIdentityProfile(
        )
        """

    def testIdentityDocumentAllOfIdentityProfile(self):
        """Test IdentityDocumentAllOfIdentityProfile"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
