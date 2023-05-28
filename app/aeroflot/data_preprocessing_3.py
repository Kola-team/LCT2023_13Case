import os
import pandas as pd
import numpy as np
import datetime, time
from sklearn.cluster import KMeans

from logger import logger
from app.config import path_project

starttime_script = time.time()

# Путь до каталога с файлами данных
path = path_project.date


flight_data_filename = path+"FlightData.csv"
flights = pd.read_csv(flight_data_filename, parse_dates=["DD"], dayfirst=True)
flights["HLDate"] = 0


def find_half_load_date(stats, load):
    i = stats.shape[0]-1
    while stats[i,1] <= load :
        i -=1
    return stats[i,0]

def get_segment_info(data,column):
    """ Собираем статистику по полю (сегменту обслуживания или классу салона) для выбранного рейса на выбранную дату"""
    twocols = data.drop([c for c in list(data.columns) if c not in ['DTD',column]],axis=1)
    twocols.sort_values(by='DTD',inplace=True)
    return twocols.values



reserv_file_names = [ "reserv_AER_SVO.csv", "reserv_SVO_AER.csv", "reserv_ASF_SVO.csv", "reserv_SVO_ASF.csv"]
for i in [0,1,2,3]:
    reserv = pd.read_csv(path+reserv_file_names[i], parse_dates=["SDAT_S", "DD"], dayfirst=True)
    logger.info(f'Файл {reserv_file_names[i]}. Объем входных данных {reserv.shape}')

    flight_list = list(reserv.FLT_NUM.unique())
    flight_list.sort()

    for fi in range(len(flight_list)):
        fn = flight_list[fi]

        complete_flight_dates = list(flights[flights.FLT_NUM==fn].DD)
        complete_flight_dates_len = len(complete_flight_dates)

        for dn in  range(complete_flight_dates_len):
            date = complete_flight_dates[dn]
            sdf = reserv[(reserv.FLT_NUM==fn)&(reserv.DD==date)]

            if sdf.shape[0] > 0 :
                dynamic = get_segment_info(sdf,"TT")
                fpos = flights[(flights.FLT_NUM==fn)&(flights.DD==date)].index[0]

                load = flights.loc[fpos,"TT"]
                if dynamic.shape[0] > 1 : hldate = np.argwhere(dynamic[:,1]>=load/2).max()
                else: hldate =0
                flights.loc[fpos,"HLDate"] = hldate



flights["HCBuy"] = 0 # Горячая или холодная покупка билетов
direct = ['ASF','AER']
q50lst = [14,28]
for i in flights.index:
    if (flights.at[i,"SORG"] == direct[0]) or (flights.at[i,"SDST"] == direct[0]) : limit = q50lst[0]
    else: limit = q50lst[1]
    flights.at[i,"HCBuy"] = 0 if flights.at[i,"HLDate"] < limit else 1
flights.to_csv(flight_data_filename, index=False)
logger.info(f'Обновили файл {flight_data_filename}')



logger.info('Время выполнения скрипта: ' + str(datetime.timedelta(seconds=(time.time() - starttime_script))))
