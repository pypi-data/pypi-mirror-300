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


class CertificationPhase(str, Enum):
    """
    The current phase of the campaign. * `STAGED`: The campaign is waiting to be activated. * `ACTIVE`: The campaign is active. * `SIGNED`: The reviewer has signed off on the campaign, and it is considered complete. 
    """

    """
    allowed enum values
    """
    STAGED = 'STAGED'
    ACTIVE = 'ACTIVE'
    SIGNED = 'SIGNED'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of CertificationPhase from a JSON string"""
        return cls(json.loads(json_str))


