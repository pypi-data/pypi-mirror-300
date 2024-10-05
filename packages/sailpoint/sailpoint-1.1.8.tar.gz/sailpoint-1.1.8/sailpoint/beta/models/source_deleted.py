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
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List
from sailpoint.beta.models.source_deleted_actor import SourceDeletedActor
from typing import Optional, Set
from typing_extensions import Self

class SourceDeleted(BaseModel):
    """
    SourceDeleted
    """ # noqa: E501
    id: StrictStr = Field(description="The unique ID of the source.")
    name: StrictStr = Field(description="Human friendly name of the source.")
    type: StrictStr = Field(description="The connection type.")
    deleted: datetime = Field(description="The date and time the source was deleted.")
    connector: StrictStr = Field(description="The connector type used to connect to the source.")
    actor: SourceDeletedActor
    __properties: ClassVar[List[str]] = ["id", "name", "type", "deleted", "connector", "actor"]

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
        """Create an instance of SourceDeleted from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of actor
        if self.actor:
            _dict['actor'] = self.actor.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of SourceDeleted from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "type": obj.get("type"),
            "deleted": obj.get("deleted"),
            "connector": obj.get("connector"),
            "actor": SourceDeletedActor.from_dict(obj["actor"]) if obj.get("actor") is not None else None
        })
        return _obj


