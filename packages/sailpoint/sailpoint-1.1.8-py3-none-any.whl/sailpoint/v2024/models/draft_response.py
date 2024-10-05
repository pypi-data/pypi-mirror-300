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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.approval_comment import ApprovalComment
from typing import Optional, Set
from typing_extensions import Self

class DraftResponse(BaseModel):
    """
    DraftResponse
    """ # noqa: E501
    job_id: Optional[StrictStr] = Field(default=None, description="Unique id assigned to this job.", alias="jobId")
    status: Optional[StrictStr] = Field(default=None, description="Status of the job.")
    type: Optional[StrictStr] = Field(default=None, description="Type of the job, will always be CREATE_DRAFT for this type of job.")
    message: Optional[StrictStr] = Field(default=None, description="Message providing information about the outcome of the draft process.")
    requester_name: Optional[StrictStr] = Field(default=None, description="The name of user that that initiated the draft process.", alias="requesterName")
    file_exists: Optional[StrictBool] = Field(default=True, description="Whether or not a file was generated for this draft.", alias="fileExists")
    created: Optional[datetime] = Field(default=None, description="The time the job was started.")
    modified: Optional[datetime] = Field(default=None, description="The time of the last update to the job.")
    completed: Optional[datetime] = Field(default=None, description="The time the job was completed.")
    name: Optional[StrictStr] = Field(default=None, description="Name of the draft.")
    source_tenant: Optional[StrictStr] = Field(default=None, description="Tenant owner of the backup from which the draft was generated.", alias="sourceTenant")
    source_backup_id: Optional[StrictStr] = Field(default=None, description="Id of the backup from which the draft was generated.", alias="sourceBackupId")
    source_backup_name: Optional[StrictStr] = Field(default=None, description="Name of the backup from which the draft was generated.", alias="sourceBackupName")
    mode: Optional[StrictStr] = Field(default=None, description="Denotes the origin of the source backup from which the draft was generated. - RESTORE - Same tenant. - PROMOTE - Different tenant. - UPLOAD - Uploaded configuration.")
    approval_status: Optional[StrictStr] = Field(default=None, description="Approval status of the draft used to determine whether or not the draft can be deployed.", alias="approvalStatus")
    approval_comment: Optional[List[ApprovalComment]] = Field(default=None, description="List of comments that have been exchanged between an approval requester and an approver.", alias="approvalComment")
    __properties: ClassVar[List[str]] = ["jobId", "status", "type", "message", "requesterName", "fileExists", "created", "modified", "completed", "name", "sourceTenant", "sourceBackupId", "sourceBackupName", "mode", "approvalStatus", "approvalComment"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['NOT_STARTED', 'IN_PROGRESS', 'COMPLETE', 'CANCELLED', 'FAILED']):
            raise ValueError("must be one of enum values ('NOT_STARTED', 'IN_PROGRESS', 'COMPLETE', 'CANCELLED', 'FAILED')")
        return value

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['CREATE_DRAFT']):
            raise ValueError("must be one of enum values ('CREATE_DRAFT')")
        return value

    @field_validator('mode')
    def mode_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['RESTORE', 'PROMOTE', 'UPLOAD']):
            raise ValueError("must be one of enum values ('RESTORE', 'PROMOTE', 'UPLOAD')")
        return value

    @field_validator('approval_status')
    def approval_status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['DEFAULT', 'PENDING_APPROVAL', 'APPROVED', 'DENIED']):
            raise ValueError("must be one of enum values ('DEFAULT', 'PENDING_APPROVAL', 'APPROVED', 'DENIED')")
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
        """Create an instance of DraftResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in approval_comment (list)
        _items = []
        if self.approval_comment:
            for _item_approval_comment in self.approval_comment:
                if _item_approval_comment:
                    _items.append(_item_approval_comment.to_dict())
            _dict['approvalComment'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of DraftResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "jobId": obj.get("jobId"),
            "status": obj.get("status"),
            "type": obj.get("type"),
            "message": obj.get("message"),
            "requesterName": obj.get("requesterName"),
            "fileExists": obj.get("fileExists") if obj.get("fileExists") is not None else True,
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "completed": obj.get("completed"),
            "name": obj.get("name"),
            "sourceTenant": obj.get("sourceTenant"),
            "sourceBackupId": obj.get("sourceBackupId"),
            "sourceBackupName": obj.get("sourceBackupName"),
            "mode": obj.get("mode"),
            "approvalStatus": obj.get("approvalStatus"),
            "approvalComment": [ApprovalComment.from_dict(_item) for _item in obj["approvalComment"]] if obj.get("approvalComment") is not None else None
        })
        return _obj


