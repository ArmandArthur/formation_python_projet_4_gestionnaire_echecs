#!/usr/bin/env python
# coding: utf-8
from models.player_gender_model import PlayerGenderModel

from pydantic import (
    BaseModel,
    PositiveInt,
    constr,
    validator
)
from datetime import date


class PlayerModel(BaseModel):
    id: PositiveInt
    name: constr(max_length=100, strict=True, min_length=2)
    firstname: constr(max_length=100, strict=True, min_length=2)
    birthday_date: date
    sexe: PlayerGenderModel
    rank: PositiveInt = 1

    class Config:
        validate_assignment = True

    @validator('rank')
    def rank_must_be_integer(cls, v):
        print(type(v))
        if isinstance(v, str):
            raise ValueError('Rank must be integer')
        return v
