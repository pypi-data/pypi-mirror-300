# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from sailpoint.beta.models.sp_config_import_results import SpConfigImportResults

class TestSpConfigImportResults(unittest.TestCase):
    """SpConfigImportResults unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> SpConfigImportResults:
        """Test SpConfigImportResults
            include_optional is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `SpConfigImportResults`
        """
        model = SpConfigImportResults()
        if include_optional:
            return SpConfigImportResults(
                results = {results={TRIGGER_SUBSCRIPTION={infos=[{key=IMPORT_PREVIEW, text=Object to be imported: [c953134c-2224-42f2-a84e-fa5cbb395904, Test 2], detail=null}, {key=IMPORT_PREVIEW, text=Object to be imported: [be9e116d-08e1-49fc-ab7f-fa585e96c9e4, Test 1], detail=null}], warnings=[], errors=[], importedObjects=[]}}},
                export_job_id = 'be9e116d-08e1-49fc-ab7f-fa585e96c9e4'
            )
        else:
            return SpConfigImportResults(
                results = {results={TRIGGER_SUBSCRIPTION={infos=[{key=IMPORT_PREVIEW, text=Object to be imported: [c953134c-2224-42f2-a84e-fa5cbb395904, Test 2], detail=null}, {key=IMPORT_PREVIEW, text=Object to be imported: [be9e116d-08e1-49fc-ab7f-fa585e96c9e4, Test 1], detail=null}], warnings=[], errors=[], importedObjects=[]}}},
        )
        """

    def testSpConfigImportResults(self):
        """Test SpConfigImportResults"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
