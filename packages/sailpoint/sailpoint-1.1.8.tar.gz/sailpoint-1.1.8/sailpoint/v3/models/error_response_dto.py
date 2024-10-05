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
from sailpoint.v3.models.error_message_dto import ErrorMessageDto
from typing import Optional, Set
from typing_extensions import Self

class ErrorResponseDto(BaseModel):
    """
    ErrorResponseDto
    """ # noqa: E501
    detail_code: Optional[StrictStr] = Field(default=None, description="Fine-grained error code providing more detail of the error.", alias="detailCode")
    tracking_id: Optional[StrictStr] = Field(default=None, description="Unique tracking id for the error.", alias="trackingId")
    messages: Optional[List[ErrorMessageDto]] = Field(default=None, description="Generic localized reason for error")
    causes: Optional[List[ErrorMessageDto]] = Field(default=None, description="Plain-text descriptive reasons to provide additional detail to the text provided in the messages field")
    __properties: ClassVar[List[str]] = ["detailCode", "trackingId", "messages", "causes"]

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
        """Create an instance of ErrorResponseDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in messages (list)
        _items = []
        if self.messages:
            for _item_messages in self.messages:
                if _item_messages:
                    _items.append(_item_messages.to_dict())
            _dict['messages'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in causes (list)
        _items = []
        if self.causes:
            for _item_causes in self.causes:
                if _item_causes:
                    _items.append(_item_causes.to_dict())
            _dict['causes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ErrorResponseDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "detailCode": obj.get("detailCode"),
            "trackingId": obj.get("trackingId"),
            "messages": [ErrorMessageDto.from_dict(_item) for _item in obj["messages"]] if obj.get("messages") is not None else None,
            "causes": [ErrorMessageDto.from_dict(_item) for _item in obj["causes"]] if obj.get("causes") is not None else None
        })
        return _obj


