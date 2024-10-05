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
from sailpoint.v2024.models.load_uncorrelated_accounts_task_task_attributes import LoadUncorrelatedAccountsTaskTaskAttributes
from sailpoint.v2024.models.load_uncorrelated_accounts_task_task_messages_inner import LoadUncorrelatedAccountsTaskTaskMessagesInner
from typing import Optional, Set
from typing_extensions import Self

class LoadUncorrelatedAccountsTaskTask(BaseModel):
    """
    LoadUncorrelatedAccountsTaskTask
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="System-generated unique ID of the task this taskStatus represents")
    type: Optional[StrictStr] = Field(default=None, description="Type of task this task represents")
    name: Optional[StrictStr] = Field(default=None, description="The name of uncorrelated accounts process")
    description: Optional[StrictStr] = Field(default=None, description="The description of the task")
    launcher: Optional[StrictStr] = Field(default=None, description="The user who initiated the task")
    created: Optional[datetime] = Field(default=None, description="The Task creation date")
    launched: Optional[datetime] = Field(default=None, description="The task start date")
    completed: Optional[datetime] = Field(default=None, description="The task completion date")
    completion_status: Optional[StrictStr] = Field(default=None, description="Task completion status.", alias="completionStatus")
    parent_name: Optional[StrictStr] = Field(default=None, description="Name of the parent task if exists.", alias="parentName")
    messages: Optional[List[LoadUncorrelatedAccountsTaskTaskMessagesInner]] = Field(default=None, description="List of the messages dedicated to the report.  From task definition perspective here usually should be warnings or errors.")
    progress: Optional[StrictStr] = Field(default=None, description="Current task state.")
    attributes: Optional[LoadUncorrelatedAccountsTaskTaskAttributes] = None
    returns: Optional[Dict[str, Any]] = Field(default=None, description="Return values from the task")
    __properties: ClassVar[List[str]] = ["id", "type", "name", "description", "launcher", "created", "launched", "completed", "completionStatus", "parentName", "messages", "progress", "attributes", "returns"]

    @field_validator('completion_status')
    def completion_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['SUCCESS', 'WARNING', 'ERROR', 'TERMINATED', 'TEMP_ERROR']):
            raise ValueError("must be one of enum values ('SUCCESS', 'WARNING', 'ERROR', 'TERMINATED', 'TEMP_ERROR')")
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
        """Create an instance of LoadUncorrelatedAccountsTaskTask from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in messages (list)
        _items = []
        if self.messages:
            for _item_messages in self.messages:
                if _item_messages:
                    _items.append(_item_messages.to_dict())
            _dict['messages'] = _items
        # override the default output from pydantic by calling `to_dict()` of attributes
        if self.attributes:
            _dict['attributes'] = self.attributes.to_dict()
        # set to None if launched (nullable) is None
        # and model_fields_set contains the field
        if self.launched is None and "launched" in self.model_fields_set:
            _dict['launched'] = None

        # set to None if completed (nullable) is None
        # and model_fields_set contains the field
        if self.completed is None and "completed" in self.model_fields_set:
            _dict['completed'] = None

        # set to None if completion_status (nullable) is None
        # and model_fields_set contains the field
        if self.completion_status is None and "completion_status" in self.model_fields_set:
            _dict['completionStatus'] = None

        # set to None if parent_name (nullable) is None
        # and model_fields_set contains the field
        if self.parent_name is None and "parent_name" in self.model_fields_set:
            _dict['parentName'] = None

        # set to None if progress (nullable) is None
        # and model_fields_set contains the field
        if self.progress is None and "progress" in self.model_fields_set:
            _dict['progress'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of LoadUncorrelatedAccountsTaskTask from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "type": obj.get("type"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "launcher": obj.get("launcher"),
            "created": obj.get("created"),
            "launched": obj.get("launched"),
            "completed": obj.get("completed"),
            "completionStatus": obj.get("completionStatus"),
            "parentName": obj.get("parentName"),
            "messages": [LoadUncorrelatedAccountsTaskTaskMessagesInner.from_dict(_item) for _item in obj["messages"]] if obj.get("messages") is not None else None,
            "progress": obj.get("progress"),
            "attributes": LoadUncorrelatedAccountsTaskTaskAttributes.from_dict(obj["attributes"]) if obj.get("attributes") is not None else None,
            "returns": obj.get("returns")
        })
        return _obj


