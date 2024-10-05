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
from typing_extensions import Annotated
from sailpoint.v2024.models.access_constraint import AccessConstraint
from sailpoint.v2024.models.campaign_all_of_search_campaign_info_reviewer import CampaignAllOfSearchCampaignInfoReviewer
from typing import Optional, Set
from typing_extensions import Self

class CampaignAllOfSearchCampaignInfo(BaseModel):
    """
    Must be set only if the campaign type is SEARCH.
    """ # noqa: E501
    type: StrictStr = Field(description="The type of search campaign represented.")
    description: Optional[StrictStr] = Field(default=None, description="Describes this search campaign. Intended for storing the query used, and possibly the number of identities selected/available.")
    reviewer: Optional[CampaignAllOfSearchCampaignInfoReviewer] = None
    query: Optional[StrictStr] = Field(default=None, description="The scope for the campaign. The campaign will cover identities returned by the query and identities that have access items returned by the query. One of `query` or `identityIds` must be set.")
    identity_ids: Optional[Annotated[List[StrictStr], Field(max_length=1000)]] = Field(default=None, description="A direct list of identities to include in this campaign. One of `identityIds` or `query` must be set.", alias="identityIds")
    access_constraints: Optional[Annotated[List[AccessConstraint], Field(max_length=1000)]] = Field(default=None, description="Further reduces the scope of the campaign by excluding identities (from `query` or `identityIds`) that do not have this access.", alias="accessConstraints")
    __properties: ClassVar[List[str]] = ["type", "description", "reviewer", "query", "identityIds", "accessConstraints"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['IDENTITY', 'ACCESS']):
            raise ValueError("must be one of enum values ('IDENTITY', 'ACCESS')")
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
        """Create an instance of CampaignAllOfSearchCampaignInfo from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of reviewer
        if self.reviewer:
            _dict['reviewer'] = self.reviewer.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in access_constraints (list)
        _items = []
        if self.access_constraints:
            for _item_access_constraints in self.access_constraints:
                if _item_access_constraints:
                    _items.append(_item_access_constraints.to_dict())
            _dict['accessConstraints'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CampaignAllOfSearchCampaignInfo from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "type": obj.get("type"),
            "description": obj.get("description"),
            "reviewer": CampaignAllOfSearchCampaignInfoReviewer.from_dict(obj["reviewer"]) if obj.get("reviewer") is not None else None,
            "query": obj.get("query"),
            "identityIds": obj.get("identityIds"),
            "accessConstraints": [AccessConstraint.from_dict(_item) for _item in obj["accessConstraints"]] if obj.get("accessConstraints") is not None else None
        })
        return _obj


