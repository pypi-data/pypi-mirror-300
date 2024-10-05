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
from sailpoint.v2024.models.access_item_associated_access_item import AccessItemAssociatedAccessItem
from sailpoint.v2024.models.correlated_governance_event import CorrelatedGovernanceEvent
from typing import Optional, Set
from typing_extensions import Self

class AccessItemRemoved(BaseModel):
    """
    AccessItemRemoved
    """ # noqa: E501
    access_item: Optional[AccessItemAssociatedAccessItem] = Field(default=None, alias="accessItem")
    identity_id: Optional[StrictStr] = Field(default=None, description="the identity id", alias="identityId")
    event_type: Optional[StrictStr] = Field(default=None, description="the event type", alias="eventType")
    dt: Optional[StrictStr] = Field(default=None, description="the date of event")
    governance_event: Optional[CorrelatedGovernanceEvent] = Field(default=None, alias="governanceEvent")
    __properties: ClassVar[List[str]] = ["accessItem", "identityId", "eventType", "dt", "governanceEvent"]

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
        """Create an instance of AccessItemRemoved from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of access_item
        if self.access_item:
            _dict['accessItem'] = self.access_item.to_dict()
        # override the default output from pydantic by calling `to_dict()` of governance_event
        if self.governance_event:
            _dict['governanceEvent'] = self.governance_event.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccessItemRemoved from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "accessItem": AccessItemAssociatedAccessItem.from_dict(obj["accessItem"]) if obj.get("accessItem") is not None else None,
            "identityId": obj.get("identityId"),
            "eventType": obj.get("eventType"),
            "dt": obj.get("dt"),
            "governanceEvent": CorrelatedGovernanceEvent.from_dict(obj["governanceEvent"]) if obj.get("governanceEvent") is not None else None
        })
        return _obj


