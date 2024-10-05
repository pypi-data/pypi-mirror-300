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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class ModelField(BaseModel):
    """
    ModelField
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="Name of the FormItem")
    display_name: Optional[StrictStr] = Field(default=None, description="Display name of the field", alias="displayName")
    display_type: Optional[StrictStr] = Field(default=None, description="Type of the field to display", alias="displayType")
    required: Optional[StrictBool] = Field(default=None, description="True if the field is required")
    allowed_values_list: Optional[List[Dict[str, Any]]] = Field(default=None, description="List of allowed values for the field", alias="allowedValuesList")
    value: Optional[Dict[str, Any]] = Field(default=None, description="Value of the field")
    __properties: ClassVar[List[str]] = ["name", "displayName", "displayType", "required", "allowedValuesList", "value"]

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
        """Create an instance of ModelField from a JSON string"""
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
        """Create an instance of ModelField from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "displayName": obj.get("displayName"),
            "displayType": obj.get("displayType"),
            "required": obj.get("required"),
            "allowedValuesList": obj.get("allowedValuesList"),
            "value": obj.get("value")
        })
        return _obj


