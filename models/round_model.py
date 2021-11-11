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
    name: constr(max_length=100)
    date_start: date
    date_end: date
    matchs: Optional[List[MatchModel]]
