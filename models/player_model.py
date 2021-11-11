#!/usr/bin/env python
# coding: utf-8
from models.player_gender_model import PlayerGenderModel

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)
from datetime import date
from typing import Optional


class PlayerModel(BaseModel):
    id:  Optional[PositiveInt] = None
    name: constr(max_length=100)
    firstname: constr(max_length=100)
    birthday_date: date
    sexe: PlayerGenderModel
    rank: PositiveInt = 1
