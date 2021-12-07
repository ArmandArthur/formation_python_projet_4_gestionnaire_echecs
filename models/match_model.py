#!/usr/bin/env python
# coding: utf-8

from pydantic import (
    BaseModel,
    PositiveInt
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
            value_return = 1.0-float(self.score_first.value)
        return MatchScoreEnum(value_return) if value_return is not None else None
