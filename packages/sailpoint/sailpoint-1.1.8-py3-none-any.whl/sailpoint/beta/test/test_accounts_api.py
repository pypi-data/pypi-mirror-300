# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.accounts_api import AccountsApi


class TestAccountsApi(unittest.TestCase):
    """AccountsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = AccountsApi()

    def tearDown(self) -> None:
        pass

    def test_create_account(self) -> None:
        """Test case for create_account

        Create Account
        """
        pass

    def test_delete_account(self) -> None:
        """Test case for delete_account

        Delete Account
        """
        pass

    def test_delete_account_async(self) -> None:
        """Test case for delete_account_async

        Remove Account
        """
        pass

    def test_disable_account(self) -> None:
        """Test case for disable_account

        Disable Account
        """
        pass

    def test_disable_account_for_identity(self) -> None:
        """Test case for disable_account_for_identity

        Disable IDN Account for Identity
        """
        pass

    def test_disable_accounts_for_identities(self) -> None:
        """Test case for disable_accounts_for_identities

        Disable IDN Accounts for Identities
        """
        pass

    def test_enable_account(self) -> None:
        """Test case for enable_account

        Enable Account
        """
        pass

    def test_enable_account_for_identity(self) -> None:
        """Test case for enable_account_for_identity

        Enable IDN Account for Identity
        """
        pass

    def test_enable_accounts_for_identities(self) -> None:
        """Test case for enable_accounts_for_identities

        Enable IDN Accounts for Identities
        """
        pass

    def test_get_account(self) -> None:
        """Test case for get_account

        Account Details
        """
        pass

    def test_get_account_entitlements(self) -> None:
        """Test case for get_account_entitlements

        Account Entitlements
        """
        pass

    def test_list_accounts(self) -> None:
        """Test case for list_accounts

        Accounts List
        """
        pass

    def test_put_account(self) -> None:
        """Test case for put_account

        Update Account
        """
        pass

    def test_submit_reload_account(self) -> None:
        """Test case for submit_reload_account

        Reload Account
        """
        pass

    def test_unlock_account(self) -> None:
        """Test case for unlock_account

        Unlock Account
        """
        pass

    def test_update_account(self) -> None:
        """Test case for update_account

        Update Account
        """
        pass


if __name__ == '__main__':
    unittest.main()
