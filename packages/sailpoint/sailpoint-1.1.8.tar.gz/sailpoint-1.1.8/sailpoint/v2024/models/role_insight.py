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
from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.role_insights_insight import RoleInsightsInsight
from sailpoint.v2024.models.role_insights_role import RoleInsightsRole
from typing import Optional, Set
from typing_extensions import Self

class RoleInsight(BaseModel):
    """
    RoleInsight
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Insight id")
    number_of_updates: Optional[StrictInt] = Field(default=None, description="Total number of updates for this role", alias="numberOfUpdates")
    created_date: Optional[datetime] = Field(default=None, description="The date-time insights were last created for this role.", alias="createdDate")
    modified_date: Optional[datetime] = Field(default=None, description="The date-time insights were last modified for this role.", alias="modifiedDate")
    role: Optional[RoleInsightsRole] = None
    insight: Optional[RoleInsightsInsight] = None
    __properties: ClassVar[List[str]] = ["id", "numberOfUpdates", "createdDate", "modifiedDate", "role", "insight"]

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
        """Create an instance of RoleInsight from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of role
        if self.role:
            _dict['role'] = self.role.to_dict()
        # override the default output from pydantic by calling `to_dict()` of insight
        if self.insight:
            _dict['insight'] = self.insight.to_dict()
        # set to None if modified_date (nullable) is None
        # and model_fields_set contains the field
        if self.modified_date is None and "modified_date" in self.model_fields_set:
            _dict['modifiedDate'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RoleInsight from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "numberOfUpdates": obj.get("numberOfUpdates"),
            "createdDate": obj.get("createdDate"),
            "modifiedDate": obj.get("modifiedDate"),
            "role": RoleInsightsRole.from_dict(obj["role"]) if obj.get("role") is not None else None,
            "insight": RoleInsightsInsight.from_dict(obj["insight"]) if obj.get("insight") is not None else None
        })
        return _obj


