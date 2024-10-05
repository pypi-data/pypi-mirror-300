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
from pydantic import BaseModel, Field
from edgeimpulse_api.models.profile_model_info_memory_eon import ProfileModelInfoMemoryEon

class ProfileModelTableMcuMemory(BaseModel):
    tflite: Optional[ProfileModelInfoMemoryEon] = None
    eon: Optional[ProfileModelInfoMemoryEon] = None
    eon_ram_optimized: Optional[ProfileModelInfoMemoryEon] = Field(None, alias="eonRamOptimized")
    __properties = ["tflite", "eon", "eonRamOptimized"]

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
    def from_json(cls, json_str: str) -> ProfileModelTableMcuMemory:
        """Create an instance of ProfileModelTableMcuMemory from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of tflite
        if self.tflite:
            _dict['tflite'] = self.tflite.to_dict()
        # override the default output from pydantic by calling `to_dict()` of eon
        if self.eon:
            _dict['eon'] = self.eon.to_dict()
        # override the default output from pydantic by calling `to_dict()` of eon_ram_optimized
        if self.eon_ram_optimized:
            _dict['eonRamOptimized'] = self.eon_ram_optimized.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProfileModelTableMcuMemory:
        """Create an instance of ProfileModelTableMcuMemory from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ProfileModelTableMcuMemory.construct(**obj)

        _obj = ProfileModelTableMcuMemory.construct(**{
            "tflite": ProfileModelInfoMemoryEon.from_dict(obj.get("tflite")) if obj.get("tflite") is not None else None,
            "eon": ProfileModelInfoMemoryEon.from_dict(obj.get("eon")) if obj.get("eon") is not None else None,
            "eon_ram_optimized": ProfileModelInfoMemoryEon.from_dict(obj.get("eonRamOptimized")) if obj.get("eonRamOptimized") is not None else None
        })
        return _obj

