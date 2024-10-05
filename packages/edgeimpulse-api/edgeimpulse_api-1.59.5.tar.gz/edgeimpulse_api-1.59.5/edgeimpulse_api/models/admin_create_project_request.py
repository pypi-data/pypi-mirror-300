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
from edgeimpulse_api.models.project_visibility import ProjectVisibility

class AdminCreateProjectRequest(BaseModel):
    project_name: StrictStr = Field(..., alias="projectName", description="The name of the project.")
    project_visibility: Optional[ProjectVisibility] = Field(None, alias="projectVisibility")
    owner_id: Optional[StrictInt] = Field(None, alias="ownerId", description="Unique identifier of the owner of the new project. Either this parameter or ownerEmail must be set.")
    owner_email: Optional[StrictStr] = Field(None, alias="ownerEmail", description="Email of the owner of the new project. Either this parameter or ownerId must be set.")
    __properties = ["projectName", "projectVisibility", "ownerId", "ownerEmail"]

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
    def from_json(cls, json_str: str) -> AdminCreateProjectRequest:
        """Create an instance of AdminCreateProjectRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AdminCreateProjectRequest:
        """Create an instance of AdminCreateProjectRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return AdminCreateProjectRequest.construct(**obj)

        _obj = AdminCreateProjectRequest.construct(**{
            "project_name": obj.get("projectName"),
            "project_visibility": obj.get("projectVisibility"),
            "owner_id": obj.get("ownerId"),
            "owner_email": obj.get("ownerEmail")
        })
        return _obj

