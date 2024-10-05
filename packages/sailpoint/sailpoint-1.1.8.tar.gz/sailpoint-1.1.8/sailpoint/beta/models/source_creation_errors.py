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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class SourceCreationErrors(BaseModel):
    """
    SourceCreationErrors
    """ # noqa: E501
    multihost_id: Optional[StrictStr] = Field(default=None, description="Multi-Host Integration ID.")
    source_name: Optional[StrictStr] = Field(default=None, description="Source's human-readable name.")
    source_error: Optional[StrictStr] = Field(default=None, description="Source's human-readable description.")
    created: Optional[datetime] = Field(default=None, description="Date-time when the source was created")
    modified: Optional[datetime] = Field(default=None, description="Date-time when the source was last modified.")
    operation: Optional[StrictStr] = Field(default=None, description="operation category (e.g. DELETE).")
    __properties: ClassVar[List[str]] = ["multihost_id", "source_name", "source_error", "created", "modified", "operation"]

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
        """Create an instance of SourceCreationErrors from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "multihost_id",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if operation (nullable) is None
        # and model_fields_set contains the field
        if self.operation is None and "operation" in self.model_fields_set:
            _dict['operation'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SourceCreationErrors from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "multihost_id": obj.get("multihost_id"),
            "source_name": obj.get("source_name"),
            "source_error": obj.get("source_error"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "operation": obj.get("operation")
        })
        return _obj


