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

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.role_criteria_level1 import RoleCriteriaLevel1
from sailpoint.v2024.models.role_membership_identity import RoleMembershipIdentity
from sailpoint.v2024.models.role_membership_selector_type import RoleMembershipSelectorType
from typing import Optional, Set
from typing_extensions import Self

class RoleMembershipSelector(BaseModel):
    """
    When present, specifies that the Role is to be granted to Identities which either satisfy specific criteria or which are members of a given list of Identities.
    """ # noqa: E501
    type: Optional[RoleMembershipSelectorType] = None
    criteria: Optional[RoleCriteriaLevel1] = None
    identities: Optional[List[RoleMembershipIdentity]] = Field(default=None, description="Defines role membership as being exclusive to the specified Identities, when type is IDENTITY_LIST.")
    __properties: ClassVar[List[str]] = ["type", "criteria", "identities"]

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
        """Create an instance of RoleMembershipSelector from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of criteria
        if self.criteria:
            _dict['criteria'] = self.criteria.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in identities (list)
        _items = []
        if self.identities:
            for _item_identities in self.identities:
                if _item_identities:
                    _items.append(_item_identities.to_dict())
            _dict['identities'] = _items
        # set to None if criteria (nullable) is None
        # and model_fields_set contains the field
        if self.criteria is None and "criteria" in self.model_fields_set:
            _dict['criteria'] = None

        # set to None if identities (nullable) is None
        # and model_fields_set contains the field
        if self.identities is None and "identities" in self.model_fields_set:
            _dict['identities'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RoleMembershipSelector from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "criteria": RoleCriteriaLevel1.from_dict(obj["criteria"]) if obj.get("criteria") is not None else None,
            "identities": [RoleMembershipIdentity.from_dict(_item) for _item in obj["identities"]] if obj.get("identities") is not None else None
        })
        return _obj


