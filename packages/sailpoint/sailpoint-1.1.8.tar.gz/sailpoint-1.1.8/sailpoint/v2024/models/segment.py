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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.owner_reference_segments import OwnerReferenceSegments
from sailpoint.v2024.models.segment_visibility_criteria import SegmentVisibilityCriteria
from typing import Optional, Set
from typing_extensions import Self

class Segment(BaseModel):
    """
    Segment
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The segment's ID.")
    name: Optional[StrictStr] = Field(default=None, description="The segment's business name.")
    created: Optional[datetime] = Field(default=None, description="The time when the segment is created.")
    modified: Optional[datetime] = Field(default=None, description="The time when the segment is modified.")
    description: Optional[StrictStr] = Field(default=None, description="The segment's optional description.")
    owner: Optional[OwnerReferenceSegments] = None
    visibility_criteria: Optional[SegmentVisibilityCriteria] = Field(default=None, alias="visibilityCriteria")
    active: Optional[StrictBool] = Field(default=False, description="This boolean indicates whether the segment is currently active. Inactive segments have no effect.")
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "description", "owner", "visibilityCriteria", "active"]

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
        """Create an instance of Segment from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of owner
        if self.owner:
            _dict['owner'] = self.owner.to_dict()
        # override the default output from pydantic by calling `to_dict()` of visibility_criteria
        if self.visibility_criteria:
            _dict['visibilityCriteria'] = self.visibility_criteria.to_dict()
        # set to None if owner (nullable) is None
        # and model_fields_set contains the field
        if self.owner is None and "owner" in self.model_fields_set:
            _dict['owner'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Segment from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "description": obj.get("description"),
            "owner": OwnerReferenceSegments.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "visibilityCriteria": SegmentVisibilityCriteria.from_dict(obj["visibilityCriteria"]) if obj.get("visibilityCriteria") is not None else None,
            "active": obj.get("active") if obj.get("active") is not None else False
        })
        return _obj


