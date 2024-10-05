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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class TemplateSlackCustomFields(BaseModel):
    """
    TemplateSlackCustomFields
    """ # noqa: E501
    request_type: Optional[StrictStr] = Field(default=None, alias="requestType")
    contains_deny: Optional[StrictStr] = Field(default=None, alias="containsDeny")
    campaign_id: Optional[StrictStr] = Field(default=None, alias="campaignId")
    campaign_status: Optional[StrictStr] = Field(default=None, alias="campaignStatus")
    __properties: ClassVar[List[str]] = ["requestType", "containsDeny", "campaignId", "campaignStatus"]

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
        """Create an instance of TemplateSlackCustomFields from a JSON string"""
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
        # set to None if request_type (nullable) is None
        # and model_fields_set contains the field
        if self.request_type is None and "request_type" in self.model_fields_set:
            _dict['requestType'] = None

        # set to None if contains_deny (nullable) is None
        # and model_fields_set contains the field
        if self.contains_deny is None and "contains_deny" in self.model_fields_set:
            _dict['containsDeny'] = None

        # set to None if campaign_id (nullable) is None
        # and model_fields_set contains the field
        if self.campaign_id is None and "campaign_id" in self.model_fields_set:
            _dict['campaignId'] = None

        # set to None if campaign_status (nullable) is None
        # and model_fields_set contains the field
        if self.campaign_status is None and "campaign_status" in self.model_fields_set:
            _dict['campaignStatus'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of TemplateSlackCustomFields from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "requestType": obj.get("requestType"),
            "containsDeny": obj.get("containsDeny"),
            "campaignId": obj.get("campaignId"),
            "campaignStatus": obj.get("campaignStatus")
        })
        return _obj


