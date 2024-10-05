# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.selector_account_match_config import SelectorAccountMatchConfig

class TestSelectorAccountMatchConfig(unittest.TestCase):
    """SelectorAccountMatchConfig unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SelectorAccountMatchConfig:
        """Test SelectorAccountMatchConfig
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SelectorAccountMatchConfig`
        """
        model = SelectorAccountMatchConfig()
        if include_optional:
            return SelectorAccountMatchConfig(
                match_expression = sailpoint.beta.models.selector_account_match_config_match_expression.selector_accountMatchConfig_matchExpression(
                    match_terms = [{name=, value=, op=null, container=true, and=false, children=[{name=businessCategory, value=Service, op=eq, container=false, and=false, children=null}]}], 
                    and = True, )
            )
        else:
            return SelectorAccountMatchConfig(
        )
        """

    def testSelectorAccountMatchConfig(self):
        """Test SelectorAccountMatchConfig"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
