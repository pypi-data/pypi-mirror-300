# coding: utf-8

"""
    Identity Security Cloud V3 API

    Use these APIs to interact with the Identity Security Cloud platform to achieve repeatable, automated processes with greater scalability. We encourage you to join the SailPoint Developer Community forum at https://developer.sailpoint.com/discuss to connect with other developers using our APIs.

    The version of the OpenAPI document: 3.0.0
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
from sailpoint.v3.models.entitlement_source import EntitlementSource
from typing import Optional, Set
from typing_extensions import Self

class EntitlementDto(BaseModel):
    """
    EntitlementDto
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="System-generated unique ID of the Object")
    name: StrictStr = Field(description="Name of the Object")
    created: Optional[datetime] = Field(default=None, description="Creation date of the Object")
    modified: Optional[datetime] = Field(default=None, description="Last modification date of the Object")
    attribute: Optional[StrictStr] = Field(default=None, description="Name of the entitlement attribute")
    value: Optional[StrictStr] = Field(default=None, description="Raw value of the entitlement")
    description: Optional[StrictStr] = Field(default=None, description="Entitlment description")
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="Entitlement attributes")
    source_schema_object_type: Optional[StrictStr] = Field(default=None, description="Schema objectType on the given application that maps to an Account Group", alias="sourceSchemaObjectType")
    privileged: Optional[StrictBool] = Field(default=None, description="Determines if this Entitlement is privileged.")
    cloud_governed: Optional[StrictBool] = Field(default=None, description="Determines if this Entitlement is goverened in the cloud.", alias="cloudGoverned")
    source: Optional[EntitlementSource] = None
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "attribute", "value", "description", "attributes", "sourceSchemaObjectType", "privileged", "cloudGoverned", "source"]

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
        """Create an instance of EntitlementDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of source
        if self.source:
            _dict['source'] = self.source.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of EntitlementDto from a dict"""
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
            "description": obj.get("description"),
            "attributes": obj.get("attributes"),
            "sourceSchemaObjectType": obj.get("sourceSchemaObjectType"),
            "privileged": obj.get("privileged"),
            "cloudGoverned": obj.get("cloudGoverned"),
            "source": EntitlementSource.from_dict(obj["source"]) if obj.get("source") is not None else None
        })
        return _obj


