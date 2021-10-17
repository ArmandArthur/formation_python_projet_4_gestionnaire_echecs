#!/usr/bin/env python
# coding: utf-8
from controllers.PlayerGender import PlayerGenderController

from pydantic import (
    BaseModel,
    PositiveInt,
    constr
)
from datetime import date
from typing import List, Optional

class PlayerController(BaseModel):
    Id:  Optional[PositiveInt] = None 
    Name: constr(max_length=100)
    FirstName: constr(max_length=100)
    BirthdayDate: date 
    Sexe: PlayerGenderController
    Classement: Optional[PositiveInt] = None 


