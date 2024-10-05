# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.source_account_deleted import SourceAccountDeleted

class TestSourceAccountDeleted(unittest.TestCase):
    """SourceAccountDeleted unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SourceAccountDeleted:
        """Test SourceAccountDeleted
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SourceAccountDeleted`
        """
        model = SourceAccountDeleted()
        if include_optional:
            return SourceAccountDeleted(
                uuid = 'b7264868-7201-415f-9118-b581d431c688',
                id = 'ee769173319b41d19ccec35ba52f237b',
                native_identifier = 'E009',
                source_id = '2c918082814e693601816e09471b29b6',
                source_name = 'Active Directory',
                identity_id = 'ee769173319b41d19ccec6c235423237b',
                identity_name = 'john.doe',
                attributes = {firstname=John, lastname=Doe, email=john.doe@gmail.com, department=Sales, displayName=John Doe, created=2020-04-27T16:48:33.597Z, employeeNumber=E009, uid=E009, inactive=true, phone=null, identificationNumber=E009}
            )
        else:
            return SourceAccountDeleted(
                id = 'ee769173319b41d19ccec35ba52f237b',
                native_identifier = 'E009',
                source_id = '2c918082814e693601816e09471b29b6',
                source_name = 'Active Directory',
                identity_id = 'ee769173319b41d19ccec6c235423237b',
                identity_name = 'john.doe',
                attributes = {firstname=John, lastname=Doe, email=john.doe@gmail.com, department=Sales, displayName=John Doe, created=2020-04-27T16:48:33.597Z, employeeNumber=E009, uid=E009, inactive=true, phone=null, identificationNumber=E009},
        )
        """

    def testSourceAccountDeleted(self):
        """Test SourceAccountDeleted"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
