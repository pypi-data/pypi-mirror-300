# coding: utf-8

"""
    Edge Impulse API

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)  # noqa: E501

    The version of the OpenAPI document: 1.0.0
    Generated by: https://openapi-generator.tech
"""


from inspect import getfullargspec
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class UserProjectsSortOrder(str, Enum):
    """
    allowed enum values
    """

    CREATED_ASC = 'created-asc'
    CREATED_DESC = 'created-desc'
    ADDED_ASC = 'added-asc'
    ADDED_DESC = 'added-desc'
    NAME_ASC = 'name-asc'
    NAME_DESC = 'name-desc'
    LAST_ACCESSED_DESC = 'last-accessed-desc'

