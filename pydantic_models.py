from datetime import date
from typing import List, Dict

from pydantic import BaseModel


class FltNum(BaseModel):
    flt_num: int


class Seasonality(BaseModel):
    date: date
    tt: int
    fly_class: Dict[str, int]
    demcluster: int


class ListSeasonality(BaseModel):
    items: List[Seasonality]


class Flight(BaseModel):
    id: int
    flt_num: int
    departure: str
    destination: str


class Fligts(BaseModel):
    items: List[Flight]


class FlyClass(BaseModel):
    c: int
    d: int
    e: int
    g: int
    h: int
    i: int
    j: int
    k: int
    l: int
    m: int
    n: int
    o: int
    p: int
    q: int
    r: int
    t: int
    u: int
    v: int
    x: int
    y: int
    z: int
