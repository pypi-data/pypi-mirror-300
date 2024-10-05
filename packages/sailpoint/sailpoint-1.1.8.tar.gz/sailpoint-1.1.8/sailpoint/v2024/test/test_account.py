# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.account import Account

class TestAccount(unittest.TestCase):
    """Account unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> Account:
        """Test Account
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `Account`
        """
        model = Account()
        if include_optional:
            return Account(
                id = 'id12345',
                name = 'aName',
                created = '2015-05-28T14:07:17Z',
                modified = '2015-05-28T14:07:17Z',
                source_id = '2c9180835d2e5168015d32f890ca1581',
                source_name = 'Employees',
                identity_id = '2c9180835d2e5168015d32f890ca1581',
                cloud_lifecycle_state = 'active',
                identity_state = 'ACTIVE',
                connection_type = 'direct',
                type = 'NON_HUMAN',
                attributes = {firstName=SailPoint, lastName=Support, displayName=SailPoint Support},
                authoritative = False,
                description = '',
                disabled = False,
                locked = False,
                native_identity = '552775',
                system_account = False,
                uncorrelated = False,
                uuid = 'slpt.support',
                manually_correlated = False,
                has_entitlements = True,
                identity = sailpoint.v2024.models.base_reference_dto.BaseReferenceDto(
                    type = 'IDENTITY', 
                    id = '2c91808568c529c60168cca6f90c1313', 
                    name = 'William Wilson', ),
                source_owner = sailpoint.v2024.models.account_all_of_source_owner.Account_allOf_sourceOwner(
                    type = 'IDENTITY', 
                    id = '4c5c8534e99445de98eef6c75e25eb01', 
                    name = 'John Cavender', ),
                features = 'ENABLE',
                origin = 'AGGREGATED',
                owner_identity = sailpoint.v2024.models.account_all_of_owner_identity.Account_allOf_ownerIdentity(
                    type = 'IDENTITY', 
                    id = '2c918084660f45d6016617daa9210584', 
                    name = 'Adam Kennedy', ),
                owner_group = sailpoint.v2024.models.account_all_of_owner_group.Account_allOf_ownerGroup(
                    type = 'GOVERNANCE_GROUP', 
                    id = '8d3e0094e99445de98eef6c75e25jc04', 
                    name = 'GovGroup AX17Z', )
            )
        else:
            return Account(
                name = 'aName',
                source_id = '2c9180835d2e5168015d32f890ca1581',
                source_name = 'Employees',
                attributes = {firstName=SailPoint, lastName=Support, displayName=SailPoint Support},
                authoritative = False,
                disabled = False,
                locked = False,
                native_identity = '552775',
                system_account = False,
                uncorrelated = False,
                manually_correlated = False,
                has_entitlements = True,
        )
        """

    def testAccount(self):
        """Test Account"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
