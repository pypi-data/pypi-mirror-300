# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
from enum import Enum
from typing_extensions import Self


class AccountActivityApprovalStatus(str, Enum):
    """
    The state of an approval status
    """

    """
    allowed enum values
    """
    FINISHED = 'FINISHED'
    REJECTED = 'REJECTED'
    RETURNED = 'RETURNED'
    EXPIRED = 'EXPIRED'
    PENDING = 'PENDING'
    CANCELED = 'CANCELED'
    NULL = 'null'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of AccountActivityApprovalStatus from a JSON string"""
        return cls(json.loads(json_str))


