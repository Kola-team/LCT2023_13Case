import os
import pandas as pd
import datetime, time
from sklearn.cluster import KMeans

from logger import logger
from app.config import path_project

starttime_script = time.time()

# Путь до каталога с файлами данных
path = path_project.date

# Сбор файлов по классам обслуживания
class_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and 'CLASS' in f]
class_files.sort()


flight_data_filename = path+"FlightData.csv"
flights = pd.read_csv(flight_data_filename, parse_dates=["DD"], dayfirst=True)

flights.set_index(keys=["FLT_NUM", "DD"],inplace=True)
# flights.head()

flights.drop(['B', 'C', 'D', 'E', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'T', 'U', 'V', 'X', 'Y', 'Z', 'CT', 'YT', 'TT', 'SORG', 'SDST',]
             ,axis=1,inplace=True)



#reserv_data = None
directions = [ ["SVO","ASF"],["SVO","AER"],["ASF","SVO"],["AER","SVO"]]
for id in [0,1,2,3]:  # Если задать список [0,1,2,3] - будут обработаны все направления за несколько минут
    depn = directions[id][0]
    dstn = directions[id][1]
    reserv_data = None
    total_reserv = 0
    logger.info(f'Выбор рейсов направления {depn}-{dstn}')
    for f in class_files:
        fn = path+f
        class_data = pd.read_csv(fn,sep=";", parse_dates=["DD"], dayfirst=True )
        #print(f,class_data.shape[0],"records")

        # get segment names
        c_class_segs = list(class_data[(class_data.PASS_DEP>0)&(class_data.SSCL1=='C')].SEG_CLASS_CODE.unique())
        c_class_segs.sort()

        y_class_segs = list(class_data[(class_data.PASS_DEP>0)&(class_data.SSCL1=='Y')].SEG_CLASS_CODE.unique())
        y_class_segs.sort()

        # select only complete flights
        reserv_class = class_data[(class_data.DTD > -1) & (class_data.SORG==depn) &(class_data.SDST == dstn) ]

        rseg = reserv_class.pivot(index=["SDAT_S", "DTD", "FLT_NUM","DD"], columns=["SEG_CLASS_CODE"], values=["PASS_BK"])

        # get column names
        seg_names = [x[1] for x in list(rseg.columns)]
        ind_names=list(rseg.index.names)
        col_names = ind_names + seg_names

        #convert from pivot to normal DF
        rseg.reset_index(inplace=True)
        rseg.columns = rseg.columns.droplevel(0)
        rseg.columns = col_names


        # calculate totals
        rseg["CT"] = rseg[c_class_segs].sum(axis=1)
        rseg["YT"] = rseg[y_class_segs].sum(axis=1)
        rseg["TT"] = rseg[["CT","YT"]].sum(axis=1)


        # add origin and destination for convinience
        org_dest = reserv_class[["FLT_NUM","SORG","SDST"]].drop_duplicates(subset=["FLT_NUM"]).set_index("FLT_NUM")
        rseg = rseg.join(org_dest, on="FLT_NUM")
        rseg.fillna(0,inplace=True) #Если данных по сегменту бронирования нет - записывается ноль


        rseg = rseg.join(flights, on= ["FLT_NUM","DD"])
        rseg.fillna(-1,inplace=True) #Если данных по кластера спроса нет - записывается -1 (спрос неизвестен)
        rseg["DemCluster"] = rseg["DemCluster"].astype(int)


        num_res = rseg.shape[0]
        total_reserv += num_res


        # combining dataframe with previous
        if reserv_data is None:
            reserv_data = rseg.copy()
        else:
            reserv_data = pd.concat([reserv_data,rseg],ignore_index=True)
        logger.info(f"{f} {class_data.shape[0]} records {num_res} reservation records")

    logger.info(f"Total {total_reserv} reservation records")
    logger.info(f"Reservations Data Shape {reserv_data.shape}")
    reserv_data.fillna(0, inplace=True)
    # сохранение кластера спроса для уже завершенных рейсов
    # информация берется из таблицы flights

    fn = path+"reserv_"+depn+"_"+dstn+".csv"
    reserv_data.to_csv(fn,index=False)
    logger.info(f'Данные направления сохранены: {fn}')


logger.info('Время выполнения скрипта: ' + str(datetime.timedelta(seconds=(time.time() - starttime_script))))
