#!/usr/bin/env python
# coding: utf-8
from models.round_model import RoundModel

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)
from datetime import date
from typing import  Optional, List


class TournamentModel(BaseModel):
    Id:  Optional[PositiveInt] = None
    Name: constr(max_length=100)
    Place: constr(max_length=100)
    StartDate: date
    EndDate: date
    RoundsNumber: PositiveInt = 4
    Rounds: Optional[List[RoundModel]]
