# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.api.sp_config_api import SPConfigApi


class TestSPConfigApi(unittest.TestCase):
    """SPConfigApi unit test stubs"""

    def setUp(self) -> None:
        self.api = SPConfigApi()

    def tearDown(self) -> None:
        pass

    def test_export_sp_config(self) -> None:
        """Test case for export_sp_config

        Initiates configuration objects export job
        """
        pass

    def test_get_sp_config_export(self) -> None:
        """Test case for get_sp_config_export

        Download export job result.
        """
        pass

    def test_get_sp_config_export_status(self) -> None:
        """Test case for get_sp_config_export_status

        Get export job status
        """
        pass

    def test_get_sp_config_import(self) -> None:
        """Test case for get_sp_config_import

        Download import job result
        """
        pass

    def test_get_sp_config_import_status(self) -> None:
        """Test case for get_sp_config_import_status

        Get import job status
        """
        pass

    def test_import_sp_config(self) -> None:
        """Test case for import_sp_config

        Initiates configuration objects import job
        """
        pass

    def test_list_sp_config_objects(self) -> None:
        """Test case for list_sp_config_objects

        Get config object details
        """
        pass


if __name__ == '__main__':
    unittest.main()
