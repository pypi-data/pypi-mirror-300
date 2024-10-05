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
from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class AccessRequestPhases(BaseModel):
    """
    Provides additional details about this access request phase.
    """ # noqa: E501
    started: Optional[datetime] = Field(default=None, description="The time that this phase started.")
    finished: Optional[datetime] = Field(default=None, description="The time that this phase finished.")
    name: Optional[StrictStr] = Field(default=None, description="The name of this phase.")
    state: Optional[StrictStr] = Field(default=None, description="The state of this phase.")
    result: Optional[StrictStr] = Field(default=None, description="The state of this phase.")
    phase_reference: Optional[StrictStr] = Field(default=None, description="A reference to another object on the RequestedItemStatus that contains more details about the phase. Note that for the Provisioning phase, this will be empty if there are no manual work items.", alias="phaseReference")
    __properties: ClassVar[List[str]] = ["started", "finished", "name", "state", "result", "phaseReference"]

    @field_validator('state')
    def state_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['PENDING', 'EXECUTING', 'COMPLETED', 'CANCELLED', 'NOT_EXECUTED']):
            raise ValueError("must be one of enum values ('PENDING', 'EXECUTING', 'COMPLETED', 'CANCELLED', 'NOT_EXECUTED')")
        return value

    @field_validator('result')
    def result_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['SUCCESSFUL', 'FAILED', 'null']):
            raise ValueError("must be one of enum values ('SUCCESSFUL', 'FAILED', 'null')")
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
        """Create an instance of AccessRequestPhases from a JSON string"""
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
        # set to None if finished (nullable) is None
        # and model_fields_set contains the field
        if self.finished is None and "finished" in self.model_fields_set:
            _dict['finished'] = None

        # set to None if result (nullable) is None
        # and model_fields_set contains the field
        if self.result is None and "result" in self.model_fields_set:
            _dict['result'] = None

        # set to None if phase_reference (nullable) is None
        # and model_fields_set contains the field
        if self.phase_reference is None and "phase_reference" in self.model_fields_set:
            _dict['phaseReference'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccessRequestPhases from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "started": obj.get("started"),
            "finished": obj.get("finished"),
            "name": obj.get("name"),
            "state": obj.get("state"),
            "result": obj.get("result"),
            "phaseReference": obj.get("phaseReference")
        })
        return _obj


