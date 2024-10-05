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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.beta.models.error_message_dto import ErrorMessageDto
from sailpoint.beta.models.sod_policy_dto import SodPolicyDto
from sailpoint.beta.models.sod_violation_context1 import SodViolationContext1
from typing import Optional, Set
from typing_extensions import Self

class SodViolationCheckResult1(BaseModel):
    """
    The inner object representing the completed SOD Violation check
    """ # noqa: E501
    message: Optional[ErrorMessageDto] = None
    client_metadata: Optional[Dict[str, StrictStr]] = Field(default=None, description="Arbitrary key-value pairs. They will never be processed by the IdentityNow system but will be returned on completion of the violation check.", alias="clientMetadata")
    violation_contexts: Optional[List[SodViolationContext1]] = Field(default=None, alias="violationContexts")
    violated_policies: Optional[List[SodPolicyDto]] = Field(default=None, description="A list of the Policies that were violated.", alias="violatedPolicies")
    __properties: ClassVar[List[str]] = ["message", "clientMetadata", "violationContexts", "violatedPolicies"]

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
        """Create an instance of SodViolationCheckResult1 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of message
        if self.message:
            _dict['message'] = self.message.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in violation_contexts (list)
        _items = []
        if self.violation_contexts:
            for _item_violation_contexts in self.violation_contexts:
                if _item_violation_contexts:
                    _items.append(_item_violation_contexts.to_dict())
            _dict['violationContexts'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in violated_policies (list)
        _items = []
        if self.violated_policies:
            for _item_violated_policies in self.violated_policies:
                if _item_violated_policies:
                    _items.append(_item_violated_policies.to_dict())
            _dict['violatedPolicies'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SodViolationCheckResult1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "message": ErrorMessageDto.from_dict(obj["message"]) if obj.get("message") is not None else None,
            "clientMetadata": obj.get("clientMetadata"),
            "violationContexts": [SodViolationContext1.from_dict(_item) for _item in obj["violationContexts"]] if obj.get("violationContexts") is not None else None,
            "violatedPolicies": [SodPolicyDto.from_dict(_item) for _item in obj["violatedPolicies"]] if obj.get("violatedPolicies") is not None else None
        })
        return _obj


