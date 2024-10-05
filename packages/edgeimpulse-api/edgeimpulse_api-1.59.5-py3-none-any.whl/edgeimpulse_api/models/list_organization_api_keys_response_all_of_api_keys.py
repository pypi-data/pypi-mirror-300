# coding: utf-8

"""
    Edge Impulse API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import annotations
from inspect import getfullargspec
import pprint
import re  # noqa: F401
import json

from datetime import datetime

from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, validator

class ListOrganizationApiKeysResponseAllOfApiKeys(BaseModel):
    id: StrictInt = ...
    api_key: StrictStr = Field(..., alias="apiKey")
    name: StrictStr = ...
    created: datetime = ...
    role: StrictStr = ...
    is_transformation_job_key: StrictBool = Field(..., alias="isTransformationJobKey")
    __properties = ["id", "apiKey", "name", "created", "role", "isTransformationJobKey"]

    @validator('role')
    def role_validate_enum(cls, v):
        if v not in ('admin', 'member'):
            raise ValueError("must validate the enum values ('admin', 'member')")
        return v

    class Config:
        allow_population_by_field_name = True
        validate_assignment = False

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self,indent=None) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict(),indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> ListOrganizationApiKeysResponseAllOfApiKeys:
        """Create an instance of ListOrganizationApiKeysResponseAllOfApiKeys from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListOrganizationApiKeysResponseAllOfApiKeys:
        """Create an instance of ListOrganizationApiKeysResponseAllOfApiKeys from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListOrganizationApiKeysResponseAllOfApiKeys.construct(**obj)

        _obj = ListOrganizationApiKeysResponseAllOfApiKeys.construct(**{
            "id": obj.get("id"),
            "api_key": obj.get("apiKey"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "role": obj.get("role"),
            "is_transformation_job_key": obj.get("isTransformationJobKey")
        })
        return _obj

