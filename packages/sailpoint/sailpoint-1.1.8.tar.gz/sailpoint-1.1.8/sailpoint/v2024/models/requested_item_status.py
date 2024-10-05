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
from sailpoint.v2024.models.access_item_requester import AccessItemRequester
from sailpoint.v2024.models.access_request_phases import AccessRequestPhases
from sailpoint.v2024.models.access_request_type import AccessRequestType
from sailpoint.v2024.models.approval_status_dto import ApprovalStatusDto
from sailpoint.v2024.models.error_message_dto import ErrorMessageDto
from sailpoint.v2024.models.manual_work_item_details import ManualWorkItemDetails
from sailpoint.v2024.models.requested_item_status_cancelled_request_details import RequestedItemStatusCancelledRequestDetails
from sailpoint.v2024.models.requested_item_status_pre_approval_trigger_details import RequestedItemStatusPreApprovalTriggerDetails
from sailpoint.v2024.models.requested_item_status_provisioning_details import RequestedItemStatusProvisioningDetails
from sailpoint.v2024.models.requested_item_status_request_state import RequestedItemStatusRequestState
from sailpoint.v2024.models.requested_item_status_requested_for import RequestedItemStatusRequestedFor
from sailpoint.v2024.models.requested_item_status_requester_comment import RequestedItemStatusRequesterComment
from sailpoint.v2024.models.requested_item_status_sod_violation_context import RequestedItemStatusSodViolationContext
from typing import Optional, Set
from typing_extensions import Self

