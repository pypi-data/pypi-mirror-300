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
from sailpoint.v3.models.before_provisioning_rule_dto import BeforeProvisioningRuleDto
from sailpoint.v3.models.owner_dto import OwnerDto
from sailpoint.v3.models.provisioning_config import ProvisioningConfig
from sailpoint.v3.models.source_cluster_dto import SourceClusterDto
from typing import Optional, Set
from typing_extensions import Self

class ServiceDeskIntegrationDto(BaseModel):
    """
    ServiceDeskIntegrationDto
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="Unique identifier for the Service Desk integration")
    name: StrictStr = Field(description="Service Desk integration's name. The name must be unique.")
    created: Optional[datetime] = Field(default=None, description="The date and time the Service Desk integration was created")
    modified: Optional[datetime] = Field(default=None, description="The date and time the Service Desk integration was last modified")
    description: StrictStr = Field(description="Service Desk integration's description.")
    type: StrictStr = Field(description="Service Desk integration types:  - ServiceNowSDIM - ServiceNow ")
    owner_ref: Optional[OwnerDto] = Field(default=None, alias="ownerRef")
    cluster_ref: Optional[SourceClusterDto] = Field(default=None, alias="clusterRef")
    cluster: Optional[StrictStr] = Field(default=None, description="Cluster ID for the Service Desk integration (replaced by clusterRef, retained for backward compatibility).")
    managed_sources: Optional[List[StrictStr]] = Field(default=None, description="Source IDs for the Service Desk integration (replaced by provisioningConfig.managedSResourceRefs, but retained here for backward compatibility).", alias="managedSources")
    provisioning_config: Optional[ProvisioningConfig] = Field(default=None, alias="provisioningConfig")
    attributes: Dict[str, Any] = Field(description="Service Desk integration's attributes. Validation constraints enforced by the implementation.")
    before_provisioning_rule: Optional[BeforeProvisioningRuleDto] = Field(default=None, alias="beforeProvisioningRule")
    __properties: ClassVar[List[str]] = ["id", "name", "created", "modified", "description", "type", "ownerRef", "clusterRef", "cluster", "managedSources", "provisioningConfig", "attributes", "beforeProvisioningRule"]

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
        """Create an instance of ServiceDeskIntegrationDto from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of owner_ref
        if self.owner_ref:
            _dict['ownerRef'] = self.owner_ref.to_dict()
        # override the default output from pydantic by calling `to_dict()` of cluster_ref
        if self.cluster_ref:
            _dict['clusterRef'] = self.cluster_ref.to_dict()
        # override the default output from pydantic by calling `to_dict()` of provisioning_config
        if self.provisioning_config:
            _dict['provisioningConfig'] = self.provisioning_config.to_dict()
        # override the default output from pydantic by calling `to_dict()` of before_provisioning_rule
        if self.before_provisioning_rule:
            _dict['beforeProvisioningRule'] = self.before_provisioning_rule.to_dict()
        # set to None if cluster (nullable) is None
        # and model_fields_set contains the field
        if self.cluster is None and "cluster" in self.model_fields_set:
            _dict['cluster'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ServiceDeskIntegrationDto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "description": obj.get("description"),
            "type": obj.get("type") if obj.get("type") is not None else 'ServiceNowSDIM',
            "ownerRef": OwnerDto.from_dict(obj["ownerRef"]) if obj.get("ownerRef") is not None else None,
            "clusterRef": SourceClusterDto.from_dict(obj["clusterRef"]) if obj.get("clusterRef") is not None else None,
            "cluster": obj.get("cluster"),
            "managedSources": obj.get("managedSources"),
            "provisioningConfig": ProvisioningConfig.from_dict(obj["provisioningConfig"]) if obj.get("provisioningConfig") is not None else None,
            "attributes": obj.get("attributes"),
            "beforeProvisioningRule": BeforeProvisioningRuleDto.from_dict(obj["beforeProvisioningRule"]) if obj.get("beforeProvisioningRule") is not None else None
        })
        return _obj


