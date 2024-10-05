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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.campaign_reference import CampaignReference
from sailpoint.v2024.models.certification_phase import CertificationPhase
from sailpoint.v2024.models.reassignment1 import Reassignment1
from sailpoint.v2024.models.reviewer1 import Reviewer1
from typing import Optional, Set
from typing_extensions import Self

class CertificationDto(BaseModel):
    """
    CertificationDto
    """ # noqa: E501
    campaign_ref: CampaignReference = Field(alias="campaignRef")
    phase: CertificationPhase
    due: datetime = Field(description="The due date of the certification.")
    signed: datetime = Field(description="The date the reviewer signed off on the certification.")
    reviewer: Reviewer1
    reassignment: Optional[Reassignment1] = None
    has_errors: StrictBool = Field(description="Indicates it the certification has any errors.", alias="hasErrors")
    error_message: Optional[StrictStr] = Field(default=None, description="A message indicating what the error is.", alias="errorMessage")
    completed: StrictBool = Field(description="Indicates if all certification decisions have been made.")
    decisions_made: StrictInt = Field(description="The number of approve/revoke/acknowledge decisions that have been made by the reviewer.", alias="decisionsMade")
    decisions_total: StrictInt = Field(description="The total number of approve/revoke/acknowledge decisions for the certification.", alias="decisionsTotal")
    entities_completed: StrictInt = Field(description="The number of entities (identities, access profiles, roles, etc.) for which all decisions have been made and are complete.", alias="entitiesCompleted")
    entities_total: StrictInt = Field(description="The total number of entities (identities, access profiles, roles, etc.) in the certification, both complete and incomplete.", alias="entitiesTotal")
    __properties: ClassVar[List[str]] = ["campaignRef", "phase", "due", "signed", "reviewer", "reassignment", "hasErrors", "errorMessage", "completed", "decisionsMade", "decisionsTotal", "entitiesCompleted", "entitiesTotal"]

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
        """Create an instance of CertificationDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of campaign_ref
        if self.campaign_ref:
            _dict['campaignRef'] = self.campaign_ref.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reviewer
        if self.reviewer:
            _dict['reviewer'] = self.reviewer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of reassignment
        if self.reassignment:
            _dict['reassignment'] = self.reassignment.to_dict()
        # set to None if error_message (nullable) is None
        # and model_fields_set contains the field
        if self.error_message is None and "error_message" in self.model_fields_set:
            _dict['errorMessage'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CertificationDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "campaignRef": CampaignReference.from_dict(obj["campaignRef"]) if obj.get("campaignRef") is not None else None,
            "phase": obj.get("phase"),
            "due": obj.get("due"),
            "signed": obj.get("signed"),
            "reviewer": Reviewer1.from_dict(obj["reviewer"]) if obj.get("reviewer") is not None else None,
            "reassignment": Reassignment1.from_dict(obj["reassignment"]) if obj.get("reassignment") is not None else None,
            "hasErrors": obj.get("hasErrors"),
            "errorMessage": obj.get("errorMessage"),
            "completed": obj.get("completed"),
            "decisionsMade": obj.get("decisionsMade"),
            "decisionsTotal": obj.get("decisionsTotal"),
            "entitiesCompleted": obj.get("entitiesCompleted"),
            "entitiesTotal": obj.get("entitiesTotal")
        })
        return _obj


