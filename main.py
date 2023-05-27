from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data_base.db_query import DB
from pydantic_models import FltNum, Flight, Fligts, Seasonality, \
    ListSeasonality, FltDD
from serializers import serializer_booking
from utils.pd_func import pd_booking_point_aer_svo, pd_booking_point_asf_svo, \
    pd_booking_point_svo_aer, pd_booking_point_svo_asf, \
    pd_booking_point_second_aer_svo, pd_booking_point_second_asf_svo, \
    pd_booking_point_second_svo_aer, pd_booking_point_second_svo_asf, \
    pd_demand_forecast_aer_svo, pd_demand_forecast_asf_svo, \
    pd_demand_forecast_svo_aer, pd_demand_forecast_svo_asf, \
    pd_demand_profile_aer_svo, pd_demand_profile_asf_svo, \
    pd_demand_profile_svo_aer, pd_demand_profile_svo_asf

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
        flyclass = {dct.get(el): res[el] for el in range(3, 25)}
        lst.append(Seasonality(
            date=res[2],
            tt=res[27],
            fly_class=flyclass,
            demcluster=res[30]
            ))
    result = ListSeasonality(items=lst)
    return result


@app.post('/booking')
async def booking(flt_num: FltNum, dd: FltDD):
    """
    Возвращает данные по бронированию в зависимости
    от направления, номера рейса и даты вылета
    """
    result = await db.get_flight_data(flt_num.flt_num)

    if result is None:
        return {'error': 'Данные не найдены'}

    if result[0] == 'AER' and result[1] == 'SVO':
        print('aer-svo')
        result = await db.get_booking_aer_svo(flt_num.flt_num, dd.dd)
        return serializer_booking(result)

    elif result[0] == 'ASF' and result[1] == 'SVO':
        print('asf-svo')
        result = await db.get_booking_asf_svo(flt_num.flt_num, dd.dd)
        return serializer_booking(result)

    elif result[0] == 'SVO' and result[1] == 'AER':
        print('svo-aer')
        result = await db.get_booking_svo_aer(flt_num.flt_num, dd.dd)
        return serializer_booking(result)

    elif result[0] == 'SVO' and result[1] == 'ASF':
        print('svo-asf')
        result = await db.get_booking_svo_asf(flt_num.flt_num, dd.dd)
        return serializer_booking(result)


@app.post('/booking_point')
async def booking_point(flt_num: FltNum, dd: FltDD):
    """
    Возвращает данные по бронированию в зависимости
    от сезона
    """
    result = await db.get_season_from_flight_data(flt_num.flt_num, dd.dd)
    print(result)

    if result is None:
        return {'error': 'Данные не найдены'}

    if result[1] == 'AER' and result[2] == 'SVO':
        print('aer-svo')
        result = await pd_booking_point_aer_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[1] == 'ASF' and result[2] == 'SVO':
        print('asf-svo')
        result = await pd_booking_point_asf_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[1] == 'SVO' and result[2] == 'AER':
        print('svo-aer')
        result = await pd_booking_point_svo_aer(flt_num.flt_num, dd.dd)
        return result

    elif result[1] == 'SVO' and result[2] == 'ASF':
        print('svo-asf')
        result = await pd_booking_point_svo_asf(flt_num.flt_num, dd.dd)
        return result


@app.post('/booking_point_second')
async def booking_point_second(flt_num: FltNum, dd: FltDD):
    """
    Возвращает данные для второго графика резервирования с учетом сезонов
    """
    result = await db.get_flight_data_with_date(flt_num.flt_num, dd.dd)
    print(result)

    if result is None:
        return {'error': 'Данные не найдены'}

    if result[0] == 'AER' and result[1] == 'SVO':
        print('aer-svo')
        result = await pd_booking_point_second_aer_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[0] == 'ASF' and result[1] == 'SVO':
        print('asf-svo')
        result = await pd_booking_point_second_asf_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[0] == 'SVO' and result[1] == 'AER':
        print('svo-aer')
        result = await pd_booking_point_second_svo_aer(flt_num.flt_num, dd.dd)
        return result

    elif result[0] == 'SVO' and result[1] == 'ASF':
        print('svo-asf')
        result = await pd_booking_point_second_svo_asf(flt_num.flt_num, dd.dd)
        return result


@app.post('/demand_profile')
async def demand_profile(flt_num: FltNum, dd: FltDD):
    """
    Возвращает данные для третьей вкладки "Профиль спроса"
    """
    result = await db.get_flight_data_with_date(flt_num.flt_num, dd.dd)
    print(result)

    if result is None:
        return {'error': 'Данные не найдены'}

    if result[0] == 'AER' and result[1] == 'SVO':
        print('aer-svo')
        result = await pd_demand_profile_aer_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[0] == 'ASF' and result[1] == 'SVO':
        print('asf-svo')
        result = await pd_demand_profile_asf_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[0] == 'SVO' and result[1] == 'AER':
        print('svo-aer')
        result = await pd_demand_profile_svo_aer(flt_num.flt_num, dd.dd)
        return result

    elif result[0] == 'SVO' and result[1] == 'ASF':
        print('svo-asf')
        result = await pd_demand_profile_svo_asf(flt_num.flt_num, dd.dd)
        return result


@app.post('/demand_forecast')
async def demand_forecast(flt_num: FltNum, dd: FltDD):
    """
    Возвращает данные для прогноза спроса
    """
    result = await db.pd_demand_forecast(flt_num.flt_num)
    print(result)

    if result is None:
        return {'error': 'Данные не найдены'}

    if result[0].strip() == 'AER' and result[1].strip() == 'SVO':
        print('aer-svo')
        result = await pd_demand_forecast_aer_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[0].strip() == 'ASF' and result[1].strip() == 'SVO':
        print('asf-svo')
        result = await pd_demand_forecast_asf_svo(flt_num.flt_num, dd.dd)
        return result

    elif result[0].strip() == 'SVO' and result[1].strip() == 'AER':
        print('svo-aer')
        result = await pd_demand_forecast_svo_aer(flt_num.flt_num, dd.dd)
        return result

    elif result[0].strip() == 'SVO' and result[1].strip() == 'ASF':
        print('svo-asf')
        result = await pd_demand_forecast_svo_asf(flt_num.flt_num, dd.dd)
        return result
