#!/usr/bin/env python
# coding: utf-8

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)
from models.match_score_enum import MatchScoreEnum

class MatchModel(BaseModel):
    player_id_first: PositiveInt
    player_id_second: PositiveInt
    score_first: MatchScoreEnum = None

    @property
    def score_second(self):
        value_return = None
        if self.score_first is not None:
            value_return = 1.0-self.score_first
        return value_return