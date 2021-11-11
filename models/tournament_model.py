#!/usr/bin/env python
# coding: utf-8
from models.round_model import RoundModel
from models.player_model import PlayerModel

from pydantic import (
    BaseModel,
    PositiveInt,
    constr,
    validator
)
from datetime import date
from typing import  Optional, List


class TournamentModel(BaseModel):
    id:  Optional[PositiveInt] = None
    name: constr(max_length=100)
    place: constr(max_length=100)
    start_date: date
    end_date: date
    rounds_number: PositiveInt = 4
    rounds: Optional[List[RoundModel]] = []
    players: List[PositiveInt]

    @validator('players')
    def player_length_must_be_even(cls, v):
        if len(v) % 2 != 0:
            raise ValueError('Players lenght must be even')
        return v
    
    # @validator('rounds_number')
    # def init_value(cls, v):
    #     if v == '':
    #         v = 4
    #     return v