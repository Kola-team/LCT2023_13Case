# -----------------------------------------------------------------
#        Загрузка файла в базу данных FlightData.csv
# -----------------------------------------------------------------

# Предварительно таблицу можно не создавать
# Она создается при загрузке датафрейма



import pandas as pd
import datetime, time
from sqlalchemy import create_engine

from logger import logger
from app.config import path_project, DATABASE_URL

print(DATABASE_URL)

starttime = time.time()
logger.info('Загрузка файла FlightData.csv в базу данных')
# Путь до каталога с файлами данных
path = path_project.date
engine = create_engine(DATABASE_URL, echo=True)


flight_data = pd.read_csv(path+"FlightData.csv")
flight_data['DD'] = pd.to_datetime(flight_data['DD']).dt.date
# Названия колонок с маленько буквы
flight_data = flight_data.rename(columns=str.lower)
flight_data.to_sql('flight_data',con=engine, if_exists='replace')
# if_exists='append' - добавить данные
# if_exists='replace' - удалить таблицу перед вставкой новых значений.


flight_forecast = pd.read_csv(path+"FlightForecast.csv")
flight_forecast['EFFV_DATE'] = pd.to_datetime(flight_forecast['EFFV_DATE']).dt.date
flight_forecast['DISC_DATE'] = pd.to_datetime(flight_forecast['DISC_DATE']).dt.date
flight_forecast['FD'] = pd.to_datetime(flight_forecast['FD']).dt.date
# Названия колонок с маленько буквы
flight_forecast = flight_forecast.rename(columns=str.lower)
flight_forecast.to_sql('flight_forecast',con=engine, if_exists='replace')



reserv_aer_svo = pd.read_csv(path+"reserv_AER_SVO.csv")
reserv_aer_svo['DD'] = pd.to_datetime(reserv_aer_svo['DD']).dt.date
reserv_aer_svo['SDAT_S'] = pd.to_datetime(reserv_aer_svo['SDAT_S']).dt.date
# Названия колонок с маленько буквы
reserv_aer_svo = reserv_aer_svo.rename(columns=str.lower)
reserv_aer_svo.to_sql('reserv_aer_svo',con=engine, if_exists='replace')



reserv_asf_svo = pd.read_csv(path+"reserv_ASF_SVO.csv")
reserv_asf_svo['DD'] = pd.to_datetime(reserv_asf_svo['DD']).dt.date
reserv_asf_svo['SDAT_S'] = pd.to_datetime(reserv_asf_svo['SDAT_S']).dt.date
# Названия колонок с маленько буквы
reserv_asf_svo = reserv_asf_svo.rename(columns=str.lower)
reserv_asf_svo.to_sql('reserv_asf_svo',con=engine, if_exists='replace')



reserv_svo_aer = pd.read_csv(path+"reserv_SVO_AER.csv")
reserv_svo_aer['DD'] = pd.to_datetime(reserv_svo_aer['DD']).dt.date
reserv_svo_aer['SDAT_S'] = pd.to_datetime(reserv_svo_aer['SDAT_S']).dt.date
# Названия колонок с маленько буквы
reserv_svo_aer = reserv_svo_aer.rename(columns=str.lower)
reserv_svo_aer.to_sql('reserv_svo_aer',con=engine, if_exists='replace')



reserv_svo_asf = pd.read_csv(path+"reserv_SVO_ASF.csv")
reserv_svo_asf['DD'] = pd.to_datetime(reserv_svo_asf['DD']).dt.date
reserv_svo_asf['SDAT_S'] = pd.to_datetime(reserv_svo_asf['SDAT_S']).dt.date
# Названия колонок с маленько буквы
reserv_svo_asf = reserv_svo_asf.rename(columns=str.lower)
reserv_svo_asf.to_sql('reserv_svo_asf',con=engine, if_exists='replace')



flights = flight_data[['flt_num','sorg', 'sdst']].drop_duplicates().reset_index(drop=True)
flights.to_sql('flights',con=engine, if_exists='replace')


logger.info('Время выполнения зашрузки: ' + str(datetime.timedelta(seconds=(time.time() - starttime))))
