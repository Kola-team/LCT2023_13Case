# -----------------------------------------------------------------
#        Загрузка файла в базу данных FlightData.csv
# -----------------------------------------------------------------

# Предварительно таблицу можно не создавать
# Она создается при загрузке датафрейма


import os

import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv('.env')


DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_PORT = os.environ.get('DB_PORT')
DATABASE_URL = \
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


# Путь до каталога с файлами данных
engine = create_engine(DATABASE_URL, echo=True)

# df = pd.read_csv("ResForecast_AER_SVO.csv")
# df['RD'] = pd.to_datetime(df['RD']).dt.date
# df['FD'] = pd.to_datetime(df['FD']).dt.date
# # Названия колонок с маленько буквы
# df = df.rename(columns=str.lower)

# df.to_sql('res_forecast_aer_svo', con=engine, if_exists='replace')
# # if_exists='append' - добавить данные
# # if_exists='replace' - удалить таблицу перед вставкой новых значений.


# df = pd.read_csv("ResForecast_ASF_SVO.csv")
# df['RD'] = pd.to_datetime(df['RD']).dt.date
# df['FD'] = pd.to_datetime(df['FD']).dt.date
# # Названия колонок с маленько буквы
# df = df.rename(columns=str.lower)

# df.to_sql('res_forecast_asf_svo', con=engine, if_exists='replace')
# # if_exists='append' - добавить данные
# # if_exists='replace' - удалить таблицу перед вставкой новых значений.


# df = pd.read_csv("ResForecast_SVO_AER.csv")
# df['RD'] = pd.to_datetime(df['RD']).dt.date
# df['FD'] = pd.to_datetime(df['FD']).dt.date
# # Названия колонок с маленько буквы
# df = df.rename(columns=str.lower)

# df.to_sql('res_forecast_svo_aer', con=engine, if_exists='replace')
# # if_exists='append' - добавить данные
# # if_exists='replace' - удалить таблицу перед вставкой новых значений.


df = pd.read_csv("ResForecast_SVO_ASF.csv")
df['RD'] = pd.to_datetime(df['RD']).dt.date
df['FD'] = pd.to_datetime(df['FD']).dt.date
# Названия колонок с маленько буквы
df = df.rename(columns=str.lower)

df.to_sql('res_forecast_svo_asf', con=engine, if_exists='replace')
# if_exists='append' - добавить данные
# if_exists='replace' - удалить таблицу перед вставкой новых значений.