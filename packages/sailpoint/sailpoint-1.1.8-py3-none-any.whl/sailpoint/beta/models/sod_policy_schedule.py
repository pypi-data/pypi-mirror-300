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
from sailpoint.beta.models.schedule1 import Schedule1
from sailpoint.beta.models.sod_recipient import SodRecipient
from typing import Optional, Set
from typing_extensions import Self

class SodPolicySchedule(BaseModel):
    """
    SodPolicySchedule
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="SOD Policy schedule name")
    created: Optional[datetime] = Field(default=None, description="The time when this SOD policy schedule is created.")
    modified: Optional[datetime] = Field(default=None, description="The time when this SOD policy schedule is modified.")
    description: Optional[StrictStr] = Field(default=None, description="SOD Policy schedule description")
    schedule: Optional[Schedule1] = None
    recipients: Optional[List[SodRecipient]] = None
    email_empty_results: Optional[StrictBool] = Field(default=None, description="Indicates if empty results need to be emailed", alias="emailEmptyResults")
    creator_id: Optional[StrictStr] = Field(default=None, description="Policy's creator ID", alias="creatorId")
    modifier_id: Optional[StrictStr] = Field(default=None, description="Policy's modifier ID", alias="modifierId")
    __properties: ClassVar[List[str]] = ["name", "created", "modified", "description", "schedule", "recipients", "emailEmptyResults", "creatorId", "modifierId"]

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
        """Create an instance of SodPolicySchedule from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of schedule
        if self.schedule:
            _dict['schedule'] = self.schedule.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in recipients (list)
        _items = []
        if self.recipients:
            for _item_recipients in self.recipients:
                if _item_recipients:
                    _items.append(_item_recipients.to_dict())
            _dict['recipients'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SodPolicySchedule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "description": obj.get("description"),
            "schedule": Schedule1.from_dict(obj["schedule"]) if obj.get("schedule") is not None else None,
            "recipients": [SodRecipient.from_dict(_item) for _item in obj["recipients"]] if obj.get("recipients") is not None else None,
            "emailEmptyResults": obj.get("emailEmptyResults"),
            "creatorId": obj.get("creatorId"),
            "modifierId": obj.get("modifierId")
        })
        return _obj


