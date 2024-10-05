# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.segments_api import SegmentsApi


class TestSegmentsApi(unittest.TestCase):
    """SegmentsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SegmentsApi()

    def tearDown(self) -> None:
        pass

    def test_create_segment(self) -> None:
        """Test case for create_segment

        Create Segment
        """
        pass

    def test_delete_segment(self) -> None:
        """Test case for delete_segment

        Delete Segment by ID
        """
        pass

    def test_get_segment(self) -> None:
        """Test case for get_segment

        Get Segment by ID
        """
        pass

    def test_list_segments(self) -> None:
        """Test case for list_segments

        List Segments
        """
        pass

    def test_patch_segment(self) -> None:
        """Test case for patch_segment

        Update Segment
        """
        pass


if __name__ == '__main__':
    unittest.main()
