import pandas as pd

from math import isnan
# from scipy.signal import periodogram
# from sklearn.linear_model import LinearRegression
from statsmodels.tsa.seasonal import seasonal_decompose

from logger import logger
from app.config import path_project
import datetime, time


starttime_script = time.time()

# Путь до каталога с файлами данных
path = path_project.date



segment_names = ['B', 'C', 'D', 'E',  'G', 'H', 'I', 'J', 'K', 'L', 'M','N', 'O', 'P', 'Q', 'R',  'T', 'U', 'V',  'X', 'Y', 'Z']
cabin_names = ['CT', 'YT']


MAXDATE = pd.to_datetime('2020-12-31')
MINDATE = pd.to_datetime('2020-01-01')

def generate_departure_days(std,fnd,freq):
    freqlst = [int(d) for d in list(freq) if d !=' ']
    fnd = min(MAXDATE,fnd)
    std = max(MINDATE,std)
    dayslist = list()
    dn = 0; nextdate = std
    while nextdate <= fnd:
        nextdate_weekday = nextdate.weekday()+1
        if nextdate_weekday in freqlst:
            dayslist.append(nextdate)
        dn += 1
        nextdate = std + pd.Timedelta(dn,'d')
    return dayslist


def estimate_seasonal_trend(data, target_col, index_col, period, minval):
    # period - кортеж из двух чисел - первого и последнего фактических значений категории.
    # target_col - признак целевого значения в наборе data
    # index_col - признак со значениями соответствующей категории в наборе data
    season =  dict()
    for i in range(period[0],period[1]+1):
        mn_val = data.loc[data[index_col]==i][target_col].mean()
        if mn_val>0: season[i]=mn_val

    return season


def get_most_freq_seg(segs):
    x = dict()
    for k in segs.keys():
        if segs[k] is None:
            pass
        else:
            s = list(segs[k].keys())[0]
            x[s] = x.get(s,0)+1
    return list({k: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}.keys())[0]


def estimate_seasonal_segments(data, segnames,indexcol):
    seasonal_segs = dict()
    for i in range(1,366):
        total_day = data.loc[data[indexcol]==i]["TT"].mean()
        # не учитываю сезонное сглаживание на дату
        # считаю пропорцию без сглаживания
        inf = dict()
        if total_day >0 :
            for seg in segnames:
                segval = data.loc[data[indexcol]==i][seg].mean()
                segval = 0 if isnan(segval) else segval
                segshare = segval / total_day
                inf[seg] = segshare
            inf = {k:v for k,v in inf.items() if v > 0}
            seasonal_segs[i] = {k: v for k, v in sorted(inf.items(), key=lambda item: item[1], reverse=True)}
    return seasonal_segs



def prepare_segment_composition(annual, seasonal, day ):
    compos = dict()
    if (day in annual.keys()) and (day in seasonal.keys()) :
        val = round(annual[day])
        shares = seasonal[day]

        for seg in shares.keys():
            compos[seg] = round(val*shares[seg])
        nval = sum(compos.values())
        err = val - nval
        if abs(err)>0:
            corrseg = list(compos.keys())[0]
            compos[corrseg] = compos[corrseg] + err
        compos["TT"] = nval
        return compos
    else:
        print("Ошибка", day)
        return None


flight_data_filename = path+"FlightData.csv"

flights = pd.read_csv(flight_data_filename, parse_dates=["DD"], dayfirst=True)
flights["dayofyear"] = flights.DD.dt.dayofyear


rasp2020 = pd.read_csv(path+"RASP2020.csv", sep=";", parse_dates=["EFFV_DATE","DISC_DATE"], dayfirst=True)
logger.info(f"Свернутый Формат Расписания {rasp2020.shape}")

