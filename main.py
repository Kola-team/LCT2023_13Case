from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_base.db_query import DB
from pydantic_models import FltNum, Flight, Fligts, Seasonality, \
    ListSeasonality

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
async def seasonality(flt_num: FltNum):
    """
    Возвращает данные сезонности по рейсу
    """
    dct = {3: 'b', 4: 'c', 5: 'd', 6: 'e', 7: 'g', 8: 'h',
           9: 'i', 10: 'j', 11: 'k', 12: 'l', 13: 'm', 14: 'n',
           15: 'o', 16: 'p', 17: 'q', 18: 'r', 19: 't', 20: 'u',
           21: 'v', 22: 'x', 23: 'y', 24: 'z'}
    result = await db.get_seasonality(flt_num.flt_num)
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
