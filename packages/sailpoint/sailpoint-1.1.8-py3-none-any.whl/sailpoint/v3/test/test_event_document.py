# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.event_document import EventDocument

class TestEventDocument(unittest.TestCase):
    """EventDocument unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> EventDocument:
        """Test EventDocument
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `EventDocument`
        """
        model = EventDocument()
        if include_optional:
            return EventDocument(
                id = '2c91808375d8e80a0175e1f88a575222',
                name = 'john.doe',
                type = 'identity',
                created = '2018-06-25T20:22:28.104Z',
                synced = '',
                action = 'update',
                type = 'SYSTEM_CONFIG',
                actor = 'System',
                target = 'Carol.Adams',
                stack = 'tpe',
                tracking_number = '63f891e0735f4cc8bf1968144a1e7440',
                ip_address = '52.52.97.85',
                details = '73b65dfbed1842548c207432a18c84b0',
                attributes = {pod=stg03-useast1, org=acme, sourceName=SailPoint},
                objects = [
                    'AUTHENTICATION'
                    ],
                operation = 'REQUEST',
                status = 'PASSED',
                technical_name = 'AUTHENTICATION_REQUEST_PASSED'
            )
        else:
            return EventDocument(
                id = '2c91808375d8e80a0175e1f88a575222',
                name = 'john.doe',
                type = 'identity',
        )
        """

    def testEventDocument(self):
        """Test EventDocument"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
