# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.form_element_data_source_config_options import FormElementDataSourceConfigOptions

class TestFormElementDataSourceConfigOptions(unittest.TestCase):
    """FormElementDataSourceConfigOptions unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> FormElementDataSourceConfigOptions:
        """Test FormElementDataSourceConfigOptions
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `FormElementDataSourceConfigOptions`
        """
        model = FormElementDataSourceConfigOptions()
        if include_optional:
            return FormElementDataSourceConfigOptions(
                label = 'regression-test-access-request-07c55dd6-3056-430a-86b5-fccc395bb6c5',
                sub_label = '',
                value = 'e96674448eba4ca1ba04eee999a8f3cd'
            )
        else:
            return FormElementDataSourceConfigOptions(
        )
        """

    def testFormElementDataSourceConfigOptions(self):
        """Test FormElementDataSourceConfigOptions"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
