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
from pydantic import BaseModel, Field, StrictInt, StrictStr, validator
from edgeimpulse_api.models.performance_calibration_parameters_standard import PerformanceCalibrationParametersStandard

class PerformanceCalibrationParameters(BaseModel):
    type: StrictStr = Field(..., description="The post-processing algorithm type.")
    version: StrictInt = Field(..., description="The version number of the post-processing algorithm.")
    parameters_standard: Optional[PerformanceCalibrationParametersStandard] = Field(None, alias="parametersStandard")
    __properties = ["type", "version", "parametersStandard"]

    @validator('type')
    def type_validate_enum(cls, v):
        if v not in ('standard'):
            raise ValueError("must validate the enum values ('standard')")
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
    def from_json(cls, json_str: str) -> PerformanceCalibrationParameters:
        """Create an instance of PerformanceCalibrationParameters from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of parameters_standard
        if self.parameters_standard:
            _dict['parametersStandard'] = self.parameters_standard.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> PerformanceCalibrationParameters:
        """Create an instance of PerformanceCalibrationParameters from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return PerformanceCalibrationParameters.construct(**obj)

        _obj = PerformanceCalibrationParameters.construct(**{
            "type": obj.get("type"),
            "version": obj.get("version"),
            "parameters_standard": PerformanceCalibrationParametersStandard.from_dict(obj.get("parametersStandard")) if obj.get("parametersStandard") is not None else None
        })
        return _obj

