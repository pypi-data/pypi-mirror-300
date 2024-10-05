# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.access_request import AccessRequest

class TestAccessRequest(unittest.TestCase):
    """AccessRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessRequest:
        """Test AccessRequest
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessRequest`
        """
        model = AccessRequest()
        if include_optional:
            return AccessRequest(
                requested_for = [
                    '2c918084660f45d6016617daa9210584'
                    ],
                request_type = 'GRANT_ACCESS',
                requested_items = [
                    sailpoint.beta.models.access_request_item.AccessRequestItem(
                        type = 'ACCESS_PROFILE', 
                        id = '2c9180835d2e5168015d32f890ca1581', 
                        comment = 'Requesting access profile for John Doe', 
                        client_metadata = {requestedAppName=test-app, requestedAppId=2c91808f7892918f0178b78da4a305a1}, 
                        remove_date = '2020-07-11T21:23:15Z', )
                    ],
                client_metadata = {requestedAppId=2c91808f7892918f0178b78da4a305a1, requestedAppName=test-app}
            )
        else:
            return AccessRequest(
                requested_for = [
                    '2c918084660f45d6016617daa9210584'
                    ],
                requested_items = [
                    sailpoint.beta.models.access_request_item.AccessRequestItem(
                        type = 'ACCESS_PROFILE', 
                        id = '2c9180835d2e5168015d32f890ca1581', 
                        comment = 'Requesting access profile for John Doe', 
                        client_metadata = {requestedAppName=test-app, requestedAppId=2c91808f7892918f0178b78da4a305a1}, 
                        remove_date = '2020-07-11T21:23:15Z', )
                    ],
        )
        """

    def testAccessRequest(self):
        """Test AccessRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
