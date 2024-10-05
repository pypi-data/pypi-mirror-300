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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v3.models.role_assignment_source_type import RoleAssignmentSourceType
from typing import Optional, Set
from typing_extensions import Self

class RoleIdentity(BaseModel):
    """
    A subset of the fields of an Identity which is a member of a Role.
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The ID of the Identity")
    alias_name: Optional[StrictStr] = Field(default=None, description="The alias / username of the Identity", alias="aliasName")
    name: Optional[StrictStr] = Field(default=None, description="The human-readable display name of the Identity")
    email: Optional[StrictStr] = Field(default=None, description="Email address of the Identity")
    role_assignment_source: Optional[RoleAssignmentSourceType] = Field(default=None, alias="roleAssignmentSource")
    __properties: ClassVar[List[str]] = ["id", "aliasName", "name", "email", "roleAssignmentSource"]

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
        """Create an instance of RoleIdentity from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RoleIdentity from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "aliasName": obj.get("aliasName"),
            "name": obj.get("name"),
            "email": obj.get("email"),
            "roleAssignmentSource": obj.get("roleAssignmentSource")
        })
        return _obj


