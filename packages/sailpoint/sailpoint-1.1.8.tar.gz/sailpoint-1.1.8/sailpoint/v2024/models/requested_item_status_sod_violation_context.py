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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.sod_violation_check_result import SodViolationCheckResult
from typing import Optional, Set
from typing_extensions import Self

class RequestedItemStatusSodViolationContext(BaseModel):
    """
    RequestedItemStatusSodViolationContext
    """ # noqa: E501
    state: Optional[StrictStr] = Field(default=None, description="The status of SOD violation check")
    uuid: Optional[StrictStr] = Field(default=None, description="The id of the Violation check event")
    violation_check_result: Optional[SodViolationCheckResult] = Field(default=None, alias="violationCheckResult")
    __properties: ClassVar[List[str]] = ["state", "uuid", "violationCheckResult"]

    @field_validator('state')
    def state_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['SUCCESS', 'ERROR', 'null']):
            raise ValueError("must be one of enum values ('SUCCESS', 'ERROR', 'null')")
        return value

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
        """Create an instance of RequestedItemStatusSodViolationContext from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of violation_check_result
        if self.violation_check_result:
            _dict['violationCheckResult'] = self.violation_check_result.to_dict()
        # set to None if state (nullable) is None
        # and model_fields_set contains the field
        if self.state is None and "state" in self.model_fields_set:
            _dict['state'] = None

        # set to None if uuid (nullable) is None
        # and model_fields_set contains the field
        if self.uuid is None and "uuid" in self.model_fields_set:
            _dict['uuid'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RequestedItemStatusSodViolationContext from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "state": obj.get("state"),
            "uuid": obj.get("uuid"),
            "violationCheckResult": SodViolationCheckResult.from_dict(obj["violationCheckResult"]) if obj.get("violationCheckResult") is not None else None
        })
        return _obj


