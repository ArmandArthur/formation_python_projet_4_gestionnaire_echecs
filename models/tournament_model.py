from models.round_model import RoundModel

from pydantic import (
    BaseModel,
    PositiveInt,
    constr,
    validator
)
from datetime import date
from typing import Optional, List


class TournamentModel(BaseModel):
    id:  Optional[PositiveInt] = None
    name: constr(max_length=100)
    place: constr(max_length=100)
    start_date: date
    end_date: date
    rounds: Optional[List[RoundModel]] = []
    players: List[PositiveInt]
    rounds_number: PositiveInt = 4

    @validator('players')
    def player_length_must_be_even(cls, v):
        if len(v) % 2 != 0:
            raise ValueError('Players lenght must be even')
        return v

    @validator('rounds_number')
    def init_value(cls, v, values):
        if v >= len(values['players']):
            raise ValueError('The number of rounds must be lower than the number of players')
        return v
