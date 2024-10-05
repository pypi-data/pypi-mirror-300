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


from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr, validator
from edgeimpulse_api.models.transformation_block_additional_mount_point import TransformationBlockAdditionalMountPoint

class AddOrganizationTransformationBlockRequest(BaseModel):
    name: StrictStr = ...
    docker_container: StrictStr = Field(..., alias="dockerContainer")
    ind_metadata: StrictBool = Field(..., alias="indMetadata", description="Whether to pass the `--metadata` parameter to the container.")
    description: StrictStr = ...
    cli_arguments: StrictStr = Field(..., alias="cliArguments")
    requests_cpu: Optional[float] = Field(None, alias="requestsCpu")
    requests_memory: Optional[StrictInt] = Field(None, alias="requestsMemory")
    limits_cpu: Optional[float] = Field(None, alias="limitsCpu")
    limits_memory: Optional[StrictInt] = Field(None, alias="limitsMemory")
    additional_mount_points: List[TransformationBlockAdditionalMountPoint] = Field(..., alias="additionalMountPoints")
    operates_on: StrictStr = Field(..., alias="operatesOn")
    allow_extra_cli_arguments: Optional[StrictBool] = Field(None, alias="allowExtraCliArguments")
    parameters: Optional[List[Dict[str, Any]]] = Field(None, description="List of parameters, spec'ed according to https://docs.edgeimpulse.com/docs/tips-and-tricks/adding-parameters-to-custom-blocks")
    max_running_time_str: Optional[StrictStr] = Field(None, alias="maxRunningTimeStr", description="15m for 15 minutes, 2h for 2 hours, 1d for 1 day. If not set, the default is 8 hours.")
    is_public: Optional[StrictBool] = Field(None, alias="isPublic")
    repository_url: Optional[StrictStr] = Field(None, alias="repositoryUrl", description="URL to the source code of this custom learn block.")
    show_in_data_sources: Optional[StrictBool] = Field(None, alias="showInDataSources", description="Whether to show this block in 'Data sources'. Only applies for standalone blocks. (defaults to 'true' when not provided)")
    show_in_create_transformation_job: Optional[StrictBool] = Field(None, alias="showInCreateTransformationJob", description="Whether to show this block in 'Create transformation job'. Only applies for standalone blocks.")
    show_in_synthetic_data: Optional[StrictBool] = Field(None, alias="showInSyntheticData", description="Whether to show this block in 'Synthetic data'. Only applies for standalone blocks.")
    __properties = ["name", "dockerContainer", "indMetadata", "description", "cliArguments", "requestsCpu", "requestsMemory", "limitsCpu", "limitsMemory", "additionalMountPoints", "operatesOn", "allowExtraCliArguments", "parameters", "maxRunningTimeStr", "isPublic", "repositoryUrl", "showInDataSources", "showInCreateTransformationJob", "showInSyntheticData"]

    @validator('operates_on')
    def operates_on_validate_enum(cls, v):
        if v not in ('file', 'directory', 'dataitem', 'standalone'):
            raise ValueError("must validate the enum values ('file', 'directory', 'dataitem', 'standalone')")
        return v

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
    def from_json(cls, json_str: str) -> AddOrganizationTransformationBlockRequest:
        """Create an instance of AddOrganizationTransformationBlockRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in additional_mount_points (list)
        _items = []
        if self.additional_mount_points:
            for _item in self.additional_mount_points:
                if _item:
                    _items.append(_item.to_dict())
            _dict['additionalMountPoints'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddOrganizationTransformationBlockRequest:
        """Create an instance of AddOrganizationTransformationBlockRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return AddOrganizationTransformationBlockRequest.construct(**obj)

        _obj = AddOrganizationTransformationBlockRequest.construct(**{
            "name": obj.get("name"),
            "docker_container": obj.get("dockerContainer"),
            "ind_metadata": obj.get("indMetadata"),
            "description": obj.get("description"),
            "cli_arguments": obj.get("cliArguments"),
            "requests_cpu": obj.get("requestsCpu"),
            "requests_memory": obj.get("requestsMemory"),
            "limits_cpu": obj.get("limitsCpu"),
            "limits_memory": obj.get("limitsMemory"),
            "additional_mount_points": [TransformationBlockAdditionalMountPoint.from_dict(_item) for _item in obj.get("additionalMountPoints")] if obj.get("additionalMountPoints") is not None else None,
            "operates_on": obj.get("operatesOn"),
            "allow_extra_cli_arguments": obj.get("allowExtraCliArguments"),
            "parameters": obj.get("parameters"),
            "max_running_time_str": obj.get("maxRunningTimeStr"),
            "is_public": obj.get("isPublic"),
            "repository_url": obj.get("repositoryUrl"),
            "show_in_data_sources": obj.get("showInDataSources"),
            "show_in_create_transformation_job": obj.get("showInCreateTransformationJob"),
            "show_in_synthetic_data": obj.get("showInSyntheticData")
        })
        return _obj

