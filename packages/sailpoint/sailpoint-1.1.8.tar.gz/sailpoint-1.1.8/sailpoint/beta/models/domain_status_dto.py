# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class DomainStatusDto(BaseModel):
    """
    Domain status DTO containing everything required to verify via DKIM
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="New UUID associated with domain to be verified")
    domain: Optional[StrictStr] = Field(default=None, description="A domain address")
    dkim_enabled: Optional[Dict[str, Any]] = Field(default=None, description="DKIM is enabled for this domain", alias="dkimEnabled")
    dkim_tokens: Optional[List[StrictStr]] = Field(default=None, description="DKIM tokens required for authentication", alias="dkimTokens")
    dkim_verification_status: Optional[StrictStr] = Field(default=None, description="Status of DKIM authentication", alias="dkimVerificationStatus")
    __properties: ClassVar[List[str]] = ["id", "domain", "dkimEnabled", "dkimTokens", "dkimVerificationStatus"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of DomainStatusDto from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DomainStatusDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "domain": obj.get("domain"),
            "dkimEnabled": obj.get("dkimEnabled"),
            "dkimTokens": obj.get("dkimTokens"),
            "dkimVerificationStatus": obj.get("dkimVerificationStatus")
        })
        return _obj


