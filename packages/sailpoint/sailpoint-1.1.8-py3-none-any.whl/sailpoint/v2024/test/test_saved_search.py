# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.saved_search import SavedSearch

class TestSavedSearch(unittest.TestCase):
    """SavedSearch unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SavedSearch:
        """Test SavedSearch
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SavedSearch`
        """
        model = SavedSearch()
        if include_optional:
            return SavedSearch(
                name = 'Disabled accounts',
                description = 'Disabled accounts',
                created = '2018-06-25T20:22:28.104Z',
                modified = '2018-06-25T20:22:28.104Z',
                indices = [identities],
                columns = {identity=[{field=displayName, header=Display Name}, {field=e-mail, header=Work Email}]},
                query = '@accounts(disabled:true)',
                fields = [disabled],
                order_by = {identity=[lastName, firstName], role=[name]},
                sort = [displayName],
                filters = None,
                id = '0de46054-fe90-434a-b84e-c6b3359d0c64',
                owner = sailpoint.v2024.models.typed_reference.TypedReference(
                    type = 'IDENTITY', 
                    id = '2c91808568c529c60168cca6f90c1313', ),
                owner_id = '2c91808568c529c60168cca6f90c1313',
                public = False
            )
        else:
            return SavedSearch(
                indices = [identities],
                query = '@accounts(disabled:true)',
        )
        """

    def testSavedSearch(self):
        """Test SavedSearch"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
