# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.source_app_create_dto_account_source import SourceAppCreateDtoAccountSource
from typing import Optional, Set
from typing_extensions import Self

class SourceAppCreateDto(BaseModel):
    """
    SourceAppCreateDto
    """ # noqa: E501
    name: StrictStr = Field(description="The source app name")
    description: StrictStr = Field(description="The description of the source app")
    match_all_accounts: Optional[StrictBool] = Field(default=False, description="True if the source app match all accounts", alias="matchAllAccounts")
    account_source: SourceAppCreateDtoAccountSource = Field(alias="accountSource")
    __properties: ClassVar[List[str]] = ["name", "description", "matchAllAccounts", "accountSource"]

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
        """Create an instance of SourceAppCreateDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of account_source
        if self.account_source:
            _dict['accountSource'] = self.account_source.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SourceAppCreateDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "matchAllAccounts": obj.get("matchAllAccounts") if obj.get("matchAllAccounts") is not None else False,
            "accountSource": SourceAppCreateDtoAccountSource.from_dict(obj["accountSource"]) if obj.get("accountSource") is not None else None
        })
        return _obj


