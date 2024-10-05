# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.api.notifications_api import NotificationsApi


class TestNotificationsApi(unittest.TestCase):
    """NotificationsApi unit test stubs"""

    def setUp(self) -> None:
        self.api = NotificationsApi()

    def tearDown(self) -> None:
        pass

    def test_create_domain_dkim(self) -> None:
        """Test case for create_domain_dkim

        Verify domain address via DKIM
        """
        pass

    def test_create_notification_template(self) -> None:
        """Test case for create_notification_template

        Create Notification Template
        """
        pass

    def test_create_verified_from_address(self) -> None:
        """Test case for create_verified_from_address

        Create Verified From Address
        """
        pass

    def test_delete_notification_templates_in_bulk(self) -> None:
        """Test case for delete_notification_templates_in_bulk

        Bulk Delete Notification Templates
        """
        pass

    def test_delete_verified_from_address(self) -> None:
        """Test case for delete_verified_from_address

        Delete Verified From Address
        """
        pass

    def test_get_dkim_attributes(self) -> None:
        """Test case for get_dkim_attributes

        Get DKIM Attributes
        """
        pass

    def test_get_mail_from_attributes(self) -> None:
        """Test case for get_mail_from_attributes

        Get MAIL FROM Attributes
        """
        pass

    def test_get_notification_template(self) -> None:
        """Test case for get_notification_template

        Get Notification Template By Id
        """
        pass

    def test_get_notifications_template_context(self) -> None:
        """Test case for get_notifications_template_context

        Get Notification Template Context
        """
        pass

    def test_list_from_addresses(self) -> None:
        """Test case for list_from_addresses

        List From Addresses
        """
        pass

    def test_list_notification_preferences(self) -> None:
        """Test case for list_notification_preferences

        List Notification Preferences for tenant.
        """
        pass

    def test_list_notification_template_defaults(self) -> None:
        """Test case for list_notification_template_defaults

        List Notification Template Defaults
        """
        pass

    def test_list_notification_templates(self) -> None:
        """Test case for list_notification_templates

        List Notification Templates
        """
        pass

    def test_put_mail_from_attributes(self) -> None:
        """Test case for put_mail_from_attributes

        Change MAIL FROM domain
        """
        pass

    def test_send_test_notification(self) -> None:
        """Test case for send_test_notification

        Send Test Notification
        """
        pass


if __name__ == '__main__':
    unittest.main()
