# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.models.non_employee_request_body import NonEmployeeRequestBody

class TestNonEmployeeRequestBody(unittest.TestCase):
    """NonEmployeeRequestBody unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> NonEmployeeRequestBody:
        """Test NonEmployeeRequestBody
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `NonEmployeeRequestBody`
        """
        model = NonEmployeeRequestBody()
        if include_optional:
            return NonEmployeeRequestBody(
                account_name = 'william.smith',
                first_name = 'William',
                last_name = 'Smith',
                email = 'william.smith@example.com',
                phone = '5555555555',
                manager = 'jane.doe',
                source_id = '2c91808568c529c60168cca6f90c1313',
                data = {description=Auditing},
                start_date = '2020-03-24T00:00-05:00',
                end_date = '2021-03-25T00:00-05:00'
            )
        else:
            return NonEmployeeRequestBody(
                account_name = 'william.smith',
                first_name = 'William',
                last_name = 'Smith',
                email = 'william.smith@example.com',
                phone = '5555555555',
                manager = 'jane.doe',
                source_id = '2c91808568c529c60168cca6f90c1313',
                start_date = '2020-03-24T00:00-05:00',
                end_date = '2021-03-25T00:00-05:00',
        )
        """

    def testNonEmployeeRequestBody(self):
        """Test NonEmployeeRequestBody"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
