# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.non_employee_schema_attribute import NonEmployeeSchemaAttribute

class TestNonEmployeeSchemaAttribute(unittest.TestCase):
    """NonEmployeeSchemaAttribute unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NonEmployeeSchemaAttribute:
        """Test NonEmployeeSchemaAttribute
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NonEmployeeSchemaAttribute`
        """
        model = NonEmployeeSchemaAttribute()
        if include_optional:
            return NonEmployeeSchemaAttribute(
                id = 'ac110005-7156-1150-8171-5b292e3e0084',
                system = True,
                modified = '2019-08-23T18:52:59.162Z',
                created = '2019-08-23T18:40:35.772Z',
                type = 'TEXT',
                label = 'Account Name',
                technical_name = 'account.name',
                help_text = 'The unique identifier for the account',
                placeholder = 'Enter a unique user name for this account.',
                required = True
            )
        else:
            return NonEmployeeSchemaAttribute(
                type = 'TEXT',
                label = 'Account Name',
                technical_name = 'account.name',
        )
        """

    def testNonEmployeeSchemaAttribute(self):
        """Test NonEmployeeSchemaAttribute"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
