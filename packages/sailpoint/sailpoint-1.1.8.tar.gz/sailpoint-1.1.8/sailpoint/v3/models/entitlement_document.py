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
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v3.models.base_segment import BaseSegment
from sailpoint.v3.models.document_type import DocumentType
from sailpoint.v3.models.entitlement_document_all_of_source import EntitlementDocumentAllOfSource
from typing import Optional, Set
from typing_extensions import Self

class EntitlementDocument(BaseModel):
    """
    Entitlement
    """ # noqa: E501
    id: StrictStr
    name: StrictStr
    type: DocumentType = Field(alias="_type")
    modified: Optional[datetime] = Field(default=None, description="ISO-8601 date-time referring to the time when the object was last modified.")
    synced: Optional[StrictStr] = Field(default=None, description="ISO-8601 date-time referring to the date-time when object was queued to be synced into search database for use in the search API.   This date-time changes anytime there is an update to the object, which triggers a synchronization event being sent to the search database.  There may be some delay between the `synced` time and the time when the updated data is actually available in the search API. ")
    display_name: Optional[StrictStr] = Field(default=None, description="Entitlement's display name.", alias="displayName")
    source: Optional[EntitlementDocumentAllOfSource] = None
    segments: Optional[List[BaseSegment]] = Field(default=None, description="Segments with the role.")
    segment_count: Optional[StrictInt] = Field(default=None, description="Number of segments with the role.", alias="segmentCount")
    requestable: Optional[StrictBool] = Field(default=False, description="Indicates whether the entitlement is requestable.")
    cloud_governed: Optional[StrictBool] = Field(default=False, description="Indicates whether the entitlement is cloud governed.", alias="cloudGoverned")
    created: Optional[datetime] = Field(default=None, description="ISO-8601 date-time referring to the time when the object was created.")
    privileged: Optional[StrictBool] = Field(default=False, description="Indicates whether the entitlement is privileged.")
    identity_count: Optional[StrictInt] = Field(default=None, description="Number of identities who have access to the entitlement.", alias="identityCount")
    tags: Optional[List[StrictStr]] = Field(default=None, description="Tags that have been applied to the object.")
    __properties: ClassVar[List[str]] = ["id", "name", "_type", "modified", "synced", "displayName", "source", "segments", "segmentCount", "requestable", "cloudGoverned", "created", "privileged", "identityCount", "tags"]

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
        """Create an instance of EntitlementDocument from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of source
        if self.source:
            _dict['source'] = self.source.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in segments (list)
        _items = []
        if self.segments:
            for _item_segments in self.segments:
                if _item_segments:
                    _items.append(_item_segments.to_dict())
            _dict['segments'] = _items
        # set to None if modified (nullable) is None
        # and model_fields_set contains the field
        if self.modified is None and "modified" in self.model_fields_set:
            _dict['modified'] = None

        # set to None if created (nullable) is None
        # and model_fields_set contains the field
        if self.created is None and "created" in self.model_fields_set:
            _dict['created'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of EntitlementDocument from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "_type": obj.get("_type"),
            "modified": obj.get("modified"),
            "synced": obj.get("synced"),
            "displayName": obj.get("displayName"),
            "source": EntitlementDocumentAllOfSource.from_dict(obj["source"]) if obj.get("source") is not None else None,
            "segments": [BaseSegment.from_dict(_item) for _item in obj["segments"]] if obj.get("segments") is not None else None,
            "segmentCount": obj.get("segmentCount"),
            "requestable": obj.get("requestable") if obj.get("requestable") is not None else False,
            "cloudGoverned": obj.get("cloudGoverned") if obj.get("cloudGoverned") is not None else False,
            "created": obj.get("created"),
            "privileged": obj.get("privileged") if obj.get("privileged") is not None else False,
            "identityCount": obj.get("identityCount"),
            "tags": obj.get("tags")
        })
        return _obj


