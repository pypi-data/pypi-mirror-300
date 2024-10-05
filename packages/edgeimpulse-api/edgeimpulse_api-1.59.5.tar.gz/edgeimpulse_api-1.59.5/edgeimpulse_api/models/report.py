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
from typing import Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr
from edgeimpulse_api.models.job_created_by_user import JobCreatedByUser

class Report(BaseModel):
    id: StrictInt = ...
    created: datetime = ...
    created_by_user: Optional[JobCreatedByUser] = Field(None, alias="createdByUser")
    job_id: StrictInt = Field(..., alias="jobId")
    job_finished: StrictBool = Field(..., alias="jobFinished")
    job_finished_successful: StrictBool = Field(..., alias="jobFinishedSuccessful")
    download_link: Optional[StrictStr] = Field(None, alias="downloadLink")
    report_start_date: datetime = Field(..., alias="reportStartDate")
    report_end_date: datetime = Field(..., alias="reportEndDate")
    __properties = ["id", "created", "createdByUser", "jobId", "jobFinished", "jobFinishedSuccessful", "downloadLink", "reportStartDate", "reportEndDate"]

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
    def from_json(cls, json_str: str) -> Report:
        """Create an instance of Report from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of created_by_user
        if self.created_by_user:
            _dict['createdByUser'] = self.created_by_user.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Report:
        """Create an instance of Report from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return Report.construct(**obj)

        _obj = Report.construct(**{
            "id": obj.get("id"),
            "created": obj.get("created"),
            "created_by_user": JobCreatedByUser.from_dict(obj.get("createdByUser")) if obj.get("createdByUser") is not None else None,
            "job_id": obj.get("jobId"),
            "job_finished": obj.get("jobFinished"),
            "job_finished_successful": obj.get("jobFinishedSuccessful"),
            "download_link": obj.get("downloadLink"),
            "report_start_date": obj.get("reportStartDate"),
            "report_end_date": obj.get("reportEndDate")
        })
        return _obj

