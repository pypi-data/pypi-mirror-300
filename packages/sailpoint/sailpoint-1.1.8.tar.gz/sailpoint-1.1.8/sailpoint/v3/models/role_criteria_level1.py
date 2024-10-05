# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v3.models.role_criteria_key import RoleCriteriaKey
from sailpoint.v3.models.role_criteria_level2 import RoleCriteriaLevel2
from sailpoint.v3.models.role_criteria_operation import RoleCriteriaOperation
from typing import Optional, Set
from typing_extensions import Self

class RoleCriteriaLevel1(BaseModel):
    """
    Defines STANDARD type Role membership
    """ # noqa: E501
    operation: Optional[RoleCriteriaOperation] = None
    key: Optional[RoleCriteriaKey] = None
    string_value: Optional[StrictStr] = Field(default=None, description="String value to test the Identity attribute, Account attribute, or Entitlement specified in the key w/r/t the specified operation. If this criteria is a leaf node, that is, if the operation is one of EQUALS, NOT_EQUALS, CONTAINS, STARTS_WITH, or ENDS_WITH, this field is required. Otherwise, specifying it is an error.", alias="stringValue")
    children: Optional[List[Optional[RoleCriteriaLevel2]]] = Field(default=None, description="Array of child criteria. Required if the operation is AND or OR, otherwise it must be left null. A maximum of three levels of criteria are supported, including leaf nodes. Additionally, AND nodes can only be children or OR nodes and vice-versa.")
    __properties: ClassVar[List[str]] = ["operation", "key", "stringValue", "children"]

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
        """Create an instance of RoleCriteriaLevel1 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of key
        if self.key:
            _dict['key'] = self.key.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in children (list)
        _items = []
        if self.children:
            for _item_children in self.children:
                if _item_children:
                    _items.append(_item_children.to_dict())
            _dict['children'] = _items
        # set to None if key (nullable) is None
        # and model_fields_set contains the field
        if self.key is None and "key" in self.model_fields_set:
            _dict['key'] = None

        # set to None if string_value (nullable) is None
        # and model_fields_set contains the field
        if self.string_value is None and "string_value" in self.model_fields_set:
            _dict['stringValue'] = None

        # set to None if children (nullable) is None
        # and model_fields_set contains the field
        if self.children is None and "children" in self.model_fields_set:
            _dict['children'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RoleCriteriaLevel1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "operation": obj.get("operation"),
            "key": RoleCriteriaKey.from_dict(obj["key"]) if obj.get("key") is not None else None,
            "stringValue": obj.get("stringValue"),
            "children": [RoleCriteriaLevel2.from_dict(_item) for _item in obj["children"]] if obj.get("children") is not None else None
        })
        return _obj