rasp2020["FD"] = rasp2020.apply( lambda x: generate_departure_days(x.EFFV_DATE, x.DISC_DATE, x.FREQ), axis=1)
rasp2020.drop(["AIRLINE_CODESH","NUM_LEGS","CAPTURE_DATE1","DEP_TIME1","ARR_TIME1","EQUIP1"],axis=1, inplace=True)
ForFlights = rasp2020.explode("FD",ignore_index=True)
ForFlights.drop(ForFlights[ForFlights.FD.isnull()].index, inplace=True)
ForFlights["FD"] = ForFlights.FD.dt.normalize()
ForFlights.drop_duplicates(subset=["FLT_NUMSH","FD"], inplace=True, ignore_index=True)
ForFlights.sort_values(by="FD", inplace=True, ignore_index=True)
ForFlights["dayofyear"] = ForFlights.FD.dt.dayofyear
logger.info(f'Развернутый Формат Расписания {ForFlights.shape}')
logger.info(f'Крайняя дата в расписании {ForFlights.FD.max()}')
cols = segment_names+["TT"]
for c in cols:
    ForFlights[c] = 0




ForFlights["LEG_ORIG"] = ForFlights.LEG_ORIG.apply(lambda x: x.strip())
ForFlights["LEG_DEST"] = ForFlights.LEG_DEST.apply(lambda x: x.strip())

flt_lst = list(ForFlights.FLT_NUMSH.unique())
logger.info(f'всего рейсов в расписании {len(flt_lst)}')


cnt = 1
LEAP_DAY = pd.to_datetime('2020-02-29')




for fltn in flt_lst:
    flt_ind = list(ForFlights[ForFlights.FLT_NUMSH==fltn].index)
    flt_ind_len = len(flt_ind)
    fst_ind = list(flt_ind)[0]
    orig = ForFlights.at[fst_ind,"LEG_ORIG"]
    dest = ForFlights.at[fst_ind,"LEG_DEST"]
    cnt+=1
    #  Формируем профиль по конкретному полету
    oneflight = flights[flights.FLT_NUM==fltn].copy()
    of_q25 = oneflight.TT.quantile(0.25); of_q75 = oneflight.TT.quantile(0.75)
    of_upperlimit = of_q75 + 1.5 * (of_q75-of_q25) ; of_lowerlimit = of_q25 - 1.5 * (of_q75-of_q25)
    oneflight["SmTT"] = oneflight.TT.apply(lambda x: x if x <= of_upperlimit else of_upperlimit)
    annual_trend = estimate_seasonal_trend(oneflight,"SmTT","dayofyear",(1,365),of_lowerlimit)

    seasonal_segments = estimate_seasonal_segments(oneflight, segment_names, "dayofyear")

    missing_days = [k for k in range(1,366) if k not in annual_trend.keys()]
    logger.info(f'{cnt}. Рейс {fltn}. Маршрут {orig}-{dest}. Запланировано {flt_ind_len} вылетов. Отсутствует информация по {len(missing_days)} вылетам, есть по {len(annual_trend.keys())} вылетам.')
    # Формируем профиль по всем полетам в этом направлении
    allflights = flights[(flights.SORG==orig)&(flights.SDST==dest)].copy()
    af_q25 = allflights.TT.quantile(0.25); af_q75 = allflights.TT.quantile(0.75)
    af_upperlimit = af_q75 + 1.5 * (af_q75-af_q25) ; af_lowerlimit = af_q25 - 1.5 * (af_q75-af_q25)
    allflights["SmTT"] = allflights.TT.apply(lambda x: x if x <= af_upperlimit else af_upperlimit)
    direct_annual_trend = estimate_seasonal_trend(allflights,"SmTT","dayofyear",(1,365),af_lowerlimit)

    direct_seasonal_segments = estimate_seasonal_segments(allflights, segment_names, "dayofyear")


    for i in flt_ind:
        day = ForFlights.at[i,"dayofyear"]
        cdate = ForFlights.at[i,"FD"]
        day = day if cdate < LEAP_DAY else day-1 #correction for leap year

        if day in missing_days:
            #полет по данному рейсу в этот день года не совершался
            composition = prepare_segment_composition(direct_annual_trend, direct_seasonal_segments, day)
        else:
            #полет раньше по данному рейсу был
            composition = prepare_segment_composition(annual_trend,seasonal_segments,day)
        for k in composition.keys():
            ForFlights.at[i,k] = composition[k]



ForFlights.drop(["dayofyear"], axis=1, inplace=True)
ForFlights.to_csv(path+"FlightForecast.csv",index=False)
logger.info('Сохранение файла FlightForecast.csv')
logger.info('Время выполнения скрипта: ' + str(datetime.timedelta(seconds=(time.time() - starttime_script))))
