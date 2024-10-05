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



from pydantic import BaseModel, Field, StrictStr, validator

class AddOrganizationApiKeyRequest(BaseModel):
    name: StrictStr = Field(..., description="Description of the key")
    api_key: StrictStr = Field(..., alias="apiKey", description="API key. This needs to start with `ei_` and will need to be at least 32 characters long.")
    role: StrictStr = ...
    __properties = ["name", "apiKey", "role"]

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
    def from_json(cls, json_str: str) -> AddOrganizationApiKeyRequest:
        """Create an instance of AddOrganizationApiKeyRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddOrganizationApiKeyRequest:
        """Create an instance of AddOrganizationApiKeyRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return AddOrganizationApiKeyRequest.construct(**obj)

        _obj = AddOrganizationApiKeyRequest.construct(**{
            "name": obj.get("name"),
            "api_key": obj.get("apiKey"),
            "role": obj.get("role")
        })
        return _obj

