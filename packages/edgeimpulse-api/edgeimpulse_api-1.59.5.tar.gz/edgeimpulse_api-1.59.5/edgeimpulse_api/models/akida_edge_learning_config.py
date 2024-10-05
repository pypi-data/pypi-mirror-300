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
from pydantic import BaseModel, Field, StrictBool

class AkidaEdgeLearningConfig(BaseModel):
    enabled: StrictBool = Field(..., description="True if Akida Edge Learning model creation is enabled. Other properties will be ignored if this is false.")
    additional_classes: Optional[float] = Field(None, alias="additionalClasses", description="Number of additional classes that will be added to the Edge Learning model.")
    neurons_per_class: Optional[float] = Field(None, alias="neuronsPerClass", description="Number of neurons in each class on the last layer in the Edge Learning model.")
    __properties = ["enabled", "additionalClasses", "neuronsPerClass"]

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
    def from_json(cls, json_str: str) -> AkidaEdgeLearningConfig:
        """Create an instance of AkidaEdgeLearningConfig from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AkidaEdgeLearningConfig:
        """Create an instance of AkidaEdgeLearningConfig from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return AkidaEdgeLearningConfig.construct(**obj)

        _obj = AkidaEdgeLearningConfig.construct(**{
            "enabled": obj.get("enabled"),
            "additional_classes": obj.get("additionalClasses"),
            "neurons_per_class": obj.get("neuronsPerClass")
        })
        return _obj

