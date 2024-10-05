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
from typing import Optional, Set
from typing_extensions import Self

class PasswordPolicyV3Dto(BaseModel):
    """
    PasswordPolicyV3Dto
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="The password policy Id.")
    description: Optional[StrictStr] = Field(default=None, description="Description for current password policy.")
    name: Optional[StrictStr] = Field(default=None, description="The name of the password policy.")
    date_created: Optional[datetime] = Field(default=None, description="Date the Password Policy was created.", alias="dateCreated")
    last_updated: Optional[datetime] = Field(default=None, description="Date the Password Policy was updated.", alias="lastUpdated")
    first_expiration_reminder: Optional[StrictInt] = Field(default=None, description="The number of days before expiration remaninder.", alias="firstExpirationReminder")
    account_id_min_word_length: Optional[StrictInt] = Field(default=None, description="The minimun length of account Id. By default is equals to -1.", alias="accountIdMinWordLength")
    account_name_min_word_length: Optional[StrictInt] = Field(default=None, description="The minimun length of account name. By default is equals to -1.", alias="accountNameMinWordLength")
    min_alpha: Optional[StrictInt] = Field(default=None, description="Maximum alpha. By default is equals to 0.", alias="minAlpha")
    min_character_types: Optional[StrictInt] = Field(default=None, description="MinCharacterTypes. By default is equals to -1.", alias="minCharacterTypes")
    max_length: Optional[StrictInt] = Field(default=None, description="Maximum length of the password.", alias="maxLength")
    min_length: Optional[StrictInt] = Field(default=None, description="Minimum length of the password. By default is equals to 0.", alias="minLength")
    max_repeated_chars: Optional[StrictInt] = Field(default=None, description="Maximum repetition of the same character in the password. By default is equals to -1.", alias="maxRepeatedChars")
    min_lower: Optional[StrictInt] = Field(default=None, description="Minimum amount of lower case character in the password. By default is equals to 0.", alias="minLower")
    min_numeric: Optional[StrictInt] = Field(default=None, description="Minimum amount of numeric characters in the password. By default is equals to 0.", alias="minNumeric")
    min_special: Optional[StrictInt] = Field(default=None, description="Minimum amount of special symbols in the password. By default is equals to 0.", alias="minSpecial")
    min_upper: Optional[StrictInt] = Field(default=None, description="Minimum amount of upper case symbols in the password. By default is equals to 0.", alias="minUpper")
    password_expiration: Optional[StrictInt] = Field(default=None, description="Number of days before current password expires. By default is equals to 90.", alias="passwordExpiration")
    default_policy: Optional[StrictBool] = Field(default=False, description="Defines whether this policy is default or not. Default policy is created automatically when an org is setup. This field is false by default.", alias="defaultPolicy")
    enable_passwd_expiration: Optional[StrictBool] = Field(default=False, description="Defines whether this policy is enabled to expire or not. This field is false by default.", alias="enablePasswdExpiration")
    require_strong_authn: Optional[StrictBool] = Field(default=False, description="Defines whether this policy require strong Auth or not. This field is false by default.", alias="requireStrongAuthn")
    require_strong_auth_off_network: Optional[StrictBool] = Field(default=False, description="Defines whether this policy require strong Auth of network or not. This field is false by default.", alias="requireStrongAuthOffNetwork")
    require_strong_auth_untrusted_geographies: Optional[StrictBool] = Field(default=False, description="Defines whether this policy require strong Auth for untrusted geographies. This field is false by default.", alias="requireStrongAuthUntrustedGeographies")
    use_account_attributes: Optional[StrictBool] = Field(default=False, description="Defines whether this policy uses account attributes or not. This field is false by default.", alias="useAccountAttributes")
    use_dictionary: Optional[StrictBool] = Field(default=False, description="Defines whether this policy uses dictionary or not. This field is false by default.", alias="useDictionary")
    use_identity_attributes: Optional[StrictBool] = Field(default=False, description="Defines whether this policy uses identity attributes or not. This field is false by default.", alias="useIdentityAttributes")
    validate_against_account_id: Optional[StrictBool] = Field(default=False, description="Defines whether this policy validate against account id or not. This field is false by default.", alias="validateAgainstAccountId")
    validate_against_account_name: Optional[StrictBool] = Field(default=False, description="Defines whether this policy validate against account name or not. This field is false by default.", alias="validateAgainstAccountName")
    created: Optional[StrictStr] = None
    modified: Optional[StrictStr] = None
    source_ids: Optional[List[StrictStr]] = Field(default=None, description="List of sources IDs managed by this password policy.", alias="sourceIds")
    __properties: ClassVar[List[str]] = ["id", "description", "name", "dateCreated", "lastUpdated", "firstExpirationReminder", "accountIdMinWordLength", "accountNameMinWordLength", "minAlpha", "minCharacterTypes", "maxLength", "minLength", "maxRepeatedChars", "minLower", "minNumeric", "minSpecial", "minUpper", "passwordExpiration", "defaultPolicy", "enablePasswdExpiration", "requireStrongAuthn", "requireStrongAuthOffNetwork", "requireStrongAuthUntrustedGeographies", "useAccountAttributes", "useDictionary", "useIdentityAttributes", "validateAgainstAccountId", "validateAgainstAccountName", "created", "modified", "sourceIds"]

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
        """Create an instance of PasswordPolicyV3Dto from a JSON string"""
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
        # set to None if description (nullable) is None
        # and model_fields_set contains the field
        if self.description is None and "description" in self.model_fields_set:
            _dict['description'] = None

        # set to None if last_updated (nullable) is None
        # and model_fields_set contains the field
        if self.last_updated is None and "last_updated" in self.model_fields_set:
            _dict['lastUpdated'] = None

        # set to None if created (nullable) is None
        # and model_fields_set contains the field
        if self.created is None and "created" in self.model_fields_set:
            _dict['created'] = None

        # set to None if modified (nullable) is None
        # and model_fields_set contains the field
        if self.modified is None and "modified" in self.model_fields_set:
            _dict['modified'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of PasswordPolicyV3Dto from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "description": obj.get("description"),
            "name": obj.get("name"),
            "dateCreated": obj.get("dateCreated"),
            "lastUpdated": obj.get("lastUpdated"),
            "firstExpirationReminder": obj.get("firstExpirationReminder"),
            "accountIdMinWordLength": obj.get("accountIdMinWordLength"),
            "accountNameMinWordLength": obj.get("accountNameMinWordLength"),
            "minAlpha": obj.get("minAlpha"),
            "minCharacterTypes": obj.get("minCharacterTypes"),
            "maxLength": obj.get("maxLength"),
            "minLength": obj.get("minLength"),
            "maxRepeatedChars": obj.get("maxRepeatedChars"),
            "minLower": obj.get("minLower"),
            "minNumeric": obj.get("minNumeric"),
            "minSpecial": obj.get("minSpecial"),
            "minUpper": obj.get("minUpper"),
            "passwordExpiration": obj.get("passwordExpiration"),
            "defaultPolicy": obj.get("defaultPolicy") if obj.get("defaultPolicy") is not None else False,
            "enablePasswdExpiration": obj.get("enablePasswdExpiration") if obj.get("enablePasswdExpiration") is not None else False,
            "requireStrongAuthn": obj.get("requireStrongAuthn") if obj.get("requireStrongAuthn") is not None else False,
            "requireStrongAuthOffNetwork": obj.get("requireStrongAuthOffNetwork") if obj.get("requireStrongAuthOffNetwork") is not None else False,
            "requireStrongAuthUntrustedGeographies": obj.get("requireStrongAuthUntrustedGeographies") if obj.get("requireStrongAuthUntrustedGeographies") is not None else False,
            "useAccountAttributes": obj.get("useAccountAttributes") if obj.get("useAccountAttributes") is not None else False,
            "useDictionary": obj.get("useDictionary") if obj.get("useDictionary") is not None else False,
            "useIdentityAttributes": obj.get("useIdentityAttributes") if obj.get("useIdentityAttributes") is not None else False,
            "validateAgainstAccountId": obj.get("validateAgainstAccountId") if obj.get("validateAgainstAccountId") is not None else False,
            "validateAgainstAccountName": obj.get("validateAgainstAccountName") if obj.get("validateAgainstAccountName") is not None else False,
            "created": obj.get("created"),
            "modified": obj.get("modified"),
            "sourceIds": obj.get("sourceIds")
        })
        return _obj


