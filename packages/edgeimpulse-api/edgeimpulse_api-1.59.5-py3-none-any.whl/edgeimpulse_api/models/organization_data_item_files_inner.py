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
from pydantic import BaseModel, Field, StrictInt, StrictStr

class OrganizationDataItemFilesInner(BaseModel):
    name: StrictStr = ...
    bucket_path: StrictStr = Field(..., alias="bucketPath")
    size: StrictInt = ...
    last_modified: Optional[datetime] = Field(None, alias="lastModified")
    __properties = ["name", "bucketPath", "size", "lastModified"]

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
    def from_json(cls, json_str: str) -> OrganizationDataItemFilesInner:
        """Create an instance of OrganizationDataItemFilesInner from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrganizationDataItemFilesInner:
        """Create an instance of OrganizationDataItemFilesInner from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return OrganizationDataItemFilesInner.construct(**obj)

        _obj = OrganizationDataItemFilesInner.construct(**{
            "name": obj.get("name"),
            "bucket_path": obj.get("bucketPath"),
            "size": obj.get("size"),
            "last_modified": obj.get("lastModified")
        })
        return _obj

