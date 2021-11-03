#!/usr/bin/env python
# coding: utf-8

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)


class MatchModel(BaseModel):
    PlayerIdFirst: PositiveInt
    PlayerIdSecond: PositiveInt
    score: constr(max_length=100)
