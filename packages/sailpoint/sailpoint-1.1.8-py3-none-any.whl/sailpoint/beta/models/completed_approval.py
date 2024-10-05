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
from sailpoint.beta.models.access_item_owner_dto import AccessItemOwnerDto
from sailpoint.beta.models.access_item_requester_dto import AccessItemRequesterDto
from sailpoint.beta.models.access_request_type import AccessRequestType
from sailpoint.beta.models.approval_forward_history import ApprovalForwardHistory
from sailpoint.beta.models.comment_dto import CommentDto
from sailpoint.beta.models.comment_dto1 import CommentDto1
from sailpoint.beta.models.completed_approval_pre_approval_trigger_result import CompletedApprovalPreApprovalTriggerResult
from sailpoint.beta.models.completed_approval_reviewed_by import CompletedApprovalReviewedBy
from sailpoint.beta.models.completed_approval_state import CompletedApprovalState
from sailpoint.beta.models.requestable_object_reference import RequestableObjectReference
from sailpoint.beta.models.requested_item_status_requested_for import RequestedItemStatusRequestedFor
from sailpoint.beta.models.sod_violation_context_check_completed1 import SodViolationContextCheckCompleted1
from typing import Optional, Set
from typing_extensions import Self

class CompletedApproval(BaseModel):
    """
    CompletedApproval
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The approval id.")
    name: Optional[StrictStr] = Field(default=None, description="The name of the approval.")
    created: Optional[datetime] = Field(default=None, description="When the approval was created.")
    modified: Optional[datetime] = Field(default=None, description="When the approval was modified last time.")
    request_created: Optional[datetime] = Field(default=None, description="When the access-request was created.", alias="requestCreated")
    request_type: Optional[AccessRequestType] = Field(default=None, alias="requestType")
    requester: Optional[AccessItemRequesterDto] = None
    requested_for: Optional[RequestedItemStatusRequestedFor] = Field(default=None, alias="requestedFor")
    reviewed_by: Optional[CompletedApprovalReviewedBy] = Field(default=None, alias="reviewedBy")
    owner: Optional[AccessItemOwnerDto] = None
    requested_object: Optional[RequestableObjectReference] = Field(default=None, alias="requestedObject")
    requester_comment: Optional[CommentDto1] = Field(default=None, alias="requesterComment")
    reviewer_comment: Optional[CommentDto] = Field(default=None, description="The approval's reviewer's comment.", alias="reviewerComment")
    previous_reviewers_comments: Optional[List[CommentDto1]] = Field(default=None, description="The history of the previous reviewers comments.", alias="previousReviewersComments")
    forward_history: Optional[List[ApprovalForwardHistory]] = Field(default=None, description="The history of approval forward action.", alias="forwardHistory")
    comment_required_when_rejected: Optional[StrictBool] = Field(default=False, description="When true the rejector has to provide comments when rejecting", alias="commentRequiredWhenRejected")
    state: Optional[CompletedApprovalState] = None
    remove_date: Optional[datetime] = Field(default=None, description="The date the role or access profile or entitlement is no longer assigned to the specified identity.", alias="removeDate")
    remove_date_update_requested: Optional[StrictBool] = Field(default=False, description="If true, then the request was to change the remove date or sunset date.", alias="removeDateUpdateRequested")
    current_remove_date: Optional[datetime] = Field(default=None, description="The remove date or sunset date that was assigned at the time of the request.", alias="currentRemoveDate")
    sod_violation_context: Optional[SodViolationContextCheckCompleted1] = Field(default=None, alias="sodViolationContext")
    pre_approval_trigger_result: Optional[CompletedApprovalPreApprovalTriggerResult] = Field(default=None, alias="preApprovalTriggerResult")
    client_metadata: Optional[Dict[str, StrictStr]] = Field(default=None, description="Arbitrary key-value pairs provided during the request.", alias="clientMetadata")
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "requestCreated", "requestType", "requester", "requestedFor", "reviewedBy", "owner", "requestedObject", "requesterComment", "reviewerComment", "previousReviewersComments", "forwardHistory", "commentRequiredWhenRejected", "state", "removeDate", "removeDateUpdateRequested", "currentRemoveDate", "sodViolationContext", "preApprovalTriggerResult", "clientMetadata"]

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
        """Create an instance of CompletedApproval from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of requester
        if self.requester:
            _dict['requester'] = self.requester.to_dict()
        # override the default output from pydantic by calling `to_dict()` of requested_for
        if self.requested_for:
            _dict['requestedFor'] = self.requested_for.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reviewed_by
        if self.reviewed_by:
            _dict['reviewedBy'] = self.reviewed_by.to_dict()
        # override the default output from pydantic by calling `to_dict()` of owner
        if self.owner:
            _dict['owner'] = self.owner.to_dict()
        # override the default output from pydantic by calling `to_dict()` of requested_object
        if self.requested_object:
            _dict['requestedObject'] = self.requested_object.to_dict()
        # override the default output from pydantic by calling `to_dict()` of requester_comment
        if self.requester_comment:
            _dict['requesterComment'] = self.requester_comment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reviewer_comment
        if self.reviewer_comment:
            _dict['reviewerComment'] = self.reviewer_comment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in previous_reviewers_comments (list)
        _items = []
        if self.previous_reviewers_comments:
            for _item_previous_reviewers_comments in self.previous_reviewers_comments:
                if _item_previous_reviewers_comments:
                    _items.append(_item_previous_reviewers_comments.to_dict())
            _dict['previousReviewersComments'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in forward_history (list)
        _items = []
        if self.forward_history:
            for _item_forward_history in self.forward_history:
                if _item_forward_history:
                    _items.append(_item_forward_history.to_dict())
            _dict['forwardHistory'] = _items
        # override the default output from pydantic by calling `to_dict()` of sod_violation_context
        if self.sod_violation_context:
            _dict['sodViolationContext'] = self.sod_violation_context.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pre_approval_trigger_result
        if self.pre_approval_trigger_result:
            _dict['preApprovalTriggerResult'] = self.pre_approval_trigger_result.to_dict()
        # set to None if request_type (nullable) is None
        # and model_fields_set contains the field
        if self.request_type is None and "request_type" in self.model_fields_set:
            _dict['requestType'] = None

        # set to None if reviewer_comment (nullable) is None
        # and model_fields_set contains the field
        if self.reviewer_comment is None and "reviewer_comment" in self.model_fields_set:
            _dict['reviewerComment'] = None

        # set to None if remove_date (nullable) is None
        # and model_fields_set contains the field
        if self.remove_date is None and "remove_date" in self.model_fields_set:
            _dict['removeDate'] = None

        # set to None if current_remove_date (nullable) is None
        # and model_fields_set contains the field
        if self.current_remove_date is None and "current_remove_date" in self.model_fields_set:
            _dict['currentRemoveDate'] = None

        # set to None if sod_violation_context (nullable) is None
        # and model_fields_set contains the field
        if self.sod_violation_context is None and "sod_violation_context" in self.model_fields_set:
            _dict['sodViolationContext'] = None

        # set to None if pre_approval_trigger_result (nullable) is None
        # and model_fields_set contains the field
        if self.pre_approval_trigger_result is None and "pre_approval_trigger_result" in self.model_fields_set:
            _dict['preApprovalTriggerResult'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CompletedApproval from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "requestCreated": obj.get("requestCreated"),
            "requestType": obj.get("requestType"),
            "requester": AccessItemRequesterDto.from_dict(obj["requester"]) if obj.get("requester") is not None else None,
            "requestedFor": RequestedItemStatusRequestedFor.from_dict(obj["requestedFor"]) if obj.get("requestedFor") is not None else None,
            "reviewedBy": CompletedApprovalReviewedBy.from_dict(obj["reviewedBy"]) if obj.get("reviewedBy") is not None else None,
            "owner": AccessItemOwnerDto.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "requestedObject": RequestableObjectReference.from_dict(obj["requestedObject"]) if obj.get("requestedObject") is not None else None,
            "requesterComment": CommentDto1.from_dict(obj["requesterComment"]) if obj.get("requesterComment") is not None else None,
            "reviewerComment": CommentDto.from_dict(obj["reviewerComment"]) if obj.get("reviewerComment") is not None else None,
            "previousReviewersComments": [CommentDto1.from_dict(_item) for _item in obj["previousReviewersComments"]] if obj.get("previousReviewersComments") is not None else None,
            "forwardHistory": [ApprovalForwardHistory.from_dict(_item) for _item in obj["forwardHistory"]] if obj.get("forwardHistory") is not None else None,
            "commentRequiredWhenRejected": obj.get("commentRequiredWhenRejected") if obj.get("commentRequiredWhenRejected") is not None else False,
            "state": obj.get("state"),
            "removeDate": obj.get("removeDate"),
            "removeDateUpdateRequested": obj.get("removeDateUpdateRequested") if obj.get("removeDateUpdateRequested") is not None else False,
            "currentRemoveDate": obj.get("currentRemoveDate"),
            "sodViolationContext": SodViolationContextCheckCompleted1.from_dict(obj["sodViolationContext"]) if obj.get("sodViolationContext") is not None else None,
            "preApprovalTriggerResult": CompletedApprovalPreApprovalTriggerResult.from_dict(obj["preApprovalTriggerResult"]) if obj.get("preApprovalTriggerResult") is not None else None,
            "clientMetadata": obj.get("clientMetadata")
        })
        return _obj


