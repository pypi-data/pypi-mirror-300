# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from sailpoint.v3.models.event_attributes import EventAttributes
from sailpoint.v3.models.external_attributes import ExternalAttributes
from sailpoint.v3.models.scheduled_attributes import ScheduledAttributes
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

WORKFLOWTRIGGERATTRIBUTES_ONE_OF_SCHEMAS = ["EventAttributes", "ExternalAttributes", "ScheduledAttributes"]

class WorkflowTriggerAttributes(BaseModel):
    """
    Workflow Trigger Attributes.
    """
    # data type: EventAttributes
    oneof_schema_1_validator: Optional[EventAttributes] = None
    # data type: ExternalAttributes
    oneof_schema_2_validator: Optional[ExternalAttributes] = None
    # data type: ScheduledAttributes
    oneof_schema_3_validator: Optional[ScheduledAttributes] = None
    actual_instance: Optional[Union[EventAttributes, ExternalAttributes, ScheduledAttributes]] = None
    one_of_schemas: Set[str] = { "EventAttributes", "ExternalAttributes", "ScheduledAttributes" }

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
        instance = WorkflowTriggerAttributes.model_construct()
        error_messages = []
        match = 0
        # validate data type: EventAttributes
        if not isinstance(v, EventAttributes):
            error_messages.append(f"Error! Input type `{type(v)}` is not `EventAttributes`")
        else:
            match += 1
        # validate data type: ExternalAttributes
        if not isinstance(v, ExternalAttributes):
            error_messages.append(f"Error! Input type `{type(v)}` is not `ExternalAttributes`")
        else:
            match += 1
        # validate data type: ScheduledAttributes
        if not isinstance(v, ScheduledAttributes):
            error_messages.append(f"Error! Input type `{type(v)}` is not `ScheduledAttributes`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in WorkflowTriggerAttributes with oneOf schemas: EventAttributes, ExternalAttributes, ScheduledAttributes. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in WorkflowTriggerAttributes with oneOf schemas: EventAttributes, ExternalAttributes, ScheduledAttributes. Details: " + ", ".join(error_messages))
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

        # deserialize data into EventAttributes
        try:
            instance.actual_instance = EventAttributes.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into ExternalAttributes
        try:
            instance.actual_instance = ExternalAttributes.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into ScheduledAttributes
        try:
            instance.actual_instance = ScheduledAttributes.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into WorkflowTriggerAttributes with oneOf schemas: EventAttributes, ExternalAttributes, ScheduledAttributes. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into WorkflowTriggerAttributes with oneOf schemas: EventAttributes, ExternalAttributes, ScheduledAttributes. Details: " + ", ".join(error_messages))
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], EventAttributes, ExternalAttributes, ScheduledAttributes]]:
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


