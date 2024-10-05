# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.identity_sync_payload import IdentitySyncPayload

class TestIdentitySyncPayload(unittest.TestCase):
    """IdentitySyncPayload unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IdentitySyncPayload:
        """Test IdentitySyncPayload
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `IdentitySyncPayload`
        """
        model = IdentitySyncPayload()
        if include_optional:
            return IdentitySyncPayload(
                type = 'SYNCHRONIZE_IDENTITY_ATTRIBUTES',
                data_json = '{"identityId":"2c918083746f642c01746f990884012a"}'
            )
        else:
            return IdentitySyncPayload(
                type = 'SYNCHRONIZE_IDENTITY_ATTRIBUTES',
                data_json = '{"identityId":"2c918083746f642c01746f990884012a"}',
        )
        """

    def testIdentitySyncPayload(self):
        """Test IdentitySyncPayload"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
