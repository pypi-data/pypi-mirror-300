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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v3.models.sod_policy_conflicting_access_criteria import SodPolicyConflictingAccessCriteria
from sailpoint.v3.models.sod_policy_owner_ref import SodPolicyOwnerRef
from sailpoint.v3.models.violation_owner_assignment_config import ViolationOwnerAssignmentConfig
from typing import Optional, Set
from typing_extensions import Self

class SodPolicy(BaseModel):
    """
    SodPolicy
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Policy id")
    name: Optional[StrictStr] = Field(default=None, description="Policy Business Name")
    created: Optional[datetime] = Field(default=None, description="The time when this SOD policy is created.")
    modified: Optional[datetime] = Field(default=None, description="The time when this SOD policy is modified.")
    description: Optional[StrictStr] = Field(default=None, description="Optional description of the SOD policy")
    owner_ref: Optional[SodPolicyOwnerRef] = Field(default=None, alias="ownerRef")
    external_policy_reference: Optional[StrictStr] = Field(default=None, description="Optional External Policy Reference", alias="externalPolicyReference")
    policy_query: Optional[StrictStr] = Field(default=None, description="Search query of the SOD policy", alias="policyQuery")
    compensating_controls: Optional[StrictStr] = Field(default=None, description="Optional compensating controls(Mitigating Controls)", alias="compensatingControls")
    correction_advice: Optional[StrictStr] = Field(default=None, description="Optional correction advice", alias="correctionAdvice")
    state: Optional[StrictStr] = Field(default=None, description="whether the policy is enforced or not")
    tags: Optional[List[StrictStr]] = Field(default=None, description="tags for this policy object")
    creator_id: Optional[StrictStr] = Field(default=None, description="Policy's creator ID", alias="creatorId")
    modifier_id: Optional[StrictStr] = Field(default=None, description="Policy's modifier ID", alias="modifierId")
    violation_owner_assignment_config: Optional[ViolationOwnerAssignmentConfig] = Field(default=None, alias="violationOwnerAssignmentConfig")
    scheduled: Optional[StrictBool] = Field(default=False, description="defines whether a policy has been scheduled or not")
    type: Optional[StrictStr] = Field(default='GENERAL', description="whether a policy is query based or conflicting access based")
    conflicting_access_criteria: Optional[SodPolicyConflictingAccessCriteria] = Field(default=None, alias="conflictingAccessCriteria")
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "description", "ownerRef", "externalPolicyReference", "policyQuery", "compensatingControls", "correctionAdvice", "state", "tags", "creatorId", "modifierId", "violationOwnerAssignmentConfig", "scheduled", "type", "conflictingAccessCriteria"]

    @field_validator('state')
    def state_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ENFORCED', 'NOT_ENFORCED']):
            raise ValueError("must be one of enum values ('ENFORCED', 'NOT_ENFORCED')")
        return value

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['GENERAL', 'CONFLICTING_ACCESS_BASED']):
            raise ValueError("must be one of enum values ('GENERAL', 'CONFLICTING_ACCESS_BASED')")
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
        """Create an instance of SodPolicy from a JSON string"""
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
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "created",
            "modified",
            "creator_id",
            "modifier_id",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of owner_ref
        if self.owner_ref:
            _dict['ownerRef'] = self.owner_ref.to_dict()
        # override the default output from pydantic by calling `to_dict()` of violation_owner_assignment_config
        if self.violation_owner_assignment_config:
            _dict['violationOwnerAssignmentConfig'] = self.violation_owner_assignment_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of conflicting_access_criteria
        if self.conflicting_access_criteria:
            _dict['conflictingAccessCriteria'] = self.conflicting_access_criteria.to_dict()
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if external_policy_reference (nullable) is None
        # and model_fields_set contains the field
        if self.external_policy_reference is None and "external_policy_reference" in self.model_fields_set:
            _dict['externalPolicyReference'] = None

        # set to None if compensating_controls (nullable) is None
        # and model_fields_set contains the field
        if self.compensating_controls is None and "compensating_controls" in self.model_fields_set:
            _dict['compensatingControls'] = None

        # set to None if correction_advice (nullable) is None
        # and model_fields_set contains the field
        if self.correction_advice is None and "correction_advice" in self.model_fields_set:
            _dict['correctionAdvice'] = None

        # set to None if modifier_id (nullable) is None
        # and model_fields_set contains the field
        if self.modifier_id is None and "modifier_id" in self.model_fields_set:
            _dict['modifierId'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SodPolicy from a dict"""
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
            "ownerRef": SodPolicyOwnerRef.from_dict(obj["ownerRef"]) if obj.get("ownerRef") is not None else None,
            "externalPolicyReference": obj.get("externalPolicyReference"),
            "policyQuery": obj.get("policyQuery"),
            "compensatingControls": obj.get("compensatingControls"),
            "correctionAdvice": obj.get("correctionAdvice"),
            "state": obj.get("state"),
            "tags": obj.get("tags"),
            "creatorId": obj.get("creatorId"),
            "modifierId": obj.get("modifierId"),
            "violationOwnerAssignmentConfig": ViolationOwnerAssignmentConfig.from_dict(obj["violationOwnerAssignmentConfig"]) if obj.get("violationOwnerAssignmentConfig") is not None else None,
            "scheduled": obj.get("scheduled") if obj.get("scheduled") is not None else False,
            "type": obj.get("type") if obj.get("type") is not None else 'GENERAL',
            "conflictingAccessCriteria": SodPolicyConflictingAccessCriteria.from_dict(obj["conflictingAccessCriteria"]) if obj.get("conflictingAccessCriteria") is not None else None
        })
        return _obj


