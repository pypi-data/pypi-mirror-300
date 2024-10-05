# coding: utf-8

"""
    Identity Security Cloud Beta API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. These APIs are in beta and are subject to change. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.1.0-beta
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from sailpoint.beta.models.access_item_access_profile_response import AccessItemAccessProfileResponse
from sailpoint.beta.models.access_item_account_response import AccessItemAccountResponse
from sailpoint.beta.models.access_item_app_response import AccessItemAppResponse
from sailpoint.beta.models.access_item_entitlement_response import AccessItemEntitlementResponse
from sailpoint.beta.models.access_item_role_response import AccessItemRoleResponse
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

ACCESSITEMASSOCIATEDACCESSITEM_ONE_OF_SCHEMAS = ["AccessItemAccessProfileResponse", "AccessItemAccountResponse", "AccessItemAppResponse", "AccessItemEntitlementResponse", "AccessItemRoleResponse"]

class AccessItemAssociatedAccessItem(BaseModel):
    """
    AccessItemAssociatedAccessItem
    """
    # data type: AccessItemAccessProfileResponse
    oneof_schema_1_validator: Optional[AccessItemAccessProfileResponse] = None
    # data type: AccessItemAccountResponse
    oneof_schema_2_validator: Optional[AccessItemAccountResponse] = None
    # data type: AccessItemAppResponse
    oneof_schema_3_validator: Optional[AccessItemAppResponse] = None
    # data type: AccessItemEntitlementResponse
    oneof_schema_4_validator: Optional[AccessItemEntitlementResponse] = None
    # data type: AccessItemRoleResponse
    oneof_schema_5_validator: Optional[AccessItemRoleResponse] = None
    actual_instance: Optional[Union[AccessItemAccessProfileResponse, AccessItemAccountResponse, AccessItemAppResponse, AccessItemEntitlementResponse, AccessItemRoleResponse]] = None
    one_of_schemas: Set[str] = { "AccessItemAccessProfileResponse", "AccessItemAccountResponse", "AccessItemAppResponse", "AccessItemEntitlementResponse", "AccessItemRoleResponse" }

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
        instance = AccessItemAssociatedAccessItem.model_construct()
        error_messages = []
        match = 0
        # validate data type: AccessItemAccessProfileResponse
        if not isinstance(v, AccessItemAccessProfileResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemAccessProfileResponse`")
        else:
            match += 1
        # validate data type: AccessItemAccountResponse
        if not isinstance(v, AccessItemAccountResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemAccountResponse`")
        else:
            match += 1
        # validate data type: AccessItemAppResponse
        if not isinstance(v, AccessItemAppResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemAppResponse`")
        else:
            match += 1
        # validate data type: AccessItemEntitlementResponse
        if not isinstance(v, AccessItemEntitlementResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemEntitlementResponse`")
        else:
            match += 1
        # validate data type: AccessItemRoleResponse
        if not isinstance(v, AccessItemRoleResponse):
            error_messages.append(f"Error! Input type `{type(v)}` is not `AccessItemRoleResponse`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in AccessItemAssociatedAccessItem with oneOf schemas: AccessItemAccessProfileResponse, AccessItemAccountResponse, AccessItemAppResponse, AccessItemEntitlementResponse, AccessItemRoleResponse. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in AccessItemAssociatedAccessItem with oneOf schemas: AccessItemAccessProfileResponse, AccessItemAccountResponse, AccessItemAppResponse, AccessItemEntitlementResponse, AccessItemRoleResponse. Details: " + ", ".join(error_messages))
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

        # deserialize data into AccessItemAccessProfileResponse
        try:
            instance.actual_instance = AccessItemAccessProfileResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AccessItemAccountResponse
        try:
            instance.actual_instance = AccessItemAccountResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AccessItemAppResponse
        try:
            instance.actual_instance = AccessItemAppResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AccessItemEntitlementResponse
        try:
            instance.actual_instance = AccessItemEntitlementResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into AccessItemRoleResponse
        try:
            instance.actual_instance = AccessItemRoleResponse.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into AccessItemAssociatedAccessItem with oneOf schemas: AccessItemAccessProfileResponse, AccessItemAccountResponse, AccessItemAppResponse, AccessItemEntitlementResponse, AccessItemRoleResponse. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into AccessItemAssociatedAccessItem with oneOf schemas: AccessItemAccessProfileResponse, AccessItemAccountResponse, AccessItemAppResponse, AccessItemEntitlementResponse, AccessItemRoleResponse. Details: " + ", ".join(error_messages))
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

    def to_dict(self) -> Optional[Union[Dict[str, Any], AccessItemAccessProfileResponse, AccessItemAccountResponse, AccessItemAppResponse, AccessItemEntitlementResponse, AccessItemRoleResponse]]:
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


