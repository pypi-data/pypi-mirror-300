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

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, StrictInt

class DailyMetricsRecord(BaseModel):
    var_date: datetime = Field(..., alias="date", description="Date of the metrics record.")
    total_users: StrictInt = Field(..., alias="totalUsers", description="Total number of users, if the metrics record applies to a non-developer profile organization. For developer profile organizations, we default to 0. ")
    total_staff_users: StrictInt = Field(..., alias="totalStaffUsers", description="Total number of staff users, if the metrics record applies to a non-developer profile organization. For developer profile organizations, we default to 0. ")
    total_projects: StrictInt = Field(..., alias="totalProjects", description="Total number of projects at the end of the metrics record date. ")
    total_current_contract_cpu_compute_time_seconds: StrictInt = Field(..., alias="totalCurrentContractCpuComputeTimeSeconds", description="Total CPU compute time since contract start date, or organization / user creation date, at the end of the metrics record date. ")
    total_current_contract_gpu_compute_time_seconds: StrictInt = Field(..., alias="totalCurrentContractGpuComputeTimeSeconds", description="Total GPU compute time since contract start date, or organization / user creation date, at the end of the metrics record date. ")
    total_current_contract_compute_time_seconds: StrictInt = Field(..., alias="totalCurrentContractComputeTimeSeconds", description="Total compute time since contract start date, or organization / user creation date, at the end of the metrics record date. Compute time is calculated as CPU + 3*GPU compute time. ")
    compute_time_calculated_since: datetime = Field(..., alias="computeTimeCalculatedSince", description="Date from which the total compute time is calculated. This is the contract start date for billing organizations, or organization / user creation date. ")
    total_storage_size_bytes: StrictInt = Field(..., alias="totalStorageSizeBytes", description="Total storage size in bytes at the end of the metrics record date. ")
    users_added: StrictInt = Field(..., alias="usersAdded", description="Number of users added during the metrics record date. ")
    staff_users_added: Optional[StrictInt] = Field(None, alias="staffUsersAdded", description="Number of staff users added during the metrics record date. ")
    users_deleted: StrictInt = Field(..., alias="usersDeleted", description="Number of users deleted during the metrics record date. ")
    staff_users_deleted: Optional[StrictInt] = Field(None, alias="staffUsersDeleted", description="Number of staff users deleted during the metrics record date. ")
    projects_added: StrictInt = Field(..., alias="projectsAdded", description="Number of projects added during the metrics record date. ")
    projects_deleted: StrictInt = Field(..., alias="projectsDeleted", description="Number of projects deleted during the metrics record date. ")
    cpu_compute_time_seconds: StrictInt = Field(..., alias="cpuComputeTimeSeconds", description="Total CPU compute time during the metrics record date. ")
    gpu_compute_time_seconds: StrictInt = Field(..., alias="gpuComputeTimeSeconds", description="Total GPU compute time during the metrics record date. ")
    compute_time_seconds: StrictInt = Field(..., alias="computeTimeSeconds", description="Total compute time during the metrics record date. Compute time is calculated as CPU + 3*GPU compute time. ")
    storage_bytes_added: StrictInt = Field(..., alias="storageBytesAdded", description="Total storage size in bytes added during the metrics record date. ")
    storage_bytes_deleted: StrictInt = Field(..., alias="storageBytesDeleted", description="Total storage size in bytes deleted during the metrics record date. ")
    __properties = ["date", "totalUsers", "totalStaffUsers", "totalProjects", "totalCurrentContractCpuComputeTimeSeconds", "totalCurrentContractGpuComputeTimeSeconds", "totalCurrentContractComputeTimeSeconds", "computeTimeCalculatedSince", "totalStorageSizeBytes", "usersAdded", "staffUsersAdded", "usersDeleted", "staffUsersDeleted", "projectsAdded", "projectsDeleted", "cpuComputeTimeSeconds", "gpuComputeTimeSeconds", "computeTimeSeconds", "storageBytesAdded", "storageBytesDeleted"]

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
    def from_json(cls, json_str: str) -> DailyMetricsRecord:
        """Create an instance of DailyMetricsRecord from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DailyMetricsRecord:
        """Create an instance of DailyMetricsRecord from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return DailyMetricsRecord.construct(**obj)

        _obj = DailyMetricsRecord.construct(**{
            "var_date": obj.get("date"),
            "total_users": obj.get("totalUsers"),
            "total_staff_users": obj.get("totalStaffUsers"),
            "total_projects": obj.get("totalProjects"),
            "total_current_contract_cpu_compute_time_seconds": obj.get("totalCurrentContractCpuComputeTimeSeconds"),
            "total_current_contract_gpu_compute_time_seconds": obj.get("totalCurrentContractGpuComputeTimeSeconds"),
            "total_current_contract_compute_time_seconds": obj.get("totalCurrentContractComputeTimeSeconds"),
            "compute_time_calculated_since": obj.get("computeTimeCalculatedSince"),
            "total_storage_size_bytes": obj.get("totalStorageSizeBytes"),
            "users_added": obj.get("usersAdded"),
            "staff_users_added": obj.get("staffUsersAdded"),
            "users_deleted": obj.get("usersDeleted"),
            "staff_users_deleted": obj.get("staffUsersDeleted"),
            "projects_added": obj.get("projectsAdded"),
            "projects_deleted": obj.get("projectsDeleted"),
            "cpu_compute_time_seconds": obj.get("cpuComputeTimeSeconds"),
            "gpu_compute_time_seconds": obj.get("gpuComputeTimeSeconds"),
            "compute_time_seconds": obj.get("computeTimeSeconds"),
            "storage_bytes_added": obj.get("storageBytesAdded"),
            "storage_bytes_deleted": obj.get("storageBytesDeleted")
        })
        return _obj

