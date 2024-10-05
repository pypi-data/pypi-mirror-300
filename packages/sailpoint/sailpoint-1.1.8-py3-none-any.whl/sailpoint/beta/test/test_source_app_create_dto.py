# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.source_app_create_dto import SourceAppCreateDto

class TestSourceAppCreateDto(unittest.TestCase):
    """SourceAppCreateDto unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SourceAppCreateDto:
        """Test SourceAppCreateDto
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SourceAppCreateDto`
        """
        model = SourceAppCreateDto()
        if include_optional:
            return SourceAppCreateDto(
                name = 'my app',
                description = 'the source app for engineers',
                match_all_accounts = True,
                account_source = sailpoint.beta.models.source_app_create_dto_account_source.SourceAppCreateDto_accountSource(
                    id = '2c9180827ca885d7017ca8ce28a000eb', 
                    type = 'SOURCE', 
                    name = 'ODS-AD-Source', )
            )
        else:
            return SourceAppCreateDto(
                name = 'my app',
                description = 'the source app for engineers',
                account_source = sailpoint.beta.models.source_app_create_dto_account_source.SourceAppCreateDto_accountSource(
                    id = '2c9180827ca885d7017ca8ce28a000eb', 
                    type = 'SOURCE', 
                    name = 'ODS-AD-Source', ),
        )
        """

    def testSourceAppCreateDto(self):
        """Test SourceAppCreateDto"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
