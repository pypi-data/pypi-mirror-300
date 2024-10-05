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
from pydantic import BaseModel, Field, StrictBool, StrictInt, StrictStr

class ListEmailResponseAllOfEmails(BaseModel):
    user_id: Optional[StrictInt] = Field(None, alias="userId")
    project_id: Optional[StrictInt] = Field(None, alias="projectId")
    var_from: StrictStr = Field(..., alias="from")
    to: StrictStr = ...
    created: datetime = ...
    subject: StrictStr = ...
    body_text: StrictStr = Field(..., alias="bodyText")
    body_html: StrictStr = Field(..., alias="bodyHTML")
    sent: StrictBool = ...
    provider_response: StrictStr = Field(..., alias="providerResponse")
    __properties = ["userId", "projectId", "from", "to", "created", "subject", "bodyText", "bodyHTML", "sent", "providerResponse"]

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
    def from_json(cls, json_str: str) -> ListEmailResponseAllOfEmails:
        """Create an instance of ListEmailResponseAllOfEmails from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ListEmailResponseAllOfEmails:
        """Create an instance of ListEmailResponseAllOfEmails from a dict"""
        if obj is None:
            return None

        if type(obj) is not dict:
            return ListEmailResponseAllOfEmails.construct(**obj)

        _obj = ListEmailResponseAllOfEmails.construct(**{
            "user_id": obj.get("userId"),
            "project_id": obj.get("projectId"),
            "var_from": obj.get("from"),
            "to": obj.get("to"),
            "created": obj.get("created"),
            "subject": obj.get("subject"),
            "body_text": obj.get("bodyText"),
            "body_html": obj.get("bodyHTML"),
            "sent": obj.get("sent"),
            "provider_response": obj.get("providerResponse")
        })
        return _obj

