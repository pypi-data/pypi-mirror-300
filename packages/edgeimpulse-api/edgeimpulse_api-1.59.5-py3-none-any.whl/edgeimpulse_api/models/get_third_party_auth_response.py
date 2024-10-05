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


from typing import Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr
from edgeimpulse_api.models.third_party_auth import ThirdPartyAuth

class GetThirdPartyAuthResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    auth: ThirdPartyAuth = ...
    __properties = ["success", "error", "auth"]

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
    def from_json(cls, json_str: str) -> GetThirdPartyAuthResponse:
        """Create an instance of GetThirdPartyAuthResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of auth
        if self.auth:
            _dict['auth'] = self.auth.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GetThirdPartyAuthResponse:
        """Create an instance of GetThirdPartyAuthResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return GetThirdPartyAuthResponse.construct(**obj)

        _obj = GetThirdPartyAuthResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "auth": ThirdPartyAuth.from_dict(obj.get("auth")) if obj.get("auth") is not None else None
        })
        return _obj

