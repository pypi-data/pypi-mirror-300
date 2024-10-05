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
from pydantic import BaseModel, Field, StrictInt, StrictStr, validator

class AddOrganizationDataCampaignDashboardRequest(BaseModel):
    name: StrictStr = ...
    email_recipient_uids: List[StrictInt] = Field(..., alias="emailRecipientUids", description="List of user IDs to notify for this dashboard (sent daily)")
    when_to_email: StrictStr = Field(..., alias="whenToEmail")
    show_no_of_days: StrictInt = Field(..., alias="showNoOfDays")
    __properties = ["name", "emailRecipientUids", "whenToEmail", "showNoOfDays"]

    @validator('when_to_email')
    def when_to_email_validate_enum(cls, v):
        if v not in ('always', 'on_changes', 'never'):
            raise ValueError("must validate the enum values ('always', 'on_changes', 'never')")
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
    def from_json(cls, json_str: str) -> AddOrganizationDataCampaignDashboardRequest:
        """Create an instance of AddOrganizationDataCampaignDashboardRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> AddOrganizationDataCampaignDashboardRequest:
        """Create an instance of AddOrganizationDataCampaignDashboardRequest from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return AddOrganizationDataCampaignDashboardRequest.construct(**obj)

        _obj = AddOrganizationDataCampaignDashboardRequest.construct(**{
            "name": obj.get("name"),
            "email_recipient_uids": obj.get("emailRecipientUids"),
            "when_to_email": obj.get("whenToEmail"),
            "show_no_of_days": obj.get("showNoOfDays")
        })
        return _obj

