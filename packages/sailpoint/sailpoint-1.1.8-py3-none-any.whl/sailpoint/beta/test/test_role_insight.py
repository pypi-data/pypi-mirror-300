# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.role_insight import RoleInsight

class TestRoleInsight(unittest.TestCase):
    """RoleInsight unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RoleInsight:
        """Test RoleInsight
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RoleInsight`
        """
        model = RoleInsight()
        if include_optional:
            return RoleInsight(
                id = '1467e61e-f284-439c-ba2d-c6cc11cf0941',
                number_of_updates = 5,
                created_date = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                modified_date = '2020-05-19T13:49:37.385Z',
                role = sailpoint.beta.models.role_insights_role.RoleInsightsRole(
                    name = 'Software Engineer', 
                    id = '1467e61e-f284-439c-ba2d-c6cc11cf0941', 
                    description = 'Person who develops software', 
                    owner_name = 'Bob', 
                    owner_id = '1467e61e-f284-439c-ba2d-c6cc11cf0941', ),
                insight = sailpoint.beta.models.role_insights_insight.RoleInsightsInsight(
                    type = 'ADD', 
                    identities_with_access = 850, 
                    identities_impacted = 150, 
                    total_number_of_identities = 1000, 
                    impacted_identity_names = '', )
            )
        else:
            return RoleInsight(
        )
        """

    def testRoleInsight(self):
        """Test RoleInsight"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
