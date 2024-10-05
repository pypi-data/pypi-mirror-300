# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class DtoType(str, Enum):
    """
    An enumeration of the types of DTOs supported within the IdentityNow infrastructure.
    """

    """
    allowed enum values
    """
    ACCOUNT_CORRELATION_CONFIG = 'ACCOUNT_CORRELATION_CONFIG'
    ACCESS_PROFILE = 'ACCESS_PROFILE'
    ACCESS_REQUEST_APPROVAL = 'ACCESS_REQUEST_APPROVAL'
    ACCOUNT = 'ACCOUNT'
    APPLICATION = 'APPLICATION'
    CAMPAIGN = 'CAMPAIGN'
    CAMPAIGN_FILTER = 'CAMPAIGN_FILTER'
    CERTIFICATION = 'CERTIFICATION'
    CLUSTER = 'CLUSTER'
    CONNECTOR_SCHEMA = 'CONNECTOR_SCHEMA'
    ENTITLEMENT = 'ENTITLEMENT'
    GOVERNANCE_GROUP = 'GOVERNANCE_GROUP'
    IDENTITY = 'IDENTITY'
    IDENTITY_PROFILE = 'IDENTITY_PROFILE'
    IDENTITY_REQUEST = 'IDENTITY_REQUEST'
    LIFECYCLE_STATE = 'LIFECYCLE_STATE'
    PASSWORD_POLICY = 'PASSWORD_POLICY'
    ROLE = 'ROLE'
    RULE = 'RULE'
    SOD_POLICY = 'SOD_POLICY'
    SOURCE = 'SOURCE'
    TAG = 'TAG'
    TAG_CATEGORY = 'TAG_CATEGORY'
    TASK_RESULT = 'TASK_RESULT'
    REPORT_RESULT = 'REPORT_RESULT'
    SOD_VIOLATION = 'SOD_VIOLATION'
    ACCOUNT_ACTIVITY = 'ACCOUNT_ACTIVITY'
    WORKGROUP = 'WORKGROUP'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of DtoType from a JSON string"""
        return cls(json.loads(json_str))


