# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.service_desk_integration_template_type import ServiceDeskIntegrationTemplateType

class TestServiceDeskIntegrationTemplateType(unittest.TestCase):
    """ServiceDeskIntegrationTemplateType unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ServiceDeskIntegrationTemplateType:
        """Test ServiceDeskIntegrationTemplateType
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ServiceDeskIntegrationTemplateType`
        """
        model = ServiceDeskIntegrationTemplateType()
        if include_optional:
            return ServiceDeskIntegrationTemplateType(
                name = 'aName',
                type = 'aType',
                script_name = 'aScriptName'
            )
        else:
            return ServiceDeskIntegrationTemplateType(
                type = 'aType',
                script_name = 'aScriptName',
        )
        """

    def testServiceDeskIntegrationTemplateType(self):
        """Test ServiceDeskIntegrationTemplateType"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
