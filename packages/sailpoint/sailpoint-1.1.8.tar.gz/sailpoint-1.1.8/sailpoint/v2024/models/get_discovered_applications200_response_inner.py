# coding: utf-8

"""
    Identity Security Cloud V2024 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: v2024
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from sailpoint.v2024.models.full_discovered_applications import FullDiscoveredApplications
from sailpoint.v2024.models.slim_discovered_applications import SlimDiscoveredApplications
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

GETDISCOVEREDAPPLICATIONS200RESPONSEINNER_ONE_OF_SCHEMAS = ["FullDiscoveredApplications", "SlimDiscoveredApplications"]

class GetDiscoveredApplications200ResponseInner(BaseModel):
    """
    GetDiscoveredApplications200ResponseInner
    """
    # data type: SlimDiscoveredApplications
    oneof_schema_1_validator: Optional[SlimDiscoveredApplications] = None
    # data type: FullDiscoveredApplications
    oneof_schema_2_validator: Optional[FullDiscoveredApplications] = None
    actual_instance: Optional[Union[FullDiscoveredApplications, SlimDiscoveredApplications]] = None
    one_of_schemas: Set[str] = { "FullDiscoveredApplications", "SlimDiscoveredApplications" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = GetDiscoveredApplications200ResponseInner.model_construct()
        error_messages = []
        match = 0
        # validate data type: SlimDiscoveredApplications
        if not isinstance(v, SlimDiscoveredApplications):
            error_messages.append(f"Error! Input type `{type(v)}` is not `SlimDiscoveredApplications`")
        else:
            match += 1
        # validate data type: FullDiscoveredApplications
        if not isinstance(v, FullDiscoveredApplications):
            error_messages.append(f"Error! Input type `{type(v)}` is not `FullDiscoveredApplications`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in GetDiscoveredApplications200ResponseInner with oneOf schemas: FullDiscoveredApplications, SlimDiscoveredApplications. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in GetDiscoveredApplications200ResponseInner with oneOf schemas: FullDiscoveredApplications, SlimDiscoveredApplications. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into SlimDiscoveredApplications
        try:
            instance.actual_instance = SlimDiscoveredApplications.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into FullDiscoveredApplications
        try:
            instance.actual_instance = FullDiscoveredApplications.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into GetDiscoveredApplications200ResponseInner with oneOf schemas: FullDiscoveredApplications, SlimDiscoveredApplications. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into GetDiscoveredApplications200ResponseInner with oneOf schemas: FullDiscoveredApplications, SlimDiscoveredApplications. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], FullDiscoveredApplications, SlimDiscoveredApplications]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


