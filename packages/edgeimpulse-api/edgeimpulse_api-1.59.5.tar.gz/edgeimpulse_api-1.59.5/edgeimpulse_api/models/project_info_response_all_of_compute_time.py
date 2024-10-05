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

from pydantic import BaseModel, Field, StrictInt

class ProjectInfoResponseAllOfComputeTime(BaseModel):
    period_start_date: datetime = Field(..., alias="periodStartDate", description="Start of the current time period.")
    period_end_date: datetime = Field(..., alias="periodEndDate", description="End of the current time period. This is the date when the compute time resets again.")
    time_used_ms: StrictInt = Field(..., alias="timeUsedMs", description="The amount of compute used for the current time period.")
    time_left_ms: StrictInt = Field(..., alias="timeLeftMs", description="The amount of compute left for the current time period.")
    __properties = ["periodStartDate", "periodEndDate", "timeUsedMs", "timeLeftMs"]

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
    def from_json(cls, json_str: str) -> ProjectInfoResponseAllOfComputeTime:
        """Create an instance of ProjectInfoResponseAllOfComputeTime from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ProjectInfoResponseAllOfComputeTime:
        """Create an instance of ProjectInfoResponseAllOfComputeTime from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ProjectInfoResponseAllOfComputeTime.construct(**obj)

        _obj = ProjectInfoResponseAllOfComputeTime.construct(**{
            "period_start_date": obj.get("periodStartDate"),
            "period_end_date": obj.get("periodEndDate"),
            "time_used_ms": obj.get("timeUsedMs"),
            "time_left_ms": obj.get("timeLeftMs")
        })
        return _obj

