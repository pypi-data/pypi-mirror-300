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

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from typing import Optional, Set
from typing_extensions import Self

class PasswordOrgConfig(BaseModel):
    """
    PasswordOrgConfig
    """ # noqa: E501
    custom_instructions_enabled: Optional[StrictBool] = Field(default=False, description="Indicator whether custom password instructions feature is enabled. The default value is false.", alias="customInstructionsEnabled")
    digit_token_enabled: Optional[StrictBool] = Field(default=False, description="Indicator whether \"digit token\" feature is enabled. The default value is false.", alias="digitTokenEnabled")
    digit_token_duration_minutes: Optional[Annotated[int, Field(le=60, strict=True, ge=1)]] = Field(default=5, description="The duration of \"digit token\" in minutes. The default value is 5.", alias="digitTokenDurationMinutes")
    digit_token_length: Optional[Annotated[int, Field(le=18, strict=True, ge=6)]] = Field(default=6, description="The length of \"digit token\". The default value is 6.", alias="digitTokenLength")
    __properties: ClassVar[List[str]] = ["customInstructionsEnabled", "digitTokenEnabled", "digitTokenDurationMinutes", "digitTokenLength"]

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
        """Create an instance of PasswordOrgConfig from a JSON string"""
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
        """Create an instance of PasswordOrgConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "customInstructionsEnabled": obj.get("customInstructionsEnabled") if obj.get("customInstructionsEnabled") is not None else False,
            "digitTokenEnabled": obj.get("digitTokenEnabled") if obj.get("digitTokenEnabled") is not None else False,
            "digitTokenDurationMinutes": obj.get("digitTokenDurationMinutes") if obj.get("digitTokenDurationMinutes") is not None else 5,
            "digitTokenLength": obj.get("digitTokenLength") if obj.get("digitTokenLength") is not None else 6
        })
        return _obj


