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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v2024.models.campaign_filter_details_criteria_list_inner import CampaignFilterDetailsCriteriaListInner
from typing import Optional, Set
from typing_extensions import Self

class CampaignFilterDetails(BaseModel):
    """
    Campaign Filter Details
    """ # noqa: E501
    id: StrictStr = Field(description="The unique ID of the campaign filter")
    name: StrictStr = Field(description="Campaign filter name.")
    description: Optional[StrictStr] = Field(default=None, description="Campaign filter description.")
    owner: Optional[StrictStr] = Field(description="Owner of the filter. This field automatically populates at creation time with the current user.")
    mode: Dict[str, Any] = Field(description="Mode/type of filter, either the INCLUSION or EXCLUSION type. The INCLUSION type includes the data in generated campaigns  as per specified in the criteria, whereas the EXCLUSION type excludes the data in generated campaigns as per specified in criteria.")
    criteria_list: Optional[List[CampaignFilterDetailsCriteriaListInner]] = Field(default=None, description="List of criteria.", alias="criteriaList")
    is_system_filter: StrictBool = Field(description="If true, the filter is created by the system. If false, the filter is created by a user.", alias="isSystemFilter")
    __properties: ClassVar[List[str]] = ["id", "name", "description", "owner", "mode", "criteriaList", "isSystemFilter"]

    @field_validator('mode')
    def mode_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['INCLUSION', 'EXCLUSION']):
            raise ValueError("must be one of enum values ('INCLUSION', 'EXCLUSION')")
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
        """Create an instance of CampaignFilterDetails from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in criteria_list (list)
        _items = []
        if self.criteria_list:
            for _item_criteria_list in self.criteria_list:
                if _item_criteria_list:
                    _items.append(_item_criteria_list.to_dict())
            _dict['criteriaList'] = _items
        # set to None if owner (nullable) is None
        # and model_fields_set contains the field
        if self.owner is None and "owner" in self.model_fields_set:
            _dict['owner'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CampaignFilterDetails from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "description": obj.get("description"),
            "owner": obj.get("owner"),
            "mode": obj.get("mode"),
            "criteriaList": [CampaignFilterDetailsCriteriaListInner.from_dict(_item) for _item in obj["criteriaList"]] if obj.get("criteriaList") is not None else None,
            "isSystemFilter": obj.get("isSystemFilter") if obj.get("isSystemFilter") is not None else False
        })
        return _obj


