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


from typing import List, Optional
from pydantic import BaseModel, StrictInt
from edgeimpulse_api.models.get_impulse_records_request_range import GetImpulseRecordsRequestRange

class GetImpulseRecordsRequest(BaseModel):
    index: Optional[StrictInt] = None
    range: Optional[GetImpulseRecordsRequestRange] = None
    list: Optional[List[StrictInt]] = None
    __properties = ["index", "range", "list"]

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
    def from_json(cls, json_str: str) -> GetImpulseRecordsRequest:
        """Create an instance of GetImpulseRecordsRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of range
        if self.range:
            _dict['range'] = self.range.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GetImpulseRecordsRequest:
        """Create an instance of GetImpulseRecordsRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return GetImpulseRecordsRequest.construct(**obj)

        _obj = GetImpulseRecordsRequest.construct(**{
            "index": obj.get("index"),
            "range": GetImpulseRecordsRequestRange.from_dict(obj.get("range")) if obj.get("range") is not None else None,
            "list": obj.get("list")
        })
        return _obj

