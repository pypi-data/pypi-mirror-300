# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class RoleMiningSessionState(str, Enum):
    """
    Role mining session status
    """

    """
    allowed enum values
    """
    CREATED = 'CREATED'
    UPDATED = 'UPDATED'
    IDENTITIES_OBTAINED = 'IDENTITIES_OBTAINED'
    PRUNE_THRESHOLD_OBTAINED = 'PRUNE_THRESHOLD_OBTAINED'
    POTENTIAL_ROLES_PROCESSING = 'POTENTIAL_ROLES_PROCESSING'
    POTENTIAL_ROLES_CREATED = 'POTENTIAL_ROLES_CREATED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of RoleMiningSessionState from a JSON string"""
        return cls(json.loads(json_str))


