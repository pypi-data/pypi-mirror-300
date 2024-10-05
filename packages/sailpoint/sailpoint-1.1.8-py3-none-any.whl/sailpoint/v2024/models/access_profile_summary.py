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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.display_reference import DisplayReference
from sailpoint.v2024.models.dto_type import DtoType
from sailpoint.v2024.models.reference import Reference
from typing import Optional, Set
from typing_extensions import Self

class AccessProfileSummary(BaseModel):
    """
    This is a summary representation of an access profile.
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The unique ID of the referenced object.")
    name: Optional[StrictStr] = Field(default=None, description="The human readable name of the referenced object.")
    display_name: Optional[StrictStr] = Field(default=None, alias="displayName")
    type: Optional[DtoType] = None
    description: Optional[StrictStr] = None
    source: Optional[Reference] = None
    owner: Optional[DisplayReference] = None
    revocable: Optional[StrictBool] = None
    __properties: ClassVar[List[str]] = ["id", "name", "displayName", "type", "description", "source", "owner", "revocable"]

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
        """Create an instance of AccessProfileSummary from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of source
        if self.source:
            _dict['source'] = self.source.to_dict()
        # override the default output from pydantic by calling `to_dict()` of owner
        if self.owner:
            _dict['owner'] = self.owner.to_dict()
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccessProfileSummary from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "displayName": obj.get("displayName"),
            "type": obj.get("type"),
            "description": obj.get("description"),
            "source": Reference.from_dict(obj["source"]) if obj.get("source") is not None else None,
            "owner": DisplayReference.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "revocable": obj.get("revocable")
        })
        return _obj


