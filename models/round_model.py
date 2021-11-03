#!/usr/bin/env python
# coding: utf-8
from models.match_model import MatchModel

from pydantic import (
    BaseModel,
    constr
)
from datetime import date
from typing import Optional, List


class RoundModel(BaseModel):
    Name: constr(max_length=100)
    DateStart: date
    DateEnd: date
    matchs: Optional[List[MatchModel]]
