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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

class ModelPrediction(BaseModel):
    sample_id: StrictInt = Field(..., alias="sampleId")
    start_ms: float = Field(..., alias="startMs")
    end_ms: float = Field(..., alias="endMs")
    label: Optional[StrictStr] = None
    prediction: StrictStr = ...
    prediction_correct: Optional[StrictBool] = Field(None, alias="predictionCorrect")
    f1_score: Optional[float] = Field(None, alias="f1Score", description="Only set for object detection projects")
    anomaly_scores: Optional[List[List[float]]] = Field(None, alias="anomalyScores", description="Only set for visual anomaly projects. 2D array of shape (n, n) with raw anomaly scores, where n varies based on the image input size and the specific visual anomaly algorithm used. The scores corresponds to each grid cell in the image's spatial matrix.")
    __properties = ["sampleId", "startMs", "endMs", "label", "prediction", "predictionCorrect", "f1Score", "anomalyScores"]

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
    def from_json(cls, json_str: str) -> ModelPrediction:
        """Create an instance of ModelPrediction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ModelPrediction:
        """Create an instance of ModelPrediction from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ModelPrediction.construct(**obj)

        _obj = ModelPrediction.construct(**{
            "sample_id": obj.get("sampleId"),
            "start_ms": obj.get("startMs"),
            "end_ms": obj.get("endMs"),
            "label": obj.get("label"),
            "prediction": obj.get("prediction"),
            "prediction_correct": obj.get("predictionCorrect"),
            "f1_score": obj.get("f1Score"),
            "anomaly_scores": obj.get("anomalyScores")
        })
        return _obj

