# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v3.api.access_request_approvals_api import AccessRequestApprovalsApi


class TestAccessRequestApprovalsApi(unittest.TestCase):
    """AccessRequestApprovalsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = AccessRequestApprovalsApi()

    def tearDown(self) -> None:
        pass

    def test_approve_access_request(self) -> None:
        """Test case for approve_access_request

        Approve Access Request Approval
        """
        pass

    def test_forward_access_request(self) -> None:
        """Test case for forward_access_request

        Forward Access Request Approval
        """
        pass

    def test_get_access_request_approval_summary(self) -> None:
        """Test case for get_access_request_approval_summary

        Get Access Requests Approvals Number
        """
        pass

    def test_list_completed_approvals(self) -> None:
        """Test case for list_completed_approvals

        Completed Access Request Approvals List
        """
        pass

    def test_list_pending_approvals(self) -> None:
        """Test case for list_pending_approvals

        Pending Access Request Approvals List
        """
        pass

    def test_reject_access_request(self) -> None:
        """Test case for reject_access_request

        Reject Access Request Approval
        """
        pass


if __name__ == '__main__':
    unittest.main()
