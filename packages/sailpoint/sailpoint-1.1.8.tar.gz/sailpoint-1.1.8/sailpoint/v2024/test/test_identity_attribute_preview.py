# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.identity_attribute_preview import IdentityAttributePreview

class TestIdentityAttributePreview(unittest.TestCase):
    """IdentityAttributePreview unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> IdentityAttributePreview:
        """Test IdentityAttributePreview
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `IdentityAttributePreview`
        """
        model = IdentityAttributePreview()
        if include_optional:
            return IdentityAttributePreview(
                name = 'email',
                value = 'email@mail.com',
                previous_value = 'oldEmail@mail.com',
                error_messages = [
                    sailpoint.v2024.models.error_message_dto.ErrorMessageDto(
                        locale = 'en-US', 
                        locale_origin = 'DEFAULT', 
                        text = 'The request was syntactically correct but its content is semantically invalid.', )
                    ]
            )
        else:
            return IdentityAttributePreview(
        )
        """

    def testIdentityAttributePreview(self):
        """Test IdentityAttributePreview"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
