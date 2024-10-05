# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.role_criteria_level3 import RoleCriteriaLevel3

class TestRoleCriteriaLevel3(unittest.TestCase):
    """RoleCriteriaLevel3 unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> RoleCriteriaLevel3:
        """Test RoleCriteriaLevel3
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `RoleCriteriaLevel3`
        """
        model = RoleCriteriaLevel3()
        if include_optional:
            return RoleCriteriaLevel3(
                operation = 'EQUALS',
                key = sailpoint.beta.models.role_criteria_key.RoleCriteriaKey(
                    type = 'ACCOUNT', 
                    property = 'attribute.email', 
                    source_id = '2c9180867427f3a301745aec18211519', ),
                string_value = 'carlee.cert1c9f9b6fd@mailinator.com'
            )
        else:
            return RoleCriteriaLevel3(
        )
        """

    def testRoleCriteriaLevel3(self):
        """Test RoleCriteriaLevel3"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
