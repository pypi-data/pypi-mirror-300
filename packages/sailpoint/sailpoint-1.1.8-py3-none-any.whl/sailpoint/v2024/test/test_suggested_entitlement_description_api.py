# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.api.suggested_entitlement_description_api import SuggestedEntitlementDescriptionApi


class TestSuggestedEntitlementDescriptionApi(unittest.TestCase):
    """SuggestedEntitlementDescriptionApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SuggestedEntitlementDescriptionApi()

    def tearDown(self) -> None:
        pass

    def test_get_sed_batch_stats(self) -> None:
        """Test case for get_sed_batch_stats

        Submit Sed Batch Stats Request
        """
        pass

    def test_get_sed_batches(self) -> None:
        """Test case for get_sed_batches

        List Sed Batch Request
        """
        pass

    def test_list_seds(self) -> None:
        """Test case for list_seds

        List Suggested Entitlement Description
        """
        pass

    def test_patch_sed(self) -> None:
        """Test case for patch_sed

        Patch Suggested Entitlement Description
        """
        pass

    def test_submit_sed_approval(self) -> None:
        """Test case for submit_sed_approval

        Submit Bulk Approval Request
        """
        pass

    def test_submit_sed_assignment(self) -> None:
        """Test case for submit_sed_assignment

        Submit Sed Assignment Request
        """
        pass

    def test_submit_sed_batch_request(self) -> None:
        """Test case for submit_sed_batch_request

        Submit Sed Batch Request
        """
        pass


if __name__ == '__main__':
    unittest.main()
