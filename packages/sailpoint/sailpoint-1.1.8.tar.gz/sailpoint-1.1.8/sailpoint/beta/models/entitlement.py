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
from sailpoint.beta.models.entitlement_access_model_metadata import EntitlementAccessModelMetadata
from sailpoint.beta.models.entitlement_manually_updated_fields import EntitlementManuallyUpdatedFields
from sailpoint.beta.models.entitlement_owner import EntitlementOwner
from sailpoint.beta.models.entitlement_source import EntitlementSource
from sailpoint.beta.models.permission_dto import PermissionDto
from typing import Optional, Set
from typing_extensions import Self

class Entitlement(BaseModel):
    """
    Entitlement
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The entitlement id")
    name: Optional[StrictStr] = Field(default=None, description="The entitlement name")
    created: Optional[datetime] = Field(default=None, description="Time when the entitlement was created")
    modified: Optional[datetime] = Field(default=None, description="Time when the entitlement was last modified")
    attribute: Optional[StrictStr] = Field(default=None, description="The entitlement attribute name")
    value: Optional[StrictStr] = Field(default=None, description="The value of the entitlement")
    source_schema_object_type: Optional[StrictStr] = Field(default=None, description="The object type of the entitlement from the source schema", alias="sourceSchemaObjectType")
    privileged: Optional[StrictBool] = Field(default=False, description="True if the entitlement is privileged")
    cloud_governed: Optional[StrictBool] = Field(default=False, description="True if the entitlement is cloud governed", alias="cloudGoverned")
    description: Optional[StrictStr] = Field(default=None, description="The description of the entitlement")
    requestable: Optional[StrictBool] = Field(default=False, description="True if the entitlement is requestable")
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="A map of free-form key-value pairs from the source system")
    source: Optional[EntitlementSource] = None
    owner: Optional[EntitlementOwner] = None
    direct_permissions: Optional[List[PermissionDto]] = Field(default=None, alias="directPermissions")
    segments: Optional[List[StrictStr]] = Field(default=None, description="List of IDs of segments, if any, to which this Entitlement is assigned.")
    manually_updated_fields: Optional[EntitlementManuallyUpdatedFields] = Field(default=None, alias="manuallyUpdatedFields")
    access_model_metadata: Optional[EntitlementAccessModelMetadata] = Field(default=None, alias="accessModelMetadata")
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "attribute", "value", "sourceSchemaObjectType", "privileged", "cloudGoverned", "description", "requestable", "attributes", "source", "owner", "directPermissions", "segments", "manuallyUpdatedFields", "accessModelMetadata"]

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
        """Create an instance of Entitlement from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of owner
        if self.owner:
            _dict['owner'] = self.owner.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in direct_permissions (list)
        _items = []
        if self.direct_permissions:
            for _item_direct_permissions in self.direct_permissions:
                if _item_direct_permissions:
                    _items.append(_item_direct_permissions.to_dict())
            _dict['directPermissions'] = _items
        # override the default output from pydantic by calling `to_dict()` of manually_updated_fields
        if self.manually_updated_fields:
            _dict['manuallyUpdatedFields'] = self.manually_updated_fields.to_dict()
        # override the default output from pydantic by calling `to_dict()` of access_model_metadata
        if self.access_model_metadata:
            _dict['accessModelMetadata'] = self.access_model_metadata.to_dict()
        # set to None if attribute (nullable) is None
        # and model_fields_set contains the field
        if self.attribute is None and "attribute" in self.model_fields_set:
            _dict['attribute'] = None

        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if segments (nullable) is None
        # and model_fields_set contains the field
        if self.segments is None and "segments" in self.model_fields_set:
            _dict['segments'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Entitlement from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "attribute": obj.get("attribute"),
            "value": obj.get("value"),
            "sourceSchemaObjectType": obj.get("sourceSchemaObjectType"),
            "privileged": obj.get("privileged") if obj.get("privileged") is not None else False,
            "cloudGoverned": obj.get("cloudGoverned") if obj.get("cloudGoverned") is not None else False,
            "description": obj.get("description"),
            "requestable": obj.get("requestable") if obj.get("requestable") is not None else False,
            "attributes": obj.get("attributes"),
            "source": EntitlementSource.from_dict(obj["source"]) if obj.get("source") is not None else None,
            "owner": EntitlementOwner.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "directPermissions": [PermissionDto.from_dict(_item) for _item in obj["directPermissions"]] if obj.get("directPermissions") is not None else None,
            "segments": obj.get("segments"),
            "manuallyUpdatedFields": EntitlementManuallyUpdatedFields.from_dict(obj["manuallyUpdatedFields"]) if obj.get("manuallyUpdatedFields") is not None else None,
            "accessModelMetadata": EntitlementAccessModelMetadata.from_dict(obj["accessModelMetadata"]) if obj.get("accessModelMetadata") is not None else None
        })
        return _obj


