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
from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.identity_reference import IdentityReference
from sailpoint.v2024.models.public_identity_attribute_config import PublicIdentityAttributeConfig
from typing import Optional, Set
from typing_extensions import Self

class PublicIdentityConfig(BaseModel):
    """
    Details of up to 5 Identity attributes that will be publicly accessible for all Identities to anyone in the org.
    """ # noqa: E501
    attributes: Optional[List[PublicIdentityAttributeConfig]] = Field(default=None, description="Up to 5 identity attributes that will be available to everyone in the org for all users in the org.")
    modified: Optional[datetime] = Field(default=None, description="When this configuration was last modified.")
    modified_by: Optional[IdentityReference] = Field(default=None, alias="modifiedBy")
    __properties: ClassVar[List[str]] = ["attributes", "modified", "modifiedBy"]

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
        """Create an instance of PublicIdentityConfig from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in attributes (list)
        _items = []
        if self.attributes:
            for _item_attributes in self.attributes:
                if _item_attributes:
                    _items.append(_item_attributes.to_dict())
            _dict['attributes'] = _items
        # override the default output from pydantic by calling `to_dict()` of modified_by
        if self.modified_by:
            _dict['modifiedBy'] = self.modified_by.to_dict()
        # set to None if modified (nullable) is None
        # and model_fields_set contains the field
        if self.modified is None and "modified" in self.model_fields_set:
            _dict['modified'] = None

        # set to None if modified_by (nullable) is None
        # and model_fields_set contains the field
        if self.modified_by is None and "modified_by" in self.model_fields_set:
            _dict['modifiedBy'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PublicIdentityConfig from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "attributes": [PublicIdentityAttributeConfig.from_dict(_item) for _item in obj["attributes"]] if obj.get("attributes") is not None else None,
            "modified": obj.get("modified"),
            "modifiedBy": IdentityReference.from_dict(obj["modifiedBy"]) if obj.get("modifiedBy") is not None else None
        })
        return _obj


