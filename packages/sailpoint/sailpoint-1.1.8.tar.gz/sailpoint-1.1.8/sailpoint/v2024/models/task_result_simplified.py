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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class TaskResultSimplified(BaseModel):
    """
    TaskResultSimplified
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Task identifier")
    name: Optional[StrictStr] = Field(default=None, description="Task name")
    description: Optional[StrictStr] = Field(default=None, description="Task description")
    launcher: Optional[StrictStr] = Field(default=None, description="User or process who launched the task")
    completed: Optional[datetime] = Field(default=None, description="Date time of completion")
    launched: Optional[datetime] = Field(default=None, description="Date time when the task was launched")
    completion_status: Optional[StrictStr] = Field(default=None, description="Task result status", alias="completionStatus")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "launcher", "completed", "launched", "completionStatus"]

    @field_validator('completion_status')
    def completion_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['Success', 'Warning', 'Error', 'Terminated', 'TempError']):
            raise ValueError("must be one of enum values ('Success', 'Warning', 'Error', 'Terminated', 'TempError')")
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
        """Create an instance of TaskResultSimplified from a JSON string"""
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
        """Create an instance of TaskResultSimplified from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "launcher": obj.get("launcher"),
            "completed": obj.get("completed"),
            "launched": obj.get("launched"),
            "completionStatus": obj.get("completionStatus")
        })
        return _obj


