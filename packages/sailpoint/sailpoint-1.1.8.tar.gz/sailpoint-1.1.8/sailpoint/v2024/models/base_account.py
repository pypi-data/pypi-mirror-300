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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.account_source import AccountSource
from typing import Optional, Set
from typing_extensions import Self

class BaseAccount(BaseModel):
    """
    BaseAccount
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The unique ID of the referenced object.")
    name: Optional[StrictStr] = Field(default=None, description="The human readable name of the referenced object.")
    account_id: Optional[StrictStr] = Field(default=None, description="Account ID.", alias="accountId")
    source: Optional[AccountSource] = None
    disabled: Optional[StrictBool] = Field(default=False, description="Indicates whether the account is disabled.")
    locked: Optional[StrictBool] = Field(default=False, description="Indicates whether the account is locked.")
    privileged: Optional[StrictBool] = Field(default=False, description="Indicates whether the account is privileged.")
    manually_correlated: Optional[StrictBool] = Field(default=False, description="Indicates whether the account has been manually correlated to an identity.", alias="manuallyCorrelated")
    password_last_set: Optional[datetime] = Field(default=None, description="A date-time in ISO-8601 format", alias="passwordLastSet")
    entitlement_attributes: Optional[Dict[str, Any]] = Field(default=None, description="Map or dictionary of key/value pairs.", alias="entitlementAttributes")
    created: Optional[datetime] = Field(default=None, description="ISO-8601 date-time referring to the time when the object was created.")
    __properties: ClassVar[List[str]] = ["id", "name", "accountId", "source", "disabled", "locked", "privileged", "manuallyCorrelated", "passwordLastSet", "entitlementAttributes", "created"]

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
        """Create an instance of BaseAccount from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of source
        if self.source:
            _dict['source'] = self.source.to_dict()
        # set to None if password_last_set (nullable) is None
        # and model_fields_set contains the field
        if self.password_last_set is None and "password_last_set" in self.model_fields_set:
            _dict['passwordLastSet'] = None

        # set to None if entitlement_attributes (nullable) is None
        # and model_fields_set contains the field
        if self.entitlement_attributes is None and "entitlement_attributes" in self.model_fields_set:
            _dict['entitlementAttributes'] = None

        # set to None if created (nullable) is None
        # and model_fields_set contains the field
        if self.created is None and "created" in self.model_fields_set:
            _dict['created'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BaseAccount from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "accountId": obj.get("accountId"),
            "source": AccountSource.from_dict(obj["source"]) if obj.get("source") is not None else None,
            "disabled": obj.get("disabled") if obj.get("disabled") is not None else False,
            "locked": obj.get("locked") if obj.get("locked") is not None else False,
            "privileged": obj.get("privileged") if obj.get("privileged") is not None else False,
            "manuallyCorrelated": obj.get("manuallyCorrelated") if obj.get("manuallyCorrelated") is not None else False,
            "passwordLastSet": obj.get("passwordLastSet"),
            "entitlementAttributes": obj.get("entitlementAttributes"),
            "created": obj.get("created")
        })
        return _obj


