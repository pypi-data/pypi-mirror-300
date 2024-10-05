# coding: utf-8

"""
    Edge Impulse API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import annotations
from inspect import getfullargspec
import json
import pprint
import re  # noqa: F401

from typing import Optional
from pydantic import BaseModel, Field, StrictStr, ValidationError, validator
from edgeimpulse_api.models.classify_sample_response import ClassifySampleResponse
from edgeimpulse_api.models.start_job_response import StartJobResponse
from typing import Any, List
from pydantic import StrictStr, Field

CLASSIFYSAMPLEV2200RESPONSE_ANY_OF_SCHEMAS = ["ClassifySampleResponse", "StartJobResponse"]

class ClassifySampleV2200Response(BaseModel):
    # data type: ClassifySampleResponse
    anyof_schema_1_validator: Optional[ClassifySampleResponse] = None
    # data type: StartJobResponse
    anyof_schema_2_validator: Optional[StartJobResponse] = None
    actual_instance: Any
    any_of_schemas: List[str] = Field(CLASSIFYSAMPLEV2200RESPONSE_ANY_OF_SCHEMAS, const=True)

    class Config:
        validate_assignment = False

    @validator('actual_instance')
    def actual_instance_must_validate_anyof(cls, v):
        instance = cls()
        error_messages = []
        # validate data type: ClassifySampleResponse
        if type(v) is not ClassifySampleResponse:
            error_messages.append(f"Error! Input type `{type(v)}` is not `ClassifySampleResponse`")
        else:
            return v

        # validate data type: StartJobResponse
        if type(v) is not StartJobResponse:
            error_messages.append(f"Error! Input type `{type(v)}` is not `StartJobResponse`")
        else:
            return v

        if error_messages:
            # no match
            raise ValueError("No match found when deserializing the JSON string into ClassifySampleV2200Response with anyOf schemas: ClassifySampleResponse, StartJobResponse. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_json(cls, json_str: str) -> ClassifySampleV2200Response:
        """Returns the object represented by the json string"""
        instance = cls()
        error_messages = []
        # anyof_schema_1_validator: Optional[ClassifySampleResponse] = None
        try:
            instance.actual_instance = ClassifySampleResponse.from_json(json_str)
            return instance
        except ValidationError as e:
             error_messages.append(str(e))
        # anyof_schema_2_validator: Optional[StartJobResponse] = None
        try:
            instance.actual_instance = StartJobResponse.from_json(json_str)
            return instance
        except ValidationError as e:
             error_messages.append(str(e))

        if error_messages:
            # no match
            raise ValueError("No match found when deserializing the JSON string into ClassifySampleV2200Response with anyOf schemas: ClassifySampleResponse, StartJobResponse. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self,indent=None) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is not None:
            return self.actual_instance.to_json(indent=indent)
        else:
            return "null"

    @classmethod
    def from_dict(cls, obj: dict) -> ClassifySampleV2200Response:
        return cls.from_json(json.dumps(obj))

    def to_dict(self) -> dict:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is not None:
            return self.actual_instance.to_dict()
        else:
            return dict()

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.dict())

