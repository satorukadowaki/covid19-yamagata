#!/usr/bin/env python

from enum import Enum
from pydantic import BaseModel, Field
from typing import Set, List, Optional

class modelResponseProperties(BaseModel):
    isSuccess: bool = Field(None, description='true/falseを返す')
    environment: str = Field(None, description='ENV_NAMEを返す(lower case)')
    version: str = Field(None, description='VERSIONを返す')


class modelResponsePing(BaseModel):
    isSuccess: bool = Field(None, description='true/falseを返す')
    message: str = Field(None, description='メッセージを返す')