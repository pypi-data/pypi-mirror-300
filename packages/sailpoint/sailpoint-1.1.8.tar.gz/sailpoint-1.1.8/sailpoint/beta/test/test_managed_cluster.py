# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.managed_cluster import ManagedCluster

class TestManagedCluster(unittest.TestCase):
    """ManagedCluster unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ManagedCluster:
        """Test ManagedCluster
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ManagedCluster`
        """
        model = ManagedCluster()
        if include_optional:
            return ManagedCluster(
                id = 'aClusterId',
                name = 'Managed Cluster Name',
                pod = 'megapod-useast1',
                org = 'denali',
                type = 'idn',
                configuration = {clusterExternalId=externalId, ccgVersion=77.0.0},
                key_pair = sailpoint.beta.models.managed_cluster_key_pair.ManagedClusterKeyPair(
                    public_key = '-----BEGIN PUBLIC KEY-----******-----END PUBLIC KEY-----', 
                    public_key_thumbprint = '6CMlaJIV44-xJxcB3CJBjDUUn54', 
                    public_key_certificate = '-----BEGIN CERTIFICATE-----****-----END CERTIFICATE-----', ),
                attributes = sailpoint.beta.models.managed_cluster_attributes.ManagedClusterAttributes(
                    queue = sailpoint.beta.models.managed_cluster_queue.ManagedClusterQueue(
                        name = 'megapod-useast1-denali-lwt-cluster-1533', 
                        region = 'us-east-1', ), 
                    keystore = '/u3+7QAAAAIAAAABAAAAAQAvL3Byb3h5LWNsdXN0ZXIvMmM5MTgwODc3Yjg3MW', ),
                description = 'A short description of the managed cluster.',
                redis = sailpoint.beta.models.managed_cluster_redis.ManagedClusterRedis(
                    redis_host = 'megapod-useast1-shared-redis.cloud.sailpoint.com', 
                    redis_port = 6379, ),
                client_type = 'CCG',
                ccg_version = 'v01',
                pinned_config = False,
                log_configuration = sailpoint.beta.models.client_log_configuration.ClientLogConfiguration(
                    client_id = 'aClientId', 
                    duration_minutes = 120, 
                    expiration = '2020-12-15T19:13:36.079Z', 
                    root_level = 'INFO', 
                    log_levels = INFO, ),
                operational = False,
                status = 'NORMAL',
                public_key_certificate = '-----BEGIN CERTIFICATE-----TCCAb2gAwIBAgIBADANBgkqhkiG9w0BAQsFADAuMQ0wCwYDVQQD-----END CERTIFICATE-----',
                public_key_thumbprint = 'obc6pLiulGbtZ',
                public_key = '-----BEGIN PUBLIC KEY-----jANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3WgnsxP52MDgBTfHR+5n4-----END PUBLIC KEY-----',
                alert_key = 'LIMITED_RESOURCES',
                client_ids = [1244, 1245],
                service_count = 6,
                cc_id = '0',
                created_at = '2023-08-04T20:48:01.865Z',
                updated_at = '2023-08-04T20:48:01.865Z'
            )
        else:
            return ManagedCluster(
                id = 'aClusterId',
                client_type = 'CCG',
                ccg_version = 'v01',
        )
        """

    def testManagedCluster(self):
        """Test ManagedCluster"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
