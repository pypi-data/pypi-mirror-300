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

from pydantic import BaseModel, ConfigDict, Field, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.identity_attribute1 import IdentityAttribute1
from sailpoint.v2024.models.identity_reference import IdentityReference
from typing import Optional, Set
from typing_extensions import Self

class PublicIdentity(BaseModel):
    """
    Details about a public identity
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Identity id")
    name: Optional[StrictStr] = Field(default=None, description="Human-readable display name of identity.")
    alias: Optional[StrictStr] = Field(default=None, description="Alternate unique identifier for the identity.")
    email: Optional[StrictStr] = Field(default=None, description="Email address of identity.")
    status: Optional[StrictStr] = Field(default=None, description="The lifecycle status for the identity")
    identity_state: Optional[StrictStr] = Field(default=None, description="The current state of the identity, which determines how Identity Security Cloud interacts with the identity. An identity that is Active will be included identity picklists in Request Center, identity processing, and more. Identities that are Inactive will be excluded from these features. ", alias="identityState")
    manager: Optional[IdentityReference] = None
    attributes: Optional[List[IdentityAttribute1]] = Field(default=None, description="The public identity attributes of the identity")
    __properties: ClassVar[List[str]] = ["id", "name", "alias", "email", "status", "identityState", "manager", "attributes"]

    @field_validator('identity_state')
    def identity_state_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['ACTIVE', 'INACTIVE_SHORT_TERM', 'INACTIVE_LONG_TERM', 'null']):
            raise ValueError("must be one of enum values ('ACTIVE', 'INACTIVE_SHORT_TERM', 'INACTIVE_LONG_TERM', 'null')")
        return value

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
        """Create an instance of PublicIdentity from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of manager
        if self.manager:
            _dict['manager'] = self.manager.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in attributes (list)
        _items = []
        if self.attributes:
            for _item_attributes in self.attributes:
                if _item_attributes:
                    _items.append(_item_attributes.to_dict())
            _dict['attributes'] = _items
        # set to None if email (nullable) is None
        # and model_fields_set contains the field
        if self.email is None and "email" in self.model_fields_set:
            _dict['email'] = None

        # set to None if status (nullable) is None
        # and model_fields_set contains the field
        if self.status is None and "status" in self.model_fields_set:
            _dict['status'] = None

        # set to None if identity_state (nullable) is None
        # and model_fields_set contains the field
        if self.identity_state is None and "identity_state" in self.model_fields_set:
            _dict['identityState'] = None

        # set to None if manager (nullable) is None
        # and model_fields_set contains the field
        if self.manager is None and "manager" in self.model_fields_set:
            _dict['manager'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PublicIdentity from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "alias": obj.get("alias"),
            "email": obj.get("email"),
            "status": obj.get("status"),
            "identityState": obj.get("identityState"),
            "manager": IdentityReference.from_dict(obj["manager"]) if obj.get("manager") is not None else None,
            "attributes": [IdentityAttribute1.from_dict(_item) for _item in obj["attributes"]] if obj.get("attributes") is not None else None
        })
        return _obj


