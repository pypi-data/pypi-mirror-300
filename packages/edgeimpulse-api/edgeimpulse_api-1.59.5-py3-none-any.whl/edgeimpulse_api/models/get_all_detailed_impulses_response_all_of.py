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


from typing import List
from pydantic import BaseModel, Field, StrictStr
from edgeimpulse_api.models.detailed_impulse import DetailedImpulse
from edgeimpulse_api.models.get_all_detailed_impulses_response_all_of_metric_keys_by_category import GetAllDetailedImpulsesResponseAllOfMetricKeysByCategory

class GetAllDetailedImpulsesResponseAllOf(BaseModel):
    impulses: List[DetailedImpulse] = ...
    metric_keys_by_category: List[GetAllDetailedImpulsesResponseAllOfMetricKeysByCategory] = Field(..., alias="metricKeysByCategory")
    extra_table_columns: List[StrictStr] = Field(..., alias="extraTableColumns", description="Which extra impulse information should be shown in the impulses table.")
    __properties = ["impulses", "metricKeysByCategory", "extraTableColumns"]

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
    def from_json(cls, json_str: str) -> GetAllDetailedImpulsesResponseAllOf:
        """Create an instance of GetAllDetailedImpulsesResponseAllOf from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in impulses (list)
        _items = []
        if self.impulses:
            for _item in self.impulses:
                if _item:
                    _items.append(_item.to_dict())
            _dict['impulses'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in metric_keys_by_category (list)
        _items = []
        if self.metric_keys_by_category:
            for _item in self.metric_keys_by_category:
                if _item:
                    _items.append(_item.to_dict())
            _dict['metricKeysByCategory'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GetAllDetailedImpulsesResponseAllOf:
        """Create an instance of GetAllDetailedImpulsesResponseAllOf from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return GetAllDetailedImpulsesResponseAllOf.construct(**obj)

        _obj = GetAllDetailedImpulsesResponseAllOf.construct(**{
            "impulses": [DetailedImpulse.from_dict(_item) for _item in obj.get("impulses")] if obj.get("impulses") is not None else None,
            "metric_keys_by_category": [GetAllDetailedImpulsesResponseAllOfMetricKeysByCategory.from_dict(_item) for _item in obj.get("metricKeysByCategory")] if obj.get("metricKeysByCategory") is not None else None,
            "extra_table_columns": obj.get("extraTableColumns")
        })
        return _obj

