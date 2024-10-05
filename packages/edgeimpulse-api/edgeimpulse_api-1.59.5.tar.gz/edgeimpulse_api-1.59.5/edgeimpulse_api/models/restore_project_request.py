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



from pydantic import BaseModel, Field, StrictInt, StrictStr

class RestoreProjectRequest(BaseModel):
    project_id: StrictInt = Field(..., alias="projectId", description="Source project ID")
    project_api_key: StrictStr = Field(..., alias="projectApiKey", description="Source project API key")
    version_id: StrictInt = Field(..., alias="versionId", description="Source project version ID")
    __properties = ["projectId", "projectApiKey", "versionId"]

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
    def from_json(cls, json_str: str) -> RestoreProjectRequest:
        """Create an instance of RestoreProjectRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RestoreProjectRequest:
        """Create an instance of RestoreProjectRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return RestoreProjectRequest.construct(**obj)

        _obj = RestoreProjectRequest.construct(**{
            "project_id": obj.get("projectId"),
            "project_api_key": obj.get("projectApiKey"),
            "version_id": obj.get("versionId")
        })
        return _obj

