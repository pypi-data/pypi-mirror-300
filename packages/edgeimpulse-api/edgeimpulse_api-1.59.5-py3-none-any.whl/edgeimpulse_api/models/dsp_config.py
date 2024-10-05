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
from pydantic import BaseModel, Field, StrictStr
from edgeimpulse_api.models.dsp_group import DSPGroup
from edgeimpulse_api.models.dsp_info import DSPInfo

class DSPConfig(BaseModel):
    dsp: Optional[DSPInfo] = None
    config: Optional[List[DSPGroup]] = None
    config_error: Optional[StrictStr] = Field(None, alias="configError")
    __properties = ["dsp", "config", "configError"]

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
    def from_json(cls, json_str: str) -> DSPConfig:
        """Create an instance of DSPConfig from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of dsp
        if self.dsp:
            _dict['dsp'] = self.dsp.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in config (list)
        _items = []
        if self.config:
            for _item in self.config:
                if _item:
                    _items.append(_item.to_dict())
            _dict['config'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DSPConfig:
        """Create an instance of DSPConfig from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return DSPConfig.construct(**obj)

        _obj = DSPConfig.construct(**{
            "dsp": DSPInfo.from_dict(obj.get("dsp")) if obj.get("dsp") is not None else None,
            "config": [DSPGroup.from_dict(_item) for _item in obj.get("config")] if obj.get("config") is not None else None,
            "config_error": obj.get("configError")
        })
        return _obj

