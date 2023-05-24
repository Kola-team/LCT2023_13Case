from datetime import date
from typing import List, Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from data_base.db_query import DB

app = FastAPI()
db = DB()

origins = [
    'http://localhost:3000',
    'http://0.0.0.0:3000',
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Flight(BaseModel):
    id: int
    flt_num: int
    departure: str
    destination: str


class Fligts(BaseModel):
    items: List[Flight]


class Seasonality(BaseModel):
    date: date
    tt: int
    # b: int
    # c: int
    # d: int
    # e: int
    # g: int
    # h: int
    # i: int
    # j: int
    # k: int
    # l: int
    # m: int
    # n: int
    # o: int
    # p: int
    # q: int
    # r: int
    # t: int
    # u: int
    # v: int
    # x: int
    # y: int
    # z: int
    fly_class: Dict[str, int]
    demcluster: int


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


class ListSeasonality(BaseModel):
    items: List[Seasonality]


@app.get('/all_flight')
async def all_flight():
    """
     Возвращает все рейсы
    """
    result = await db.get_all_flights()
    lst = []
    for f in result:
        lst.append(Flight(id=f[0],
                   flt_num=f[1],
                   departure=f[2],
                   destination=f[3]))
    result = Fligts(items=lst)
    return result


@app.post('/seasonality')
async def seasonality(flt_num: int):
    """
    Возвращает данные сезонности по рейсу
    """
    dct = {3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'g', 8: 'h',
           9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n',
           15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 't', 20: 'u',
           21: 'v', 22: 'x', 23: 'y', 24: 'z'}
    result = await db.get_seasonality(flt_num)
    lst = []
    for res in result:
        # print(res)
        flyclass = {dct.get(el): res[el] for el in range(3, 25)}
        lst.append(Seasonality(
            date=res[2],
            tt=res[27],
            fly_class=flyclass,
            demcluster=res[30]
            ))
    result = ListSeasonality(items=lst)
    return result
