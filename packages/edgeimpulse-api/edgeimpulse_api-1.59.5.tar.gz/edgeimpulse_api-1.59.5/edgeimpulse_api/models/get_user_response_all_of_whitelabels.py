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



from pydantic import BaseModel, Field, StrictBool, StrictStr

class GetUserResponseAllOfWhitelabels(BaseModel):
    id: float = ...
    domain: StrictStr = ...
    name: StrictStr = ...
    owner_organization_id: float = Field(..., alias="ownerOrganizationId")
    is_admin: StrictBool = Field(..., alias="isAdmin", description="Whether the user is an admin of the white label.")
    __properties = ["id", "domain", "name", "ownerOrganizationId", "isAdmin"]

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
    def from_json(cls, json_str: str) -> GetUserResponseAllOfWhitelabels:
        """Create an instance of GetUserResponseAllOfWhitelabels from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GetUserResponseAllOfWhitelabels:
        """Create an instance of GetUserResponseAllOfWhitelabels from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return GetUserResponseAllOfWhitelabels.construct(**obj)

        _obj = GetUserResponseAllOfWhitelabels.construct(**{
            "id": obj.get("id"),
            "domain": obj.get("domain"),
            "name": obj.get("name"),
            "owner_organization_id": obj.get("ownerOrganizationId"),
            "is_admin": obj.get("isAdmin")
        })
        return _obj

