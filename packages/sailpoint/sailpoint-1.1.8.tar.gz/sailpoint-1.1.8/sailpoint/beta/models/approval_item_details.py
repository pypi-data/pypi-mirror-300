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
from sailpoint.beta.models.work_item_state import WorkItemState
from typing import Optional, Set
from typing_extensions import Self

class ApprovalItemDetails(BaseModel):
    """
    ApprovalItemDetails
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The approval item's ID")
    account: Optional[StrictStr] = Field(default=None, description="The account referenced by the approval item")
    application: Optional[StrictStr] = Field(default=None, description="The name of the application/source")
    name: Optional[StrictStr] = Field(default=None, description="The attribute's name")
    operation: Optional[StrictStr] = Field(default=None, description="The attribute's operation")
    value: Optional[StrictStr] = Field(default=None, description="The attribute's value")
    state: Optional[WorkItemState] = None
    __properties: ClassVar[List[str]] = ["id", "account", "application", "name", "operation", "value", "state"]

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
        """Create an instance of ApprovalItemDetails from a JSON string"""
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
        # set to None if account (nullable) is None
        # and model_fields_set contains the field
        if self.account is None and "account" in self.model_fields_set:
            _dict['account'] = None

        # set to None if name (nullable) is None
        # and model_fields_set contains the field
        if self.name is None and "name" in self.model_fields_set:
            _dict['name'] = None

        # set to None if value (nullable) is None
        # and model_fields_set contains the field
        if self.value is None and "value" in self.model_fields_set:
            _dict['value'] = None

        # set to None if state (nullable) is None
        # and model_fields_set contains the field
        if self.state is None and "state" in self.model_fields_set:
            _dict['state'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ApprovalItemDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "account": obj.get("account"),
            "application": obj.get("application"),
            "name": obj.get("name"),
            "operation": obj.get("operation"),
            "value": obj.get("value"),
            "state": obj.get("state")
        })
        return _obj