class RequestedItemStatus(BaseModel):
    """
    RequestedItemStatus
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="Human-readable display name of the item being requested.")
    type: Optional[StrictStr] = Field(default=None, description="Type of requested object.")
    cancelled_request_details: Optional[RequestedItemStatusCancelledRequestDetails] = Field(default=None, alias="cancelledRequestDetails")
    error_messages: Optional[List[List[ErrorMessageDto]]] = Field(default=None, description="List of list of localized error messages, if any, encountered during the approval/provisioning process.", alias="errorMessages")
    state: Optional[RequestedItemStatusRequestState] = None
    approval_details: Optional[List[ApprovalStatusDto]] = Field(default=None, description="Approval details for each item.", alias="approvalDetails")
    manual_work_item_details: Optional[List[ManualWorkItemDetails]] = Field(default=None, description="Manual work items created for provisioning the item.", alias="manualWorkItemDetails")
    account_activity_item_id: Optional[StrictStr] = Field(default=None, description="Id of associated account activity item.", alias="accountActivityItemId")
    request_type: Optional[AccessRequestType] = Field(default=None, alias="requestType")
    modified: Optional[datetime] = Field(default=None, description="When the request was last modified.")
    created: Optional[datetime] = Field(default=None, description="When the request was created.")
    requester: Optional[AccessItemRequester] = None
    requested_for: Optional[RequestedItemStatusRequestedFor] = Field(default=None, alias="requestedFor")
    requester_comment: Optional[RequestedItemStatusRequesterComment] = Field(default=None, alias="requesterComment")
    sod_violation_context: Optional[RequestedItemStatusSodViolationContext] = Field(default=None, alias="sodViolationContext")
    provisioning_details: Optional[RequestedItemStatusProvisioningDetails] = Field(default=None, alias="provisioningDetails")
    pre_approval_trigger_details: Optional[RequestedItemStatusPreApprovalTriggerDetails] = Field(default=None, alias="preApprovalTriggerDetails")
    access_request_phases: Optional[List[AccessRequestPhases]] = Field(default=None, description="A list of Phases that the Access Request has gone through in order, to help determine the status of the request.", alias="accessRequestPhases")
    description: Optional[StrictStr] = Field(default=None, description="Description associated to the requested object.")
    remove_date: Optional[datetime] = Field(default=None, description="When the role access is scheduled for removal.", alias="removeDate")
    cancelable: Optional[StrictBool] = Field(default=False, description="True if the request can be canceled.")
    access_request_id: Optional[StrictStr] = Field(default=None, description="This is the account activity id.", alias="accessRequestId")
    client_metadata: Optional[Dict[str, StrictStr]] = Field(default=None, description="Arbitrary key-value pairs, if any were included in the corresponding access request", alias="clientMetadata")
    __properties: ClassVar[List[str]] = ["name", "type", "cancelledRequestDetails", "errorMessages", "state", "approvalDetails", "manualWorkItemDetails", "accountActivityItemId", "requestType", "modified", "created", "requester", "requestedFor", "requesterComment", "sodViolationContext", "provisioningDetails", "preApprovalTriggerDetails", "accessRequestPhases", "description", "removeDate", "cancelable", "accessRequestId", "clientMetadata"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ACCESS_PROFILE', 'ROLE', 'ENTITLEMENT', 'null']):
            raise ValueError("must be one of enum values ('ACCESS_PROFILE', 'ROLE', 'ENTITLEMENT', 'null')")
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
        """Create an instance of RequestedItemStatus from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of cancelled_request_details
        if self.cancelled_request_details:
            _dict['cancelledRequestDetails'] = self.cancelled_request_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in error_messages (list of list)
        _items = []
        if self.error_messages:
            for _item_error_messages in self.error_messages:
                if _item_error_messages:
                    _items.append(
                         [_inner_item.to_dict() for _inner_item in _item_error_messages if _inner_item is not None]
                    )
            _dict['errorMessages'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in approval_details (list)
        _items = []
        if self.approval_details:
            for _item_approval_details in self.approval_details:
                if _item_approval_details:
                    _items.append(_item_approval_details.to_dict())
            _dict['approvalDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in manual_work_item_details (list)
        _items = []
        if self.manual_work_item_details:
            for _item_manual_work_item_details in self.manual_work_item_details:
                if _item_manual_work_item_details:
                    _items.append(_item_manual_work_item_details.to_dict())
            _dict['manualWorkItemDetails'] = _items
        # override the default output from pydantic by calling `to_dict()` of requester
        if self.requester:
            _dict['requester'] = self.requester.to_dict()
        # override the default output from pydantic by calling `to_dict()` of requested_for
        if self.requested_for:
            _dict['requestedFor'] = self.requested_for.to_dict()
        # override the default output from pydantic by calling `to_dict()` of requester_comment
        if self.requester_comment:
            _dict['requesterComment'] = self.requester_comment.to_dict()
        # override the default output from pydantic by calling `to_dict()` of sod_violation_context
        if self.sod_violation_context:
            _dict['sodViolationContext'] = self.sod_violation_context.to_dict()
        # override the default output from pydantic by calling `to_dict()` of provisioning_details
        if self.provisioning_details:
            _dict['provisioningDetails'] = self.provisioning_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of pre_approval_trigger_details
        if self.pre_approval_trigger_details:
            _dict['preApprovalTriggerDetails'] = self.pre_approval_trigger_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in access_request_phases (list)
        _items = []
        if self.access_request_phases:
            for _item_access_request_phases in self.access_request_phases:
                if _item_access_request_phases:
                    _items.append(_item_access_request_phases.to_dict())
            _dict['accessRequestPhases'] = _items
        # set to None if name (nullable) is None
        # and model_fields_set contains the field
        if self.name is None and "name" in self.model_fields_set:
            _dict['name'] = None

        # set to None if type (nullable) is None
        # and model_fields_set contains the field
        if self.type is None and "type" in self.model_fields_set:
            _dict['type'] = None

        # set to None if error_messages (nullable) is None
        # and model_fields_set contains the field
        if self.error_messages is None and "error_messages" in self.model_fields_set:
            _dict['errorMessages'] = None

        # set to None if manual_work_item_details (nullable) is None
        # and model_fields_set contains the field
        if self.manual_work_item_details is None and "manual_work_item_details" in self.model_fields_set:
            _dict['manualWorkItemDetails'] = None

        # set to None if request_type (nullable) is None
        # and model_fields_set contains the field
        if self.request_type is None and "request_type" in self.model_fields_set:
            _dict['requestType'] = None

        # set to None if modified (nullable) is None
        # and model_fields_set contains the field
        if self.modified is None and "modified" in self.model_fields_set:
            _dict['modified'] = None

        # set to None if access_request_phases (nullable) is None
        # and model_fields_set contains the field
        if self.access_request_phases is None and "access_request_phases" in self.model_fields_set:
            _dict['accessRequestPhases'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if remove_date (nullable) is None
        # and model_fields_set contains the field
        if self.remove_date is None and "remove_date" in self.model_fields_set:
            _dict['removeDate'] = None

        # set to None if client_metadata (nullable) is None
        # and model_fields_set contains the field
        if self.client_metadata is None and "client_metadata" in self.model_fields_set:
            _dict['clientMetadata'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RequestedItemStatus from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "type": obj.get("type"),
            "cancelledRequestDetails": RequestedItemStatusCancelledRequestDetails.from_dict(obj["cancelledRequestDetails"]) if obj.get("cancelledRequestDetails") is not None else None,
            "errorMessages": [
                    [ErrorMessageDto.from_dict(_inner_item) for _inner_item in _item]
                    for _item in obj["errorMessages"]
                ] if obj.get("errorMessages") is not None else None,
            "state": obj.get("state"),
            "approvalDetails": [ApprovalStatusDto.from_dict(_item) for _item in obj["approvalDetails"]] if obj.get("approvalDetails") is not None else None,
            "manualWorkItemDetails": [ManualWorkItemDetails.from_dict(_item) for _item in obj["manualWorkItemDetails"]] if obj.get("manualWorkItemDetails") is not None else None,
            "accountActivityItemId": obj.get("accountActivityItemId"),
            "requestType": obj.get("requestType"),
            "modified": obj.get("modified"),
            "created": obj.get("created"),
            "requester": AccessItemRequester.from_dict(obj["requester"]) if obj.get("requester") is not None else None,
            "requestedFor": RequestedItemStatusRequestedFor.from_dict(obj["requestedFor"]) if obj.get("requestedFor") is not None else None,
            "requesterComment": RequestedItemStatusRequesterComment.from_dict(obj["requesterComment"]) if obj.get("requesterComment") is not None else None,
            "sodViolationContext": RequestedItemStatusSodViolationContext.from_dict(obj["sodViolationContext"]) if obj.get("sodViolationContext") is not None else None,
            "provisioningDetails": RequestedItemStatusProvisioningDetails.from_dict(obj["provisioningDetails"]) if obj.get("provisioningDetails") is not None else None,
            "preApprovalTriggerDetails": RequestedItemStatusPreApprovalTriggerDetails.from_dict(obj["preApprovalTriggerDetails"]) if obj.get("preApprovalTriggerDetails") is not None else None,
            "accessRequestPhases": [AccessRequestPhases.from_dict(_item) for _item in obj["accessRequestPhases"]] if obj.get("accessRequestPhases") is not None else None,
            "description": obj.get("description"),
            "removeDate": obj.get("removeDate"),
            "cancelable": obj.get("cancelable") if obj.get("cancelable") is not None else False,
            "accessRequestId": obj.get("accessRequestId"),
            "clientMetadata": obj.get("clientMetadata")
        })
        return _obj


