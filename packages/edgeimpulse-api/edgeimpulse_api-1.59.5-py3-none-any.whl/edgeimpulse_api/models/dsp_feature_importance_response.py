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


from typing import Dict, Optional
from pydantic import BaseModel, Field, StrictBool, StrictStr
from edgeimpulse_api.models.dsp_feature_importance_response_all_of_labels import DspFeatureImportanceResponseAllOfLabels

class DspFeatureImportanceResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    has_feature_importance: StrictBool = Field(..., alias="hasFeatureImportance")
    labels: Dict[str, DspFeatureImportanceResponseAllOfLabels] = ...
    __properties = ["success", "error", "hasFeatureImportance", "labels"]

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
    def from_json(cls, json_str: str) -> DspFeatureImportanceResponse:
        """Create an instance of DspFeatureImportanceResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in labels (dict)
        _field_dict = {}
        if self.labels:
            for _key in self.labels:
                if self.labels[_key]:
                    _field_dict[_key] = self.labels[_key].to_dict()
            _dict['labels'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DspFeatureImportanceResponse:
        """Create an instance of DspFeatureImportanceResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return DspFeatureImportanceResponse.construct(**obj)

        _obj = DspFeatureImportanceResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "has_feature_importance": obj.get("hasFeatureImportance"),
            "labels": dict((_k, Dict[str, DspFeatureImportanceResponseAllOfLabels].from_dict(_v)) for _k, _v in obj.get("labels").items())
        })
        return _obj

