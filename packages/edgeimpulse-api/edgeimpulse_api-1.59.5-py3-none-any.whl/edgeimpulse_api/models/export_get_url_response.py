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
from pydantic import BaseModel, Field, StrictBool, StrictStr

class ExportGetUrlResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    has_export: StrictBool = Field(..., alias="hasExport")
    created: Optional[datetime] = Field(None, description="Set if hasExport is true")
    url: Optional[StrictStr] = Field(None, description="Set if hasExport is true")
    __properties = ["success", "error", "hasExport", "created", "url"]

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
    def from_json(cls, json_str: str) -> ExportGetUrlResponse:
        """Create an instance of ExportGetUrlResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ExportGetUrlResponse:
        """Create an instance of ExportGetUrlResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ExportGetUrlResponse.construct(**obj)

        _obj = ExportGetUrlResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "has_export": obj.get("hasExport"),
            "created": obj.get("created"),
            "url": obj.get("url")
        })
        return _obj

