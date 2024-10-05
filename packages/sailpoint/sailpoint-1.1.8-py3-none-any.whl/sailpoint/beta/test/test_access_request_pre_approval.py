# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.access_request_pre_approval import AccessRequestPreApproval

class TestAccessRequestPreApproval(unittest.TestCase):
    """AccessRequestPreApproval unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AccessRequestPreApproval:
        """Test AccessRequestPreApproval
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AccessRequestPreApproval`
        """
        model = AccessRequestPreApproval()
        if include_optional:
            return AccessRequestPreApproval(
                access_request_id = '2c91808b6ef1d43e016efba0ce470904',
                requested_for = [
                    sailpoint.beta.models.access_item_requested_for_dto.AccessItemRequestedForDto(
                        type = 'IDENTITY', 
                        id = '2c4180a46faadee4016fb4e018c20626', 
                        name = 'Robert Robinson', )
                    ],
                requested_items = [
                    sailpoint.beta.models.access_request_pre_approval_requested_items_inner.AccessRequestPreApproval_requestedItems_inner(
                        id = '2c91808b6ef1d43e016efba0ce470904', 
                        name = 'Engineering Access', 
                        description = 'Access to engineering database', 
                        type = ACCESS_PROFILE, 
                        operation = Add, 
                        comment = 'William needs this access to do his job.', )
                    ],
                requested_by = sailpoint.beta.models.access_item_requester_dto.AccessItemRequesterDto(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20648', 
                    name = 'William Wilson', )
            )
        else:
            return AccessRequestPreApproval(
                access_request_id = '2c91808b6ef1d43e016efba0ce470904',
                requested_for = [
                    sailpoint.beta.models.access_item_requested_for_dto.AccessItemRequestedForDto(
                        type = 'IDENTITY', 
                        id = '2c4180a46faadee4016fb4e018c20626', 
                        name = 'Robert Robinson', )
                    ],
                requested_items = [
                    sailpoint.beta.models.access_request_pre_approval_requested_items_inner.AccessRequestPreApproval_requestedItems_inner(
                        id = '2c91808b6ef1d43e016efba0ce470904', 
                        name = 'Engineering Access', 
                        description = 'Access to engineering database', 
                        type = ACCESS_PROFILE, 
                        operation = Add, 
                        comment = 'William needs this access to do his job.', )
                    ],
                requested_by = sailpoint.beta.models.access_item_requester_dto.AccessItemRequesterDto(
                    type = 'IDENTITY', 
                    id = '2c7180a46faadee4016fb4e018c20648', 
                    name = 'William Wilson', ),
        )
        """

    def testAccessRequestPreApproval(self):
        """Test AccessRequestPreApproval"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
