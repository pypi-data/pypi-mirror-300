# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.va_cluster_status_change_event import VAClusterStatusChangeEvent

class TestVAClusterStatusChangeEvent(unittest.TestCase):
    """VAClusterStatusChangeEvent unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> VAClusterStatusChangeEvent:
        """Test VAClusterStatusChangeEvent
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `VAClusterStatusChangeEvent`
        """
        model = VAClusterStatusChangeEvent()
        if include_optional:
            return VAClusterStatusChangeEvent(
                created = '2020-06-29T22:01:50.474Z',
                type = CLUSTER,
                application = sailpoint.beta.models.va_cluster_status_change_event_application.VAClusterStatusChangeEvent_application(
                    id = '2c9180866166b5b0016167c32ef31a66', 
                    name = 'Production VA Cluster', 
                    attributes = { }, ),
                health_check_result = sailpoint.beta.models.va_cluster_status_change_event_health_check_result.VAClusterStatusChangeEvent_healthCheckResult(
                    message = 'Test Connection failed with exception. Error message - java.lang Exception', 
                    result_type = 'SOURCE_STATE_ERROR_CLUSTER', 
                    status = Succeeded, ),
                previous_health_check_result = sailpoint.beta.models.va_cluster_status_change_event_previous_health_check_result.VAClusterStatusChangeEvent_previousHealthCheckResult(
                    message = 'Test Connection failed with exception. Error message - java.lang Exception', 
                    result_type = 'SOURCE_STATE_ERROR_CLUSTER', 
                    status = Failed, )
            )
        else:
            return VAClusterStatusChangeEvent(
                created = '2020-06-29T22:01:50.474Z',
                type = CLUSTER,
                application = sailpoint.beta.models.va_cluster_status_change_event_application.VAClusterStatusChangeEvent_application(
                    id = '2c9180866166b5b0016167c32ef31a66', 
                    name = 'Production VA Cluster', 
                    attributes = { }, ),
                health_check_result = sailpoint.beta.models.va_cluster_status_change_event_health_check_result.VAClusterStatusChangeEvent_healthCheckResult(
                    message = 'Test Connection failed with exception. Error message - java.lang Exception', 
                    result_type = 'SOURCE_STATE_ERROR_CLUSTER', 
                    status = Succeeded, ),
                previous_health_check_result = sailpoint.beta.models.va_cluster_status_change_event_previous_health_check_result.VAClusterStatusChangeEvent_previousHealthCheckResult(
                    message = 'Test Connection failed with exception. Error message - java.lang Exception', 
                    result_type = 'SOURCE_STATE_ERROR_CLUSTER', 
                    status = Failed, ),
        )
        """

    def testVAClusterStatusChangeEvent(self):
        """Test VAClusterStatusChangeEvent"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
