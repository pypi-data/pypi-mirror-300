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
from sailpoint.v2024.models.json_patch_operation_value import JsonPatchOperationValue
from typing import Optional, Set
from typing_extensions import Self

class PatchPotentialRoleRequestInner(BaseModel):
    """
    PatchPotentialRoleRequestInner
    """ # noqa: E501
    op: Optional[StrictStr] = Field(default=None, description="The operation to be performed")
    path: StrictStr = Field(description="A string JSON Pointer representing the target path to an element to be affected by the operation")
    value: Optional[JsonPatchOperationValue] = None
    __properties: ClassVar[List[str]] = ["op", "path", "value"]

    @field_validator('op')
    def op_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['remove', 'replace']):
            raise ValueError("must be one of enum values ('remove', 'replace')")
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
        """Create an instance of PatchPotentialRoleRequestInner from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of value
        if self.value:
            _dict['value'] = self.value.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PatchPotentialRoleRequestInner from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "op": obj.get("op"),
            "path": obj.get("path"),
            "value": JsonPatchOperationValue.from_dict(obj["value"]) if obj.get("value") is not None else None
        })
        return _obj


