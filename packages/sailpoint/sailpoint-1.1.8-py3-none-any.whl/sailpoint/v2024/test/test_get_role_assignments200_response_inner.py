# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.get_role_assignments200_response_inner import GetRoleAssignments200ResponseInner

class TestGetRoleAssignments200ResponseInner(unittest.TestCase):
    """GetRoleAssignments200ResponseInner unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> GetRoleAssignments200ResponseInner:
        """Test GetRoleAssignments200ResponseInner
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `GetRoleAssignments200ResponseInner`
        """
        model = GetRoleAssignments200ResponseInner()
        if include_optional:
            return GetRoleAssignments200ResponseInner(
                id = '1cbb0705b38c4226b1334eadd8874086',
                role = sailpoint.v2024.models.base_reference_dto_1.BaseReferenceDto_1(
                    id = 'ff8081814d977c21014da056804a0af3', 
                    name = 'Github', ),
                comments = 'I'm a new Engineer and need this role to do my work',
                assignment_source = 'UI',
                assigner = sailpoint.v2024.models.base_reference_dto_1.BaseReferenceDto_1(
                    id = 'ff8081814d977c21014da056804a0af3', 
                    name = 'Github', ),
                assigned_dimensions = [{id=1acc8ffe5fcf457090de28bee2af36ee, type=DIMENSION, name=Northeast region}],
                assignment_context = sailpoint.v2024.models.assignment_context_dto.AssignmentContextDto(
                    requested = sailpoint.v2024.models.access_request_context.AccessRequestContext(
                        context_attributes = [
                            sailpoint.v2024.models.context_attribute_dto.ContextAttributeDto(
                                attribute = 'location', 
                                value = Austin, 
                                derived = False, )
                            ], ), 
                    matched = [
                        sailpoint.v2024.models.role_match_dto.RoleMatchDto(
                            role_ref = sailpoint.v2024.models.base_reference_dto_1.BaseReferenceDto_1(
                                id = 'ff8081814d977c21014da056804a0af3', 
                                name = 'Github', ), 
                            matched_attributes = [
                                sailpoint.v2024.models.context_attribute_dto.ContextAttributeDto(
                                    attribute = 'location', 
                                    derived = False, )
                                ], )
                        ], 
                    computed_date = 'Wed Feb 14 10:58:42', ),
                account_targets = [
                    sailpoint.v2024.models.role_target_dto.RoleTargetDto(
                        source = sailpoint.v2024.models.base_reference_dto_1.BaseReferenceDto_1(
                            id = 'ff8081814d977c21014da056804a0af3', 
                            name = 'Github', ), 
                        account_info = sailpoint.v2024.models.account_info_dto.AccountInfoDto(
                            native_identity = 'CN=Abby Smith,OU=Austin,OU=Americas,OU=Demo,DC=seri,DC=acme,DC=com', 
                            display_name = 'Abby.Smith', 
                            uuid = '{ad9fc391-246d-40af-b248-b6556a2b7c01}', ), 
                        role_name = 'Marketing', )
                    ],
                remove_date = 'Wed Feb 14 10:58:42'
            )
        else:
            return GetRoleAssignments200ResponseInner(
        )
        """

    def testGetRoleAssignments200ResponseInner(self):
        """Test GetRoleAssignments200ResponseInner"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
