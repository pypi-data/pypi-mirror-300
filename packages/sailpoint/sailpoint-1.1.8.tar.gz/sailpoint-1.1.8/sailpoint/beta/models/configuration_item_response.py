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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.beta.models.configuration_details_response import ConfigurationDetailsResponse
from sailpoint.beta.models.identity1 import Identity1
from typing import Optional, Set
from typing_extensions import Self

class ConfigurationItemResponse(BaseModel):
    """
    The response body of a Reassignment Configuration for a single identity
    """ # noqa: E501
    identity: Optional[Identity1] = None
    config_details: Optional[List[ConfigurationDetailsResponse]] = Field(default=None, description="Details of how work should be reassigned for an Identity", alias="configDetails")
    __properties: ClassVar[List[str]] = ["identity", "configDetails"]

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
        """Create an instance of ConfigurationItemResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of identity
        if self.identity:
            _dict['identity'] = self.identity.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in config_details (list)
        _items = []
        if self.config_details:
            for _item_config_details in self.config_details:
                if _item_config_details:
                    _items.append(_item_config_details.to_dict())
            _dict['configDetails'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ConfigurationItemResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "identity": Identity1.from_dict(obj["identity"]) if obj.get("identity") is not None else None,
            "configDetails": [ConfigurationDetailsResponse.from_dict(_item) for _item in obj["configDetails"]] if obj.get("configDetails") is not None else None
        })
        return _obj


