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
from typing import List, Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr
from edgeimpulse_api.models.job_status import JobStatus
from edgeimpulse_api.models.tuner_space_impulse import TunerSpaceImpulse

class TunerRun(BaseModel):
    tuner_job_id: StrictInt = Field(..., alias="tunerJobId")
    tuner_coordinator_job_id: StrictInt = Field(..., alias="tunerCoordinatorJobId")
    index: StrictInt = ...
    name: Optional[StrictStr] = None
    created: datetime = ...
    job_status: JobStatus = Field(..., alias="jobStatus")
    space: Optional[List[TunerSpaceImpulse]] = Field(None, description="List of impulses specifying the EON Tuner search space")
    __properties = ["tunerJobId", "tunerCoordinatorJobId", "index", "name", "created", "jobStatus", "space"]

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
    def from_json(cls, json_str: str) -> TunerRun:
        """Create an instance of TunerRun from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in space (list)
        _items = []
        if self.space:
            for _item in self.space:
                if _item:
                    _items.append(_item.to_dict())
            _dict['space'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> TunerRun:
        """Create an instance of TunerRun from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return TunerRun.construct(**obj)

        _obj = TunerRun.construct(**{
            "tuner_job_id": obj.get("tunerJobId"),
            "tuner_coordinator_job_id": obj.get("tunerCoordinatorJobId"),
            "index": obj.get("index"),
            "name": obj.get("name"),
            "created": obj.get("created"),
            "job_status": obj.get("jobStatus"),
            "space": [TunerSpaceImpulse.from_dict(_item) for _item in obj.get("space")] if obj.get("space") is not None else None
        })
        return _obj

