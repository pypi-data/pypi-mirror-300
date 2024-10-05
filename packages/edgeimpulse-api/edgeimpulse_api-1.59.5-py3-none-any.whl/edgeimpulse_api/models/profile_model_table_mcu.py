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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from edgeimpulse_api.models.profile_model_table_mcu_memory import ProfileModelTableMcuMemory

class ProfileModelTableMcu(BaseModel):
    description: StrictStr = ...
    time_per_inference_ms: Optional[StrictInt] = Field(None, alias="timePerInferenceMs")
    memory: Optional[ProfileModelTableMcuMemory] = None
    supported: StrictBool = ...
    mcu_support_error: Optional[StrictStr] = Field(None, alias="mcuSupportError")
    __properties = ["description", "timePerInferenceMs", "memory", "supported", "mcuSupportError"]

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
    def from_json(cls, json_str: str) -> ProfileModelTableMcu:
        """Create an instance of ProfileModelTableMcu from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of memory
        if self.memory:
            _dict['memory'] = self.memory.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProfileModelTableMcu:
        """Create an instance of ProfileModelTableMcu from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ProfileModelTableMcu.construct(**obj)

        _obj = ProfileModelTableMcu.construct(**{
            "description": obj.get("description"),
            "time_per_inference_ms": obj.get("timePerInferenceMs"),
            "memory": ProfileModelTableMcuMemory.from_dict(obj.get("memory")) if obj.get("memory") is not None else None,
            "supported": obj.get("supported"),
            "mcu_support_error": obj.get("mcuSupportError")
        })
        return _obj

