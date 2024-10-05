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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.beta.models.identity_attribute_config import IdentityAttributeConfig
from sailpoint.beta.models.identity_exception_report_reference import IdentityExceptionReportReference
from sailpoint.beta.models.identity_profile_all_of_authoritative_source import IdentityProfileAllOfAuthoritativeSource
from sailpoint.beta.models.identity_profile_all_of_owner import IdentityProfileAllOfOwner
from typing import Optional, Set
from typing_extensions import Self

class IdentityProfile(BaseModel):
    """
    IdentityProfile
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="System-generated unique ID of the Object")
    name: StrictStr = Field(description="Name of the Object")
    created: Optional[datetime] = Field(default=None, description="Creation date of the Object")
    modified: Optional[datetime] = Field(default=None, description="Last modification date of the Object")
    description: Optional[StrictStr] = Field(default=None, description="The description of the Identity Profile.")
    owner: Optional[IdentityProfileAllOfOwner] = None
    priority: Optional[StrictInt] = Field(default=None, description="The priority for an Identity Profile.")
    authoritative_source: IdentityProfileAllOfAuthoritativeSource = Field(alias="authoritativeSource")
    identity_refresh_required: Optional[StrictBool] = Field(default=False, description="True if a identity refresh is needed. Typically triggered when a change on the source has been made", alias="identityRefreshRequired")
    identity_count: Optional[StrictInt] = Field(default=None, description="The number of identities that belong to the Identity Profile.", alias="identityCount")
    identity_attribute_config: Optional[IdentityAttributeConfig] = Field(default=None, alias="identityAttributeConfig")
    identity_exception_report_reference: Optional[IdentityExceptionReportReference] = Field(default=None, alias="identityExceptionReportReference")
    has_time_based_attr: Optional[StrictBool] = Field(default=True, description="Indicates the value of requiresPeriodicRefresh attribute for the Identity Profile.", alias="hasTimeBasedAttr")
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "description", "owner", "priority", "authoritativeSource", "identityRefreshRequired", "identityCount", "identityAttributeConfig", "identityExceptionReportReference", "hasTimeBasedAttr"]

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
        """Create an instance of IdentityProfile from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        * OpenAPI `readOnly` fields are excluded.
        """
        excluded_fields: Set[str] = set([
            "id",
            "created",
            "modified",
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of owner
        if self.owner:
            _dict['owner'] = self.owner.to_dict()
        # override the default output from pydantic by calling `to_dict()` of authoritative_source
        if self.authoritative_source:
            _dict['authoritativeSource'] = self.authoritative_source.to_dict()
        # override the default output from pydantic by calling `to_dict()` of identity_attribute_config
        if self.identity_attribute_config:
            _dict['identityAttributeConfig'] = self.identity_attribute_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of identity_exception_report_reference
        if self.identity_exception_report_reference:
            _dict['identityExceptionReportReference'] = self.identity_exception_report_reference.to_dict()
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if owner (nullable) is None
        # and model_fields_set contains the field
        if self.owner is None and "owner" in self.model_fields_set:
            _dict['owner'] = None

        # set to None if identity_exception_report_reference (nullable) is None
        # and model_fields_set contains the field
        if self.identity_exception_report_reference is None and "identity_exception_report_reference" in self.model_fields_set:
            _dict['identityExceptionReportReference'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of IdentityProfile from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "description": obj.get("description"),
            "owner": IdentityProfileAllOfOwner.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "priority": obj.get("priority"),
            "authoritativeSource": IdentityProfileAllOfAuthoritativeSource.from_dict(obj["authoritativeSource"]) if obj.get("authoritativeSource") is not None else None,
            "identityRefreshRequired": obj.get("identityRefreshRequired") if obj.get("identityRefreshRequired") is not None else False,
            "identityCount": obj.get("identityCount"),
            "identityAttributeConfig": IdentityAttributeConfig.from_dict(obj["identityAttributeConfig"]) if obj.get("identityAttributeConfig") is not None else None,
            "identityExceptionReportReference": IdentityExceptionReportReference.from_dict(obj["identityExceptionReportReference"]) if obj.get("identityExceptionReportReference") is not None else None,
            "hasTimeBasedAttr": obj.get("hasTimeBasedAttr") if obj.get("hasTimeBasedAttr") is not None else True
        })
        return _obj


