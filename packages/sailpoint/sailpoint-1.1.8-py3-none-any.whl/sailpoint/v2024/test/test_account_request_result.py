# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.account_request_result import AccountRequestResult

class TestAccountRequestResult(unittest.TestCase):
    """AccountRequestResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccountRequestResult:
        """Test AccountRequestResult
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccountRequestResult`
        """
        model = AccountRequestResult()
        if include_optional:
            return AccountRequestResult(
                errors = [
                    '[ConnectorError] [
  {
    "code": "unrecognized_keys",
    "keys": [
      "groups"
    ],
    "path": [],
    "message": "Unrecognized key(s) in object: 'groups'"
  }
] (requestId: 5e9d6df5-9b1b-47d9-9bf1-dc3a2893299e)'
                    ],
                status = 'failed',
                ticket_id = ''
            )
        else:
            return AccountRequestResult(
        )
        """

    def testAccountRequestResult(self):
        """Test AccountRequestResult"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
