# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.non_employee_source_request_body import NonEmployeeSourceRequestBody

class TestNonEmployeeSourceRequestBody(unittest.TestCase):
    """NonEmployeeSourceRequestBody unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NonEmployeeSourceRequestBody:
        """Test NonEmployeeSourceRequestBody
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NonEmployeeSourceRequestBody`
        """
        model = NonEmployeeSourceRequestBody()
        if include_optional:
            return NonEmployeeSourceRequestBody(
                name = 'Retail',
                description = 'Source description',
                owner = sailpoint.beta.models.non_employee_idn_user_request.NonEmployeeIdnUserRequest(
                    id = '2c91808570313110017040b06f344ec9', ),
                management_workgroup = '123299',
                approvers = [
                    sailpoint.beta.models.non_employee_idn_user_request.NonEmployeeIdnUserRequest(
                        id = '2c91808570313110017040b06f344ec9', )
                    ],
                account_managers = [
                    sailpoint.beta.models.non_employee_idn_user_request.NonEmployeeIdnUserRequest(
                        id = '2c91808570313110017040b06f344ec9', )
                    ]
            )
        else:
            return NonEmployeeSourceRequestBody(
                name = 'Retail',
                description = 'Source description',
                owner = sailpoint.beta.models.non_employee_idn_user_request.NonEmployeeIdnUserRequest(
                    id = '2c91808570313110017040b06f344ec9', ),
        )
        """

    def testNonEmployeeSourceRequestBody(self):
        """Test NonEmployeeSourceRequestBody"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
