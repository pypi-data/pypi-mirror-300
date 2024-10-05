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
from sailpoint.v3.models.workflow_all_of_creator import WorkflowAllOfCreator
from sailpoint.v3.models.workflow_body_owner import WorkflowBodyOwner
from sailpoint.v3.models.workflow_definition import WorkflowDefinition
from sailpoint.v3.models.workflow_modified_by import WorkflowModifiedBy
from sailpoint.v3.models.workflow_trigger import WorkflowTrigger
from typing import Optional, Set
from typing_extensions import Self

class Workflow(BaseModel):
    """
    Workflow
    """ # noqa: E501
    name: Optional[StrictStr] = Field(default=None, description="The name of the workflow")
    owner: Optional[WorkflowBodyOwner] = None
    description: Optional[StrictStr] = Field(default=None, description="Description of what the workflow accomplishes")
    definition: Optional[WorkflowDefinition] = None
    enabled: Optional[StrictBool] = Field(default=False, description="Enable or disable the workflow.  Workflows cannot be created in an enabled state.")
    trigger: Optional[WorkflowTrigger] = None
    id: Optional[StrictStr] = Field(default=None, description="Workflow ID. This is a UUID generated upon creation.")
    execution_count: Optional[StrictInt] = Field(default=None, description="The number of times this workflow has been executed.", alias="executionCount")
    failure_count: Optional[StrictInt] = Field(default=None, description="The number of times this workflow has failed during execution.", alias="failureCount")
    created: Optional[datetime] = Field(default=None, description="The date and time the workflow was created.")
    modified: Optional[datetime] = Field(default=None, description="The date and time the workflow was modified.")
    modified_by: Optional[WorkflowModifiedBy] = Field(default=None, alias="modifiedBy")
    creator: Optional[WorkflowAllOfCreator] = None
    __properties: ClassVar[List[str]] = ["name", "owner", "description", "definition", "enabled", "trigger", "id", "executionCount", "failureCount", "created", "modified", "modifiedBy", "creator"]

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
        """Create an instance of Workflow from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of definition
        if self.definition:
            _dict['definition'] = self.definition.to_dict()
        # override the default output from pydantic by calling `to_dict()` of trigger
        if self.trigger:
            _dict['trigger'] = self.trigger.to_dict()
        # override the default output from pydantic by calling `to_dict()` of modified_by
        if self.modified_by:
            _dict['modifiedBy'] = self.modified_by.to_dict()
        # override the default output from pydantic by calling `to_dict()` of creator
        if self.creator:
            _dict['creator'] = self.creator.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Workflow from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "owner": WorkflowBodyOwner.from_dict(obj["owner"]) if obj.get("owner") is not None else None,
            "description": obj.get("description"),
            "definition": WorkflowDefinition.from_dict(obj["definition"]) if obj.get("definition") is not None else None,
            "enabled": obj.get("enabled") if obj.get("enabled") is not None else False,
            "trigger": WorkflowTrigger.from_dict(obj["trigger"]) if obj.get("trigger") is not None else None,
            "id": obj.get("id"),
            "executionCount": obj.get("executionCount"),
            "failureCount": obj.get("failureCount"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "modifiedBy": WorkflowModifiedBy.from_dict(obj["modifiedBy"]) if obj.get("modifiedBy") is not None else None,
            "creator": WorkflowAllOfCreator.from_dict(obj["creator"]) if obj.get("creator") is not None else None
        })
        return _obj


