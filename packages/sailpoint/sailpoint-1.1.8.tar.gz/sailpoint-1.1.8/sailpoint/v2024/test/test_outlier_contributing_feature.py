# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.v2024.models.outlier_contributing_feature import OutlierContributingFeature

class TestOutlierContributingFeature(unittest.TestCase):
    """OutlierContributingFeature unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> OutlierContributingFeature:
        """Test OutlierContributingFeature
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `OutlierContributingFeature`
        """
        model = OutlierContributingFeature()
        if include_optional:
            return OutlierContributingFeature(
                id = '66e38828-5017-47af-92ff-9844871352c5',
                name = 'entitlement_count',
                value_type = 'INTEGER',
                value = 0.92,
                importance = -0.15,
                display_name = 'Number of entitlements',
                description = 'The total number of entitlements belonging to an identity',
                translation_messages = sailpoint.v2024.models.outlier_feature_translation.OutlierFeatureTranslation(
                    display_name = sailpoint.v2024.models.translation_message.TranslationMessage(
                        key = 'recommender-api.V2_WEIGHT_FEATURE_PRODUCT_INTERPRETATION_HIGH', 
                        values = [75, department], ), 
                    description = sailpoint.v2024.models.translation_message.TranslationMessage(
                        key = 'recommender-api.V2_WEIGHT_FEATURE_PRODUCT_INTERPRETATION_HIGH', 
                        values = [75, department], ), )
            )
        else:
            return OutlierContributingFeature(
        )
        """

    def testOutlierContributingFeature(self):
        """Test OutlierContributingFeature"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
