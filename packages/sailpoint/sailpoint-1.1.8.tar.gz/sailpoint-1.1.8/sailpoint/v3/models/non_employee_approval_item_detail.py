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

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from sailpoint.v3.models.approval_status import ApprovalStatus
from sailpoint.v3.models.non_employee_identity_reference_with_id import NonEmployeeIdentityReferenceWithId
from sailpoint.v3.models.non_employee_request_without_approval_item import NonEmployeeRequestWithoutApprovalItem
from typing import Optional, Set
from typing_extensions import Self

class NonEmployeeApprovalItemDetail(BaseModel):
    """
    NonEmployeeApprovalItemDetail
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Non-Employee approval item id")
    approver: Optional[NonEmployeeIdentityReferenceWithId] = None
    account_name: Optional[StrictStr] = Field(default=None, description="Requested identity account name", alias="accountName")
    approval_status: Optional[ApprovalStatus] = Field(default=None, alias="approvalStatus")
    approval_order: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Approval order", alias="approvalOrder")
    comment: Optional[StrictStr] = Field(default=None, description="comment of approver")
    modified: Optional[datetime] = Field(default=None, description="When the request was last modified.")
    created: Optional[datetime] = Field(default=None, description="When the request was created.")
    non_employee_request: Optional[NonEmployeeRequestWithoutApprovalItem] = Field(default=None, alias="nonEmployeeRequest")
    __properties: ClassVar[List[str]] = ["id", "approver", "accountName", "approvalStatus", "approvalOrder", "comment", "modified", "created", "nonEmployeeRequest"]

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
        """Create an instance of NonEmployeeApprovalItemDetail from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of approver
        if self.approver:
            _dict['approver'] = self.approver.to_dict()
        # override the default output from pydantic by calling `to_dict()` of non_employee_request
        if self.non_employee_request:
            _dict['nonEmployeeRequest'] = self.non_employee_request.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of NonEmployeeApprovalItemDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "approver": NonEmployeeIdentityReferenceWithId.from_dict(obj["approver"]) if obj.get("approver") is not None else None,
            "accountName": obj.get("accountName"),
            "approvalStatus": obj.get("approvalStatus"),
            "approvalOrder": obj.get("approvalOrder"),
            "comment": obj.get("comment"),
            "modified": obj.get("modified"),
            "created": obj.get("created"),
            "nonEmployeeRequest": NonEmployeeRequestWithoutApprovalItem.from_dict(obj["nonEmployeeRequest"]) if obj.get("nonEmployeeRequest") is not None else None
        })
        return _obj


