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
from pydantic import BaseModel, Field, StrictBool, StrictStr
from edgeimpulse_api.models.list_api_keys_response_all_of_api_keys import ListApiKeysResponseAllOfApiKeys

class ListApiKeysResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    api_keys: List[ListApiKeysResponseAllOfApiKeys] = Field(..., alias="apiKeys", description="List of API keys.")
    __properties = ["success", "error", "apiKeys"]

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
    def from_json(cls, json_str: str) -> ListApiKeysResponse:
        """Create an instance of ListApiKeysResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in api_keys (list)
        _items = []
        if self.api_keys:
            for _item in self.api_keys:
                if _item:
                    _items.append(_item.to_dict())
            _dict['apiKeys'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListApiKeysResponse:
        """Create an instance of ListApiKeysResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListApiKeysResponse.construct(**obj)

        _obj = ListApiKeysResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "api_keys": [ListApiKeysResponseAllOfApiKeys.from_dict(_item) for _item in obj.get("apiKeys")] if obj.get("apiKeys") is not None else None
        })
        return _obj

