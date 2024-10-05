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
from edgeimpulse_api.models.object_detection_auto_label_response_all_of_results import ObjectDetectionAutoLabelResponseAllOfResults

class ObjectDetectionAutoLabelResponse(BaseModel):
    success: StrictBool = Field(..., description="Whether the operation succeeded")
    error: Optional[StrictStr] = Field(None, description="Optional error description (set if 'success' was false)")
    results: List[ObjectDetectionAutoLabelResponseAllOfResults] = ...
    all_labels: List[StrictStr] = Field(..., alias="allLabels")
    __properties = ["success", "error", "results", "allLabels"]

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
    def from_json(cls, json_str: str) -> ObjectDetectionAutoLabelResponse:
        """Create an instance of ObjectDetectionAutoLabelResponse from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in results (list)
        _items = []
        if self.results:
            for _item in self.results:
                if _item:
                    _items.append(_item.to_dict())
            _dict['results'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ObjectDetectionAutoLabelResponse:
        """Create an instance of ObjectDetectionAutoLabelResponse from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ObjectDetectionAutoLabelResponse.construct(**obj)

        _obj = ObjectDetectionAutoLabelResponse.construct(**{
            "success": obj.get("success"),
            "error": obj.get("error"),
            "results": [ObjectDetectionAutoLabelResponseAllOfResults.from_dict(_item) for _item in obj.get("results")] if obj.get("results") is not None else None,
            "all_labels": obj.get("allLabels")
        })
        return _obj

