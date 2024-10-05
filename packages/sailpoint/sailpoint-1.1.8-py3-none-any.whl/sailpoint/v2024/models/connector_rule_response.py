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
from sailpoint.v2024.models.connector_rule_create_request_signature import ConnectorRuleCreateRequestSignature
from sailpoint.v2024.models.source_code import SourceCode
from typing import Optional, Set
from typing_extensions import Self

class ConnectorRuleResponse(BaseModel):
    """
    ConnectorRuleResponse
    """ # noqa: E501
    name: Annotated[str, Field(min_length=1, strict=True, max_length=128)] = Field(description="the name of the rule")
    description: Optional[StrictStr] = Field(default=None, description="a description of the rule's purpose")
    type: StrictStr = Field(description="the type of rule")
    signature: Optional[ConnectorRuleCreateRequestSignature] = None
    source_code: SourceCode = Field(alias="sourceCode")
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="a map of string to objects")
    id: StrictStr = Field(description="the ID of the rule")
    created: StrictStr = Field(description="an ISO 8601 UTC timestamp when this rule was created")
    modified: Optional[StrictStr] = Field(default=None, description="an ISO 8601 UTC timestamp when this rule was last modified")
    __properties: ClassVar[List[str]] = ["name", "description", "type", "signature", "sourceCode", "attributes", "id", "created", "modified"]

    @field_validator('type')
    def type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in set(['BuildMap', 'ConnectorAfterCreate', 'ConnectorAfterDelete', 'ConnectorAfterModify', 'ConnectorBeforeCreate', 'ConnectorBeforeDelete', 'ConnectorBeforeModify', 'JDBCBuildMap', 'JDBCOperationProvisioning', 'JDBCProvision', 'PeopleSoftHRMSBuildMap', 'PeopleSoftHRMSOperationProvisioning', 'PeopleSoftHRMSProvision', 'RACFPermissionCustomization', 'SAPBuildMap', 'SapHrManagerRule', 'SapHrOperationProvisioning', 'SapHrProvision', 'SuccessFactorsOperationProvisioning', 'WebServiceAfterOperationRule', 'WebServiceBeforeOperationRule']):
            raise ValueError("must be one of enum values ('BuildMap', 'ConnectorAfterCreate', 'ConnectorAfterDelete', 'ConnectorAfterModify', 'ConnectorBeforeCreate', 'ConnectorBeforeDelete', 'ConnectorBeforeModify', 'JDBCBuildMap', 'JDBCOperationProvisioning', 'JDBCProvision', 'PeopleSoftHRMSBuildMap', 'PeopleSoftHRMSOperationProvisioning', 'PeopleSoftHRMSProvision', 'RACFPermissionCustomization', 'SAPBuildMap', 'SapHrManagerRule', 'SapHrOperationProvisioning', 'SapHrProvision', 'SuccessFactorsOperationProvisioning', 'WebServiceAfterOperationRule', 'WebServiceBeforeOperationRule')")
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
        """Create an instance of ConnectorRuleResponse from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of signature
        if self.signature:
            _dict['signature'] = self.signature.to_dict()
        # override the default output from pydantic by calling `to_dict()` of source_code
        if self.source_code:
            _dict['sourceCode'] = self.source_code.to_dict()
        # set to None if attributes (nullable) is None
        # and model_fields_set contains the field
        if self.attributes is None and "attributes" in self.model_fields_set:
            _dict['attributes'] = None

        # set to None if modified (nullable) is None
        # and model_fields_set contains the field
        if self.modified is None and "modified" in self.model_fields_set:
            _dict['modified'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ConnectorRuleResponse from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "name": obj.get("name"),
            "description": obj.get("description"),
            "type": obj.get("type"),
            "signature": ConnectorRuleCreateRequestSignature.from_dict(obj["signature"]) if obj.get("signature") is not None else None,
            "sourceCode": SourceCode.from_dict(obj["sourceCode"]) if obj.get("sourceCode") is not None else None,
            "attributes": obj.get("attributes"),
            "id": obj.get("id"),
            "created": obj.get("created"),
            "modified": obj.get("modified")
        })
        return _obj


