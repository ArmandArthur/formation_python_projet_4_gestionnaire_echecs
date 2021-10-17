#!/usr/bin/env python
# coding: utf-8
from controllers.PlayerGender import PlayerGenderController

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)
from datetime import datetime
from typing import List, Optional

class PlayerController(BaseModel):
    Id: PositiveInt
    Name: constr(max_length=100)
    FirstName: constr(max_length=100)
    BirthdayDate: datetime 
    Sexe: PlayerGenderController
    Classement: PositiveInt



