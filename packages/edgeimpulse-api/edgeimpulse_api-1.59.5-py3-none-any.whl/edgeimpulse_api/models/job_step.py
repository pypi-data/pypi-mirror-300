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
from edgeimpulse_api.models.job_failure_details import JobFailureDetails

class JobStep(BaseModel):
    ordinal: float = Field(..., description="ordinal number representing the step")
    progress: Optional[float] = Field(None, description="progress percentage inside the same step example for \"scheduled\" step, we have the following values: 0%: pod scheduled to some node (but node creation may not be finished yet) 50%: image pulling started 90%: image pulled ")
    name: StrictStr = Field(..., description="short name describing the step")
    attempt: Optional[StrictInt] = Field(None, description="execution attempt (starts at 0)")
    failure_details: Optional[JobFailureDetails] = Field(None, alias="failureDetails")
    __properties = ["ordinal", "progress", "name", "attempt", "failureDetails"]

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
    def from_json(cls, json_str: str) -> JobStep:
        """Create an instance of JobStep from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of failure_details
        if self.failure_details:
            _dict['failureDetails'] = self.failure_details.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> JobStep:
        """Create an instance of JobStep from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return JobStep.construct(**obj)

        _obj = JobStep.construct(**{
            "ordinal": obj.get("ordinal"),
            "progress": obj.get("progress"),
            "name": obj.get("name"),
            "attempt": obj.get("attempt"),
            "failure_details": JobFailureDetails.from_dict(obj.get("failureDetails")) if obj.get("failureDetails") is not None else None
        })
        return _obj

