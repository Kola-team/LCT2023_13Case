# -----------------------------------------------------------------
#        Предподготовка данных для загрузки в базу данных
#               обработка файлов CLASS_MMYYYY.csv
# -----------------------------------------------------------------


import os
import pandas as pd
import datetime
import time
from sklearn.cluster import KMeans

from logger import logger
from app.config import path_project

starttime_script = time.time()

# Путь до каталога с файлами данных
path = path_project.date

# Сбор файлов по классам обслуживания
class_files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and 'CLASS' in f]
class_files.sort()

# -----------------------------------------------------------------
#    Процедура формирования статистики по соверешенным полетам
# -----------------------------------------------------------------

starttime = time.time()


total_flights = 0
flight_data_filename = path+"FlightData.csv"
logger.info(f'Создание файла {flight_data_filename}')
flight_data = None
for f in class_files:
    fn = path+f
    class_data = pd.read_csv(fn,sep=";")
    #print(f,class_data.shape[0],"records")

    # получаем имена сегментов
    c_class_segs = list(class_data[(class_data.PASS_DEP>0)&(class_data.SSCL1=='C')].SEG_CLASS_CODE.unique())
    c_class_segs.sort()
    #print(c_class_segs)
    y_class_segs = list(class_data[(class_data.PASS_DEP>0)&(class_data.SSCL1=='Y')].SEG_CLASS_CODE.unique())
    y_class_segs.sort()
    #print(y_class_segs)

    # выбираем только завершенные рейсы
    flight_class = class_data[(class_data.DTD == -1)]  #&(class_012018.PASS_DEP>0)
    #flight_class.head(10)

    flight_seg = flight_class.pivot(index=["FLT_NUM","DD"], columns=["SEG_CLASS_CODE"], values=["PASS_DEP"])
    #print(flight_seg.shape)
    #flight_seg.head()
    # получаем имена столбцов
    seg_names = [x[1] for x in list(flight_seg.columns)]
    ind_names=list(flight_seg.index.names)
    col_names = ind_names + seg_names
    #преобразуем pivot таблицу в DF
    flight_seg.reset_index(inplace=True)
    flight_seg.columns = flight_seg.columns.droplevel(0)
    flight_seg.columns = col_names
    #print(flight_seg.shape)
    #flight_seg.head()
    # считаем общее по классу кабины и борту в целом
    flight_seg["CT"] = flight_seg[c_class_segs].sum(axis=1)
    flight_seg["YT"] = flight_seg[y_class_segs].sum(axis=1)
    flight_seg["TT"] = flight_seg[["CT","YT"]].sum(axis=1)
    #print(flight_seg.shape)
    #flight_seg.head()

    # добавляю аэропорт вылета и прилета для удобства
    org_dest = flight_class[["FLT_NUM","SORG","SDST"]].drop_duplicates(subset=["FLT_NUM"]).set_index("FLT_NUM")
    flight_seg = flight_seg.join(org_dest, on="FLT_NUM")
    num_flights = flight_seg.shape[0]
    total_flights += num_flights
    #print(flight_seg.shape)
    #flight_seg.head()
    # сливаю df с предыдущим
    if flight_data is None:
        flight_data = flight_seg.copy()
    else:
        flight_data = pd.concat([flight_data,flight_seg],ignore_index=True)
    logger.info(f,class_data.shape[0],"записей",num_flights,"полетов")

logger.info("Total" + str(total_flights) + "flighs")
logger.info("Flight Data Shape" + str(flight_data.shape))
flight_data.fillna(0,inplace=True)
flight_data.to_csv(flight_data_filename,index=False)
# flight_data.head()

logger.info('Время выполнения: ' + str(datetime.timedelta(seconds=(time.time() - starttime))))
del flight_data  # Далее загружаем сохраненный файл


flights = pd.read_csv(flight_data_filename, parse_dates=["DD"], dayfirst=True)
logger.info(f'Загрузка файла: {flight_data_filename}, размерданных:', flights.shape)

flights.fillna(0,inplace=True)
flights.drop(flights[flights.TT==0].index, axis=0, inplace=True)
flights.sort_values(by="DD", inplace=True)

# ----------------------------------------------------------------------------
#    Кластеризация полетов по кластерам спроса по каждому рейсу отдельно
# ----------------------------------------------------------------------------

logger.info('Кластеризация полетов по кластерам спроса по каждому рейсу отдельно')
starttime = time.time()

flight_list = flights.FLT_NUM.unique()
NuM_CLUSTERS = 3
MIN_FLIGHTS = 10
clust_models = dict()
subst = dict()
clust_limits = dict()
num_flights = 0
for fl in flight_list: #[1120, 1135]: #  # # #:  #
    sf = flights[flights.FLT_NUM==fl]
    if sf.shape[0] > MIN_FLIGHTS:
        clust_model = KMeans(n_clusters=NuM_CLUSTERS, random_state=19, n_init='auto')
        xin = sf.TT.values.reshape((-1,1))
        clust_model.fit(xin)
        yout = clust_model.predict(xin)
        mnv = dict()
        for i in range(NuM_CLUSTERS):
            mnv[i] = xin[yout==i].mean()
        xlim = list(mnv.values())
        xlim.sort()
        limits = [ round((xlim[i-1]+xlim[i])/2,2) for i in range(1,NuM_CLUSTERS)]
        clust_limits[fl] = limits
    else:
        clust_limits[fl] = None
    num_flights +=1
logger.info(f'{num_flights} рейсов обработано')
logger.info('Время выполнения: ' + str(datetime.timedelta(seconds=(time.time() - starttime))))


# Добавление результата кластеризации к датафрейму

def colorise_demand(x,f,dlims):
    """ Разметка экземпляра рейса"""
    #print(x, f,dlims[fl])
    if dlims[f] is None:
        return 0
    else:
        return 0 if x <= dlims[f][0] else 1 if x <= dlims[f][1] else 2

flights["DemCluster"] = flights.apply(lambda x: colorise_demand(x.TT, x.FLT_NUM, clust_limits), axis=1)

#  Сохранение файла со статистикой по рейсам
flights.to_csv(flight_data_filename,index=False)
logger.info(f'Сохранение датасета для последующей загрузки в БД: {flight_data_filename}' )

logger.info('Время выполнения скрипта: ' + str(datetime.timedelta(seconds=(time.time() - starttime_script))))
