#!/usr/bin/env python
# coding: utf-8
from models.match_model import MatchModel

from pydantic import (
    BaseModel,
    constr
)
from datetime import datetime
from typing import Optional, List


class RoundModel(BaseModel):
    name: constr(max_length=100)
    date_start: datetime = datetime.today()
    date_end: datetime = None
    matchs: Optional[List[MatchModel]]
