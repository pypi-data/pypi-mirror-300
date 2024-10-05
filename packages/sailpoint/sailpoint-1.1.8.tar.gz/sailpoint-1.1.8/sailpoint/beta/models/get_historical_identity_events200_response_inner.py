# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
from inspect import getfullargspec
import json
import pprint
import re  # noqa: F401
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Optional
from sailpoint.beta.models.access_item_associated import AccessItemAssociated
from sailpoint.beta.models.access_item_removed import AccessItemRemoved
from sailpoint.beta.models.access_requested import AccessRequested
from sailpoint.beta.models.account_status_changed import AccountStatusChanged
from sailpoint.beta.models.attributes_changed import AttributesChanged
from sailpoint.beta.models.identity_certified import IdentityCertified
from typing import Union, Any, List, Set, TYPE_CHECKING, Optional, Dict
from typing_extensions import Literal, Self
from pydantic import Field

GETHISTORICALIDENTITYEVENTS200RESPONSEINNER_ANY_OF_SCHEMAS = ["AccessItemAssociated", "AccessItemRemoved", "AccessRequested", "AccountStatusChanged", "AttributesChanged", "IdentityCertified"]

class GetHistoricalIdentityEvents200ResponseInner(BaseModel):
    """
    GetHistoricalIdentityEvents200ResponseInner
    """

    # data type: AccessItemAssociated
    anyof_schema_1_validator: Optional[AccessItemAssociated] = None
    # data type: AccessItemRemoved
    anyof_schema_2_validator: Optional[AccessItemRemoved] = None
    # data type: AttributesChanged
    anyof_schema_3_validator: Optional[AttributesChanged] = None
    # data type: AccessRequested
    anyof_schema_4_validator: Optional[AccessRequested] = None
    # data type: IdentityCertified
    anyof_schema_5_validator: Optional[IdentityCertified] = None
    # data type: AccountStatusChanged
    anyof_schema_6_validator: Optional[AccountStatusChanged] = None
    if TYPE_CHECKING:
        actual_instance: Optional[Union[AccessItemAssociated, AccessItemRemoved, AccessRequested, AccountStatusChanged, AttributesChanged, IdentityCertified]] = None
    else:
        actual_instance: Any = None
    any_of_schemas: Set[str] = { "AccessItemAssociated", "AccessItemRemoved", "AccessRequested", "AccountStatusChanged", "AttributesChanged", "IdentityCertified" }

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

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
    def actual_instance_must_validate_anyof(cls, v):
        instance = GetHistoricalIdentityEvents200ResponseInner.model_construct()
        error_messages = []
        # validate data type: AccessItemAssociated
        if not isinstance(v, AccessItemAssociated):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemAssociated`")
        else:
            return v

        # validate data type: AccessItemRemoved
        if not isinstance(v, AccessItemRemoved):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemRemoved`")
        else:
            return v

        # validate data type: AttributesChanged
        if not isinstance(v, AttributesChanged):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AttributesChanged`")
        else:
            return v

        # validate data type: AccessRequested
        if not isinstance(v, AccessRequested):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessRequested`")
        else:
            return v

        # validate data type: IdentityCertified
        if not isinstance(v, IdentityCertified):
            error_messages.append(f"Error! Input type `{type(v)}` is not `IdentityCertified`")
        else:
            return v

        # validate data type: AccountStatusChanged
        if not isinstance(v, AccountStatusChanged):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccountStatusChanged`")
        else:
            return v

        if error_messages:
            # no match
            raise ValueError("No match found when setting the actual_instance in GetHistoricalIdentityEvents200ResponseInner with anyOf schemas: AccessItemAssociated, AccessItemRemoved, AccessRequested, AccountStatusChanged, AttributesChanged, IdentityCertified. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        # anyof_schema_1_validator: Optional[AccessItemAssociated] = None
        try:
            instance.actual_instance = AccessItemAssociated.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_2_validator: Optional[AccessItemRemoved] = None
        try:
            instance.actual_instance = AccessItemRemoved.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_3_validator: Optional[AttributesChanged] = None
        try:
            instance.actual_instance = AttributesChanged.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_4_validator: Optional[AccessRequested] = None
        try:
            instance.actual_instance = AccessRequested.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_5_validator: Optional[IdentityCertified] = None
        try:
            instance.actual_instance = IdentityCertified.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))
        # anyof_schema_6_validator: Optional[AccountStatusChanged] = None
        try:
            instance.actual_instance = AccountStatusChanged.from_json(json_str)
            return instance
        except (ValidationError, ValueError) as e:
             error_messages.append(str(e))

        if error_messages:
            # no match
            raise ValueError("No match found when deserializing the JSON string into GetHistoricalIdentityEvents200ResponseInner with anyOf schemas: AccessItemAssociated, AccessItemRemoved, AccessRequested, AccountStatusChanged, AttributesChanged, IdentityCertified. Details: " + ", ".join(error_messages))
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], AccessItemAssociated, AccessItemRemoved, AccessRequested, AccountStatusChanged, AttributesChanged, IdentityCertified]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


