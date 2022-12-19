from typing import Optional

from pydantic import BaseModel


class PokemonBase(BaseModel):
    number: int
    name: str
    type_one: str
    type_two: Optional[str] = None
    total: int
    hp: int
    attack: int
    defense: int
    sp_atk: int
    sp_def: int
    speed: int
    generation: int
    legendary: bool


class PokemonCreate(PokemonBase):
    pass


class Pokemon(PokemonBase):
    id: int

    class Config:
        orm_mode = True


class PokemonUpdate(BaseModel):
    number: Optional[int] = None
    name: Optional[str] = None
    type_one: Optional[str] = None
    type_two: Optional[str] = None
    total: Optional[int] = None
    hp: Optional[int] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    sp_atk: Optional[int] = None
    sp_def: Optional[int] = None
    speed: Optional[int] = None
    generation: Optional[int] = None
    legendary: Optional[bool] = None
