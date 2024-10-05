# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.connector_rule_response import ConnectorRuleResponse

class TestConnectorRuleResponse(unittest.TestCase):
    """ConnectorRuleResponse unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ConnectorRuleResponse:
        """Test ConnectorRuleResponse
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ConnectorRuleResponse`
        """
        model = ConnectorRuleResponse()
        if include_optional:
            return ConnectorRuleResponse(
                name = 'WebServiceBeforeOperationRule',
                description = 'This rule does that',
                type = 'BuildMap',
                signature = sailpoint.v2024.models.connector_rule_create_request_signature.ConnectorRuleCreateRequest_signature(
                    input = [
                        sailpoint.v2024.models.argument.Argument(
                            name = 'firstName', 
                            description = 'the first name of the identity', 
                            type = 'String', )
                        ], 
                    output = sailpoint.v2024.models.argument.Argument(
                        name = 'firstName', 
                        description = 'the first name of the identity', 
                        type = 'String', ), ),
                source_code = sailpoint.v2024.models.source_code.SourceCode(
                    version = '1.0', 
                    script = 'return "Mr. " + firstName;', ),
                attributes = {},
                id = '8113d48c0b914f17b4c6072d4dcb9dfe',
                created = '021-07-22T15:59:23Z',
                modified = '021-07-22T15:59:23Z'
            )
        else:
            return ConnectorRuleResponse(
                name = 'WebServiceBeforeOperationRule',
                type = 'BuildMap',
                source_code = sailpoint.v2024.models.source_code.SourceCode(
                    version = '1.0', 
                    script = 'return "Mr. " + firstName;', ),
                id = '8113d48c0b914f17b4c6072d4dcb9dfe',
                created = '021-07-22T15:59:23Z',
        )
        """

    def testConnectorRuleResponse(self):
        """Test ConnectorRuleResponse"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
