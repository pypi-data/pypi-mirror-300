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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.beta.models.common_access_item_access import CommonAccessItemAccess
from typing import Optional, Set
from typing_extensions import Self

class CommonAccessResponse(BaseModel):
    """
    CommonAccessResponse
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique ID of the common access item")
    access: Optional[CommonAccessItemAccess] = None
    status: Optional[StrictStr] = Field(default=None, description="CONFIRMED or DENIED")
    common_access_type: Optional[StrictStr] = Field(default=None, alias="commonAccessType")
    last_updated: Optional[datetime] = Field(default=None, alias="lastUpdated")
    reviewed_by_user: Optional[StrictBool] = Field(default=None, description="true if user has confirmed or denied status", alias="reviewedByUser")
    last_reviewed: Optional[datetime] = Field(default=None, alias="lastReviewed")
    created_by_user: Optional[StrictBool] = Field(default=False, alias="createdByUser")
    __properties: ClassVar[List[str]] = ["id", "access", "status", "commonAccessType", "lastUpdated", "reviewedByUser", "lastReviewed", "createdByUser"]

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
        """Create an instance of CommonAccessResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "last_updated",
            "last_reviewed",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of access
        if self.access:
            _dict['access'] = self.access.to_dict()
        # set to None if last_reviewed (nullable) is None
        # and model_fields_set contains the field
        if self.last_reviewed is None and "last_reviewed" in self.model_fields_set:
            _dict['lastReviewed'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CommonAccessResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "access": CommonAccessItemAccess.from_dict(obj["access"]) if obj.get("access") is not None else None,
            "status": obj.get("status"),
            "commonAccessType": obj.get("commonAccessType"),
            "lastUpdated": obj.get("lastUpdated"),
            "reviewedByUser": obj.get("reviewedByUser"),
            "lastReviewed": obj.get("lastReviewed"),
            "createdByUser": obj.get("createdByUser") if obj.get("createdByUser") is not None else False
        })
        return _obj


