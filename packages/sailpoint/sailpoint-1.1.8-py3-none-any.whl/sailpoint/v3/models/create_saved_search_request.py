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
from pydantic import BaseModel, ConfigDict, Field, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from sailpoint.v3.models.column import Column
from sailpoint.v3.models.index import Index
from sailpoint.v3.models.saved_search_detail_filters import SavedSearchDetailFilters
from typing import Optional, Set
from typing_extensions import Self

class CreateSavedSearchRequest(BaseModel):
    """
    CreateSavedSearchRequest
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="The name of the saved search. ")
    description: Optional[StrictStr] = Field(default=None, description="The description of the saved search. ")
    created: Optional[datetime] = Field(default=None, description="A date-time in ISO-8601 format")
    modified: Optional[datetime] = Field(default=None, description="A date-time in ISO-8601 format")
    indices: List[Index] = Field(description="The names of the Elasticsearch indices in which to search. ")
    columns: Optional[Dict[str, List[Column]]] = Field(default=None, description="The columns to be returned (specifies the order in which they will be presented) for each document type.  The currently supported document types are: _accessprofile_, _accountactivity_, _account_, _aggregation_, _entitlement_, _event_, _identity_, and _role_. ")
    query: StrictStr = Field(description="The search query using Elasticsearch [Query String Query](https://www.elastic.co/guide/en/elasticsearch/reference/5.2/query-dsl-query-string-query.html#query-string) syntax from the Query DSL. ")
    fields: Optional[List[StrictStr]] = Field(default=None, description="The fields to be searched against in a multi-field query. ")
    order_by: Optional[Dict[str, List[StrictStr]]] = Field(default=None, description="Sort by index. This takes precedence over the `sort` property. ", alias="orderBy")
    sort: Optional[List[StrictStr]] = Field(default=None, description="The fields to be used to sort the search results. ")
    filters: Optional[SavedSearchDetailFilters] = None
    __properties: ClassVar[List[str]] = ["name", "description", "created", "modified", "indices", "columns", "query", "fields", "orderBy", "sort", "filters"]

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
        """Create an instance of CreateSavedSearchRequest from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each value in columns (dict of array)
        _field_dict_of_array = {}
        if self.columns:
            for _key_columns in self.columns:
                if self.columns[_key_columns] is not None:
                    _field_dict_of_array[_key_columns] = [
                        _item.to_dict() for _item in self.columns[_key_columns]
                    ]
            _dict['columns'] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of filters
        if self.filters:
            _dict['filters'] = self.filters.to_dict()
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if created (nullable) is None
        # and model_fields_set contains the field
        if self.created is None and "created" in self.model_fields_set:
            _dict['created'] = None

        # set to None if modified (nullable) is None
        # and model_fields_set contains the field
        if self.modified is None and "modified" in self.model_fields_set:
            _dict['modified'] = None

        # set to None if fields (nullable) is None
        # and model_fields_set contains the field
        if self.fields is None and "fields" in self.model_fields_set:
            _dict['fields'] = None

        # set to None if order_by (nullable) is None
        # and model_fields_set contains the field
        if self.order_by is None and "order_by" in self.model_fields_set:
            _dict['orderBy'] = None

        # set to None if sort (nullable) is None
        # and model_fields_set contains the field
        if self.sort is None and "sort" in self.model_fields_set:
            _dict['sort'] = None

        # set to None if filters (nullable) is None
        # and model_fields_set contains the field
        if self.filters is None and "filters" in self.model_fields_set:
            _dict['filters'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of CreateSavedSearchRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "indices": obj.get("indices"),
            "columns": dict(
                (_k,
                        [Column.from_dict(_item) for _item in _v]
                        if _v is not None
                        else None
                )
                for _k, _v in obj.get("columns", {}).items()
            ),
            "query": obj.get("query"),
            "fields": obj.get("fields"),
            "orderBy": obj.get("orderBy"),
            "sort": obj.get("sort"),
            "filters": SavedSearchDetailFilters.from_dict(obj["filters"]) if obj.get("filters") is not None else None
        })
        return _obj


