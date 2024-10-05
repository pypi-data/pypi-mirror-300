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
from pydantic import BaseModel, Field, StrictBool, StrictStr, validator

class ProjectInfoResponseAllOfDeploySettings(BaseModel):
    eon_compiler: StrictBool = Field(..., alias="eonCompiler")
    sensor: StrictStr = ...
    arduino_library_name: StrictStr = Field(..., alias="arduinoLibraryName")
    tinkergen_library_name: StrictStr = Field(..., alias="tinkergenLibraryName")
    particle_library_name: StrictStr = Field(..., alias="particleLibraryName")
    last_deploy_model_engine: Optional[StrictStr] = Field(None, alias="lastDeployModelEngine")
    __properties = ["eonCompiler", "sensor", "arduinoLibraryName", "tinkergenLibraryName", "particleLibraryName", "lastDeployModelEngine"]

    @validator('sensor')
    def sensor_validate_enum(cls, v):
        if v not in ('accelerometer', 'microphone', 'camera', 'positional', 'environmental', 'fusion', 'unknown'):
            raise ValueError("must validate the enum values ('accelerometer', 'microphone', 'camera', 'positional', 'environmental', 'fusion', 'unknown')")
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
    def from_json(cls, json_str: str) -> ProjectInfoResponseAllOfDeploySettings:
        """Create an instance of ProjectInfoResponseAllOfDeploySettings from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProjectInfoResponseAllOfDeploySettings:
        """Create an instance of ProjectInfoResponseAllOfDeploySettings from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ProjectInfoResponseAllOfDeploySettings.construct(**obj)

        _obj = ProjectInfoResponseAllOfDeploySettings.construct(**{
            "eon_compiler": obj.get("eonCompiler"),
            "sensor": obj.get("sensor"),
            "arduino_library_name": obj.get("arduinoLibraryName"),
            "tinkergen_library_name": obj.get("tinkergenLibraryName"),
            "particle_library_name": obj.get("particleLibraryName"),
            "last_deploy_model_engine": obj.get("lastDeployModelEngine")
        })
        return _obj

