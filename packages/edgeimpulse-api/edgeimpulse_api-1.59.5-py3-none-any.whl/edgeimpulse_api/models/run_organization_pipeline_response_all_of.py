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



from pydantic import BaseModel, Field
from edgeimpulse_api.models.organization_pipeline_run import OrganizationPipelineRun

class RunOrganizationPipelineResponseAllOf(BaseModel):
    pipeline_run: OrganizationPipelineRun = Field(..., alias="pipelineRun")
    __properties = ["pipelineRun"]

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
    def from_json(cls, json_str: str) -> RunOrganizationPipelineResponseAllOf:
        """Create an instance of RunOrganizationPipelineResponseAllOf from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of pipeline_run
        if self.pipeline_run:
            _dict['pipelineRun'] = self.pipeline_run.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RunOrganizationPipelineResponseAllOf:
        """Create an instance of RunOrganizationPipelineResponseAllOf from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return RunOrganizationPipelineResponseAllOf.construct(**obj)

        _obj = RunOrganizationPipelineResponseAllOf.construct(**{
            "pipeline_run": OrganizationPipelineRun.from_dict(obj.get("pipelineRun")) if obj.get("pipelineRun") is not None else None
        })
        return _obj

