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
from pydantic import BaseModel, Field, StrictInt, StrictStr

class CreateEnterpriseTrialResponseAllOf(BaseModel):
    user_id: Optional[StrictInt] = Field(None, alias="userId", description="ID of the user created for the trial, if the user did not already exist.")
    redirect_url: Optional[StrictStr] = Field(None, alias="redirectUrl", description="URL to redirect the user to in order to access the enterprise trial.")
    __properties = ["userId", "redirectUrl"]

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
    def from_json(cls, json_str: str) -> CreateEnterpriseTrialResponseAllOf:
        """Create an instance of CreateEnterpriseTrialResponseAllOf from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> CreateEnterpriseTrialResponseAllOf:
        """Create an instance of CreateEnterpriseTrialResponseAllOf from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return CreateEnterpriseTrialResponseAllOf.construct(**obj)

        _obj = CreateEnterpriseTrialResponseAllOf.construct(**{
            "user_id": obj.get("userId"),
            "redirect_url": obj.get("redirectUrl")
        })
        return _obj

