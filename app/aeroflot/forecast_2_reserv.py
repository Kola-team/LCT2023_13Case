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


def estimate_seasonal_trend(data, target_col, index_col, period, minval=0, factor=1.0 ):
    # period - кортеж из двух чисел - первого и последнего фактических значений категории.
    # target_col - признак целевого значения в наборе data
    # index_col - признак со значениями соответствующей категории в наборе data
    season =  dict()
    for i in range(period[0], period[1]+1):
        season[i] = data.loc[data[index_col]==i][target_col].mean()
        season[i] = minval * factor if isnan(season[i]) else season[i] * factor
    season = {k:v for k,v in season.items() if v >0 }
    return season


flight_data_filename = path+"FlightData.csv"
flights = pd.read_csv(flight_data_filename, parse_dates=["DD"], dayfirst=True)
flights["dayofyear"] = flights.DD.dt.dayofyear

flight_forecast_filename = path+ "FlightForecast.csv"
flight_forecasts = pd.read_csv(flight_forecast_filename, parse_dates=["FD"], dayfirst=True)
flight_forecasts["dayofyear"] = flight_forecasts.FD.dt.dayofyear
flight_forecasts["LEG_ORIG"] = flight_forecasts.LEG_ORIG.apply( lambda x: x.strip())
flight_forecasts["LEG_DEST"] = flight_forecasts.LEG_DEST.apply( lambda x: x.strip())


reserv_file_names = [ "reserv_AER_SVO.csv", "reserv_SVO_AER.csv", "reserv_ASF_SVO.csv", "reserv_SVO_ASF.csv"]
reserv_forecast_names = [ "ResForecast_AER_SVO.csv", "ResForecast_SVO_AER.csv", "ResForecast_ASF_SVO.csv", "ResForecast_SVO_ASF.csv"]
MAX_RESERVE_DEPTH = 180 #217
LEAP_DAY = pd.to_datetime('2020-02-29').dayofyear

segment_names = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
ext_seg_names = ["TT"] + segment_names

global_index = 0

for fi in [0,1,2,3]:
    starttime = time.time()
    reserv_forecast_df = None
    reserv = pd.read_csv(path+reserv_file_names[fi], parse_dates=["SDAT_S", "DD"], dayfirst=True)
    reserv["dayofyear"] = reserv.DD.dt.dayofyear
    first_index = list(reserv.index)[0]
    orig = reserv.at[first_index,"SORG"]
    dest = reserv.at[first_index,"SDST"]
    logger.info(f'Файл {reserv_file_names[fi]}. Направление {orig}-{dest}. Объем входных данных {reserv.shape}')
    selected_forecast = flight_forecasts[(flight_forecasts.LEG_ORIG==orig)&(flight_forecasts.LEG_DEST==dest)]
    selected_flights = selected_forecast.FLT_NUMSH.unique()
    selected_flights_len = len(selected_flights)
    logger.info(f'В расписании на направление {selected_forecast.shape[0]} полетов по {selected_flights_len} рейсам.')
    for flt in selected_flights: #[1172]:
        flight_forecast_df = None
        sel_flight = selected_forecast[selected_forecast.FLT_NUMSH==flt]
        forecast_days = list(sel_flight.dayofyear.unique())
        forecast_len = len(forecast_days)
        forecast_ind = list(sel_flight.index)

        reserv_days = list(reserv[reserv.FLT_NUM==flt].dayofyear.unique())
        missing_days = [x for x in forecast_days if x not in reserv_days]
        #print(missing_days)
        missing_days_len = len(missing_days)
        logger.info(f'Рейс {flt}, {forecast_len} полетов запланировано, по {missing_days_len} информация отсутствует.')
        short_list = sorted(list(set(forecast_days).intersection(set(reserv_days))),reverse=True)
        flight_res_forecast = dict()
        flight_res_forecast_ind = 0
        for ind in range(len(forecast_ind)):
            doy = sel_flight.at[forecast_ind[ind],"dayofyear"]
            doy = doy if doy < LEAP_DAY else doy-1 #превращаем 29 февраля в 28 февраля и так далее
            forecast_FD = sel_flight.at[forecast_ind[ind],"FD"]
            forecast_load = sel_flight.at[forecast_ind[ind],"TT"]
            sel_reserv = reserv[(reserv.FLT_NUM==flt)&(reserv.dayofyear==doy)]#.copy()
            flight_load = flights[(flights.FLT_NUM==flt)&(flights.dayofyear==doy)].TT.mean()
            if isnan(flight_load):
                # На этот день истории по рейсу нет, берем среднее за день
                sel_reserv = reserv[(reserv.SORG==orig)&(reserv.SDST==dest)&(reserv.dayofyear==doy)]#.copy()
                flight_load = flights[(flights.SORG==orig)&(flights.SDST==dest)&(flights.dayofyear==doy)].TT.mean()

            day_comp = dict()
            for sn in ext_seg_names:
                if sn in sel_reserv.columns:
                    if sel_reserv[sn].sum() > 0:
                        day_comp[sn] = estimate_seasonal_trend(sel_reserv, sn, "DTD", (0,MAX_RESERVE_DEPTH), factor=1/flight_load)
            missing_seg = [x for x in ext_seg_names if x not in day_comp.keys()]

            history = day_comp["TT"].keys()
            for d in history:
                res_day = dict()
                forecast_RD = forecast_FD - pd.Timedelta(d,'d')
                res_day["RD"] = forecast_RD
                res_day["DTD"] = d
                res_day["FD"]  = forecast_FD
                res_day["FLT"] = flt
                res_day["ORIG"] = orig
                res_day["DEST"] = dest
                sum_seg = 0
                for k in segment_names:
                    if k in day_comp.keys():
                        res_day[k] = round(day_comp[k].get(d,0) * forecast_load)
                        sum_seg += res_day[k]
                    else:
                        res_day[k] = 0
                res_day["TT"] = sum_seg
                flight_res_forecast[flight_res_forecast_ind] = res_day
                flight_res_forecast_ind +=1

        logger.info(f'{len(flight_res_forecast.keys())} записей по рейсу {flt}')
        reserv_forecast_df = pd.concat([reserv_forecast_df, pd.DataFrame.from_dict(flight_res_forecast).T], ignore_index=True )
        reserv_forecast_df.fillna(0,inplace=True)
    reserv_forecast_df.sort_values(by=["RD","FD","FLT"],inplace=True, ignore_index=True)
    logger.info(f'{reserv_forecast_df.shape[0]} записей в прогнозе резервирования.')

    reserv_forecast_df.to_csv(path+reserv_forecast_names[fi], index=False)
    logger.info(f'Сохранеие в файл {reserv_forecast_names[fi]}')
    logger.info('Время расчета: ' + str(datetime.timedelta(seconds=(time.time() - starttime))))


logger.info('Время выполнения скрипта: ' + str(datetime.timedelta(seconds=(time.time() - starttime_script))))
