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
from pydantic import BaseModel, Field, StrictBool, StrictStr
from edgeimpulse_api.models.verify_dsp_block_url_response_all_of_block import VerifyDspBlockUrlResponseAllOfBlock

class VerifyDspBlockUrlResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    block: Optional[VerifyDspBlockUrlResponseAllOfBlock] = None
    __properties = ["success", "error", "block"]

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
    def from_json(cls, json_str: str) -> VerifyDspBlockUrlResponse:
        """Create an instance of VerifyDspBlockUrlResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of block
        if self.block:
            _dict['block'] = self.block.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> VerifyDspBlockUrlResponse:
        """Create an instance of VerifyDspBlockUrlResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return VerifyDspBlockUrlResponse.construct(**obj)

        _obj = VerifyDspBlockUrlResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "block": VerifyDspBlockUrlResponseAllOfBlock.from_dict(obj.get("block")) if obj.get("block") is not None else None
        })
        return _obj

