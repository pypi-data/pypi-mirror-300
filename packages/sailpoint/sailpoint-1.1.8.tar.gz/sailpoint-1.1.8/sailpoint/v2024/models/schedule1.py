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
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.schedule1_days import Schedule1Days
from sailpoint.v2024.models.schedule1_hours import Schedule1Hours
from sailpoint.v2024.models.schedule1_months import Schedule1Months
from sailpoint.v2024.models.schedule_type import ScheduleType
from typing import Optional, Set
from typing_extensions import Self

class Schedule1(BaseModel):
    """
    The schedule information.
    """ # noqa: E501
    type: ScheduleType
    months: Optional[Schedule1Months] = None
    days: Optional[Schedule1Days] = None
    hours: Schedule1Hours
    expiration: Optional[datetime] = Field(default=None, description="A date-time in ISO-8601 format")
    time_zone_id: Optional[StrictStr] = Field(default=None, description="The canonical TZ identifier the schedule will run in (ex. America/New_York).  If no timezone is specified, the org's default timezone is used.", alias="timeZoneId")
    __properties: ClassVar[List[str]] = ["type", "months", "days", "hours", "expiration", "timeZoneId"]

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
        """Create an instance of Schedule1 from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of months
        if self.months:
            _dict['months'] = self.months.to_dict()
        # override the default output from pydantic by calling `to_dict()` of days
        if self.days:
            _dict['days'] = self.days.to_dict()
        # override the default output from pydantic by calling `to_dict()` of hours
        if self.hours:
            _dict['hours'] = self.hours.to_dict()
        # set to None if expiration (nullable) is None
        # and model_fields_set contains the field
        if self.expiration is None and "expiration" in self.model_fields_set:
            _dict['expiration'] = None

        # set to None if time_zone_id (nullable) is None
        # and model_fields_set contains the field
        if self.time_zone_id is None and "time_zone_id" in self.model_fields_set:
            _dict['timeZoneId'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Schedule1 from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "months": Schedule1Months.from_dict(obj["months"]) if obj.get("months") is not None else None,
            "days": Schedule1Days.from_dict(obj["days"]) if obj.get("days") is not None else None,
            "hours": Schedule1Hours.from_dict(obj["hours"]) if obj.get("hours") is not None else None,
            "expiration": obj.get("expiration"),
            "timeZoneId": obj.get("timeZoneId")
        })
        return _obj


