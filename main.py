from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

from data_base.db_query import DB

app = FastAPI()
db = DB()


class Flight(BaseModel):
    id: int
    flt_num: int
    departure: str
    destination: str


class Fligts(BaseModel):
    items: List[Flight]


@app.get('/all_flight')
async def all_flight():
    result = await db.get_all_flights()
    lst = []
    for f in result:
        lst.append(Flight(id=f[0],
                   flt_num=f[1],
                   departure=f[2],
                   destination=f[3]))
    result = Fligts(items=lst)
    return result
