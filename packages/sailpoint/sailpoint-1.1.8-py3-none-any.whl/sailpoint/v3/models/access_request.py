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
from typing_extensions import Annotated
from sailpoint.v3.models.access_request_item import AccessRequestItem
from sailpoint.v3.models.access_request_type import AccessRequestType
from typing import Optional, Set
from typing_extensions import Self

class AccessRequest(BaseModel):
    """
    AccessRequest
    """ # noqa: E501
    requested_for: List[StrictStr] = Field(description="A list of Identity IDs for whom the Access is requested. If it's a Revoke request, there can only be one Identity ID.", alias="requestedFor")
    request_type: Optional[AccessRequestType] = Field(default=None, alias="requestType")
    requested_items: Annotated[List[AccessRequestItem], Field(min_length=1, max_length=25)] = Field(alias="requestedItems")
    client_metadata: Optional[Dict[str, StrictStr]] = Field(default=None, description="Arbitrary key-value pairs. They will never be processed by the IdentityNow system but will be returned on associated APIs such as /account-activities.", alias="clientMetadata")
    __properties: ClassVar[List[str]] = ["requestedFor", "requestType", "requestedItems", "clientMetadata"]

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
        """Create an instance of AccessRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in requested_items (list)
        _items = []
        if self.requested_items:
            for _item_requested_items in self.requested_items:
                if _item_requested_items:
                    _items.append(_item_requested_items.to_dict())
            _dict['requestedItems'] = _items
        # set to None if request_type (nullable) is None
        # and model_fields_set contains the field
        if self.request_type is None and "request_type" in self.model_fields_set:
            _dict['requestType'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of AccessRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "requestedFor": obj.get("requestedFor"),
            "requestType": obj.get("requestType"),
            "requestedItems": [AccessRequestItem.from_dict(_item) for _item in obj["requestedItems"]] if obj.get("requestedItems") is not None else None,
            "clientMetadata": obj.get("clientMetadata")
        })
        return _obj


