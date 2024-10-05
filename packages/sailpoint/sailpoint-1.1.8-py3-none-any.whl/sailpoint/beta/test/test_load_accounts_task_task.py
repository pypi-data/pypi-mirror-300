# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.load_accounts_task_task import LoadAccountsTaskTask

class TestLoadAccountsTaskTask(unittest.TestCase):
    """LoadAccountsTaskTask unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> LoadAccountsTaskTask:
        """Test LoadAccountsTaskTask
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `LoadAccountsTaskTask`
        """
        model = LoadAccountsTaskTask()
        if include_optional:
            return LoadAccountsTaskTask(
                id = 'ef38f94347e94562b5bb8424a56397d8',
                type = 'QUARTZ',
                name = 'Cloud Account Aggregation',
                description = 'Aggregate from the specified application',
                launcher = 'John Doe',
                created = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                launched = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                completed = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'),
                completion_status = 'Success',
                parent_name = 'Audit Report',
                messages = [],
                progress = 'Initializing...',
                attributes = {
                    'key' : None
                    },
                returns = [
                    [{displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_APPLICATIONS, attributeName=applications}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_TOTAL, attributeName=total}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_OPTIMIZED, attributeName=optimizedAggregation}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_IGNORED, attributeName=ignored}, {displayLabel=TASK_OUT_UNCHANGED_ACCOUNTS, attributeName=optimized}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_CREATED, attributeName=created}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_UPDATED, attributeName=updated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_DELETED, attributeName=deleted}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_MANAGER_CHANGES, attributeName=managerChanges}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_BUSINESS_ROLE_CHANGES, attributeName=detectedRoleChanges}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_EXCEPTION_CHANGES, attributeName=exceptionChanges}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_POLICIES, attributeName=policies}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_POLICY_VIOLATIONS, attributeName=policyViolations}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_POLICY_NOTIFICATIONS, attributeName=policyNotifications}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_SCORES_CHANGED, attributeName=scoresChanged}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_SNAPSHOTS_CREATED, attributeName=snapshotsCreated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_SCOPES_CREATED, attributeName=scopesCreated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_SCOPES_CORRELATED, attributeName=scopesCorrelated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_SCOPES_SELECTED, attributeName=scopesSelected}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_SCOPES_DORMANT, attributeName=scopesDormant}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_UNSCOPED_IDENTITIES, attributeName=unscopedIdentities}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_CERTIFICATIONS_CREATED, attributeName=certificationsCreated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_CERTIFICATIONS_DELETED, attributeName=certificationsDeleted}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_APPLICATIONS_GENERATED, attributeName=applicationsGenerated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_MANAGED_ATTRIBUTES_PROMOTED, attributeName=managedAttributesCreated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_MANAGED_ATTRIBUTES_PROMOTED_BY_APP, attributeName=managedAttributesCreatedByApplication}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_IDENTITYENTITLEMENTS_CREATED, attributeName=identityEntitlementsCreated}, {displayLabel=TASK_OUT_ACCOUNT_AGGREGATION_GROUPS_CREATED, attributeName=groupsCreated}]
                    ]
            )
        else:
            return LoadAccountsTaskTask(
        )
        """

    def testLoadAccountsTaskTask(self):
        """Test LoadAccountsTaskTask"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
