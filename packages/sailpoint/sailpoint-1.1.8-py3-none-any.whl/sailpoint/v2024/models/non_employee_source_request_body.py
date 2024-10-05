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

from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from sailpoint.v2024.models.non_employee_idn_user_request import NonEmployeeIdnUserRequest
from typing import Optional, Set
from typing_extensions import Self

class NonEmployeeSourceRequestBody(BaseModel):
    """
    NonEmployeeSourceRequestBody
    """ # noqa: E501
    name: StrictStr = Field(description="Name of non-employee source.")
    description: StrictStr = Field(description="Description of non-employee source.")
    owner: NonEmployeeIdnUserRequest
    management_workgroup: Optional[StrictStr] = Field(default=None, description="The ID for the management workgroup that contains source sub-admins", alias="managementWorkgroup")
    approvers: Optional[Annotated[List[NonEmployeeIdnUserRequest], Field(max_length=3)]] = Field(default=None, description="List of approvers.")
    account_managers: Optional[Annotated[List[NonEmployeeIdnUserRequest], Field(max_length=10)]] = Field(default=None, description="List of account managers.", alias="accountManagers")
    __properties: ClassVar[List[str]] = ["name", "description", "owner", "managementWorkgroup", "approvers", "accountManagers"]

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
        """Create an instance of NonEmployeeSourceRequestBody from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in approvers (list)
        _items = []
        if self.approvers:
            for _item_approvers in self.approvers:
                if _item_approvers:
                    _items.append(_item_approvers.to_dict())
            _dict['approvers'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in account_managers (list)
        _items = []
        if self.account_managers:
            for _item_account_managers in self.account_managers:
                if _item_account_managers:
                    _items.append(_item_account_managers.to_dict())
            _dict['accountManagers'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of NonEmployeeSourceRequestBody from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "owner": NonEmployeeIdnUserRequest.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "managementWorkgroup": obj.get("managementWorkgroup"),
            "approvers": [NonEmployeeIdnUserRequest.from_dict(_item) for _item in obj["approvers"]] if obj.get("approvers") is not None else None,
            "accountManagers": [NonEmployeeIdnUserRequest.from_dict(_item) for _item in obj["accountManagers"]] if obj.get("accountManagers") is not None else None
        })
        return _obj


