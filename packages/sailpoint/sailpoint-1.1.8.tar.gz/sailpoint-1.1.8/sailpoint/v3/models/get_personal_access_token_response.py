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
from sailpoint.v3.models.pat_owner import PatOwner
from typing import Optional, Set
from typing_extensions import Self

class GetPersonalAccessTokenResponse(BaseModel):
    """
    GetPersonalAccessTokenResponse
    """ # noqa: E501
    id: StrictStr = Field(description="The ID of the personal access token (to be used as the username for Basic Auth).")
    name: StrictStr = Field(description="The name of the personal access token. Cannot be the same as other personal access tokens owned by a user.")
    scope: Optional[List[StrictStr]] = Field(description="Scopes of the personal  access token.")
    owner: PatOwner
    created: datetime = Field(description="The date and time, down to the millisecond, when this personal access token was created.")
    last_used: Optional[datetime] = Field(default=None, description="The date and time, down to the millisecond, when this personal access token was last used to generate an access token. This timestamp does not get updated on every PAT usage, but only once a day. This property can be useful for identifying which PATs are no longer actively used and can be removed.", alias="lastUsed")
    managed: Optional[StrictBool] = Field(default=False, description="If true, this token is managed by the SailPoint platform, and is not visible in the user interface. For example, Workflows will create managed personal access tokens for users who create workflows.")
    __properties: ClassVar[List[str]] = ["id", "name", "scope", "owner", "created", "lastUsed", "managed"]

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
        """Create an instance of GetPersonalAccessTokenResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of owner
        if self.owner:
            _dict['owner'] = self.owner.to_dict()
        # set to None if scope (nullable) is None
        # and model_fields_set contains the field
        if self.scope is None and "scope" in self.model_fields_set:
            _dict['scope'] = None

        # set to None if last_used (nullable) is None
        # and model_fields_set contains the field
        if self.last_used is None and "last_used" in self.model_fields_set:
            _dict['lastUsed'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of GetPersonalAccessTokenResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "scope": obj.get("scope"),
            "owner": PatOwner.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "created": obj.get("created"),
            "lastUsed": obj.get("lastUsed"),
            "managed": obj.get("managed") if obj.get("managed") is not None else False
        })
        return _obj


