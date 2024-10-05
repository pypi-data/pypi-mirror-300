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
from sailpoint.beta.models.access_profile_source_ref import AccessProfileSourceRef
from sailpoint.beta.models.entitlement_ref import EntitlementRef
from sailpoint.beta.models.owner_reference import OwnerReference
from sailpoint.beta.models.provisioning_criteria_level1 import ProvisioningCriteriaLevel1
from sailpoint.beta.models.requestability import Requestability
from sailpoint.beta.models.revocability import Revocability
from typing import Optional, Set
from typing_extensions import Self

class AccessProfile(BaseModel):
    """
    Access Profile
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The ID of the Access Profile")
    name: StrictStr = Field(description="Name of the Access Profile")
    description: Optional[StrictStr] = Field(default=None, description="Information about the Access Profile")
    created: Optional[datetime] = Field(default=None, description="Date the Access Profile was created")
    modified: Optional[datetime] = Field(default=None, description="Date the Access Profile was last modified.")
    enabled: Optional[StrictBool] = Field(default=True, description="Whether the Access Profile is enabled. If the Access Profile is enabled then you must include at least one Entitlement.")
    owner: OwnerReference
    source: AccessProfileSourceRef
    entitlements: Optional[List[EntitlementRef]] = Field(default=None, description="A list of entitlements associated with the Access Profile. If enabled is false this is allowed to be empty otherwise it needs to contain at least one Entitlement.")
    requestable: Optional[StrictBool] = Field(default=True, description="Whether the Access Profile is requestable via access request. Currently, making an Access Profile non-requestable is only supported  for customers enabled with the new Request Center. Otherwise, attempting to create an Access Profile with a value  **false** in this field results in a 400 error.")
    access_request_config: Optional[Requestability] = Field(default=None, alias="accessRequestConfig")
    revocation_request_config: Optional[Revocability] = Field(default=None, alias="revocationRequestConfig")
    segments: Optional[List[StrictStr]] = Field(default=None, description="List of IDs of segments, if any, to which this Access Profile is assigned.")
    provisioning_criteria: Optional[ProvisioningCriteriaLevel1] = Field(default=None, alias="provisioningCriteria")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "created", "modified", "enabled", "owner", "source", "entitlements", "requestable", "accessRequestConfig", "revocationRequestConfig", "segments", "provisioningCriteria"]

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
        """Create an instance of AccessProfile from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of source
        if self.source:
            _dict['source'] = self.source.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in entitlements (list)
        _items = []
        if self.entitlements:
            for _item_entitlements in self.entitlements:
                if _item_entitlements:
                    _items.append(_item_entitlements.to_dict())
            _dict['entitlements'] = _items
        # override the default output from pydantic by calling `to_dict()` of access_request_config
        if self.access_request_config:
            _dict['accessRequestConfig'] = self.access_request_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of revocation_request_config
        if self.revocation_request_config:
            _dict['revocationRequestConfig'] = self.revocation_request_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of provisioning_criteria
        if self.provisioning_criteria:
            _dict['provisioningCriteria'] = self.provisioning_criteria.to_dict()
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if entitlements (nullable) is None
        # and model_fields_set contains the field
        if self.entitlements is None and "entitlements" in self.model_fields_set:
            _dict['entitlements'] = None

        # set to None if access_request_config (nullable) is None
        # and model_fields_set contains the field
        if self.access_request_config is None and "access_request_config" in self.model_fields_set:
            _dict['accessRequestConfig'] = None

        # set to None if revocation_request_config (nullable) is None
        # and model_fields_set contains the field
        if self.revocation_request_config is None and "revocation_request_config" in self.model_fields_set:
            _dict['revocationRequestConfig'] = None

        # set to None if segments (nullable) is None
        # and model_fields_set contains the field
        if self.segments is None and "segments" in self.model_fields_set:
            _dict['segments'] = None

        # set to None if provisioning_criteria (nullable) is None
        # and model_fields_set contains the field
        if self.provisioning_criteria is None and "provisioning_criteria" in self.model_fields_set:
            _dict['provisioningCriteria'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccessProfile from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "enabled": obj.get("enabled") if obj.get("enabled") is not None else True,
            "owner": OwnerReference.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "source": AccessProfileSourceRef.from_dict(obj["source"]) if obj.get("source") is not None else None,
            "entitlements": [EntitlementRef.from_dict(_item) for _item in obj["entitlements"]] if obj.get("entitlements") is not None else None,
            "requestable": obj.get("requestable") if obj.get("requestable") is not None else True,
            "accessRequestConfig": Requestability.from_dict(obj["accessRequestConfig"]) if obj.get("accessRequestConfig") is not None else None,
            "revocationRequestConfig": Revocability.from_dict(obj["revocationRequestConfig"]) if obj.get("revocationRequestConfig") is not None else None,
            "segments": obj.get("segments"),
            "provisioningCriteria": ProvisioningCriteriaLevel1.from_dict(obj["provisioningCriteria"]) if obj.get("provisioningCriteria") is not None else None
        })
        return _obj


