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

from pydantic import BaseModel, ConfigDict, Field, StrictBool
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.approval_scheme_for_role import ApprovalSchemeForRole
from typing import Optional, Set
from typing_extensions import Self

class RequestabilityForRole(BaseModel):
    """
    RequestabilityForRole
    """ # noqa: E501
    comments_required: Optional[StrictBool] = Field(default=False, description="Whether the requester of the containing object must provide comments justifying the request", alias="commentsRequired")
    denial_comments_required: Optional[StrictBool] = Field(default=False, description="Whether an approver must provide comments when denying the request", alias="denialCommentsRequired")
    approval_schemes: Optional[List[ApprovalSchemeForRole]] = Field(default=None, description="List describing the steps in approving the request", alias="approvalSchemes")
    __properties: ClassVar[List[str]] = ["commentsRequired", "denialCommentsRequired", "approvalSchemes"]

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
        """Create an instance of RequestabilityForRole from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in approval_schemes (list)
        _items = []
        if self.approval_schemes:
            for _item_approval_schemes in self.approval_schemes:
                if _item_approval_schemes:
                    _items.append(_item_approval_schemes.to_dict())
            _dict['approvalSchemes'] = _items
        # set to None if comments_required (nullable) is None
        # and model_fields_set contains the field
        if self.comments_required is None and "comments_required" in self.model_fields_set:
            _dict['commentsRequired'] = None

        # set to None if denial_comments_required (nullable) is None
        # and model_fields_set contains the field
        if self.denial_comments_required is None and "denial_comments_required" in self.model_fields_set:
            _dict['denialCommentsRequired'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RequestabilityForRole from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "commentsRequired": obj.get("commentsRequired") if obj.get("commentsRequired") is not None else False,
            "denialCommentsRequired": obj.get("denialCommentsRequired") if obj.get("denialCommentsRequired") is not None else False,
            "approvalSchemes": [ApprovalSchemeForRole.from_dict(_item) for _item in obj["approvalSchemes"]] if obj.get("approvalSchemes") is not None else None
        })
        return _obj


