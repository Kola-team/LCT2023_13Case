import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv('./.env')


DB_USER = os.environ.get('POSTGRES_USER')
DB_PASS = os.environ.get('POSTGRES_PASS')
DB_HOST = os.environ.get('POSTGRES_HOST')
DB_NAME = os.environ.get('POSTGRES_DB')
DB_PORT = os.environ.get('POSTGRES_PORT')
DATABASE_URL = \
    f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


@dataclass
class PathProject:
    logs = os.environ.get('PATH_LOGS')
    date = os.environ.get('PATH_DATE')
    scr = os.environ.get('PATH_SCR')


path_project = PathProject()
