from pydantic import BaseModel


class CompititieBase(BaseModel):
    hoogste_positie: int
    huidige_positie: int


class CompititieCreate(CompititieBase):
    hoogste_positie: int
    huidige_positie: int


class Compititie(CompititieBase):
    id: int
    compititie_id: int

    class Config:
        orm_mode = True

class Bekerbase(BaseModel):
    hoogste_positie: int
    huidige_positie: int

class BekerCreate(CompititieBase):
    hoogste_positie: int
    huidige_positie: int


class Beker(CompititieBase):
    id: int
    beker_id: int

    class Config:
        orm_mode = True

class PlayerBase(BaseModel):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str
    team: str

class PlayerCreate(PlayerBase):
    naam: str
    achternaam: str
    email: str
    hashed_password: str
    leeftijd: int
    nationaliteit: str
    team: str


class Player(PlayerBase):
    id: int
    is_active: bool
    compitite: list[Compititie] = []
    beker: list[Beker] = []

    class Config:
        orm_mode = True