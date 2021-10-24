#!/usr/bin/env python
# coding: utf-8
from models.player_gender_model import PlayerGenderModel

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)
from datetime import datetime
from typing import Optional


class PlayerModel(BaseModel):
    Id:  Optional[PositiveInt] = None
    Name: constr(max_length=100)
    FirstName: constr(max_length=100)
    BirthdayDate: datetime
    Sexe: PlayerGenderModel
    Classement: Optional[PositiveInt] = None
